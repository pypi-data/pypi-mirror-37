#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys

from lims.tools.login import login
import utils


reload(sys)
sys.setdefaultencoding('utf8')


class Report(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(**kwargs)

    def start(self):

        if self.kwargs['show_status']:
            self.show_report_status()
            exit(0)

        if self.kwargs['delete']:
            self.delete_report()
            exit(0)

        if not self.kwargs['filename']:
            print '[error] please supply your report file!'
            exit(1)

        if not self.kwargs['type']:
            print '[error] please specific the type of report!'
            exit(1)

        if self.kwargs['type'] == 'final' and self.has_upload_final():
            print 'final report already uploaded!'
            # exit(1)

        self.upload_report()

    def has_upload_final(self):

        url = '{base_url}/KF_DataAnalysis.HasUploadFinalReport.lims'.format(**self.kwargs)
        print '>>>[check_final POST]', url

        payload = [self.kwargs['stage_code']]

        return self.session.post(url, json=payload).text == 'false'

    def upload_report(self):

        # step1: 上传文件
        url = '{base_url}/Runtime_Support.SaveFileFromHTML.lims?ScriptName=QuickIntro.uploadFileProcessingScript'.format(**self.kwargs)
        print '>>>[upload_processing POST]', url
        with utils.safe_open(self.kwargs['filename'], 'rb') as f:
            resp = self.session.post(url, files={'file': f}).json()

        if resp['success']:
            print resp['result']

        # step2: 填写报告
        payload = resp['result'] + [
            self.kwargs['stage_code'], self.kwargs['type'].upper(), None
        ]

        if self.kwargs['type'] == 'final':
            payload += [
                self.kwargs['sop_method'], self.kwargs['sample_count'],
                self.kwargs['data_size']
            ]

        url = '{base_url}/KF_DataAnalysis.UploadReport_H.lims'.format(**self.kwargs)
        print '>>>[upload_report POST]', url
        resp = self.session.post(url, json=payload).json()

        if resp[-1] == 'SUCCESS':
            report_ftp = 'ftp://172.17.8.208/KFREPORT'
            report_name = resp[0]
            print 'report upload successfully! see result: {report_ftp}/{report_name}'.format(**locals())

            report_guid = self.get_reports(report_name)['REPORT_GUID']
            print report_guid

        # step3: 提交给DoubleCheck
        url = '{base_url}/KF_DataAnalysis.SubmitStaging_H2.lims'.format(**self.kwargs)
        print '>>>[submit_report POST]', url
        payload = [report_guid, 'Draft', 'Submit']
        resp = self.session.post(url, json=payload).text

        if resp == '""':
            print 'submit report to doublecheck successfully!'
            self.show_report_status(report_guid)

    def get_reports(self, report_name=None):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgReport&Type=json&p1={stage_code}&p2=Draft'.format(**self.kwargs)
        print '>>>[get_reports GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if report_name:
            print report_name
            for row in rows:
                if row['REPORT_NAME'] == report_name:
                    return row
            return None

        return rows

    def delete_report(self):

        report = self.get_reports(self.kwargs['delete'])

        if not report:
            print 'no report names {delete}'.format(**self.kwargs)
            exit(1)

        if report['STATUS'] != 'Draft':
            print '[error] the status of report "{delete}" is "{STATUS}", only "Draft" can be deleted'.format(**dict(self.kwargs, **report))
            exit(1)

        url = '{base_url}/Sunway.DeleteRows.lims'.format(**self.kwargs)
        print '>>>[delete_report POST]', url
        payload = [
            'kf_geneticanalysis_report',
            [report['ORIGREC']]
        ]
        print payload
        resp = self.session.post(url, json=payload)

        if resp.text == 'true':
            print '[info] the report "{delete}" has been deleted'.format(**self.kwargs)

    def show_report_status(self, report_guid=None):

        rows = self.get_reports()

        for row in rows:

            if report_guid and row['REPORT_GUID'] != report_guid:
                continue

            print '{STATUS}\t{DISPSTATUS}\t{REPORT_NAME}\t{REPORT_URL}'.format(**row)


def parser_add_report(parser):

    parser.add_argument('filename', help='the report file to upload', nargs='?')

    parser.add_argument(
        '-stage', '--stage-code', help='the stage code', required=True)

    parser.add_argument(
        '-t',
        '--type',
        help='the type of report, choose from [%(choices)s]',
        choices=['qc', 'mapping', 'final'])

    parser.add_argument(
        '-sop',
        '--sop-method',
        help='the method of SOP, choose from [%(choices)s]',
        choices=['SOPTNXX0001', 'SOPTNXX0002'],
        default='SOPTNXX0001')

    parser.add_argument('-count', '--sample-count', help='the count of sample')

    parser.add_argument('-data', '--data-size', help='the total data size')

    parser.add_argument(
        '-status',
        '--show-status',
        help='show the report status',
        action='store_true')

    parser.add_argument('-d', '--delete', help='the report name to delete')

    parser.set_defaults(func=main)


def main(**args):

    Report(**args).start()


# if __name__ == "__main__":

#     main()
