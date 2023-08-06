#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''\033[1;32m========================================================
      ___                    ___           ___
     /  /\       ___        /  /\         /  /\\
    /  /:/      /__/\      /  /::|       /  /::\\
   /  /:/       \__\:\    /  /:|:|      /__/:/\:\\
  /  /:/        /  /::\  /  /:/|:|__   _\_ \:\ \:\\
 /__/:/      __/  /:/\/ /__/:/_|::::\ /__/\ \:\ \:\\
 \  \:\     /__/\/:/~~  \__\/  /~~/:/ \  \:\ \:\_\/
  \  \:\    \  \::/           /  /:/   \  \:\_\:\\
   \  \:\    \  \:\          /  /:/     \  \:\/:/
    \  \:\    \__\/         /__/:/       \  \::/
     \__\/                  \__\/         \__\/

                --toolkits to operate lims for novogene
========================================================\033[0m
'''
import os
import sys
import getpass
import argparse


ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
sys.path.insert(0, ROOT_DIR)


from lims.tools.report import parser_add_report
from lims.tools.sample import parser_add_sample
from lims.tools.check import parser_add_check
from lims.tools.release import parser_add_release


BASE_URL = 'http://172.17.8.19/starlims11.novogene'


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__,
        # usage='lims [OPTIONS] SUBCMD [SUB-OPTIONS]',
        epilog='contact: suqingdong@novogene.com',
        formatter_class=argparse.RawTextHelpFormatter)

    # parser.add_argument(
    #     '-stage',
    #     '--stage-code',
    #     help='the stage code',
    #     required=True)

    parser.add_argument(
        '-u',
        '--username',
        help='the username to login lims[default=%(default)s]',
        default=getpass.getuser())

    parser.add_argument('-p', '--password', help='the password to login lims')

    parser.add_argument(
        '-c',
        '--config',
        help='the config file to login lims[default=%(default)s]',
        default=os.path.join(os.path.expanduser('~'), '.lims.ini'))

    # 子命令解析
    subparser = parser.add_subparsers(
        title='sub-commands',
        description='valid sub-commands',
        help='additional help',
        dest='subparser_name')

    # 1 上传报告
    parser_report = subparser.add_parser('report')
    parser_add_report(parser_report)

    # 2 获取样本信息
    parser_sample = subparser.add_parser('sample')
    parser_add_sample(parser_sample)

    # 3 DoubleCheck报告
    parser_check = subparser.add_parser('check')
    parser_add_check(parser_check)

    # 4 数据释放
    parser_release = subparser.add_parser('release')
    parser_add_release(parser_release)

    args = parser.parse_args()

    args.func(base_url=BASE_URL, **vars(args))
