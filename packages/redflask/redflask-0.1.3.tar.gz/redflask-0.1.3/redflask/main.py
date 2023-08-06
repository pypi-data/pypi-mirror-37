# -*- coding: utf-8 -*-
# @Time    : 18-10-23 上午11:37
# @Author  : Redtree
# @File    : main.py
# @Desc :

import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Use this command to build your project:' + '\n' +
                                                     'redflask -b [project_name]' + '\n')

    parser.add_argument("-v", "--version", help="show redflask version")
    parser.add_argument("-b", "--build", help="build redflask project")

    args = parser.parse_args()

    if args.version:
           print('redflask v0.1.3')
    elif args.build:
           print('project:' + args.build + '---start building .....')
           dojob(args.build)
    else:
        print('Use this command to build your project:' + '\n' +
                                                     'redflask -b [project_name]' + '\n')


def dojob(pj_name):
    try:
        src_path = sys.path[0] + '/src'
        os.popen('cp -r '+src_path+' '+pj_name)
        print(pj_name+'build success')
    except Exception as err:
        print(pj_name+'build error')
        print(err)


if __name__ == '__main__':
    main()