from typing import *
from dataclasses import dataclass
import unittest
import sys
sys.setrecursionlimit(10**6)

#Converts a string to a list of occurences for each ASCII character in range 0-255
def cnt_freq(text: str) -> List[int]:
    freq = [0 for _ in range(256)]
    
    for character in text:
       character = ord(character)
       if 0 <= character <= 255:  
            freq[character] += 1 
   
    return freq

HTree: TypeAlias = Union["HNode", "HLeaf"]

class HNode:
    occurence_count: int
    character: str

class HLeaf:
    occurence_count: int
    character: str
    left: HTree
    right: HTree


'''def tree_lt(Huff1: Htree, Huff2:Htree) ->bool:
    match Htree:
        case Htree()
            return True
        case
            return True
        else:
            return False'''




class Tests(unittest.TestCase):
    def test_cnt_freq(self):
        self.assertEqual(cnt_freq(""), [0]*256)
        
        expected = [0] * 256
        expected[ord('t')] = 2
        expected[ord('e')] = 1
        expected[ord('x')] = 1
        self.assertEqual(cnt_freq("text"), expected)



if (__name__ == '__main__'):
    unittest.main()