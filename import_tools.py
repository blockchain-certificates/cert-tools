'''
Tools to facilitate importing certificate and recipient data into mongodb after certificates
have been issued.
'''
import glob
import json

import import_config
import gridfs
import os
from pymongo import MongoClient


def create_certificates_mongo_collection(certificates_file_name):
    json_files = glob.glob(import_config.signed_certificates_glob)
    certificates = []

    for file in json_files:
        with open(file) as infile:
            # read corresponding transaction file to find transaction id
            tx1 = file.replace('.json', '.txt')
            tx2 = tx1.replace(import_config.signed_certificates_dir, import_config.transaction_ids_dir)
            with open(tx2) as tx_file:
                content = infile.read()
                tx = tx_file.read()
                cert = json.loads(content)
                out_json = {
                    '_id': {'$oid': cert['assertion']['uid']},
                    'issued': True,
                    'pubkey': cert['recipient']['pubkey'],
                    'txid': tx
                }
                certificates.append(out_json)

    certs_string = json.dumps(certificates)
    with open(certificates_file_name, 'wb') as outfile:
        outfile.write(bytes(certs_string, 'utf-8'))


def create_certificates_mongo_collection_v2(certificates_file_name, txid):
    json_files = glob.glob(import_config.signed_certificates_glob)
    certificates = []

    for file in json_files:
        with open(file) as infile:
            proof = file.replace(import_config.signed_certificates_dir, import_config.receipts_dir)
            with open(proof) as proof_file:
                content = infile.read()
                proof_str = proof_file.read()
                cert = json.loads(content)
                proof_json = json.loads(proof_str)
                out_json = {
                    '_id': {'$oid': cert['assertion']['uid']},
                    'issued': True,
                    'pubkey': cert['recipient']['pubkey'],
                    'txid': txid,
                    'proof': proof_json
                }
                certificates.append(out_json)

    certs_string = json.dumps(certificates)
    with open(certificates_file_name, 'wb') as outfile:
        outfile.write(certs_string.decode('utf-8'))


def load_certificates_into_gridfs():
    json_files = glob.glob(import_config.signed_certificates_glob)

    client = MongoClient(host=import_config.mongo_host_string)
    fs = gridfs.GridFS(client.admin)

    for file in json_files:
        with open(file) as infile:
            content = infile.read()
            head, tail = os.path.split(file)
            fs.put(content, filename=tail, encoding='utf-8')


def create_links(link_file_name):
    json_files = glob.glob(import_config.signed_certificates_glob)

    links = []

    for file in json_files:
        with open(file) as infile:
            content = infile.read()
            cert = json.loads(content)
            links.append(str(cert['recipient']['givenName']) + ': ' + str(cert['assertion']['id']))

    output = '\n'.join(links)
    with open(link_file_name, 'w') as outfile:
        outfile.write(output)


def main(arg):
    if arg == 'create_certificates_collection':
        create_certificates_mongo_collection('certificates.json')
    elif arg == 'create_v2_certificates_collection':
        create_certificates_mongo_collection_v2('certificates.json', 'TXID TODO')
    elif arg == 'load_gridfs':
        load_certificates_into_gridfs()
    elif arg == 'create_links':
        create_links('list.txt')
    else:
        print('specify an action')


if __name__ == "__main__":
    main('load_gridfs')
