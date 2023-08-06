import pytest
import re
import threading
from fixtures import asciiserial, fake
from mockport import MockPort
from asciiserialwrapper import AsciiSerialWrapper
from zaber.serial import AsciiDevice, AsciiCommand


@pytest.fixture
def device(asciiserial):
    return AsciiDevice(asciiserial, 1)


def test_constructor(asciiserial):
    ad = AsciiDevice(asciiserial, 1)
    assert(ad.port == asciiserial)
    assert(ad.address == 1)


def test_send_command(device, fake):
    fake.expect("/1 0 home\r\n", "@01 0 OK BUSY WR 0\r\n")
    device.send(AsciiCommand("home"))
    fake.validate()


def test_send_command_with_device_number(device, fake):
    fake.expect("/1 0 home\r\n", "@01 0 OK BUSY -- 0\r\n")
    device.send(AsciiCommand("1 home"))
    fake.validate()


def test_send_str(device, fake):
    fake.expect("/1 0 home\r\n", "@01 0 OK BUSY -- 0\r\n")
    device.send("home")
    fake.validate()


def test_send_str_with_device_number(device, fake):
    fake.expect("/1 0 move vel 1000\r\n", "@01 0 OK BUSY -- 0\r\n")
    device.send("1 move vel 1000")
    fake.validate()


def test_send_str_with_axis_number(device, fake):
    fake.expect("/1 1 move rel -1000\r\n", "@01 1 OK BUSY -- 0\r\n")
    device.send("1 1 move rel -1000")
    fake.validate()


def test_send_str_with_multiple_arguments(device, fake):
    fake.expect("/1 0 tools setcomm 9600 1\r\n", "@01 0 OK IDLE NU 0\r\n")
    device.send("/tools setcomm 9600 1\r\n")
    fake.validate()


def test_home(device, fake):
    fake.expect("/1 0 home\r\n", "@01 0 OK BUSY WR 0\r\n")
    fake.expect("/1 0\r\n", "@01 0 OK BUSY WR 0\r\n")
    fake.expect("/1 0\r\n", "@01 0 OK IDLE -- 0\r\n")
    device.home()
    fake.validate()


def test_move_abs(device, fake):
    fake.expect("/1 0 move abs 1000\r\n", "@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0\r\n", "@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0\r\n", "@01 0 OK IDLE -- 0\r\n")
    device.move_abs(1000)
    fake.validate()


def test_move_rel(device, fake):
    fake.expect("/1 0 move rel 1322\r\n", "@01 0 OK BUSY -- 0\r\n")
    fake.expect("/1 0\r\n", "@01 0 OK IDLE -- 0\r\n")
    device.move_rel(1322)
    fake.validate()


def test_move_vel(device, fake):
    fake.expect("/1 0 move vel 3243\r\n", "@01 0 OK BUSY -- 0\r\n")
    device.move_vel(3243)
    fake.validate()


def test_stop(device, fake):
    fake.expect("/1 0 stop\r\n", "@01 0 OK BUSY NI 0\r\n")
    fake.expect("/1 0\r\n", "@01 0 OK IDLE NI 0\r\n")
    device.stop()
    fake.validate()


def test_get_status(device, fake):
    fake.expect("/1 0\r\n", "@01 0 OK BUSY -- 0\r\n")
    device.get_status()
    fake.validate()


def test_get_position(device, fake):
    fake.expect("/1 0 get pos\r\n", "@01 0 OK BUSY -- 10000\r\n")
    fake.expect("/1 0 get pos\r\n", "@01 0 OK BUSY -- 10001\r\n")
    assert(device.get_position() == 10000)
    assert(device.get_position() == 10001)
    fake.validate()


def test_get_position_multiaxis(device, fake):
    fake.expect("/1 0 get pos\r\n", "@01 0 OK BUSY -- 10000 10001\r\n")
    assert(device.get_position() == 10000)
    fake.validate()


class AsciiLoopbackMockPort(MockPort):
    def write(self, aData):
        self._lastMessage = aData
        return len(aData)

    def readline(self, aCount = -1):
        if (self._lastMessage is not None):
            match = re.match("/1 0 (?P<id>\d+) thread (?P<thread>\d+) dummy", self._lastMessage)
            return "@01 0 {id} OK IDLE -- thread {thread} dummy\r\n".format(**match.groupdict())


def test_send_multithreaded():
    """
    Check that the send method works in multi-threaded environments. All other
    methods depend on send() so will also be thread safe if send() is thread
    safe.
    """

    device = AsciiDevice(AsciiSerialWrapper(AsciiLoopbackMockPort()), 1)

    def worker(id):
        """
        A worker thread

        Args:
            id: an integer to identify the thread
        """
        for i in range(50):
            reply = device.send("/1 0 {:02} thread {} dummy".format(i, id))
            assert reply.message_id == i, \
                "expected message id {}, got {}".format(i, reply.message_id)
            assert reply.data == "thread {} dummy".format(id), \
                "incorrect data: got {}".format(reply.data)

    t1 = threading.Thread(target=worker, args=(1,))
    t2 = threading.Thread(target=worker, args=(2,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()
