"""Layer2 Demo App

- Implements reactive forwarding for a vlan-aware layer 2 switch.
- Ignores LLDP packets.
- Does not support loops.

"""

import zof
from zof.pktview import pktview_from_list

APP = zof.Application('layer2', exception_fatal=True)

# The forwarding table is a dictionary that maps:
#   datapath_id -> { (eth_dst, vlan_vid) -> (out_port, time) }

APP.forwarding_table = {}


@APP.message('channel_up')
def channel_up(event):
    """Set up datapath when switch connects."""
    APP.logger.info('%s Connected from %s (%d ports, version %d)',
                    event['datapath_id'], event['msg']['endpoint'],
                    len(event['datapath']), event['version'])
    APP.logger.info('%s Remove all flows', event['datapath_id'])

    DELETE_FLOWS.send()
    BARRIER.send()
    TABLE_MISS_FLOW.send()


@APP.message('channel_down')
def channel_down(event):
    """Clean up when switch disconnects."""
    APP.logger.info('%s Disconnected', event['datapath_id'])
    APP.forwarding_table.pop(event['datapath_id'], None)


@APP.message('packet_in', eth_type=0x88cc)
def lldp_packet_in(_event):
    """Ignore lldp packets."""
    APP.logger.debug('lldp packet ignored')


@APP.message('packet_in')
def packet_in(event):
    """Handle incoming packets."""
    APP.logger.debug('packet in %r', event)
    datapath_id = event['datapath_id']
    msg = event['msg']
    time = event['time']
    data = msg['data']

    # Check for incomplete packet data.
    if len(data) < msg['total_len']:
        APP.logger.warning('Incomplete packet data: %r', event)
        return

    in_port = msg['in_port']
    pkt = msg['pkt']
    vlan_vid = pkt('vlan_vid', default=0)

    # Retrieve fwd_table for this datapath.
    fwd_table = APP.forwarding_table.setdefault(datapath_id, {})

    # Update fwd_table based on eth_src and in_port.
    if (pkt.eth_src, vlan_vid) not in fwd_table:
        APP.logger.info('%s Learn %s vlan %s on port %s', datapath_id,
                        pkt.eth_src, vlan_vid, in_port)
        fwd_table[(pkt.eth_src, vlan_vid)] = (in_port, time)

    # Lookup output port for eth_dst. If not found, set output port to 'ALL'.
    out_port, _ = fwd_table.get((pkt.eth_dst, vlan_vid), ('ALL', None))

    if out_port != 'ALL':
        APP.logger.info('%s Forward %s vlan %s to port %s', datapath_id,
                        pkt.eth_dst, vlan_vid, out_port)
        LEARN_MAC_FLOW.send(
            vlan_vid=vlan_vid, eth_dst=pkt.eth_dst, out_port=out_port)
        PACKET_OUT.send(out_port=out_port, data=data)

    else:
        # Send packet back out all ports (except the one it came in).
        APP.logger.info('%s Flood %s to %s vlan %s', datapath_id,
                        pkt.get_description(), pkt.eth_dst, vlan_vid)
        PACKET_FLOOD.send(in_port=in_port, data=data)


@APP.message('flow_removed')
def flow_removed(event):
    """Handle flow removed message."""
    datapath_id = event['datapath_id']
    match = pktview_from_list(event['msg']['match'])
    eth_dst = match.eth_dst
    vlan_vid = match.vlan_vid
    reason = event['msg']['reason']

    APP.logger.info('%s Remove %s vlan %s (%s)', datapath_id, eth_dst,
                    vlan_vid, reason)

    fwd_table = APP.forwarding_table.get(datapath_id)
    if fwd_table:
        fwd_table.pop((eth_dst, vlan_vid), None)


@APP.message(any)
def other_message(event):
    """Log ignored messages."""
    APP.logger.debug('Ignored message: %r', event)


DELETE_FLOWS = zof.compile('''
  # Delete flows in table 0.
  type: FLOW_MOD
  msg:
    command: DELETE
    table_id: 0
''')

BARRIER = zof.compile('''
  type: BARRIER_REQUEST
''')

TABLE_MISS_FLOW = zof.compile('''
  # Add permanent table miss flow entry to table 0
  type: FLOW_MOD
  msg:
    command: ADD
    table_id: 0
    priority: 0
    instructions:
      - instruction: APPLY_ACTIONS
        actions:
          - action: OUTPUT
            port_no: CONTROLLER
            max_len: NO_BUFFER
''')

LEARN_MAC_FLOW = zof.compile('''
  type: FLOW_MOD
  msg:
    table_id: 0
    command: ADD
    idle_timeout: 60
    hard_timeout: 120
    priority: 10
    buffer_id: NO_BUFFER
    flags: [ SEND_FLOW_REM ]
    match:
      - field: ETH_DST
        value: $eth_dst
      - field: VLAN_VID
        value: $vlan_vid
    instructions:
      - instruction: APPLY_ACTIONS
        actions:
          - action: OUTPUT
            port_no: $out_port
            max_len: MAX
''')

PACKET_OUT = zof.compile('''
  type: PACKET_OUT
  msg:
    actions:
      - action: OUTPUT
        port_no: $out_port
        max_len: MAX
    data: $data
''')

PACKET_FLOOD = zof.compile('''
  type: PACKET_OUT
  msg:
    in_port: $in_port
    actions:
      - action: OUTPUT
        port_no: ALL
        max_len: MAX
    data: $data
''')

if __name__ == '__main__':
    zof.run()
