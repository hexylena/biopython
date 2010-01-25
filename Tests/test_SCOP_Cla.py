# Copyright 2001 by Gavin E. Crooks.  All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.


"""Unit test for Cla"""

import unittest

from Bio.SCOP import Cla




class ClaTests(unittest.TestCase):

    def setUp(self):
        self.filename = './SCOP/dir.cla.scop.txt_test'

    def testParse(self):
        """Test if all records in a CLA file are being read"""
        f=open(self.filename)
        try: 
            count = 0
            records = Cla.parse(f)
            for record in records:
                count +=1
            self.assertEqual(count, 14)
        finally:
            f.close()
    
    def testStr(self):
        """Test if we can convert each record to a string correctly"""
        f = open(self.filename)
        try: 
            for line in f:
                record = Cla.Record(line)
                #End of line is platform dependent. Strip it off
                self.assertEqual(str(record).rstrip(), line.rstrip())
        finally:
            f.close()        

    def testError(self):
        """Test if a corrupt record raises the appropriate exception"""
        corruptRec = "49268\tsp\tb.1.2.1\t-\n"
        self.assertRaises(ValueError, Cla.Record, corruptRec)

    def testRecord(self):
        """Test one record in detail"""
        recLine = 'd1dan.1\t1dan\tT:,U:91-106\tb.1.2.1\t21953\tcl=48724,cf=48725,sf=49265,fa=49266,dm=49267,sp=49268,px=21953'

        record = Cla.Record(recLine)
        self.assertEqual(record.sid, 'd1dan.1')
        self.assertEqual(record.residues.pdbid, '1dan')
        self.assertEqual(record.residues.fragments, (('T','',''),('U','91','106')))
        self.assertEqual(record.sccs, 'b.1.2.1')
        self.assertEqual(record.sunid, 21953)
        self.assertEqual(record.hierarchy, [['cl',48724],
                                            ['cf',48725],
                                            ['sf',49265],
                                            ['fa',49266],
                                            ['dm',49267],
                                            ['sp',49268],
                                            ['px',21953]])

    def testIndex(self):
        """Test CLA file indexing"""
        index = Cla.Index(self.filename)
        
        self.assertEqual(len(index), 14)
        self.assertTrue(index.has_key('d4hbia_'))

        rec = index['d1hbia_']
        self.assertEqual(rec.sunid, 14996)



if __name__=='__main__':
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
