import binascii

import Camellia_ECB as encryption  # Placeholder for Camellia_ECB or any encryption module
import DH as DH
import RS
from Participant import Participant  # Assuming User has been refactored to Participant
def receiveMsg(user_instance, ciphertext, signature, key, n):
    plaintext = encryption.decrypt(ciphertext, key)
    message = plaintext.decode('utf-8')
    hexmessage = binascii.hexlify(message.encode())
    verify = RS.verify_rabin(n, hexmessage, signature[0], signature[1])
    if verify == True:
        print(user_instance.name, "received a message and Rabin verified succeeded")

names = ['Alice', 'Bob', 'Carol']  # List to maintain order
password = ['123456']
sender_indices = {name: i for i, name in enumerate(names)}
participants = [Participant(name) for name in names]

# Assuming generate_3_keys is appropriately refactored in DH module
DH.exchange_keys(participants)
mutual_key = participants[0].final_key  # Assuming final_key is the mutual key
Rabin_key = []
for user in participants:
    n = user.p * user.q
    Rabin_key.append(n)
while True:
    valid_sender = False
    while not valid_sender:
        sender_name = input("To login please insert username and password ")
        if sender_name not in sender_indices:
            print("Wrong username or password")
        else:
            valid_sender = True

    sender_index = sender_indices[sender_name]
    message_to_encrypt = input("Enter your message to deliver: ")
    
    # Assuming Encrypt and Decrypt functions are available and accept keys correctly
    ciphertext = encryption.encrypt(message_to_encrypt, mutual_key)  # Key conversion if necessary
    print(f"Ciphertext: {ciphertext}")
    sign = RS.sign_rabin(participants[sender_index].p,participants[sender_index].q,binascii.hexlify(message_to_encrypt.encode()))
    print("Sign: ",sign)
    for participant in participants:
        if participant.name != sender_name:
            receiveMsg(participant, ciphertext,sign, mutual_key, Rabin_key[sender_index])
            print("Original message was:",encryption.decrypt(ciphertext, mutual_key))

    answer = input("Do you wish to stop? write Yes to stop conversation,No to continue: ")
    if (answer == 'Yes' or answer == 'yes'):
        break

