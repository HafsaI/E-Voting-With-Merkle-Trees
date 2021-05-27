import pickle, hashlib, csv
from Merkle_Tree import MerkleTree


def get_decvote(voter_id):
    with open("Files\\voters_data.csv", "r") as votes:
        vote = csv.reader(votes)
        for i in vote:
            if i[0] == voter_id:
                public_key = i[2]
                with open("Files\\ballots.csv", "r") as ballots:
                    ballot = csv.reader(ballots)
                    for j in ballot:
                        if j[1] == i[0]:
                            with open("Files\polls.csv", "r") as polls:
                                poll = csv.reader(polls)
                                for k in poll:
                                    if k[0] == j[0]:
                                        enc_vote = k[1]
        n, e = public_key.split(",")
        enc_vote, n, e = int(enc_vote), int(n), int(e)
        dec_vote = pow(enc_vote, e, n)
    return str(dec_vote)


def get_hash(n):
    return hashlib.sha256(n.encode()).digest().hex()


def run_audit(check_leaf_value):
    """  
    Checks for the consistency of votes received. This way we can know if any new vote has been added or if any existing votes have been changed.
    """
    Id = check_leaf_value
    leaf_value = get_hash(check_leaf_value)
 
    merkletree1 = pickle.load(open("merkle1", "rb"))
    merkletree2 = pickle.load(open("merkle2", "rb"))
    merkletree3 = pickle.load(open("merkle3", "rb"))
    if get_decvote(Id) == '2':
        leaves = merkletree1.leaves_count()
        merkletree = merkletree1
    elif get_decvote(Id) == '3':
        leaves = merkletree2.leaves_count()
        merkletree = merkletree2
    else:
        leaves = merkletree3.leaves_count()
        merkletree = merkletree3

    votes = []
    for i in range(leaves):
        votes.append(merkletree.get_leaf(i))
    try:
        index = votes.index(leaf_value)
        leaf_proof = merkletree.get_proof(index)
        given_leaf = merkletree.get_leaf(index)
        root = merkletree.get_merkle_root()

        print(merkletree.verify_proof(leaf_proof, given_leaf, root),
              ", voter ID:", Id, " exists.")
        if merkletree.verify_proof(leaf_proof, given_leaf, root):
            return True
        else:
            return False
    except:
        print("Voter ID: ", Id, " doesn't exist.")
        return False


#print(run_audit("9f77061288"))