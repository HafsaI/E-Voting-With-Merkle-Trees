import pickle
from Merkle_Tree import MerkleTree
import csv


# if _name_ == "_main_":

def run_votes():
    """
    Creates a list of all the votes that have been placed post-election
    and stores these votes into a merkle tree.

    """
    with open("Files\polls.csv", "r") as polls:
        poll = csv.reader(polls)
        votes = []
        voterids2 = []
        voterids3 = []
        voterids4 = []
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
                                    voterid = k[0]
                n, e = public_key.split(",")
                enc_vote, n, e = int(enc_vote), int(n), int(e)
                dec_vote = pow(enc_vote, e, n)
                if dec_vote == 2:
                    voterids2.append(voterid)
                elif dec_vote == 3:
                    voterids3.append(voterid)
                elif dec_vote == 4:
                    voterids4.append(voterid)

    # print("The sequence of votes stored:-")
    # print(votes)

    # if voterids2:
    mt1 = MerkleTree(hash_type="sha256")
    mt1.add_leaves(voterids2, True)
    mt1.build_merkle_tree()

    # if voterids3:
    mt2 = MerkleTree(hash_type="sha256")
    mt2.add_leaves(voterids3, True)
    mt2.build_merkle_tree()

    # if voterids4:
    mt3 = MerkleTree(hash_type="sha256")
    mt3.add_leaves(voterids4, True)
    mt3.build_merkle_tree()

    with open("merkle1", "wb") as m_file1:  # writing in binary mode
        # converting merkle tree object to a byte stream for later use
        pickle.dump(mt1, m_file1)
    with open("merkle2", "wb") as m_file2:
        pickle.dump(mt2, m_file2)

    with open("merkle3", "wb") as m_file3:
        pickle.dump(mt3, m_file3)
# return votes


#print(run_votes())
