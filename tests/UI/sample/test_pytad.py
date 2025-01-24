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

@pytest.mark.test_id()
def test_test_id_no_param():
    #test_test_id_no_param
    pass

def test_dummy2():
    #test_dummy2
    pass

def test_dummy3():
    #test_dummy3
    if True:
        pass

def test_dummy4():
    #test_dummy4
    pass

def test_dummy5():
    #test_dummy5
    pass

def test_dummy6():
    #test_dummy6
    pass
