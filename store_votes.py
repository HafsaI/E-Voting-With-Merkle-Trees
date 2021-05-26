import pickle
from Merkle_Tree import MerkleTree
import csv


# if __name__ == "__main__":

def run_votes():
    """
    Creates a list of all the votes that have been placed post-election
    and stores these votes into a merkle tree.

    """
    with open("Files\polls.csv", "r") as polls:
        poll = csv.reader(polls)
        votes = []
        for i in poll:
            with open("Files\\ballots.csv", "r") as ballots:
                ballot = csv.reader(ballots)
                for j in ballot:
                    if i[0] == j[0]:
                        enc_vote = i[1]
                        with open("Files\\voters_data.csv", "r") as voters:
                            voter = csv.reader(voters)
                            for k in voter:
                                if j[1] == k[0]:
                                    public_key = k[2]
                n, e = public_key.split(",")
                enc_vote, n, e = int(enc_vote), int(n), int(e)
                dec_vote = pow(enc_vote, e, n)
                votes.append(str(dec_vote))
        # print("The sequence of votes stored:-")
        # print(votes)
    if votes:
        mt = MerkleTree(hash_type="sha256")
        mt.add_leaves(votes, True)
        mt.build_merkle_tree()
        with open("merkle", "wb") as m_file:  # writing in binary mode
            # converting merkle tree object to a byte stream for later use
            pickle.dump(mt, m_file)
    return votes

