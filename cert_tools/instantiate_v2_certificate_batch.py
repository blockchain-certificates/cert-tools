#!/usr/bin/env python

'''
Merges a certificate template with recipients defined in a roster file. The result is
unsigned certificates that can be given to cert-issuer.
'''
import copy
import csv
import hashlib
import json
import os
import uuid
from datetime import date

import configargparse

from cert_core.model import scope_name
from cert_schema.schema_tools import schema_validator

import helpers
import jsonpath_helpers


class Recipient:
    def __init__(self, fields):
        self.name = fields['name']
        self.pubkey = fields['pubkey']
        self.identity = fields['identity']

        fields.pop('name', None)
        fields.pop('pubkey', None)
        fields.pop('identity', None)

        self.additional_fields = fields


def hash_and_salt_email_address(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest()


def instantiate_assertion(config, cert, uid, issued_on):
    cert['issuedOn'] = issued_on
    cert['id'] = helpers.URN_UUID_PREFIX + uid
    return cert


def instantiate_recipient(config, cert, recipient):

    if config.hash_emails:
        salt = helpers.encode(os.urandom(16))
        cert['recipient']['hashed'] = True
        cert['recipient']['salt'] = salt
        cert['recipient']['identity'] = hash_and_salt_email_address(recipient.identity, salt)
    else:
        cert['recipient']['identity'] = recipient.identity
        cert['recipient']['hashed'] = False

    profile_field = scope_name('recipientProfile')

    cert['recipient'][profile_field] = {}
    cert['recipient'][profile_field]['type'] = ['RecipientProfile', 'Extension']
    cert['recipient'][profile_field]['name'] = recipient.name
    cert['recipient'][profile_field]['publicKey'] = 'ecdsa-koblitz-pubkey:' + recipient.pubkey

    if config.additional_per_recipient_fields:
        if not recipient.additional_fields:
            raise Exception('expected additional recipient fields in the csv file but none found')
        for field in config.additional_per_recipient_fields:
            cert = jsonpath_helpers.set_field(cert, field['path'], recipient.additional_fields[field['csv_column']])
    else:
        if recipient.additional_fields:
            # throw an exception on this in case it's a user error. We may decide to remove this if it's a nuisance
            raise Exception(
                'there are fields in the csv file that are not expected by the additional_per_recipient_fields configuration')


def create_unsigned_certificates_from_roster(config):
    roster = os.path.join(config.abs_data_dir, config.roster)
    template = os.path.join(config.abs_data_dir, config.template_dir, config.template_file_name)
    issued_on = str(date.today())
    output_dir = os.path.join(config.abs_data_dir, config.unsigned_certificates_dir)

    recipients = []
    with open(roster, 'r') as theFile:
        reader = csv.DictReader(theFile)
        for line in reader:
            r = Recipient(line)
            recipients.append(r)

    with open(template) as template:
        cert_str = template.read()
        template = json.loads(cert_str)

        for recipient in recipients:
            uid = str(uuid.uuid4())

            cert = copy.deepcopy(template)

            instantiate_assertion(config, cert, uid, issued_on)
            instantiate_recipient(config, cert, recipient)

            # validate certificate before writing
            schema_validator.validate_v2(cert)

            with open(os.path.join(output_dir, uid + '.json'), 'w') as unsigned_cert:
                json.dump(cert, unsigned_cert)


def get_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(base_dir, 'conf.ini')])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--issuer_certs_url', type=str, help='issuer certificates URL')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--hash_emails', action='store_true',
                   help='whether to hash emails in the certificate')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'), help='additional per-recipient fields')
    p.add_argument('--unsigned_certificates_dir', type=str, help='output directory for unsigned certificates')
    p.add_argument('--roster', type=str, help='roster file name')
    p.add_argument('--blockcerts_v2_alias', type=str, help='blockcerts v2 alias')
    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(base_dir, args.data_dir))

    return args


def main():
    conf = get_config()
    create_unsigned_certificates_from_roster(conf)
    print('Instantiated batch!')


if __name__ == "__main__":
    main()

