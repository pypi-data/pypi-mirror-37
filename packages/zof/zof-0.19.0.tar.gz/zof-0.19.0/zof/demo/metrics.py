import argparse
from prometheus_client import REGISTRY, CollectorRegistry, generate_latest, ProcessCollector
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
import zof
from zof import exception as _exc
from zof.http import HttpServer


def arg_parser():
    parser = argparse.ArgumentParser(
        prog='Metrics', description='Metric Demo', add_help=False)
    parser.add_argument(
        '--metrics-endpoint', help='HTTP endpoint for metrics server')
    return parser


APP = zof.Application('metrics', arg_parser=arg_parser())
WEB = HttpServer()


@APP.event('preflight')
def preflight(_):
    if not APP.args.metrics_endpoint:
        # If we're not listening, unload the application.
        raise _exc.PreflightUnloadException()


@APP.event('prestart')
async def start(_):
    # Start a process collector for our oftr subprocess.
    ProcessCollector(namespace='oftr', pid=lambda: APP.oftr_connection.pid)
    await WEB.start(APP.args.metrics_endpoint)
    APP.logger.info('Start listening on %s', APP.args.metrics_endpoint)


@APP.event('stop')
async def stop(_):
    await WEB.stop()
    APP.logger.info('Stop listening on %s', APP.args.metrics_endpoint)


@WEB.get('/', 'text')
@WEB.get('/metrics', 'text')
@WEB.get('/metrics/', 'text')
async def metrics():
    return generate_latest(REGISTRY)


@WEB.get('/metrics/ports?{target}', 'text')
async def ports(target):
    if target:
        met = PortMetrics()
        await _collect_port_stats(target, met)
    else:
        met = PortMetrics(include_instance=True)
        await _collect_port_stats_all(met)
    return _dump_prometheus(met)


PORT_STATS = zof.compile('''
type: REQUEST.PORT_STATS
msg:
  port_no: ANY
''')


def _supported_counter(value):
    return value != 0xffffffffffffffff


class PortMetrics:
    def __init__(self, include_instance=False):
        self.include_instance = include_instance
        self.error = None
        if include_instance:
            labels = ['port_no', 'instance']
        else:
            labels = ['port_no']
        self.tx_bytes = CounterMetricFamily('port_tx_bytes_total',
                                            'bytes transmitted', None, labels)
        self.rx_bytes = CounterMetricFamily('port_rx_bytes_total',
                                            'bytes received', None, labels)
        self.tx_packets = CounterMetricFamily(
            'port_tx_packets_total', 'packets transmitted', None, labels)
        self.rx_packets = CounterMetricFamily('port_rx_packets_total',
                                              'packets received', None, labels)
        self.tx_dropped = CounterMetricFamily(
            'port_tx_drops_total', 'packets dropped by TX', None, labels)
        self.rx_dropped = CounterMetricFamily(
            'port_rx_drops_total', 'packets dropped by RX', None, labels)
        self.rx_errors = CounterMetricFamily('port_rx_errors_total',
                                             'receive errors', None, labels)
        self.duration = CounterMetricFamily(
            'port_duration_seconds_total', 'duration in seconds', None, labels)
        self.port_up = GaugeMetricFamily('port_up', 'port is up', None, labels)

    def collect(self):
        return [
            self.tx_bytes, self.rx_bytes, self.tx_packets, self.rx_packets,
            self.tx_dropped, self.rx_dropped, self.rx_errors, self.duration,
            self.port_up
        ]

    def update(self, dpid, stat):
        port_no = stat['port_no']
        if self.include_instance:
            labels = [str(port_no), dpid]
        else:
            labels = [str(port_no)]
        for counter, value in [(self.tx_bytes, stat['tx_bytes']),
                               (self.rx_bytes,
                                stat['rx_bytes']), (self.tx_packets,
                                                    stat['tx_packets']),
                               (self.rx_packets,
                                stat['rx_packets']), (self.tx_dropped,
                                                      stat['tx_dropped']),
                               (self.rx_dropped,
                                stat['rx_dropped']), (self.rx_errors,
                                                      stat['rx_errors'])]:
            if _supported_counter(value):
                counter.add_metric(labels, value)
        if stat['duration'] != '0':
            self.duration.add_metric(labels, float(stat['duration']))
        port = zof.find_port(datapath_id=dpid, port_no=port_no)
        if port:
            self.port_up.add_metric(labels, int(port.up))


async def _collect_port_stats(dpid, metric):
    try:
        reply = await PORT_STATS.request(datapath_id=dpid)
        for stat in reply['msg']:
            metric.update(reply['datapath_id'], stat)
    except _exc.ControllerException as ex:
        APP.logger.warning('Unable to retrieve stats for dpid %s: %r', dpid,
                           ex)
        metric.error = ('Unable to retrieve stats for dpid "%s"' % dpid, 404)


async def _collect_port_stats_all(metric):
    async for reply in PORT_STATS.request_all(parallelism=5):
        try:
            reply = await reply
            for stat in reply['msg']:
                metric.update(reply['datapath_id'], stat)
        except _exc.ControllerException:
            pass


def _dump_prometheus(stats):
    if stats.error:
        return stats.error
    registry = CollectorRegistry()
    registry.register(stats)
    return generate_latest(registry)


if __name__ == '__main__':
    zof.run()
