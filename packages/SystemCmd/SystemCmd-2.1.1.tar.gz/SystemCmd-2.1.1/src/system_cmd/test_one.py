from system_cmd import system_cmd_result


def test_one():
    system_cmd_result('.', 'ls -a')
