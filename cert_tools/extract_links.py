#!/usr/bin/env python

import os
import json

import configargparse


def extract_links(cert_path, url_prefix, output_file):
    certs = [os.path.join(cert_path, f) for f in os.path.listdir(cert_path) if f.endswith('json')]

    certs_dict = dict()

    for cert in certs:
        with open(cert) as the_cert:
            cert_str = the_cert.read()
            a_cert = json.loads(cert_str)
            print(a_cert)
            certificate_uid = a_cert['assertion']['uid']
            name = a_cert['recipient']['givenName'] + ' ' + a_cert['recipient']['familyName']
            certs_dict[name] = certificate_uid

    with open(output_file, 'w') as links:
        for key in sorted(certs_dict.iterkeys()):
            the_url = '{}/{}'.format(url_prefix, certs_dict[key])
            links.write(key + ' : ' + the_url + '\n')


def get_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(base_dir, 'conf.ini')])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('-p', '--cert_path', type=str, required=True,
                   help='Path to certificates')
    p.add_argument('-u', '--url_prefix', type=str,
                   help='URL prefix')
    p.add_argument('-o', '--output_path', type=str,
                   help='Path to output file')
    args, _ = p.parse_known_args()

    return args


def main():
    conf = get_config()

    extract_links(conf.cert_path, conf.url_prefix, conf.output_path)


if __name__ == "__main__":
    main()
