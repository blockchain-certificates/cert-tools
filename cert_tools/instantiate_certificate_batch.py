#!/usr/bin/env

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

from cert_schema.schema_tools import schema_validator

import helpers
import jsonpath_helpers

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


class Recipient:
    def __init__(self, fields):
        self.family_name = fields['familyName']
        self.given_name = fields['givenName']
        self.pubkey = fields['pubkey']
        self.identity = fields['identity']

        fields.pop('familyName', None)
        fields.pop('givenName', None)
        fields.pop('pubkey', None)
        fields.pop('identity', None)

        self.additional_fields = fields


def hash_and_salt_email_address(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest()


def instantiate_assertion(config, cert, uid, issued_on):
    cert['assertion']['issuedOn'] = issued_on
    cert['assertion']['uid'] = uid
    cert['assertion']['id'] = helpers.urljoin_wrapper(config.issuer_certs_url, uid)
    return cert


def instantiate_recipient(config, cert, recipient):
    cert['recipient']['givenName'] = recipient.given_name
    cert['recipient']['familyName'] = recipient.family_name
    cert['recipient']['publicKey'] = recipient.pubkey
    if config.hash_emails:
        salt = encode(os.urandom(16))
        cert['recipient']['salt'] = salt
        cert['recipient']['identity'] = hash_and_salt_email_address(recipient.identity, salt)
    else:
        cert['recipient']['identity'] = recipient.identity

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
    roster = helpers.normalize_data_path(config.data_dir, config.roster)
    template = helpers.normalize_data_path(config.data_dir, config.template_dir, config.template_file_name)
    issued_on = str(date.today())
    output_dir = helpers.normalize_data_path(config.data_dir, config.unsigned_certificates_dir)

    recipients = []
    with open(roster, "r") as theFile:
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
            schema_validator.validate_unsigned_v1_2(cert)

            with open(helpers.normalize_data_path(output_dir, uid + '.json'), 'w') as unsigned_cert:
                json.dump(cert, unsigned_cert)


def main():
    import config
    conf = config.get_config()
    create_unsigned_certificates_from_roster(conf)
    print('Instantiated batch!')


if __name__ == "__main__":
    main()
