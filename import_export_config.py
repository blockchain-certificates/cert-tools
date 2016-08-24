import os

#########################
## IMPORT/EXPORT TOOLS ##
#########################
mongo_host_string = 'mongodb://localhost:27017'
signed_certificates_dir = 'signed_certificates'
transaction_ids_dir = 'transaction_ids'
receipts_dir = 'receipts'
signed_certificates_glob = os.path.join(signed_certificates_dir, '*.json')
transaction_ids_glob = os.path.join(transaction_ids_dir, '*.txt')
receipts_glob = os.path.join(receipts_dir, '*.json')