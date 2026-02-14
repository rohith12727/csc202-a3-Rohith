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


HTList: TypeAlias = Union["HTLNode", None]

@dataclass(frozen = True)
class HTLNode:
    value: HTree
    rest: HTList



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
        
        case HTLNode(v, r):
            if idx == 0:
                return v
            return list_ref(r, idx - 1)

#Converts the 256 length array of ASCII character from lsd_freq to a HTList of HTrees
def base_tree_list(ASCII: List[int]) -> HTList:
    lst: HTList = None
    
    for i in range(255, -1, -1):  # 255 down to 0
        leaf = HLeaf(ASCII[i], chr(i))
        lst = HTLNode(leaf, lst)
    
    return lst

#Inserts a new HTree into a list of Htrees already sorted by tree_lt
def tree_list_insert(lst: HTList, t: HTree)-> HTList:
    match lst:
        case None:
            return HTLNode(t, None)

        case HTLNode(v, r):
            if tree_lt(t, v):
                return HTLNode(t, lst)
            return HTLNode(v, tree_list_insert(r, t))

#sorts an unsorted HTList and returns the sorted list
def initial_tree_sort(lst: HTList) -> HTList:
    match lst:
        case None:
            return None
        case HTLNode(v, r):
            sorted = initial_tree_sort(r)
            return tree_list_insert(sorted, v)


#Accepts a sorted HTList of length 2 or greater and joins the first and second nodes together before inserting back into the lst
def coalesce_once(lst: HTList) -> HTList:
    match lst:
        case None:
            return None
        case HTLNode(v, r):
            if list_len(lst) < 2:
                raise ValueError("Input list must be 2 elements or longer")
            else:
                match r:
                    case None:
                        return None
                    case HTLNode(v2, rest):
                        new_count = v.occurence_count + v2.occurence_count
                        new_char = min(v.character, v2.character)
                        new_node = HNode(new_count, new_char, v, v2)
                        
                        return tree_list_insert(rest, new_node)

#calls coalesce_once on a HTlist over and over until only one HTree of all combined values remains                     
def coalesce_all(lst: HTList) -> HTree:
    if lst is None:
        raise ValueError("Input list must contain at least one element")

    if list_len(lst) < 2:
        return lst.value

    return coalesce_all(coalesce_once(lst))

# Construct a Huffman tree from 's'.
def string_to_HTree(s : str) -> HTree:
    # chain together the functions required for the task:
    freqs = cnt_freq(s)
    treelist = base_tree_list(freqs)
    sorted_treelist = initial_tree_sort(treelist)
    return coalesce_all(sorted_treelist)

#represents an HTree as an array of 1 and 0, 1 = right, 0 = left.
def build_encoder_array(tree: HTree) -> List[str]:
    encoded = [""] * 256  
    def helper(t: HTree, path: str) -> None:
        match t:
            case HLeaf(_, ch):
                code_index = ord(ch)
                if 0 <= code_index <= 255:
                    encoded[code_index] = path
            case HNode(_, _, l, r):
                helper(l, path + "0")
                helper(r, path + "1")

    helper(tree, "")
    return encoded

def encode_string_one(s:str, encoded: List[str])-> str:
    result = ""

    for ch in s:
        result += encoded[ord(ch)]

    return result

def bits_to_bytes(bits: str) -> bytearray:
    while len(bits) % 8 != 0:
        bits += "0"

    nbytes = len(bits) // 8
    val = bytearray(nbytes)

    for i in range(nbytes):
        chunk = bits[i * 8 : (i + 1) * 8]
        val[i] = int(chunk, 2)
    return val

