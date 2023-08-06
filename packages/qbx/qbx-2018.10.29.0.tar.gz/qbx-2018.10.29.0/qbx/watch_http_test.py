def test_watch():
    from qbx import watch_http
    r = watch_http.check('api.qbtrade.org')
    assert not r

    r = watch_http.check('api.qbtrade.org/v1/basic/time')
    assert r

    r = watch_http.check('xxx.qbtrade.org/v1/basic/time')
    assert r


def test_timeout():
    from qbx import watch_http
    import pytest
    with pytest.raises(SystemExit):
        watch_http.watch_http(['qadfaf.afafasfsadfasdfasf.com', '--timeout', '3'])
