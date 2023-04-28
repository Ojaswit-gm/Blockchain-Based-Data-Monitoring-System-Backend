import ast
from decouple import config

key = config('SERVER_KEY', cast=str)
hash_key = config('HASH_KEY', cast=str)

def hashVerified(hash):
    return hash == hash_key

def DOSVerified(sensor_id):
    pass

def decrypt(ciphertext):
  plaintext = ''
  for i, c in enumerate(ciphertext):
    key_c = ord(key[i % len(key)])
    ciphertext_c = ord(c)
    plaintext += chr((ciphertext_c - key_c) % 256)
  return plaintext

def encrypt(plaintext):
  ciphertext = ''
  for i, c in enumerate(plaintext):
    key_c = ord(key[i % len(key)])
    plaintext_c = ord(c)
    ciphertext += chr((plaintext_c + key_c) % 256)
  return ciphertext

# {
#   "sensor_id": "4567",
#   "data": "56",
#   "timestamp": "2023-01-05T07:55:59.575834Z",
#   "hashKey" : "e627b52aeb2e360a2cce525131b8f6de"
# }

def encrypt(key, plaintext):
  ciphertext = ''
  for i, c in enumerate(plaintext):
    key_c = ord(key[i % len(key)])
    plaintext_c = ord(c)
    ciphertext += chr((plaintext_c + key_c) % 256)
  return ciphertext

def decryptTransactions(all_transactions):
    decrypted_transactions = []
    for transaction in all_transactions:
        decrypt_txn = decrypt(transaction.txn)
        transaction = ast.literal_eval(str(decrypt_txn))
        decrypted_transactions.append(transaction)
    return decrypted_transactions

