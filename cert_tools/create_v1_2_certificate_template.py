#!/usr/bin/env python

'''
Creates a certificate template with merge tags for recipient/assertion-specific data.
'''
import json
import os

import configargparse

from cert_tools import helpers
from cert_tools import jsonpath_helpers


def create_certificate_section(config):
    cert_image_path = os.path.join(config.abs_data_dir, config.cert_image_file)
    issuer_image_path = os.path.join(config.abs_data_dir, config.issuer_logo_file)
    certificate = {
        'type': 'Certificate',
        'name': config.certificate_title,
        'image': helpers.encode_image(cert_image_path),
        'description': config.certificate_description,
        'language': config.certificate_language,
        'issuer': {
            'type': 'Issuer',
            'url': config.issuer_url,
            'image': helpers.encode_image(issuer_image_path),
            'email': config.issuer_email,
            'name': config.issuer_name,
            'id': config.issuer_id
        }
    }

    return certificate


def create_verification_section(config):
    verify = {
        'attribute-signed': 'uid',
        'type': 'ECDSA(secp256k1)'
    }
    return verify


def create_recipient_section(config):
    recipient = {
        'type': 'email',
        'familyName': '*|LNAME|*',
        'givenName': '*|FNAME|*',
        'publicKey': '*|PUBKEY|*',
        'identity': '*|EMAIL|*',
        'hashed': config.hash_emails
    }
    return recipient


def create_assertion_section(config):
    assertion = {
        'type': 'Assertion',
        'issuedOn': '*|DATE|*',
        'uid': '*|CERTUID|*',
        'id': helpers.urljoin_wrapper(config.issuer_certs_url, '*|CERTUID|*')
    }
    if config.issuer_signature_file:
        issuer_image_path = os.path.join(config.abs_data_dir, config.issuer_signature_file)
        assertion['image:signature'] = helpers.encode_image(issuer_image_path)
    return assertion


def create_certificate_template(config):
    certificate = create_certificate_section(config)
    verify = create_verification_section(config)
    assertion = create_assertion_section(config)
    recipient = create_recipient_section(config)

    template_dir = config.template_dir
    if not os.path.isabs(template_dir):
        template_dir = os.path.join(config.abs_data_dir, template_dir)
    template_file_name = config.template_file_name

    raw_json = {
        '@context': 'https://w3id.org/blockcerts/v1',
        'type': 'CertificateDocument',
        'recipient': recipient,
        'assertion': assertion,
        'certificate': certificate,
        'verify': verify
    }

    if config.additional_global_fields:
        for field in config.additional_global_fields:
            raw_json = jsonpath_helpers.set_field(raw_json, field['path'], field['value'])

    if config.additional_per_recipient_fields:
        for field in config.additional_per_recipient_fields:
            raw_json = jsonpath_helpers.set_field(raw_json, field['path'], field['value'])

    template_path = os.path.join(config.abs_data_dir, template_dir, template_file_name)

    with open(template_path, 'w') as cert_template:
        json.dump(raw_json, cert_template)

    return raw_json


def get_config():
    cwd = os.getcwd()
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(cwd, 'conf.ini')])

    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')

    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--issuer_logo_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--issuer_signature_file', type=str, help='issuer signature image file, png format')
    p.add_argument('--cert_image_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--issuer_url', type=str, help='issuer URL')
    p.add_argument('--issuer_certs_url', type=str, help='issuer certificates URL')
    p.add_argument('--issuer_email', type=str, help='issuer email')
    p.add_argument('--issuer_name', type=str, help='issuer name')
    p.add_argument('--issuer_id', type=str, help='path to issuer public keys')
    p.add_argument('--certificate_language', type=str, required=False, help='certificate language')
    p.add_argument('--certificate_description', type=str, help='the display description of the certificate')
    p.add_argument('--certificate_title', type=str, help='the title of the certificate')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--hash_emails', action='store_true',
                   help='whether to hash emails in the certificate')
    p.add_argument('--additional_global_fields', action=helpers.make_action('global_fields'),
                   help='additional global fields')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'),
                   help='additional per-recipient fields')

    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))
    return args


def main():
    conf = get_config()
    template = create_certificate_template(conf)
    print('Created template!')


if __name__ == "__main__":
    main()
