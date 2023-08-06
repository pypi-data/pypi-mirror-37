# -*- coding: utf-8 -*-
'''
redflask工程快速构建工具
'''
import sys
import os

def main(argv):
    if len(argv) ==1:
        print( 'Use this command to build your project:' + '\n' +
              'redflask -b [project_name]' + '\n')

    elif argv[1] == '-b':
        try:
            print('project:' + argv[2] + '---start building .....')
            dojob(argv[2])
        except Exception as err:
            print('please write down your project_name')

    elif argv[1] == '-v':
        print('redflask version v0.1')

    else:
        print('error command ' + '\n' + 'Use this command to build your project:' + '\n' +
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
    main(sys.argv)