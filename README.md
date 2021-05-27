# Secure E-Voting System

Secure E-Voting System is a python based project, whose main focus is handling the security of data before, during and after elections takes place. It also allows auditing of votes to ensure an unbiased voting environment. The server is made based on elections occuring in our university.

The encryption method used to ensure safety are:-

    RSA Encryption 
    Merkle Tree Hashing
  
## How to Run
Install the following libraries if you do not have them using pip on command prompt:-

    pip install flask
    pip install wtform
    
Once Installed run forms.py and interact with the GUI!
  
The Libraries used are:-

    hashlib
    pickle
    random
    csv
    flask 
    wtforms

## registeration.py
This file focuses on the registeration procedure of the voter. It takes as input a list of all data that is collected from the form and the collected data is then stores in Files/voters_data.csv. Here the candidates voter ID is created and shown to them on the form so that they can save it with themselves for whenever they want to vote. At the backend a Public and Private key of the voter is created and stored in order for encryption and decryption to take place in the other parts of the system. The method used tp generate the Public and Privates keys and the encryption and decryption of vote in further files is followed from this article:-

https://core.ac.uk/download/pdf/11779635.pdf

## vote_cast.py
This is the file where the vote is casted. The  voter's name, voter ID and the vote for their candidate is given to the function run_polls() in this file as a list. Using the voter ID the private key is retreived from Files/voters_data.csv. Once retreived a ballot is created for this voter and their ballot ID and voter ID is stored in Files/ballots.csv, once stored the vote of the voter is encrypted with the extracted private key using the RSA encryption method and then this encrypted vote and the ballot ID that was generated previously is stored in Files/polls.csv. 

## store_votes.py
Reads data from all the files i.e. voters_data.csv, ballots.csv and polls.csv. Here the encrypted vote is extracted by using the voter ID, the public key of the voter is accessed and then using the key the vote is decrypted by the RSA Encryption method. This decrypted vote basically returns the candidates ID, the votes are then stored in a list. This sequence of candidate IDs is then hashed using SHA-256 and added as a leaf node to a merkle tree. This tree is then dumped using pickle, in a file called Merkle.

## count_votes.py
This file reads data from the Merkle file and counts the total number of votes for each candidate by using a counter for each of them while reading it from the Merkle file. The file initially reads from the pickled 'merkle' file which consists of the MerkleTools object. This object has the whole merkle tree in an immutable, binary form to read and process the leaves. The leaves of the Merkle Tree consists of the individual vote received for the candidate. The merkle tree helps in protecting the vote data from any kind of tampering and preserves the state of the voting sequence.

## audit_trail.py
This file is used to verify the state of the merkle tree which is pickled from the 'Merkle' file. In this, a Voter Id is taken from the output of the audit form. It is then checked against the Merkle file to check if it is a valid leaf node or sister node. If not, it will have a different root than the actual root. This way we can verify if the votes have ever been tampered at any time. Validating the proof of the target node provided in the argument makes the audit a success. If the node exists as leaf, then the tree is valid. Whereas it gives a false response on reading the tampered tree thereby verifying the voting sequence.

## forms.py
This file is used to make the forms using Flask and wtForm libraries. In this file forms for registeration, Login and Vote Casting, Counting all votes and then Auditing them are made. 
### Main Screen
![1](https://user-images.githubusercontent.com/46850039/119775183-b4c7af00-bedc-11eb-8dfc-a404a3efa16a.jpg)

### Registration
![2](https://user-images.githubusercontent.com/46850039/119715906-f83f0080-be7d-11eb-9f59-830807e5aea6.jpg)

### Login Before Voting
![3](https://user-images.githubusercontent.com/46850039/119715915-f8d79700-be7d-11eb-9fbd-5944bfdab4a6.jpg)

### Cast your Vote!
![4](https://user-images.githubusercontent.com/46850039/119715923-f9702d80-be7d-11eb-9431-485855e4a6df.jpg)

### Audit a Candidate
![6](https://user-images.githubusercontent.com/46850039/119775260-cc9f3300-bedc-11eb-9eaf-f1c6479771ff.jpg)

### Display Voting Results
![5](https://user-images.githubusercontent.com/46850039/119775210-bee9ad80-bedc-11eb-912e-ab7392cdd1fb.JPG)

## Video Demonstration
https://youtu.be/iacn5mAhHhw
