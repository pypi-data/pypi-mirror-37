import pytest


@pytest.fixture(autouse=True)
def b(capsys):
    print("hello pytest")
    out, err = capsys.readouterr()
    assert out == "hello pytest\n"


@pytest.mark.hello
def test_hello():
    assert "test" == "test"


@pytest.fixture(params=["a", "b", "c"])
def param(request):
    return request.param


def test_world(param):
    assert param
    assert "test" == "test"


# @pytest.mark.usefixtures("b")
class TestClass:
    def test_a(self,):
        pass

    def test_b(self, b):
        pass


import pytest


@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
def data_set(request):
    return request.param


def test_data(data_set):
    assert "data"


@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
