import pytest
from threading import Thread
from fixtures import asciiserial, fake
from mockport import MockPort
from asciiserialwrapper import AsciiSerialWrapper
from zaber.serial import AsciiAxis, AsciiDevice, TimeoutError


@pytest.fixture
def device(asciiserial):
    return AsciiDevice(asciiserial, 1)


@pytest.fixture
def axis(device):
    return AsciiAxis(device, 1)


def test_constructor(device):
    a = AsciiAxis(device, 1)
    assert(a.number == 1)
    assert(a.parent is not None)


def test_can_be_constructed_from_asciidevice(device):
    a = device.axis(1)
    b = device.axis(2)
    assert(a.number == 1)
    assert(b.number == 2)


def test_home(axis, fake):
    fake.expect("/1 1 home\r\n", "@01 1 OK BUSY WR 0\r\n")
    fake.expect("/1 1\r\n", "@01 1 OK IDLE -- 0\r\n")
    axis.home()
    fake.validate()


def test_move_abs(axis,fake):
    fake.expect("/1 1 move abs 10234\r\n", "@01 1 OK BUSY -- 0\r\n")
    fake.expect("/1 1\r\n", "@01 1 OK IDLE -- 0\r\n")
    axis.move_abs(10234)
    fake.validate()


def test_poll_until_idle_will_continue_polling(axis, fake):
    for i in range(100):
        fake.expect("/1 1\r\n", "@01 1 OK BUSY -- 0\r\n")
    fake.expect("/1 1\r\n", "@01 1 OK IDLE -- 0\r\n")
    axis.poll_until_idle()
    fake.validate()


def test_move_rel(axis, fake):
    fake.expect("/1 1 move rel 12312\r\n", "@01 1 OK BUSY -- 0\r\n")
    fake.expect("/1 1\r\n", "@01 1 OK IDLE -- 0\r\n")
    axis.move_rel(12312)
    fake.validate()


def test_move_vel(axis, fake):
    fake.expect("/1 1 move vel 1005\r\n", "@01 1 OK BUSY -- 0\r\n")
    axis.move_vel(1005)
    fake.validate()


def test_stop(axis, fake):
    fake.expect("/1 1 stop\r\n", "@01 1 OK BUSY NI 0\r\n")
    fake.expect("/1 1\r\n", "@01 1 OK IDLE -- 0\r\n")
    axis.stop()
    fake.validate()


def test_invalid_axis_number_raises_value_error(device):
    with pytest.raises(ValueError):
        AsciiAxis(device, 10)


def test_get_status(axis, fake):
    fake.expect("/1 1\r\n", "@01 1 OK IDLE -- 0\r\n")
    fake.expect("/1 1\r\n", "@01 1 OK BUSY -- 0\r\n")
    assert(axis.get_status() == "IDLE")
    assert(axis.get_status() == "BUSY")
    fake.validate()


def test_get_position(axis, fake):
    fake.expect("/1 1 get pos\r\n", "@01 1 OK BUSY -- 10000\r\n")
    fake.expect("/1 1 get pos\r\n", "@01 1 OK BUSY -- 10001\r\n")
    assert(axis.get_position() == 10000)
    assert(axis.get_position() == 10001)
    fake.validate()


class AsciiLoopbackMockPort(MockPort):
    def write(self, aData):
        self._lastMessage = aData
        return len(aData)

    def readline(self, aCount = -1):
        if (self._lastMessage is not None):
            match = re.match("/1 1 (?P<id>\d+) thread (?P<thread>\d+) dummy", self._lastMessage)
            return "@01 1 {id} OK IDLE -- thread {thread} dummy\r\n".format(**match.groupdict())

def test_send_multithreaded():
    """
    Check that the send method works in multi-threaded environments. All other
    methods depend on send() so will also be thread safe if send() is thread
    safe.
    """

    axis = AsciiAxis(AsciiDevice(AsciiSerialWrapper(AsciiLoopbackMockPort()), 1), 1)

    def worker(id):
        """
        A worker thread

        Args:
            id: an integer to identify the thread
        """
        for i in range(50):
            reply = axis.send("/1 1 {:02} thread {} dummy".format(i, id))
            assert reply.message_id == i, \
                "expected message id {}, got {}".format(i, reply.message_id)
            assert reply.data == "thread {} dummy".format(id), \
                "incorrect data: got {}".format(reply.data)

    t1 = Thread(target=worker, args=(1,))
    t2 = Thread(target=worker, args=(2,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()