# pylint: disable=C0325
import os
import time
import json
import unittest
from murano_client.client import MuranoClient
from exoedge.exo_edge import ExoEdge
# from collections import deque
from six.moves import queue

test_dir = os.path.dirname(os.path.abspath(__file__))



class TestSimulator(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass
    @classmethod
    def tearDownClass(cls):
        pass
    def setUp(self):
        test_case_timeout = 5.0
        test_name = self.id().split('.')[-1]
        print("setting up for test: {}".format(test_name))

        self.test_q = queue.Queue()
        def tell_function_override(data):
            """ utilize the tell_function_override feature in murano_client """
            print("tell_function_override called with: {}".format(data))
            self.test_q.put(data)

        self.client = MuranoClient(
            murano_host='https://dne.m2.exosite.io/',
            watchlist=['config_io'],
            tell_function_override=tell_function_override,
        )

        self.edged = ExoEdge(
            self.client,
            **{'local_strategy': True,
               'config_io_file': os.path.join(test_dir, 'assets', test_name+'.json'),
               'debug': 'DEBUG'
              })
        self.edged.setup()

        start = time.time()
        while self.test_q.qsize() < 2:
            if time.time()-start >= test_case_timeout:
                break
            time.sleep(0.1)

    def tearDown(self):
        self.edged.stop()

    def test_001_sin_wave(self):
        self.assertIsNotNone(self.test_q.get(timeout=0.1))

    def test_002_echo(self):
        print("throwing away config_io from queue: {}".format(self.test_q.get(timeout=0.1)))
        data_in = self.test_q.get(timeout=0.5)['data_in']
        data_in_values = list(data_in.values())
        self.assertEqual(json.loads(data_in_values[-1])['one'], "there is no spoon")

    def test_003_do_wave(self):
        time.sleep(2.0)
        num_samples = 0
        print('*'*8+"THE LIST"+'*'*8)
        print(list(self.test_q.queue))
        for i in list(self.test_q.queue):
            print("checking: {}".format(i))
            if i.get('data_in'):
                num_samples += 1
        self.assertGreater(num_samples, 8)

    def test_004_report_on_change(self):
        time.sleep(0.2)
        num_samples = 0
        for i in list(self.test_q.queue):
            print("checking: {}".format(i))
            if i.get('data_in'):
                num_samples += 1
        self.assertLess(num_samples, 2)
        self.edged.config_io.channels["one"].protocol_config.app_specific_config['parameters'] = {"value": 0.0}
        time.sleep(0.2)
        print("queue contains: {}".format(list(self.test_q.queue)))
        last_dp = list(self.test_q.queue)[-1]
        print('last_dp: {}'.format(last_dp))
        last_dp_value = json.loads(list(last_dp['data_in'].values())[-1])["one"]
        self.assertEqual(0.0, float(last_dp_value))

    def test_005_classic_import_style(self):
        num_samples = 0
        for i in list(self.test_q.queue):
            print("checking: {}".format(i))
            if i.get('data_in'):
                num_samples += 1
        self.assertGreater(num_samples, 0)
        self.test_q.queue.clear()
        time.sleep(0.1)
        num_samples = 0
        for i in list(self.test_q.queue):
            print("checking: {}".format(i))
            if i.get('data_in'):
                num_samples += 1

        self.assertGreater(num_samples, 0)

    @unittest.skip("need to find replacement for psutil")
    def test_006_architecture(self):
        num_samples = 0
        for i in list(self.test_q.queue):
            print("checking: {}".format(i))
            if i.get('data_in'):
                num_samples += 1
        self.assertGreater(num_samples, 0)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
