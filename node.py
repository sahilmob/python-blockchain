
from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Sahil"
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        tx_recipient = input("Enter the recipient of the transaction:")
        tx_amount = float(input("Your transcation amount please: "))
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        user_input = input("Your choice: ")
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print(block)
        else:
            print("-" * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose: ")
            print("1: Add a new transaction value")
            print("2: Mine a new block")
            print("3: Output the blockchain blocks")
            print("4: Check transactions validity")
            print("q: Quit")
            user_choice = self.get_user_choice()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(recipient=recipient, sender=self.id, amount=amount):
                    print("Added transaction")
                else:
                    print("Transaction failed")
            elif user_choice == "2":
                self.blockchain.mine_block(self.id)
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                verifier = Verification()
                if verifier.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("Input was invalid, please pick a value from the list!")
            verifier = Verification()
            if not verifier.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("invalid blockchain")
                break
            print(
                f"Balance of {self.id}: {self.blockchain.get_balance():6.2f}")
        else:
            print("User left")

        print("Done")


node = Node()

node.listen_for_input()
