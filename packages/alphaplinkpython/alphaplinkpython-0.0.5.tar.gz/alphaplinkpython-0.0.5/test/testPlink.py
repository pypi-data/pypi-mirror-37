import unittest
from context import PlinkWriter 
import numpy as np

class testPlink(unittest.TestCase):

    def file_len(self,fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def testWriteBimFile(self):
        
        arr = np.random.randint(0,1,100, dtype=np.int8)

        PlinkWriter.writeBimFile(arr, "test.bim")

        self.assertEqual(self.file_len("test.bim"),100)


    def testAppendBam(self):

        arr = np.random.randint(0, 1, (100,100), dtype=np.int8)

        PlinkWriter.appendLociToBedAndBim(arr, "test")
        for i in range(0,100):
            PlinkWriter.appendLociToBedAndBim(arr, "test")

        self.assertEqual(self.file_len("test.bim"), 10200)
