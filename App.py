import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import binascii

import Camellia_ECB as encryption  # Placeholder for Camellia_ECB or any encryption module
import DH as DH
import RS
from Participant import Participant
def sign_message(message, p, q):
    return ('signature_part_1', 'signature_part_2')

# Main application class
class MessagingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x150")
        self.title("Secure Emailing App")

        self.participants = [Participant(name) for name in ['Alice', 'Bob', 'Carol']]
        self.current_user = None  # To store the currently logged-in user
        self.create_widgets()

    def create_widgets(self):
        # Login area
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)  # Adjust padding for better visual separation

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")  # Mask password input
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Message area
        self.message_frame = tk.Frame(self)
        self.message_frame.pack(pady=10,padx=10, fill=tk.X, expand=True)

        self.message_entry = tk.Entry(self.message_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.send_button = tk.Button(self.message_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)


        # Log area
        self.log_text = tk.Text(self, state='disabled', height=10)
        self.log_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Placeholder login logic; validate username
        if username in [user.name for user in self.participants]:
            self.current_user = username
            messagebox.showinfo("Login", f"Logged in as {username}")
            self.geometry("600x400")  # Resize window after successful login
            self.resizable(True, True)  # Allow resizing after login
            self.login_frame.pack_forget()
            self.initialize_message_area()
        else:
            messagebox.showerror("Login failed", "Username not found.")
            
    def receiveMsg(self, user_instance, ciphertext, signature, key, n):
        plaintext = encryption.decrypt(ciphertext, key)
        message = plaintext.decode('utf-8')
        hexmessage = binascii.hexlify(message.encode())
        verify = RS.verify_rabin(n, hexmessage, signature[0], signature[1])
        if verify:
            self.log(f"{user_instance.name}: {message} (decrypted email)")
            self.log(f"{user_instance.name}: received an email and Rabin verified succeeded")

    def send_message(self):
        message = self.message_entry.get()
        ciphertext = encryption.encrypt(message, mutual_key)  # Key conversion if necessary     
        sender_index = sender_indices[self.current_user]
        sign = RS.sign_rabin(participants[sender_index].p,participants[sender_index].q,binascii.hexlify(message.encode()))
        self.log(f"{self.current_user}: {ciphertext} (encrypted email)")
        self.log(f"{self.current_user}: {sign} (signature)")
        self.log("mutual key is " + str(mutual_key))
        for participant in self.participants:
            if participant.name != self.current_user:
                self.receiveMsg(participant, ciphertext, sign, mutual_key,Rabin_key[sender_index])
        
        self.log("\n")

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')



if __name__ == "__main__":
    names = ['Alice', 'Bob', 'Carol']  # List to maintain order
    password = ['123456']
    sender_indices = {name: i for i, name in enumerate(names)}
    participants = [Participant(name) for name in names]
    DH.exchange_keys(participants)
    key = participants[0].final_key  # Assuming final_key is the mutual key
    mutual_key = key
    Rabin_key = []
    for user in participants:
        n = user.p * user.q
        Rabin_key.append(n)
    app = MessagingApp()
    app.mainloop()
