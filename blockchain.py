MINING_REWARD = 10

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = [genesis_block]
open_transactions = []
owner = "Sahil"
participants = {"Sahil"}


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def get_balance(participant):
    amount_sent = 0
    amount_recivied = 0
    tx_sender = [[tx["amount"] for tx in block["transactions"]
                  if tx["sender"] == participant] for block in blockchain]
    open_tx_sender = [
        tx["amount"] for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)
    tx_recipient = [[tx["amount"] for tx in block["transactions"]
                     if tx["recipient"] == participant] for block in blockchain]
    for tx in tx_sender:
        if(len(tx) > 0):
            amount_sent += tx[0]
    for tx in tx_recipient:
        if(len(tx) > 0):
            amount_recivied += tx[0]
    return amount_recivied - amount_sent


def get_last_blockchain_value():
    """ Returns the last transaction in the blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions
    }
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
        if block["previous_hash"] != hash_block(blockchain[index - 1]):
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
    print("h: Manipulate the chain")
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
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{"sender": "Max", "recipient": "Sahil", "amount": 100000}]
            }
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input was invalid, please pick a value from the list!")
    if not verify_chain():
        print_blockchain_elements()
        print("invalid blockchain")
        break
    print(get_balance("Sahil"))
else:
    print("User left")

print("Done")
