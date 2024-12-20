import pytest

def test_simple():
    #test_simple
    pass

def test_fail():
    #test_fail
    assert False

@pytest.mark.xfail(reason="reason1")
def test_xfail_fail():
    #test_xfail_fail
    assert False

@pytest.mark.xfail(reason="reason1")
def test_xfail_pass():
    #test_xfail_pass
    assert True

@pytest.mark.skip(reason="skipper")
def test_skip():
    #test_skip
    assert True

def test_raised_exception():
    #test_raised_exception
    raise Exception("uncaught")

@pytest.mark.parametrize("a,b,c", [(1,1,1), (2,2,2), (3,3,3)])
def test_parametrize(a,b,c):
    #test_parametrize
    pass

@pytest.mark.test_id(id="this_unique_id")
def test_mark_test_id():
    #test_mark_test_id
    pass