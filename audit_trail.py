import pickle
import hashlib
from Merkle_Tree import MerkleTree


def get_hash(n):
    return hashlib.sha256(n.encode()).digest().hex()


def run_audit(check_leaf_value):
    """  
    Checks for the consistency of votes received. This way we can know if any new vote has been added or if any existing votes have been changed.
    """
    Id = check_leaf_value
    leaf_value = get_hash(check_leaf_value)

    merkletree = pickle.load(open('merkle', 'rb'))
    leaves = merkletree.leaves_count()
    votes = []
    for i in range(leaves):
        votes.append(merkletree.get_leaf(i))
    try:
        index = votes.index(leaf_value)
        leaf_proof = merkletree.get_proof(index)
        given_leaf = merkletree.get_leaf(index)
        root = merkletree.get_merkle_root()

        print(merkletree.verify_proof(leaf_proof, given_leaf, root), ", candidate ID:", Id, " exists.")
        return [True, merkletree.verify_proof(leaf_proof, given_leaf, root)]
    except:
        print("Candidate ID: ", Id, " doesn't exist.")
        return [False]

    return [False]  # candidate ID exists,  merkle tree consistent


# run_audit('1')
