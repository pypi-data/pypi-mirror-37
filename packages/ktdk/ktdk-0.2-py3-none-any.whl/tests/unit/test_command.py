from ktdk.tasks.command import Command


def test_command_construction():
    echo_cmd = "echo"
    command = Command(echo_cmd)
    assert command.command == echo_cmd
    assert command.args == []


def test_command_args():
    echo_cmd = ["echo"]
    command = Command(*echo_cmd)
    command.add_args("-Wall", "-Wextra")
    assert command.args == ["-Wall", "-Wextra"]


def test_execution_simple_echo():
    echo_cmd = ["ahoj svet!"]
    command = Command('echo', args=echo_cmd)
    result = command.run()
    assert result.return_code == 0
    assert result.stdout.content == "ahoj svet!\n"
    assert result.stderr.content == ""
    assert result.ok
    assert not result.timeout


def test_execution_return_non_zero():
    echo_cmd = "exit 1"
    command = Command(echo_cmd).shell(True)
    result = command.run()
    assert result.return_code == 1
    assert result.stdout.content == ""
    assert result.stderr.content == ""
    assert result.nok
    assert not result.timeout


def test_execution_timeout():
    echo_cmd = ["127.0.0.1"]
    command = Command('ping', args=echo_cmd)
    result = command.timeout(0.5).run()
    assert result.return_code != 0
    assert result.timeout
    assert result.nok
