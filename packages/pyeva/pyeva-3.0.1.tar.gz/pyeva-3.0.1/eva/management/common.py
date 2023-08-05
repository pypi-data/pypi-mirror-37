# pylint: disable=E1101

import argparse


def apply_common_options(args):

    import tornado.options
    tornado.options.options.logging = "debug" if args.debug else 'info'
    tornado.options.parse_command_line()


class EvaManagementCommand:

    def __init__(self):
        self.cmd = None
        self.help = None
        self.args = None

    def get_argument_parser(self):
        parser = argparse.ArgumentParser(prog=self.cmd)
        return parser

    def add_arguments(self, parser):
        pass

    def parse_argv(self, argv):
        parser = self.get_argument_parser()

        # 增加通用选项
        parser.add_argument('-d', dest='debug', action='store_true',
                            help='show debug')
        parser.add_argument('--ignore-env-check', action='store_true',
                            help='忽略开发/测试环境检查')

        self.add_arguments(parser)
        self.args = parser.parse_args(argv)

    def __call__(self, argv):
        self.parse_argv(argv)

        # 应用通用配置
        apply_common_options(self.args)

        self.run()
