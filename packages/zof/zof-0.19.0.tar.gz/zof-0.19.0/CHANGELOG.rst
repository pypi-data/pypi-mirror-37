CHANGELOG
=========

Version 0.19.0
--------------

- Update zof for oftr API changes to Port structure, PortMod, and PortStats.


Version 0.18.0
--------------

- Update zof for recent oftr API changes (e.g. ext_hdrs, channel_alert).
- REST API supports POST to /stats/flow/{dpid} to pass JSON parameters to search flows.
- Add serve_forever() method to HTTP api.
- REST API supports a multi-valued query string (using []).
- Add REST API handler for portdesc request to specific port number.


Version 0.17.0
--------------

- oftr changes CHANNEL_UP event to include FeaturesReply with ports.
- oftr renames some events, e.g. REQUEST.FLOW -> REQUEST.FLOW_DESC.
- LLDP support for multiple TLV values with the same subtype.


Version 0.16.0
--------------

- Allow OF messages to be compiled from non-zof tasks.
- Allow zof.ensure_future to be called from outside an async task.
- Update requirements.txt.
- Update http API shim to use aiohttp 3.0 AppRunner API.


Version 0.15.0
--------------

- Add support for 'nxt' and 'ext_hdrs' aliases to PktView.
- CallbackInfo class now allows a base class member to bind to a direct subclass instance.
- Update base alpine image version to v0.48.0-alpine3.7.


Version 0.14.0
--------------

- The contents of the FeaturesReply message is now available from the built-in Datapath object. 
- The FeaturesReply message is no longer dispatched separately.


Version 0.13.0
--------------

- Add curr_speed and max_speed to zof.Port class.
- PktView now supports fields with multiple values (e.g. x_lldp_org_specific).
- Add lldp support for get_protocol API in PktView.
- Validate that mac, ipv4 and ipv6 addresses are non-empty strings (ofctl).
- Datapath class now has a send_msg method.


Version 0.12.0
--------------

- Add support for APP.bind decorator for classes.
- Datapath object instances now have an 'id' attribute (datapath_id as int).
- Prevent datapath service from propagating messages if datapath is not ready.
- Update requirements.txt.


Version 0.11.0
--------------

- Default cacert and privkey to '' if not present.
- Rest API allows datapath's that begin with '0x'.
- Fix bug in stopping web server (when there was an error starting it).
- Update oftr version in alpine docker file.


Version 0.10.0
--------------

- Clean up HTTP decorator api.
- Improved handling of RPC connection failure; add ClosedException (Issue #2).
- Metrics demo app: /metrics/ports unknown target returns HTTP status 404 (Issue #1).
- Small fixes to the simulator demo app.


Version 0.9.0
-------------

- zof.compile can be used to create RPC message events from Python objects.
- Update oftr version in alpine docker file.
- Add autoresponder demo app.


Version 0.8.0
-------------

- Fix rest_api demo handler for /stats/flow to stream multipart replies.
- Fix ready flag usage for manually closed datapaths.
- Remove Event class, make_event and make_objectview API's.
- Fix stderr logging in oftr Protocol implementation.
- Update oftr version in alpine docker file.


Version 0.7.0
-------------

- Use regular Python dictionary for events instead of wrapping them in Event object.
- Fix _ReplyFuture in controller.py to handle asyncio API change, and fix streaming multipart requests.
- Change underlying oftr connection to use protocol-based implementation (instead of streams).
- Add -xp prefix to experimental performance command line arguments: -xp-uvloop, -xp-ujson, -xp-streams. 
- Add command line arguments to conntest demo.
- Add reconnect interval command line option and more features to simulator demo.
- Fix support for --help command line argument.
- Rename "poststop" phase to "postflight".
- ofctl processing code now supports validation of field names and values.


Version 0.6.0
-------------

- Add rest_api demo handlers for /stats/portdesc, /stats/port/{dpid} (needed for faucet).
- Minor performance improvements. Fix cooperative yielding behavior.
- Add experimental demos for benchmarking (cbenchreply, zbench, oftr_bench).
- Include milliseconds in log timestamp.
- Add CodecError exception for use by zof codec.
- Add alpine docker image.


Version 0.5.0
-------------

- Add request_all() api.
- Add support for the --pidfile command line argument.
- Add zof.codec module with Python codec for encode/decode OF messages.
- Refactor CompiledMessage into a base class.
- Add argument to control number of ports in simulator demo app.
- Fix KeyError bug in datapath class.


Version 0.4.1
-------------

- Fix exception in datapath service caused by manually closed datapath.
- All fields support slash notation.
- zof.run() supports arguments passed as a list.
- Fixed zof.encode() function to support dict and ObjectView argument types.
- Fixed zof.encode() function so exception messages are strings, not bytes.


Version 0.4.0
-------------

- Exceptions in async tasks will be associated with the app that created the task.
- Add get() method to PktView.
- Added zof.encode() function.
- Added --sim-endpoint command line argument to simulator demo app.
- Handle failure in datapath service _get_ports() function.


Version 0.3.1
-------------

- Fix UDP tp_src/tp_dst bug in convert_from_ofctl.


Version 0.3.0
-------------

- Rename to zof.
- Add close() method to Datapath class for hanging up.
- Change default log format.
- Metrics app now initiates on prestart event.
- Add zof.demo.hub module.


Version 0.2.0
-------------

- Add the set_apps function.
- Datapath service adds 'datapath' property to all message events.
- Add 'src' and 'dst' read-only properties to PktView.
- Add 'port_up' metric.
- Support slash notation in IPV6_ND_TARGET, IPV6_ND_SLL, and IPV6_ND_TLL fields.


Version 0.1.1
-------------

- Fix bug in datapath service.


Version 0.1.0
-------------

- Initial release.
