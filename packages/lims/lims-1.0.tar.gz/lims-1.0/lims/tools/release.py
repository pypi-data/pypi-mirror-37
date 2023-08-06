#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import json

from lims.tools.login import login
import utils

# reload(sys)
# sys.setdefaultencoding('utf8')


class Release(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs
        self.__dict__.update(**kwargs)

        self.session = login(**kwargs)

        self.cluster = self.get_cluster()

    def start(self):

        if not self.kwargs['releaseid']:
            for row in self.get_releases():
                row['APPLYREMARK'] = row['APPLYREMARK'].replace('\n', ';') if row['APPLYREMARK']  else ''
                print '{RID}\t{PROJECTCODE}\t{PROJECTNAME}\t{APPLYREMARK}'.format(**row)

        elif not self.kwargs['release_path']:
            print 'please supply the path to release'

        else:
            self.update_release()

    def update_release(self):

        row = self.get_releases()
        print json.dumps(row, ensure_ascii=False, indent=2)

        release_size = self.get_release_size()

        release_way = self.get_release_way(release_size)

        origrec = row['ORIGREC']

        payload = [
            origrec,
            [
                release_size,
                self.kwargs['release_path'],
                'GB',
                self.kwargs['release_remark'],
                self.cluster,
                release_way,
                release_size
            ]
        ]
        print json.dumps(payload, ensure_ascii=False)

        url = '{base_url}/KF_AnalysisReport.kf_UpdateRelease.lims'.format(
            **self.kwargs)
        print '>>>[update_release POST]', url

        resp = self.session.post(url, json=payload).json()
        print resp

        if resp:
            print 'release failed because of', resp[1]
        else:
            print 'release successfully!'

        row = self.get_releases()
        print json.dumps(row, ensure_ascii=False, indent=2)

        print 'RELEASE RESULT:', row['RELEASERESULT']

    def get_cluster(self):

        cluster_map = {
            'TJ': '天津集群',
            'NJ': '南京集群',
            'USA': '美国集群'
        }

        return cluster_map.get(self.kwargs['cluster_name'])

    def get_release_size(self):

        url = '{base_url}/KF_WebServices.kf_GetReleaseSize.lims'.format(**self.kwargs)
        print '>>>[get_release_size POST]', url

        payload = [self.kwargs['release_path'], self.cluster]
        print payload[0], payload[1]

        resp = self.session.post(url, json=payload)

        return resp.text

    def get_release_way(self, release_size):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_AnalysisReport.cmbReleaseWay&Type=json&p1={cluster}&p2={release_size}'.format(
            **dict(self.__dict__, **locals()))
        print '>>>[get_release_way GET]', url

        resp = self.session.get(url)

        if resp.status_code != 200:
            print 'please check your release path: {release_path}'.format(**self.kwargs)
            exit(1)

        rows = resp.json()['Tables'][0]['Rows']

        ways = [row['TEXT'] for row in rows]

        release_way = self.kwargs['release_way']

        if release_way and release_way not in ways:
            print 'your input release way is unavailable: {release_way}'.format(**self.kwargs)
            release_way = None

        if not release_way:
            if len(ways) > 1:
                print 'There are {} ways to release, please choos from follows:\n{}'.format(
                    len(ways),
                    '\n'.join('{} {}'.format(idx, way) for idx, way in enumerate(ways)))
                while True:
                    choice = input('choose the number:')
                    if choice not in range(len(ways)):
                        print 'bad choice, please choose from {}'.format(range(len(ways)))
                        continue
                    release_way = ways[choice]
                    break
            else:
                release_way = ways[0]

        print 'release_way:', release_way

        return release_way

    def get_releases(self):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_AnalysisReport.kf_GetRelease&Type=json'.format(
            **self.kwargs)
        print '>>>[get_releases GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if not rows:
            print 'nothing to release'
            exit(0)

        if self.kwargs['project_code']:
            ret_rows = []
            for row in rows:
                if self.kwargs['project_code'] == row['PROJECTCODE']:
                    ret_rows.append(row)
            return ret_rows

        if self.kwargs['releaseid']:
            for row in rows:
                if self.kwargs['releaseid'] == row['RID']:
                    return row
            return None

        return rows


def parser_add_release(parser):

    parser.add_argument(
        '-rid', '--releaseid', help='the release id')

    parser.add_argument(
        '-project', '--project-code', help='the project code')

    parser.add_argument('-path', '--release-path', help='the path to release')

    parser.add_argument('-remark', '--release-remark', help='the remark information for this release')

    parser.add_argument(
        '-way',
        '--release-way',
        help='the release way if available',
        choices=['FTP', 'HWFTP', '阿里云', '拷盘'])

    parser.add_argument(
        '-cluster',
        '--cluster-name',
        help='the cluster to release, choose from (%(choices)s)',
        choices=['TJ', 'NJ', 'USA'],
        default='TJ')

    parser.set_defaults(func=main)


def main(**args):

    Release(**args).start()


# if __name__ == "__main__":

#     main()
