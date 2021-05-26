import pickle
import hashlib
import sys
from Merkle_Tree import MerkleTree
from store_votes import run_votes


def get_hex(n):
    # encoding, hashing, binary, hex
    return hashlib.sha256(n.encode("utf-8")).hexdigest()


def run_count():
    """
    calculates total number vote for each candidate
    """
    # dicts to store number of votes for each candidate
    count_OF_candidate = dict()
    secure_vote_count = dict()
    lst = []

    cand_Id_votes = run_votes()
    print(cand_Id_votes)
    # loading a pickled file back into a Python program
    merkletree = pickle.load(open("merkle", "rb"))

    no_of_leaves = merkletree.leaves_count()

    for i in range(no_of_leaves):
        leaf = merkletree.get_leaf(i)
        if not secure_vote_count.get(leaf, None):
            secure_vote_count[leaf] = 0
        secure_vote_count[leaf] += 1

    cand_Id_votes = list(dict.fromkeys(cand_Id_votes))  # duplicate votes removed
    for vote in cand_Id_votes:
        # hex of those in cand_Id_votes
        lst.append(get_hex(vote))

    for index, key in enumerate(lst):
        count = secure_vote_count[key]
        count_OF_candidate[cand_Id_votes[index]] = count
    return count_OF_candidate

    # print("The count of votes for each candidate:-")
    # print(candidate_vote)
    # print("The candidate ID has been hidden for security reasons.")


#print(run_count())
