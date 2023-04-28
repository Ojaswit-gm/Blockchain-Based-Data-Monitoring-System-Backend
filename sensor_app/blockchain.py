from .models import Block, Transaction, Mempool, TxnDB1, TxnDB2
from .serializers import BlockSerializer, MempoolSerializer
import datetime as _dt
import hashlib as _hashlib
import json
from decouple import config

def addBlockInDBWithTransactions(block):
    index = block["index"]
    nonce = block["nonce"]
    merkle_root_hash = block["merkle_root"]
    prev_hash = block["prevHash"]
    timestamp = block["timestamp"]

    newBlock = Block(index=index, nonce=nonce, merkle_root_hash=merkle_root_hash, prev_hash=prev_hash, timestamp=timestamp)
    newBlock.save()

    # Adding all the transactions of a block in blockchain
    for transaction in block["transactions"]:
        if(int(transaction['sensor_id']) <= config('TXN_1_DB_LIMIT', cast=int)):
            # TXN_1_DB is used
            newTransaction = TxnDB1(block=newBlock, sensor_id=transaction['sensor_id'], data=transaction['data'], timestamp=transaction['timestamp'])
            newTransaction.save()
        else:
            # TXN_2_DB is used
            newTransaction = TxnDB2(block=newBlock, sensor_id=transaction['sensor_id'], data=transaction['data'], timestamp=transaction['timestamp'])
            newTransaction.save()
    
    return True

class Wallet:
    # prk, puk = rsa.newkeys(512)
    mempool = list()
    chain = list()
    
    # Minor Specific Functions
    def __init__(self):
        genesis_block = self._create_block(
            transactions=[], index=1, nonce=1, prevHash="0", merkle_root_hash="0")
        self.chain.append(genesis_block)

    def _create_block(self, index: int, transactions: list, prevHash: str, nonce: int, merkle_root_hash: str) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "transactions": transactions,
            "merkle_root": merkle_root_hash,
            "nonce": nonce,
            "prevHash": prevHash,
        }
        return block

    def _to_digest(self, index: int, nonce: int, prevHash: str) -> str:
        to_digest = str(nonce ** 2 + index)
        return _hashlib.sha256(to_digest.encode()).hexdigest()

    def getHashBlocks(self, block : dict) -> str:
        newblock = {
            "index" : block['index'],
            "nonce" : block['nonce'],
            "merkle_root_hash" : block['merkle_root_hash'],
            "timestamp" : block['timestamp'],
            "prevHash" : block['prev_hash'],
        }
            
        encoded_block = json.dumps(newblock, sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()

    def getHash(self, block : dict) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, data: list, index: int, prevHash: str) -> int:
        nonce = 1
        isValid = False
        while isValid is False:
            # print(nonce)
            newHash = self._to_digest(index=index, nonce=nonce, prevHash=prevHash)

            if(newHash[:4] == "0000"):
                return nonce
            else:
                nonce+=1

    def _create_merkle_root(self, transactions: list) -> str:
        hash_values = []
        for ele in transactions:
            hash_values.append(self.getHash(ele))
        while len(hash_values)>1:
            curr_values = []
            second_taken = False
            currHash = ""
            for ele in hash_values:
                if second_taken is False:
                    currHash = self.getHash(ele)
                    second_taken = True
                else:
                    currHash = currHash + self.getHash(ele)
                    curr_values.append(currHash)
                    currHash = ""
                    second_taken = False
            hash_values = curr_values
        return hash_values[0]

    def get_prev_block(self):
        return self.chain[-1]

    def mine_block(self) -> dict:
        self.update_mempool_with_db()
        self.update_chain_with_db()
        prev_block = self.get_prev_block()
        transactions = []
        for ele in self.mempool:
            obj = {
                'sensor_id' : ele['sensor_id'],
                'data' : ele['data'],
                'timestamp': ele['timestamp']
            }
            transactions.append(obj)
        index = prev_block["index"] + 1
        prevHash = self.getHashBlocks(prev_block)
        nonce = self.proof_of_work(data=transactions, index=index, prevHash=prevHash)
        merkle_root = self._create_merkle_root(transactions)
        newBlock = self._create_block(transactions=transactions, index=index, nonce=nonce, prevHash=prevHash, merkle_root_hash=merkle_root)
        self.chain.append(newBlock)
        self.mempool = []
        Mempool.objects.all().delete()
        addBlockInDBWithTransactions(newBlock)
        return newBlock

    # General Functions
    def get_all_blocks(self) -> list():
        return self.chain

    def is_chain_valid(self, chain: list) -> bool:
        if(len(chain) == 1):
            return True
        current_block = chain[1]
        index = current_block["index"]
        while index < len(chain):
            new_block = chain[index]
            if(self.getHashBlocks(current_block) != new_block["prev_hash"]):
                return False
            
            hash = self._to_digest(index=new_block["index"], nonce=new_block["nonce"], prevHash=new_block["prev_hash"])
            if(hash[:4]!="0000"):
                return False
            
            current_block = new_block
            index += 1
        
        return True

    def update_mempool_with_db(self):
        self.mempool = MempoolSerializer(Mempool.objects.all(), many=True).data

    def update_chain_with_db(self):
        self.chain = BlockSerializer(Block.objects.all().order_by('index'), many=True).data

node = Wallet()
