from functools import reduce
from json import dumps, loads

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, "", [], 100, 0)

        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node_id = hosting_node_id

        self.load_data()

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                file_content = f.readlines()
                blockchain = loads(file_content[0][:-1])
                self.__chain = [Block(
                    block["index"],
                    block["previous_hash"],
                    [
                        Transaction(
                            tx["sender"], tx["recipient"], tx["amount"])
                        for tx in block["transactions"]],
                    block["proof"],
                    block["timestamp"]
                ) for block in blockchain]
                self.__open_transactions = loads(file_content[1])
                self.__open_transactions = [Transaction(
                    tx["sender"], tx["recipient"], tx["amount"]) for tx in self.__open_transactions]
        except (IOError, IndexError):
            pass

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                f.write(dumps([block.__dict__ for block in
                               [Block(block_el.index, block_el.previous_hash, [
                                tx.__dict__ for tx in block_el.transactions
                                ], block_el.proof, block_el.timestamp) for block_el in self.__chain]
                               ]))
                f.write("\n")
                f.write(
                    dumps([tx.__dict__ for tx in self.__open_transactions]))
        except IOError:
            print("Saving failed")

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block((last_block))
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == self.hosting_node_id] for block in self.__chain]
        open_tx_sender = [
            tx.amount for tx in self.__open_transactions if tx.sender == self.hosting_node_id]
        tx_sender.append(open_tx_sender)
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == self.hosting_node_id] for block in self.__chain]
        amount_sent = reduce(
            lambda tx_sum, tx_current: tx_sum + sum(tx_current) if len(tx_current) > 0 else tx_sum + 0, tx_sender, 0)
        amount_recivied = reduce(
            lambda tx_sum, tx_current: tx_sum + sum(tx_current) if len(tx_current) > 0 else tx_sum + 0, tx_recipient, 0)
        return amount_recivied - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last transaction in the blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self, node):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            "MINING", self.hosting_node_id, MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True
