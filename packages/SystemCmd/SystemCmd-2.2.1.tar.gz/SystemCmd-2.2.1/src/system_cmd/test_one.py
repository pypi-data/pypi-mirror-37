from system_cmd import system_cmd_result


def test_one():
    system_cmd_result('.', 'ls -a')



def test_false():
    system_cmd_result('.', 'cp not-existing done')
