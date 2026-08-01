"""Contains the FastrakDevice class."""

import threading
import time
from typing import Self

from serial import Serial, SerialException

from .commands.noResp import (
    Boresight,
    DisableContMd,
    EnableBinOut,
    EnableContMd,
    OutputDataList,
    UnBoresight,
)
from .commands.support import FastrakStations, OutputData, SerialBaudrates
from .commands.withResp import ActiveStnState, SingleDataRecord, StationState


class FastrakDevice:
    """Defines interface for connecting, setting up, and streaming from a Fastrak.

    Attributes
    ----------
    _ser : Serial | None
        Serial connection to a Fastrak.

    _station : FastrakStations
        Station index on the Fastrak.

    _thread : threading.Thread
        Child thread for non blocking data retrieval.

    _thread :#️⃣_PollingThread | None
        Thread for polling Fastrak data.

    _COMport :
        String representing the COM port to be connected to.

    _baud : SerialBaudrates
        Baudrate for the serial connection.

    _station : FastrakStations
        Station on the Fastrak to use.

    _timeout : int, default: 1second
        Serial timeout for the connection.

    """

    _ser: Serial | None
    _station: FastrakStations
    _thread: '_PollingThread | None'
    _COMport: str
    _baud: SerialBaudrates
    _station: FastrakStations
    _timeout: int

    class _PollingThread(threading.Thread):
        """Defines a polling class for reading from a Fastrak.

        Attributes
        ----------
        _ser : Serial
            Serial connection to a Fastrak.
        _data : bytearray
            Data from last streaming session.
        _pollRate : float
            The rate to pool the Fastrak.
        """

        _ser: Serial
        _data: bytearray
        _pollRate: float

        def __init__(self, serial: Serial, pollRate: float):
            """Construct a _PollingThread class.

            Parameters
            ----------
            serial : Serial
                Serial connection to a Fastrak.
            pollRate : float
                The rate to pool the Fastrak.
            """
            super().__init__()
            self._ser = serial
            self._stop_event = threading.Event()
            self._data = bytearray()
            self._pollRate = pollRate

        @property
        def data(self) -> bytearray:
            """Contains the byte data from the last/current streaming session.

            Returns
            -------
            bytearray
                Contains the byte data from the last/current streaming session.

            """
            return self._data

        def run(self):
            """Run the polling process."""
            EnableContMd().send(self._ser)
            while True:
                try:
                    data = self._ser.read(self._ser.in_waiting)
                    self._data.extend(data)
                    is_stopped = self._stop_event.wait(self._pollRate)
                    if is_stopped:
                        break

                except SerialException:
                    break  # TODO: Add Error flag
            DisableContMd().send(self._ser)

        def stop(self):
            """Stop the thread."""
            self._stop_event.set()
            start_time = time.time()
            while self.is_alive():
                if (time.time() - start_time) > 10:
                    raise Exception('an error occurred')  # TODO: Add specific Exception
                time.sleep(0.01)

    @property
    def streaming(self) -> bool:
        """Reports the streaming status of the device.

        Returns
        -------
        bool
            True when streaming False otherwise.

        """
        if self._thread is not None:
            return self._thread.is_alive()
        return False

    @property
    def data(self) -> bytearray | None:
        """Contains the byte data from the last/current streaming session.

        Returns
        -------
        bytearray
            Contains the byte data from the last/current streaming session.

        """
        if self._thread is not None:
            return self._thread.data
        return None

    def __init__(
        self,
        COMport: str = 'COM1',
        baud: SerialBaudrates = SerialBaudrates.BAUD_19200,
        station: FastrakStations = FastrakStations.STATION_1,
        timeout: int = 1,
        setup: bool = True,
    ) -> None:
        """Construct a FastrakDevice class.

        Parameters
        ----------
        COMport : str
            String representing the COM port to be connected to.

        baud : SerialBaudrates
            Baudrate for the serial connection.

        station : FastrakStations, default: STATION_1
            Station on the Fastrak to use.

        timeout : int, default: 1second
            Serial timeout for the connection.

        setup : bool, default: True


        """
        self._ser = None
        self._COMport = COMport
        self._baud = baud
        self._timeout = timeout
        self._station = station
        self._thread = None
        if setup:
            self.connect()
            self.basicSetup()

    @classmethod
    def create_valid_device(
        cls,
        COMport: str = 'COM1',
        baud: SerialBaudrates = SerialBaudrates.BAUD_19200,
        station: FastrakStations = FastrakStations.STATION_1,
        timeout: int = 1,
        setup: bool = True,
    ) -> None | Self:
        """Construct a FastrakDevice class.

        Parameters
        ----------
        COMport : str
            String representing the COM port to be connected to.

        baud : SerialBaudrates
            Baudrate for the serial connection.

        station : FastrakStations, default: STATION_1
            Station on the Fastrak to use.

        timeout : int, default: 1second
            Serial timeout for the connection.

        setup : bool, default: True


        """
        """Create a user, or return None if conditions are not met"""
        if not (COMport and baud and station and timeout and setup is not None):
            return None
        return cls(COMport, baud, station, timeout, setup)

    def connect(self) -> None:
        """Connect to the serial device."""
        if self._ser is not None:
            self._ser.open()
        else:
            self._ser = Serial(
                self._COMport, self._baud.value * 100, timeout=self._timeout
            )

    def enableStream(self) -> None:
        """Enable streaming on the Fastrak.

        Set up streaming on the Fastrak by creating a thread where the serial stream is polled.

        """
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if not self._ser.is_open:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if self._thread is None:
            self._thread = self._PollingThread(self._ser, 0.001)

        if not self._thread.is_alive():
            self._thread.start()

    def disableStream(self) -> None:
        """Disable streaming on the Fastrak.

        Close the streaming on the Fastrak and join thread where the serial stream was polled.

        """
        if not self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if self._thread is not None:
            self._thread.stop()

    def readLine(self) -> bytes:
        """Request a single data frame from the Fastrak."""
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if not self._ser.is_open:
            raise Exception('an error occurred')  # TODO: Add specific Exception
        if self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        return SingleDataRecord().sendResp(self._ser)

    def boresight(self) -> None:
        """Set the zero position for the station."""
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if not self._ser.is_open or self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        UnBoresight(self._station).send(self._ser)
        Boresight(self._station).send(self._ser)

    def basicSetup(self) -> None:
        """Complete the basic setup of a Fastrak."""
        if self._ser is None:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        if not self._ser.is_open or self.streaming:
            raise Exception('an error occurred')  # TODO: Add specific Exception

        DisableContMd().send(self._ser)

        ActiveStnState(FastrakStations.STATION_1, StationState.OFF).send(self._ser)
        ActiveStnState(FastrakStations.STATION_2, StationState.OFF).send(self._ser)
        ActiveStnState(FastrakStations.STATION_3, StationState.OFF).send(self._ser)
        ActiveStnState(FastrakStations.STATION_4, StationState.OFF).send(self._ser)

        ActiveStnState(self._station, StationState.ON).send(self._ser)

        EnableBinOut().send(self._ser)

        OutputDataList(
            self._station,
            [
                OutputData.CART_COORDS,
                OutputData.AER_EULER_ANGLE,
                OutputData.CARRIAGE_RETURN,
            ],
        ).send(self._ser)
