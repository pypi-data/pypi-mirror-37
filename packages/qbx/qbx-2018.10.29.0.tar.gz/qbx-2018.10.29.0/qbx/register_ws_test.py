from qbx import register_ws

print(register_ws)


def test_reg():
    register_ws.register_ws(['--name', '/pytest', '--uri', '/ws-random', '--port', '3000', '--ot', '--test'])
