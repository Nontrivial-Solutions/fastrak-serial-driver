"""Support file."""

import pytest
from pytest_mock.plugin import MockerFixture

from src.fastrakDevice import FastrakDevice

# =================================================================================================
# =================================================================================================
# =================================================================================================
#  Support
# =================================================================================================
# =================================================================================================
# =================================================================================================

# =================================================================================================
# =================================================================================================
# Stub and Mock Classes
# =================================================================================================
# =================================================================================================


# ruff: disable[D103]
class _SerialStub:
    """Stub of a pyserial interface."""

    _is_open: bool
    _in_waiting: int

    def __init__(self, *args, **kwargs):
        self._is_open = True
        self._in_waiting = 1
        pass

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def in_waiting(self) -> int:
        return self._is_open

    def open(self):
        self._is_open = True
        pass

    def close(self):
        self._is_open = False
        pass

    def read(self, size=1):
        return b'Some Bytes'

    def write(self, data):
        pass

    def readline(self):
        return b'Some Bytes'


# ruff: enable[D103]
# =================================================================================================
# =================================================================================================
# Fixtures
# =================================================================================================
# =================================================================================================
@pytest.fixture
def setupFastrakDevice(mocker: MockerFixture):
    """Fixture for setting up a FastrakDevice with a mocked serial interface.

    ----------
    mocker : MockerFixture
        Mocking tooling fixture.
    """
    mocker.patch('src.fastrakDevice.Serial', _SerialStub)
    device = FastrakDevice.create_valid_device()
    assert device is not None
    assert device._ser.is_open  # ty: ignore

    yield device

    if device._thread is not None and device._thread is not None:
        device._thread.stop()


@pytest.fixture
def setupSerial():
    """Fixture for setting up a serial device with a mocked serial interface."""
    device = _SerialStub()
    assert device is not None

    yield device

