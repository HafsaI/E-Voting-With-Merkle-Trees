import csv, hashlib


def generateBallot(vid) -> bool:

    """
    Generates a unique Ballot Id of voter if voter has not already voted.

    Args:
    - vid: Voter Id

    Returns:
    False if voter has already voted. 
    Ballot ID if ballot generation successful.
    """

    ballotID = hashlib.shake_256(vid.encode("utf-8")).hexdigest(5)
    flag = False
    try:
        with open("Files\\ballots.csv", "r") as readcsv:
            read_file = csv.reader(readcsv)
            for i in read_file:
                if i[1] == vid:
                    flag = True
            if not flag:
                with open("Files\\ballots.csv", "a", newline="") as csvfile:
                    file = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
                    file.writerow([ballotID, vid])
            else:
                pass

    except FileNotFoundError:
        with open("Files\\ballots.csv", "w", newline="") as csvfile:
            file = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            file.writerow([ballotID, vid])

    return ballotID if not flag else False


def encVote(vote, ballot_id, prv_key) -> bool:

    """
    Stores and encrypts vote using RSA Encryption method.

    Args:
    - vote: candidate number
    - ballot_id: Ballot ID of the voter
    - prv_key: Private key of voter

    Returns:
    True when encryption is successful

    """
    n, d = prv_key.split(",")
    vote, d, n = int(vote), int(d), int(n)
    enc_vote = pow(vote, d, n)

    with open("Files\polls.csv", "a", newline="") as csvfile:
        file = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        file.writerow([ballot_id, str(enc_vote)])

    return True


def run_polls(vote_cast) -> bool:

    """
    Generates ballot, Encrypts vote and Casts vote of user.

    Args:
    - vote_cast: lst of data in the form [name, voter_id, candidate_name, cand_number]

    Returns:
    True if vote casted successfully. False if voter has already voted.
    """

    voted = False
    voterID = vote_cast[1]
    vote = vote_cast[3]
    with open("Files\\voters_data.csv", "r") as voter_file:
        voters = csv.reader(voter_file)
        flag = False
        prv_key = ""
        for voter in voters:
            if voter[0] == voterID:
                prv_key = voter[3]
                flag = True
        if flag:
            ballotID = generateBallot(voterID)
            if ballotID:
                encVote(vote, ballotID, prv_key)
                voted = True
            else:
                voted = False

    return voted
