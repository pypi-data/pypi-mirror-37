from unittest.mock import MagicMock, Mock, patch
import ..sdp
from ..sdp import handle_msg, method, sub, handle_watch
import pytest

@method
async def add(user, a, b):
    return a + b

@method
async def with_exception_method(user):
    raise Exception('x')

@sub
def sub_1(user):
    return {}

@pytest.mark.asyncio    
async def test_no_method():
    msg = '{"msg": "method", "id": 0, "params": {}, "method": "abc"}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'nomethod', 'id': 0, 'error': 'method does not exist'})

@pytest.mark.asyncio
async def test_method():
    msg = '{"msg": "method", "id": 0, "params": {"a": 1, "b": 2}, "method": "add"}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'result', 'id': 0, 'result': 3})

@pytest.mark.asyncio
async def test_no_sub():
    msg = '{"msg": "sub", "id": "sub_not_exists", "params": {}}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'nosub', 'id': 'sub_not_exists', 'error': 'sub does not exist'})

@pytest.mark.asyncio
async def test_sub():
    msg = '{"msg": "sub", "id": "sub_1", "params": {}}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    with patch('msdp.get_event_loop') as mock_loop:
        with patch('msdp.watch') as mock_watch:
            mock_create_task = MagicMock()
            mock_loop(return_value=mock_create_task)
            await handle_msg(msg, {}, send)
            mock_watch.assert_called_with('sub_1', {}, send)

@pytest.mark.asyncio
async def test_error_json_loads():
    msg = '{'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'error', 'id': None, 'error': 'error in json.loads'})

@pytest.mark.asyncio
async def test_error_keyerror():
    msg = '{}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'error', 'id': None, 'error': "key error 'msg'"})

@pytest.mark.asyncio
async def test_error_jwt():
    msg = '{"jwt": "..."}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'error', 'id': None, 'error': "error decode jwt"})

@pytest.mark.asyncio
async def test_method_with_exception():
    msg = '{"msg": "method", "id": 0, "params": {}, "method": "with_exception_method"}'
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_msg(msg, {}, send)
    m.assert_called_with({'msg': 'error', 'id': 0, 'error': "x"})

@pytest.mark.asyncio
async def test_watch_send_ready():
    item = {"state": "ready"}
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_watch(item, 'sub_id', send)
    m.assert_called_with({'msg': 'ready', 'id': 'sub_id'})

@pytest.mark.asyncio
async def test_watch_send_initializing():
    item = {"state": "initializing"}
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_watch(item, 'sub_id', send)
    m.assert_called_with({'msg': 'initializing', 'id': 'sub_id'})

@pytest.mark.asyncio
async def test_watch_send_added():
    item = {'new_val': {'x': 0}}
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_watch(item, 'sub_id', send)
    m.assert_called_with({'msg': 'added', 'id': 'sub_id', 'doc': item['new_val']})

@pytest.mark.asyncio
async def test_watch_send_():
    item = {'old_val': {'id': 0}}
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_watch(item, 'sub_id', send)
    m.assert_called_with({'msg': 'removed', 'id': 'sub_id', 'doc_id': 0})

@pytest.mark.asyncio
async def test_watch_send_changed():
    item = {'new_val': {'x': 0}, 'old_val': {'x': 1}}
    m = MagicMock()
    async def send(*args, **kwargs):
        m(*args, **kwargs)
    
    await handle_watch(item, 'sub_id', send)
    m.assert_called_with({'msg': 'changed', 'id': 'sub_id', 'doc': item['new_val']})