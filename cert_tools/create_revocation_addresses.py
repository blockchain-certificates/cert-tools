#!/usr/bin/env
'''
Generates Bitcoin addresses using an HD extended public key to be used as the issuer's revocation addresses for the certificates. 

It creates a list of addresses that could then be easily merged with the roster file, e.g. using unix's paste command.
'''
import os
import sys

import configargparse
from pycoin.key.BIP32Node import BIP32Node


def generate_revocation_addresses(config):
    key_path = config.key_path if config.key_path else ''
    output_handle = open(config.output_file, 'w') if config.output_file else sys.stdout

    try:
        key = BIP32Node.from_text(config.extended_public_key)
    except:
        print('The extended public (or private) key seems invalid.')
        sys.exit()
    key_path_batch = key.subkey_for_path(key_path)
    for i in range(config.number_of_addresses):
        subkey = key_path_batch.subkey(i)
        output_handle.write("{0}\n".format(subkey.address(config.use_uncompressed)))

    if output_handle is not sys.stdout:
        output_handle.close()


def get_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(base_dir, 'conf.ini')])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('-k', '--extended_public_key', type=str, required=True,
                   help='the HD extended public key used to generate the revocation addresses')
    p.add_argument('-p', '--key_path', type=str,
                   help='the key path used to derive the child key under which the addresses will be generated')
    p.add_argument('-n', '--number_of_addresses', type=int, default=10,
                   help='the number of revocation addresses to generate')
    p.add_argument('-o', '--output_file', type=str, help='the output file to save the revocation addresses')
    p.add_argument('-u', '--use_uncompressed', action='store_true', default=False,
                   help='whether to use uncompressed bitcoin addresses')
    args, _ = p.parse_known_args()

    return args


def main():
    conf = get_config()
    generate_revocation_addresses(conf)


if __name__ == "__main__":
    main()
