import random

# Assuming the refactored module is named 'DiffieHellman' for clarity
import DH
import RS


class Participant:
    def __init__(self, name):
        """
        Initializes a participant with a name, private key, and placeholders for keys involved in the exchange.
        """
        self.p, self.q = RS.generate_keys()
        self.name = name
        self.private_key = DH.generate_random_private_key(DH.prime)
        self.firstShared_key = None  # To be shared with other participants
        self.intermediate_key = None  # Intermediate key used in the exchange process
        self.final_key = None  # The final mutual key computed

    def firstShared_key(self):
        """
        Computes and sets the public key to be shared with other participants.
        """
        self.firstShared_key = DH.compute_shared_key(self.private_key, DH.prime, DH.g)

    def receive_and_set_intermediate_key(self, firstShared_key):
        """
        Receives a public key from another participant and sets the intermediate key.
        """
        self.intermediate_key = DH.compute_shared_key(self.private_key, DH.prime, firstShared_key)

    def finalize_mutual_key(self):
        """
        Finalizes the mutual key computation using the intermediate key.
        """
        self.final_key = DH.compute_shared_key(self.private_key, DH.prime, self.intermediate_key)

    def __str__(self):
        """
        String representation of the participant's state for debugging purposes.
        """
        return f"Participant: {self.name}, Final Key: {self.final_key}"
