import pickle, hashlib
from Merkle_Tree import MerkleTree
from store_votes import run_votes


def get_hex(n):
    # encoding, hashing, binary, hex
    return hashlib.sha256(n.encode("utf-8")).hexdigest()


def run_count():
    """
    calculates total number vote for each candidate
    """

    run_votes()  # just to make merkle tree
    # loading a pickled file back into a Python program
    merkletree1 = pickle.load(open("merkle1", "rb"))
    merkletree2 = pickle.load(open("merkle2", "rb"))
    merkletree3 = pickle.load(open("merkle3", "rb"))

    no_of_leaves1 = merkletree1.leaves_count()
    no_of_leaves2 = merkletree2.leaves_count()
    no_of_leaves3 = merkletree3.leaves_count()


    dictt = dict()
    dictt['2'] = no_of_leaves1
    dictt['3'] = no_of_leaves2
    dictt['4'] = no_of_leaves3
    return dictt

#print(run_count())
