import unittest
import sys, os
import numpy as np
sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from startracker.star import Star
from startracker.edge import Edge

class Edge_test(unittest.TestCase):
    
    
    def test_equal_self(self):
        s1 = Star(1,0,None,None)
        s2 = Star(2,0,None,None)
        e = Edge(s1,s2)
        self.assertEquals(e,e)
    
    def test_equal_duplicate(self):
        s1 = Star(1,0,None,None)
        s2 = Star(2,0,None,None)
        e1 = Edge(s1,s2)
        e2 = Edge(s1,s2)
        self.assertEquals(e1,e2)
       
    def test_unequals(self):
        s1 = Star(1,0,None,None)
        s2 = Star(2,0,None,None)
        e1 = Edge(s1,s2)
        s3 = Star(3,0,None,None)
        e2 = Edge(s1,s3)
        self.assertNotEquals(e1,e2)
