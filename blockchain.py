from functools import reduce
from json import dumps, loads

from hash_util import hash_block, has_string_265
from block import Block
from transaction import Transaction

MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = "Sahil"
participants = {"Sahil"}


def load_data():
    global blockchain
    global open_transactions
    try:
        with open("blockchain.txt", mode="r") as f:
            file_content = f.readlines()
            blockchain = loads(file_content[0][:-1])
            blockchain = [Block(
                block["index"],
                block["previous_hash"],
                [
                    Transaction(tx["sender"], tx["recipient"], tx["amount"])
                    for tx in block["transactions"]],
                block["proof"],
                block["timestamp"]
            ) for block in blockchain]
            open_transactions = loads(file_content[1])
            open_transactions = [Transaction(
                tx["sender"], tx["recipient"], tx["amount"]) for tx in open_transactions]
    except (IOError, IndexError):
        genesis_block = Block(0, "", [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []


load_data()


def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            f.write(dumps([block.__dict__ for block in
                           [Block(block_el.index, block_el.previous_hash, [
                               tx.__dict__ for tx in block_el.transactions
                           ], block_el.proof, block_el.timestamp) for block_el in blockchain]
                           ]))
            f.write("\n")
            f.write(dumps([tx.__dict__ for tx in open_transactions]))
    except IOError:
        print("Saving failed")


def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) +
             str(last_hash) + str(proof)).encode()
    guess_hash = has_string_265(guess)
    print(guess_hash)
    return guess_hash[0: 2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block((last_block))
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions
                  if tx.sender == participant] for block in blockchain]
    open_tx_sender = [
        tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participant] for block in blockchain]
    amount_sent = reduce(
        lambda tx_sum, tx_current: tx_sum + sum(tx_current) if len(tx_current) > 0 else tx_sum + 0, tx_sender, 0)
    amount_recivied = reduce(
        lambda tx_sum, tx_current: tx_sum + sum(tx_current) if len(tx_current) > 0 else tx_sum + 0, tx_recipient, 0)
    return amount_recivied - amount_sent


def get_last_blockchain_value():
    """ Returns the last transaction in the blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction("MINING", owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input("Enter the recipient of the transaction:")
    tx_amount = float(input("Your transcation amount please: "))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of work is invalid")
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print("Please choose: ")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output the blockchain participants")
    print("5: Check transactions validity")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == "1":
        recipient, amount = get_transaction_value()
        if add_transaction(recipient=recipient, amount=amount):
            print("Added transaction")
        else:
            print("Transaction failed")
        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input was invalid, please pick a value from the list!")
    if not verify_chain():
        print_blockchain_elements()
        print("invalid blockchain")
        break
    print(f"Balance of {owner}: {get_balance('Sahil'):6.2f}")
else:
    print("User left")

print("Done")
