#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys

from lims.tools.login import login
import utils


reload(sys)
sys.setdefaultencoding('utf8')


class Sample(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(**kwargs)

    def get_samples(self):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingSample_H&Type=json&p1={stage_code}'.format(**self.kwargs)
        print '>>>[get_samples GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        # print 'keys:', '\n'.join(rows[0].keys())

        outfile = self.kwargs['output'] or '{stage_code}.samples.xls'.format(**self.kwargs)

        with open(outfile, 'w') as out:
            fields = 'STAGECODE SAMPLEID SAMPLENAME LIBINDEX QCINDEX PATH'.split()
            print '\t'.join(fields)
            out.write('\t'.join(fields) + '\n')

            for row in rows:
                line = [str(row.get(field)) for field in fields]
                print '\t'.join(line)
                out.write('\t'.join(line) + '\n')


def parser_add_sample(parser):

    parser.add_argument(
        '-stage', '--stage-code', help='the stage code', required=True)

    parser.add_argument(
        '-o',
        '--output',
        help='the output filename')

    parser.set_defaults(func=main)


def main(**args):

    Sample(**args).get_samples()


# if __name__ == "__main__":

#     main()
