#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
# import time
import getpass
import binascii
import requests
import ConfigParser


reload(sys)
sys.setdefaultencoding('utf8')


def login(**args):
    '''
    need params: base_url, config, username, password
    '''

    session = requests.session()

    conf = ConfigParser.ConfigParser()

    ori_username, ori_password = get_username_password(conf=conf, **args)

    # real username and password to login
    username = ori_username.upper()
    password = map(binascii.b2a_hex, ori_password)
    password = ''.join(map('{:0>4}'.format, password)).upper()

    # step1: get user info
    url = '{base_url}/Authentication.GetUserInfoHtml.lims'.format(**args)
    print '>>>[getinfo POST]', url
    payload = [username, password]
    user_info = session.post(url, json=payload).json()

    if not user_info:
        print 'login failed, wrong username or password!'
        exit(1)

    print 'get user info successfully'
    depts = user_info[0]['Tables'][0]['Rows']
    roles = user_info[1]['Tables'][0]['Rows']

    dept_idx = role_idx = 0

    if len(depts) > 1:
        print 'There are {} depts for {}:'.format(len(depts), username)
        print '\n'.join('{} {}'.format(idx, dept['Dept']) for idx, dept in enumerate(depts))
        dept_idx = input('please choose your dept:')

    if len(roles) > 1:
        print 'There are {} roles for {}:'.format(len(roles), username)
        print '\n'.join('{} {}'.format(idx, role['ROLE']) for idx, role in enumerate(roles))
        role_idx = input('please choose your role:')

    dept = user_info[0]['Tables'][0]['Rows'][dept_idx]['Dept']
    role = user_info[1]['Tables'][0]['Rows'][role_idx]['ROLE']
    print username, dept, role

    # step2: login
    url = '{base_url}/Authentication.LoginMobile.lims'.format(**args)
    print '>>>[auth GET]', url
    payload = {
        'user': username,
        'password': password,
        'dept': dept,
        'role': role,
        'platforma': 'HTML',
        # 'FormId': '',
        # 'FormArgs': '',
        # 'no_c': int(time.time()),
    }
    result = session.get(url, params=payload).text

    if 'Error' in result:
        print result
        exit(1)

    print 'login successfully!'

    if args.get('config'):

        if os.path.exists(args['config']):
            conf.read(args['config'])

        with open(args['config'], 'w') as out:
            if not conf.has_section(ori_username):
                conf.add_section(ori_username)
            conf.set(ori_username, 'password', ori_password)
            conf.write(out)
            print 'update config file'

    return session


def get_username_password(conf, **args):

    username = args.get('username')

    password = args.get('password')

    if not password:

        if args.get('config') and os.path.exists(args['config']):

            print 'read config file: {}'.format(args['config'])
            conf.read(args['config'])

            if conf.has_section(username):
                password = conf.get(username, 'password')

    if not password:
        print 'password or config file is required to login for user {}'.format(username)
        password = getpass.getpass()

    return username, password


if __name__ == '__main__':

    import sys

    if len(sys.argv) < 3:
        print 'usage: python %s <username> <password>' % sys.argv[0]
        exit(1)

    username, password = sys.argv[1:3]

    base_url = 'http://172.17.8.19/starlims11.novogene'

    login(**locals())
