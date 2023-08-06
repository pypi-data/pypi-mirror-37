
import unittest, cppa3, logging, lxml, os
from cppa3.index import InboundConfiguration

from inspect import getsourcefile
from os.path import abspath, dirname, join

from copy import deepcopy

import pprint
pp = pprint.PrettyPrinter(indent=4)

class IndexTestCase( unittest.TestCase ):

    def setUp(self):
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.DEBUG,
                            filename="index_test.log")
        thisdir = dirname(abspath(getsourcefile(lambda:0)))
        self.unify_testdatadir = join(thisdir,'data')
        self.match_testdatadir = join(thisdir,'data_match')
        self.parser = lxml.etree.XMLParser(remove_blank_text=True)

    def do_index_push_bindings(self, id):
        logging.info('------------------')
        logging.info('Running test {}'.format(id))
        logging.info('Running index for CPA for id {}'.format(id))
        cpa_file = os.path.join(self.unify_testdatadir,'cppa_ab_{}.xml'.format(id))
        cpa =  (lxml.etree.parse(cpa_file, self.parser)).getroot()
        config = InboundConfiguration()
        config.load_cpa(cpa)
        logging.info(pp.pformat(config.incoming_channel_from_push_transport))


    def test_1625(self):
       self.do_index_push_bindings('1625')