#Use functions to open file, and replace code as encoded
def huffman_code_file(source: str, target: str) -> None:
    # Read input file
    with open(source, "r", encoding="utf-8") as f:
        text = f.read()

    # Build Huffman tree
    tree = string_to_HTree(text)

    # Build encoder array
    encoder = build_encoder_array(tree)

    # Encode text into bit string
    bit_string = encode_string_one(text, encoder)

    # Convert bits to bytearray
    encoded_bytes = bits_to_bytes(bit_string)

    # Write output file 
    with open(target, "wb") as f:
        f.write(encoded_bytes)
 

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

    def test_base_tree_list(self):
        freq = [0] * 256
        freq[65] = 3  

        lst = base_tree_list(freq)

        first = list_ref(lst, 0)
        self.assertEqual(first.character, chr(0))
        self.assertEqual(first.occurence_count, 0)

        node_65 = list_ref(lst, 65)
        self.assertEqual(node_65.character, 'A')
        self.assertEqual(node_65.occurence_count, 3)

    def test_tree_list_insert(self):
        a = HLeaf(1, 'a')
        b = HLeaf(2, 'b')
        d = HLeaf(4, 'd')

        empty: HTList = None
        one = tree_list_insert(empty, b)
        self.assertEqual(list_len(one), 1)

        lst = HTLNode(a, HTLNode(b, HTLNode(d, None)))
        z0 = HLeaf(0, 'z')
        lst_front = tree_list_insert(lst, z0)
        self.assertEqual(list_len(lst_front), 4)
        self.assertEqual(list_ref(lst_front, 3), d)

        c = HLeaf(3, 'c')
        lst_mid = tree_list_insert(lst, c)
        self.assertEqual(list_len(lst_mid), 4)
        self.assertEqual(list_ref(lst_mid, 3), d)

        e = HLeaf(10, 'e')
        lst_end = tree_list_insert(lst, e)
        self.assertEqual(list_len(lst_end), 4)
        self.assertEqual(list_ref(lst_end, 0), a)
   
    def test_initial_tree_sort(self):
        self.assertEqual(initial_tree_sort(None), None)

        a = HLeaf(3, 'a')
        b = HLeaf(1, 'b')
        c = HLeaf(2, 'c')

        unsorted = HTLNode(a, HTLNode(b, HTLNode(c, None)))
        sorted_lst = initial_tree_sort(unsorted)
        self.assertEqual(list_ref(sorted_lst, 0), b)  
        self.assertEqual(list_ref(sorted_lst, 1), c)  
        self.assertEqual(list_ref(sorted_lst, 2), a) 

    def test_coalesce_once(self):
        a = HLeaf(1, 'a')
        b = HLeaf(2, 'b')
        c = HLeaf(5, 'c')

        lst = HTLNode(a, HTLNode(b, HTLNode(c, None)))
        result = coalesce_once(lst)
        
        merged = list_ref(result, 0)
        self.assertEqual(merged.occurence_count, 3)
    
    def test_coalesce_all(self):
        a = HLeaf(1, 'a')
        b = HLeaf(2, 'b')

        lst = HTLNode(a, HTLNode(b, None))

        result = coalesce_all(lst)
        self.assertEqual(result.character, 'a')
        self.assertEqual(result.left, a)
        self.assertEqual(result.right, b)
    
    def test_build_encoder_array(self):
        a = HLeaf(1, 'A')
        b = HLeaf(2, 'B')
        c = HLeaf(3, 'C')

        right_node = HNode(5, 'B', b, c)
        root = HNode(6, 'A', a, right_node)

        enc = build_encoder_array(root)

        self.assertEqual(enc[ord('A')], "0")
        self.assertEqual(enc[ord('B')], "10")
        self.assertEqual(enc[ord('C')], "11")
    
    def test_bits_to_bytes(self):
        self.assertEqual(bits_to_bytes(""), bytearray())

        self.assertEqual(bits_to_bytes("11111111"), bytearray([255]))
        self.assertEqual(bits_to_bytes("1"), bytearray([128]))
        self.assertEqual(bits_to_bytes("101"), bytearray([160]))

if (__name__ == '__main__'):
    unittest.main()