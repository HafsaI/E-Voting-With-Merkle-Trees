import hashlib
import binascii


class MerkleTree(object):
    def __init__(self, hash_type="sha256"):
        self.hash_function = getattr(hashlib, hash_type)
        self.reset_tree()

    def reset_tree(self):
        """ initializes an empty tree """
        self.leaves = list()
        self.levels = None
        self.complete = False

    def convert_to_hex(self, x):
        return x.hex()

    def get_leaf(self, index):
        """
        returns hex of leaf
        """
        return self.convert_to_hex(self.leaves[index])

    def add_leaves(self, datachunks, hash_required=False):
        """
        values = candidate IDs:  hashed using SHA-256 hash algorithm and the binary hashes are stored in merkle tree 
        """
        self.complete = False
        for chunk in datachunks:
            if hash_required:
                # converts string into byte to be acceptable by hash function
                chunk = chunk.encode('utf-8')
                # returns hashed encoded data in hexa decimal format
                chunk = self.hash_function(chunk).hexdigest()
                # a new bytearray object initialized from a string of hex numbers, 2 hexa-decimal digits per byte
            chunk = bytearray.fromhex(chunk)

            self.leaves.append(chunk)
        for m in range(0, len(self.leaves)):
            self.get_leaf(m)
        return self.leaves

    def leaves_count(self):
        """ 
        gives length of leaves
        """
        return len(self.leaves)

    def next_level_nodes(self):
        """ 
        Going up the merkle tree, a new level is generated with nodes of previous level
        """
        odd_leaf = None  # extra leaf from Right most that will be duplicated up the merkle tree
        N = len(self.levels[0])  # number of leaves on the current level
        if N % 2 == 1:  # if odd number of leaves on the current level
            odd_leaf = self.levels[0][-1]
            N -= 1

        level_up = []
        for left, right in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):
            level_up.append(self.hash_function(left+right).digest())
        if odd_leaf is not None:  # if odd number of leaves on the current level
            level_up.append(odd_leaf)
        # prepend new level
        self.levels.insert(0, level_up)
        # print(self.levels)

    def build_merkle_tree(self):
        """ 
        creates bottom leaves level + calls _calculate_next_level() to create levels for merkle tree
        """
        self.complete = False
        self.levels = []
        if self.leaves_count() > 0:  # if there are leaves
            self.levels.insert(0, self.leaves)
            while len(self.levels[0]) > 1:  # until root node reached
                self.next_level_nodes()
        self.complete = True

    def get_merkle_root(self):
        """ 
        gets hashed root
        """
        if self.complete:
            if self.levels is not None:
                return self.convert_to_hex(self.levels[0][0])
            else:
                return None
        else:
            return None

    def get_proof(self, index):
        """
        Generates the proof trail in a bottom-up fashion
        """
        if self.levels is None:
            return None

        # if merkle tree not complete or incorrect index
        elif not self.complete or index > len(self.leaves)-1 or index < 0:
            return None
        else:
            proof_result = []
            no_of_levels = len(self.levels)
            for x in range(no_of_levels - 1, 0, -1):
                level_nodes = len(self.levels[x])

                # skip if this is an odd end node
                if (index == level_nodes - 1) and (level_nodes % 2 == 1):
                    index = int(index / 2.)

                # if mod 2 = 0 , an even index , hashed with right sibling else with left
                # checks if the merkle_node is the left sibling or the right sibling
                Right_node = index % 2
                if Right_node:
                    sibIndex = index - 1
                    sibPos = "left"
                else:
                    sibIndex = index + 1
                    sibPos = "right"

                sibVal = self.convert_to_hex(
                    self.levels[x][sibIndex])
                proof_result.append({sibPos: sibVal})
                # current node gets adjusted as we go up the merkle tree
                index = int(index / 2.)
            return proof_result

    def verify_proof(self, proof_trail, given_leaf, merkle_root):
        """
        Performs the audit-proof from the audit_trail received from the trusted server.
        """
        merkle_root = bytearray.fromhex(merkle_root)
        given_leaf = bytearray.fromhex(given_leaf)  # index leaf given
        if len(proof_trail) == 0:
            return given_leaf == merkle_root
        else:
            proof_hash = given_leaf

            for p in proof_trail:
                # the order of hash concatenation depends on whether the node is a left child or right child of its parent
                try:
                    # the child is a left node
                    proof_till_now = bytearray.fromhex(p['left'])
                    proof_hash = self.hash_function(
                        proof_till_now + proof_hash).digest()
                except:
                    # the child is a right node
                    proof_till_now = bytearray.fromhex(p['right'])
                    proof_hash = self.hash_function(
                        proof_hash + proof_till_now).digest()
             # verifying the computed root hash against the actual root hash
            return proof_hash == merkle_root
