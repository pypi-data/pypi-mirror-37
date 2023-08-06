import pytest
import threading
import time
from fixtures import fake, asciiserial
from zaber.serial import AsciiSerial, AsciiCommand, AsciiReply, BinaryCommand, TimeoutError


def test_write_command(asciiserial, fake):
    fake.expect("/1 0 echo TEST\r\n")
    asciiserial.write(AsciiCommand("/1 echo TEST\r\n"))
    fake.expect("/1 0 echo TEST\r\n")
    asciiserial.write("/1 echo TEST\r\n")
    fake.expect("/1 0 echo TEST\r\n")
    asciiserial.write("1 echo TEST")
    fake.validate()


def test_write_empty_string(asciiserial, fake):
    fake.expect("/0 0\s*\r\n")
    asciiserial.write("")
    fake.expect("/1 0\r\n")
    asciiserial.write("1")
    fake.expect("/2 2\r\n")
    asciiserial.write("2 2")
    fake.validate()


def test_write_string(asciiserial, fake):
    fake.expect("/0 0 home\r\n")
    asciiserial.write("home")
    fake.expect("/1 0 move abs 2000\r\n")
    asciiserial.write("1 move abs 2000")
    fake.expect("/5 0 tools setcomm 9600 1\r\n")
    asciiserial.write("5 tools setcomm 9600 1")
    fake.expect("/3 2 move rel -200\r\n")
    asciiserial.write("3 2 move rel -200")
    fake.validate()


def test_write_binary_bytes(asciiserial, fake):
    fake.expect("/1 0 home\r\n")
    asciiserial.write(b"1 home\r\n")
    fake.validate()


def test_read_returns_command(asciiserial, fake):
    fake.stuff_receive_buffer("@01 0 OK IDLE -- 0\r\n")
    reply = asciiserial.read()
    assert(isinstance(reply, AsciiReply))
    assert(reply.device_address == 1)
    assert(reply.axis_number == 0)
    assert(reply.reply_flag == 'OK')
    assert(reply.device_status == 'IDLE')
    assert(reply.warning_flag == '--')
    assert(reply.data == '0')
    fake.validate()


def test_read_complains_on_malformed_input(asciiserial, fake):
    fake.stuff_receive_buffer("bad input\r\n")
    with pytest.raises(ValueError):
        asciiserial.read()
    fake.validate()
        

def test_can_change_baudrate():
    asciiserial = AsciiSerial("loop://")
    # If _ser gets renamed, then this test will need to be changed too.
    underlying_serial = asciiserial._ser
    for rate in (9600, 19200, 38400, 57600, 115200):
        asciiserial.baudrate = rate
        assert(underlying_serial.baudrate == rate)


def test_sending_BinaryCommand_raises_error(asciiserial):
    with pytest.raises(TypeError):
        asciiserial.write(BinaryCommand(1, 55, 23423))


def test_read_times_out_with_empty_buffer(asciiserial):
    with pytest.raises(TimeoutError):
        asciiserial.read()


def test_close_and_reopen(asciiserial):
    asciiserial.close()
    asciiserial.open()


def test_port_not_string_trac1365():
    with pytest.raises(TypeError):
        ser = AsciiSerial(1)


def test_port_url_works_trac1362():
    ser = AsciiSerial("loop://")


def test_cannot_set_lock(asciiserial):
    with pytest.raises(AttributeError):
        asciiserial.lock = "anything"


def test_can_read(asciiserial, fake):
    assert not asciiserial.can_read()
    fake.stuff_receive_buffer(" ")
    assert asciiserial.can_read()
