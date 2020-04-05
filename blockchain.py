blockchain = []


def get_last_blockchain_value():
    """ Returns the last transaction in the blockchain """
    return blockchain[-1]


def add_value(transaction_amount, last_transation=[1.0]):
    blockchain.append([last_transation, transaction_amount])
    print(blockchain)


def get_user_input():
    return float(input("Your transcation amount please: "))


tx_amount = get_user_input()
add_value(tx_amount)


while True:
    tx_amount = get_user_input()
    add_value(tx_amount, get_last_blockchain_value())

    for block in blockchain:
        print("----------")
        print(block)
