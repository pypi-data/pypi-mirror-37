import asyncio
from .controller import Controller
from .service.datapath import APP as DATAPATH_APP


def get_apps():
    """Get list of app's.
    """
    return [app.ref for app in Controller.singleton().apps]


def set_apps(apps):
    """Set list of apps.

    Avoid this function; it is provided for testing.
    """
    # pylint: disable=protected-access
    Controller.singleton().apps = [app._app for app in apps]


def get_datapaths():
    """Get list of currently connected datapaths.
    """
    return DATAPATH_APP.get_datapaths()


def find_datapath(*, datapath_id):
    """Return given datapath object.
    """
    return DATAPATH_APP.find_datapath(datapath_id)


def find_port(*, datapath_id, port_no):
    """Return given port object.
    """
    return DATAPATH_APP.find_port(datapath_id, port_no)


def post_event(event):
    """Function used to send an internal event to all app modules.

    Args:
        event (dict): event object
    """
    if not isinstance(event, dict):
        raise ValueError('%s not a dictionary: %r' % (type(event), event))
    Controller.singleton().post_event(event)


def ensure_future(coroutine, *, datapath_id=None, conn_id=None):
    """Function used by an app to run an async coroutine, under a specific
    scope.
    """
    task = asyncio.Task.current_task()
    if task:
        # Execute task within scope of current app.
        app = task.zof_task_app
        return app.ensure_future(coroutine, datapath_id=datapath_id, conn_id=conn_id)
    else:
        return asyncio.ensure_future(coroutine)

def _rpc_call(method, **params):
    """Function used to send a RPC request and receive a response.

    Returns:
        asyncio.Future: future for RPC reply
    """
    return Controller.singleton().rpc_call(method, **params)


async def connect(endpoint, *, options=(), versions=(), tls_id=0):
    """Make an outgoing OpenFlow connection.
    """
    result = await _rpc_call(
        'OFP.CONNECT',
        endpoint=endpoint,
        tls_id=tls_id,
        options=options,
        versions=versions)
    return result['conn_id']


async def close(*, conn_id=0, datapath_id=None):
    """Close an OpenFlow connection.
    """
    result = await _rpc_call(
        'OFP.CLOSE', conn_id=conn_id, datapath_id=datapath_id)
    return result['count']


async def get_connections(*, conn_id=0):
    """Get list of OpenFlow connections.
    """
    result = await _rpc_call('OFP.LIST_CONNECTIONS', conn_id=conn_id)
    return result['stats']


async def add_identity(*, cert, cacert, privkey):
    """Add a TLS identity.

    Returns:
        int: tls_id
    """
    result = await _rpc_call(
        'OFP.ADD_IDENTITY', cert=cert, cacert=cacert, privkey=privkey)
    return result['tls_id']
