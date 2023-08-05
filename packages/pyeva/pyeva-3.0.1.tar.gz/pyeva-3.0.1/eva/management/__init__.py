# pylint: disable=C1801,W0212,C0103,W0122

import os
import sys
import logging
import importlib

from eva.conf import settings

CURDIR = os.path.dirname(os.path.realpath(__file__))


# cache
MAP_COMMANDS = {}


def exec_command_file(filepath):
    global_namespace = {
        "__file__": filepath,
        "__name__": "__main__",
    }
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), global_namespace)
    return global_namespace.get('Command')


def _load_commands(cmdDir):

    LOCAL_COMMANDS = {}

    for f in os.listdir(cmdDir):
        if not f.endswith('.py'):
            continue

        if f.startswith('__'):
            continue

        cmdFile = os.path.join(cmdDir, f)
        Command = exec_command_file(cmdFile)

        if not Command:
            logging.warning('%s is not a Command Module!', cmdFile)
            continue

        c = Command()

        if not (hasattr(c, 'cmd') and
                hasattr(c, 'help') and
                hasattr(c, 'run')):
            logging.warning(
                '%s is not a Command Module!', os.path.join(CURDIR, f))
            continue

        LOCAL_COMMANDS[c.cmd] = c

    return LOCAL_COMMANDS


def load_commands():

    if len(MAP_COMMANDS) != 0:
        return

    cmds = _load_commands(os.path.join(CURDIR, 'commands'))

    mod = importlib.import_module(settings.MANAGEMENT_MODULE)
    cmd_dir = os.path.realpath(mod.__path__[0])
    cmds.update(_load_commands(cmd_dir))

    MAP_COMMANDS['core'] = cmds


def print_usage():
    print('''{prog} - Eva Management Tools

Usage:

    {prog} NAMESPACE COMMAND OPTIONS

Help:

    {prog} help | -h | --help

Command:

'''.format(prog=sys.argv[0]))
    for name in MAP_COMMANDS:
        print('[{0}]'.format(name))
        cmds = MAP_COMMANDS[name]
        for k in cmds:
            command = cmds[k]
            print('    {cmd:16} {help}'.format(cmd=command.cmd, help=command.help))
        print('')

    print('''
Example:

    # 同步/创建/初始化数据库
    {prog} core syncdb --db-echo

    # core 类型的 namespace 可以省略，因此上一条命令等于
    {prog} syncdb --db-echo
'''.format(prog=sys.argv[0]))


def main(argv=None):

    if not argv:
        argv = sys.argv[1:]

    load_commands()

    if len(argv) < 1:
        print_usage()
        sys.exit(1)

    namespace = argv[0]

    # nice hack!
    if namespace.startswith('main') or namespace == 'core':
        if len(argv) < 2:
            print_usage()
            sys.exit(1)
        else:
            cmd = argv[1]
            argv = argv[2:] if len(argv) > 1 else []
    else:
        namespace = 'core'
        cmd = argv[0]
        argv = argv[1:] if argv else []

    if namespace in MAP_COMMANDS:
        cmds = MAP_COMMANDS[namespace]
        if cmd in cmds:
            cmds[cmd](argv)
            return

    if cmd in ['help', '-h', '--help']:
        print_usage()

    else:
        print('unknown cmd: ', cmd)
