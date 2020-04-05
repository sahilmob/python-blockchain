blockchain = []


def get_last_blockchain_value():
    """ Returns the last transaction in the blockchain """
    return blockchain[-1]


def add_value(transaction_amount, last_transation=[1.0]):
    blockchain.append([last_transation, transaction_amount])
    print(blockchain)


def get_transaction_value():
    user_input = float(input("Your transcation amount please: "))
    return user_input


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print("----------")
        print(block)


tx_amount = get_transaction_value()
add_value(tx_amount)


while True:
    print("Please choose: ")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
    print("q: quit")
    user_choice = get_user_choice()

    if user_choice == "1":
        tx_amount = get_transaction_value()
        add_value(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "q":
        break
    else:
        print("Input was invalid, please pick a value from the list!")

print("Done")
