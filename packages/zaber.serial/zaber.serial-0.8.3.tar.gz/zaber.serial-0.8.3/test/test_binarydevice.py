import random
import struct
import threading
import pytest
from fixtures import binaryserial, fake
from zaber.serial import BinaryCommand, BinaryDevice, BinaryReply, BinarySerial, UnexpectedReplyError


@pytest.fixture()
def device(binaryserial):
    return BinaryDevice(binaryserial, 1)


def test_constructor(binaryserial):
    bd1 = BinaryDevice(binaryserial, 1)
    bd2 = BinaryDevice(binaryserial, 2)
    assert(bd1.number == 1)
    assert(bd2.number == 2)
    assert(bd1.port == bd2.port == binaryserial)


def test_send(device, fake):
    fake.expect(pack(device.number, 1, 2, 3), pack(device.number, 1, 44, 3))
    device.send(1, 2, 3)
    fake.validate()


def test_send_overwrites_device_number(device, fake):
    fake.expect(pack(device.number, 1, 2), pack(device.number, 1, 0))
    device.send(BinaryCommand(device.number + 1, 1, 2))
    fake.validate()


def test_send_complains_on_unexpected_response(device, fake):
    fake.expect(pack(device.number, 2, 3, 4), pack(device.number + 1, 2, 3, 4))
    with pytest.raises(UnexpectedReplyError):
        device.send(2, 3, 4)
    fake.validate()


def test_send_complains_if_message_id_does_not_match(device, fake):
    fake.expect(pack(device.number, 3, 3, 3), pack(device.number, 3, 3, 45))
    with pytest.raises(UnexpectedReplyError):
        device.send(3, 3, 3)
    fake.validate()


def test_send_with_id_receives_with_id(device, fake):
    fake.expect(pack(device.number, 3, 3, 7), pack(device.number, 3, 3, 7))
    replies = []
    replies.append(device.send(3, 3, 7))
    assert(len(replies) == 1)
    assert(replies[0].message_id == 7)
    fake.validate()


def test_send_without_id_receives_without_id(device, fake):
    fake.expect(pack(device.number, 3, 3), pack(device.number, 3, 3))
    replies = []
    replies.append(device.send(3, 3))
    assert(len(replies) == 1)
    assert(replies[0].message_id is None)
    fake.validate()


def test_home(device, fake):
    fake.expect(pack(device.number, 1, 0), pack(device.number, 1, 0))
    device.home()
    fake.validate()


def test_moveabs(device, fake):
    fake.expect(pack(device.number, 20, 1000), pack(device.number, 20 ,1000))
    device.move_abs(1000)
    fake.validate()


def test_moverel(device, fake):
    fake.expect(pack(device.number, 21, 1000), pack(device.number, 21, 2000))
    device.move_rel(1000)
    fake.validate()


def test_movevel(device, fake):
    fake.expect(pack(device.number, 22, 200), pack(device.number, 22, 200))
    device.move_vel(200)
    fake.validate()


def test_stop(device, fake):
    fake.expect(pack(device.number, 23, 0), pack(device.number, 23, 23134))
    device.stop()
    fake.validate()


def test_getstatus(device, fake):
    fake.expect(pack(device.number, 54, 0), pack(device.number, 54, 0))
    status = device.get_status()
    assert(status == 0)
    fake.validate()


def test_getposition(device, fake):
    fake.expect(pack(device.number, 60, 0), pack(device.number, 60, 10000))
    fake.expect(pack(device.number, 60, 0), pack(device.number, 60, 10001))
    assert(device.get_position() == 10000)
    assert(device.get_position() == 10001)
    fake.validate()


def pack(device, command, data = 0, message_id = None):
    packed = struct.pack("<2Bl", device, command, data)
    if message_id is not None:
        packed = packed[:5] + struct.pack("B", message_id)
    return packed


def test_send_multithreaded():
    device = BinarySerial("loop://")
    """
    Check that the send method works in multi-threaded environments. All other
    methods depend on send() so will also be thread safe if send() is thread
    safe.
    """
    def worker(id):
        """
        A worker thread

        Args:
            id: an integer to identify the thread
        """
        for msg_id in range(50):
            command = random.choice(range(255))
            data = random.choice(range(65535))
            print("sending", int(pack(id, command, data, msg_id)))
            reply = device.send(pack(id, command, data, msg_id))
            assert reply.device_number == id, \
                "expected device id {}, got {}".format(id, reply.device_number)
            assert reply.command_number == command, \
                "expected command {}, got {}".format(command, reply.command_number)
            assert reply.message_id == msg_id, \
                "expected message id {}, got {}".format(msg_id, reply.message_id)
            assert reply.data == data, \
                "expected data {}, got {}".format(data, reply.data)

    t1 = threading.Thread(target=worker, args=(1,))
    t2 = threading.Thread(target=worker, args=(2,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()
