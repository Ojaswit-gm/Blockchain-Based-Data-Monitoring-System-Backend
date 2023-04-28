# nodes = get_nodes()
#     my_transactions = list()
#     utxo_list = list()


#     def _update_utxo(self):
#         for block in self.chain:
#             for transaction in block["transactions"]:
#                 try:
#                     if transaction["receiver"] == self.wallet_id:
#                         self.utxo += float(transaction["amount"])
#                     elif transaction["sender"] == self.wallet_id:
#                         self.utxo -= float(transaction["amount"])
#                         self.utxo -= float(transaction["fee"])
#                     self.wallet.utxo = self.utxo
#                     self.wallet.save()
#                 except:
#                     pass


    # def _validate_transaction(self, amount):
    #     self._update_utxo()
    #     return self.utxo >= amount


        # def replace_chain(self):
        # network = self.nodes
        # longest_chain = None
        # max_length = len(self.chain)
        # for node in network:
        #     response = requests.get(f'http://{node}/get_chain')
        #     if response.status_code == 200:
        #         length = response.json()['length']
        #         chain = response.json()['chain']
        #         if length > max_length:
        #             max_length = length
        #             longest_chain = chain
        # if longest_chain:
        #     self.chain = longest_chain
        #     return True
        # return False



    #         def _update_mempool(self):
    #     network = self.nodes
    #     longest_mempool = None
    #     max_length = len(self.mempool)
    #     for node in network:
    #         response = requests.get(f'http://{node}/get_mempool')
    #         if response.status_code == 200:
    #             length = response.json()['length']
    #             mempool = response.json()['mempool']
    #             if length > max_length:
    #                 max_length = length
    #                 longest_mempool = mempool
    #     if longest_mempool:
    #         self.mempool = longest_mempool
    #         return True
    #     return False

    # def _get_my_transactions(self) -> list():
    #     my_transactions = list()
    #     # Initially empty the UTXO's list, so that we can fill them with latest transactions of that particular.
    #     self.utxo_list = []
    #     for block in self.chain:
    #         for transaction in block["transactions"]:
    #             try:
    #                 string = ""
    #                 # decrypted_transaction = json.loads(rsa.decrypt(transaction, self.__private_key).decode())
    #                 if(str(transaction["sender"]) == str(self.wallet_id)):
    #                     string = f"Me -> {transaction['receiver']} : {transaction['amount']}BTC : Transaction Fee: {transaction['fee']}"
    #                 elif(str(transaction["receiver"]) == str(self.wallet_id)):
    #                     string = f"{transaction['sender']} -> Me : {transaction['amount']}BTC"
    #                     self.utxo_list.append(string)
    #                 my_transactions.append(string)
    #             except:
    #                 pass
    #     return my_transactions