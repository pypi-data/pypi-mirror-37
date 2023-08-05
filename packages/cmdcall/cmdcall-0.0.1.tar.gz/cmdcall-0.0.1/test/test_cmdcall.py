#!/usr/bin/env python

import sys
import subprocess
import unittest
import logging

log = logging.getLogger(__name__)

class TestJobExporter(unittest.TestCase):
    """
    Test job_exporter.py
    """
    def setUp(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                level=logging.INFO)

    def tearDown(self):
        pass

    def call_entry(self, *args):
        cmd = ["python", "entry.py", "foo"]
        cmd.extend(args)
        p = subprocess.Popen(cmd)
        p.wait()
        return p.returncode

    def test_cmdcall_with_all_positional_args(self):
        self.assertEquals(10, self.call_entry("1", "2", "3", "4"))

    def test_cmdcall_with_key_val_args(self):
        self.assertEquals(10, self.call_entry("1", "--c", "3", "2", "--d", "4"))

    def test_cmdcall_with_wrong_number_of_args(self):
        self.assertEquals(1, self.call_entry("1", "2", "3", "4", "5"))


if __name__ == '__main__':
    unittest.main()
