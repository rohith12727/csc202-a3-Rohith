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

@dataclass(frozen = True)
class HLeaf:
    occurence_count: int
    character: str

@dataclass(frozen = True)
class HNode:
    occurence_count: int
    character: str
    left: HTree
    right: HTree

@dataclass(frozen = True)
class HTLNode:
    value: HTree
    rest: "HTList"


HTList: TypeAlias = Union[HTLNode, None]

# Return True if Huff1 is less than Huff2.
def tree_lt(Huff1: HTree, Huff2:HTree) ->bool:
    if Huff1.occurence_count < Huff2.occurence_count:
        return True
    elif Huff1.occurence_count == Huff2.occurence_count and Huff1.character < Huff2.character:
        return True
    return False

#Returns the length of a list of HTrees
def list_len(lst: HTList) -> int:
    match lst:
        case None:
            return 0
        case HTLNode(_, r):
            return 1 + list_len(r)

#Returns the Htree at the idx specified of a list of Htrees, will not work for idx > len(lst), or empty lists
def list_ref(lst: HTList, idx: int) -> HTree:
    if idx < 0:
        raise IndexError("Index out of bounds")
    match lst:
        case None:
            raise IndexError("Index out of bounds")
        
        case HTLNode(value=v, rest=r):
            if idx == 0:
                return v
            return list_ref(r, idx - 1)


           
class Tests(unittest.TestCase):
    def test_cnt_freq(self):
        self.assertEqual(cnt_freq(""), [0]*256)
        
        expected = [0] * 256
        expected[ord('t')] = 2
        expected[ord('e')] = 1
        expected[ord('x')] = 1
        self.assertEqual(cnt_freq("text"), expected)

    def test_list_len(self):
        self.assertEqual(list_len(None), 0)

        a = HLeaf(1, 'a')
        b = HLeaf(2, 'b')
        c = HLeaf(3, 'c')
        lst3 = HTLNode(a, HTLNode(b, HTLNode(c, None)))
        self.assertEqual(list_len(lst3), 3)
    
    def test_list_ref(self):
        a = HLeaf(1, 'a')
        b = HLeaf(2, 'b')
        c = HLeaf(3, 'c')

        lst = HTLNode(a, HTLNode(b, HTLNode(c, None)))

        self.assertEqual(list_ref(lst, 0), a)
        self.assertEqual(list_ref(lst, 1), b)
        self.assertEqual(list_ref(lst, 2), c)
if (__name__ == '__main__'):
    unittest.main()