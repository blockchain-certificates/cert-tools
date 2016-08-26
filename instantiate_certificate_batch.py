'''
Merges a certificate template with recipients defined in a roster file. The result is
unsigned certificates that can be given to cert-issuer.
'''
import json
import uuid
from datetime import date
import copy

from sample_data import config
import helpers
import os
import hashlib
from cert_schema.schema_tools import schema_validator
import bcrypt
import csv
import jsonpath_helpers

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

def instantiate_assertion(cert, uid, issued_on):
    cert['assertion']['issuedOn'] = issued_on
    cert['assertion']['uid'] = uid
    cert['assertion']['id'] = helpers.urljoin_wrapper(config.issuer_certs_url, uid)
    return cert


def instantiate_recipient(cert, recipient):
    cert['recipient']['givenName'] = recipient.given_name
    cert['recipient']['familyName'] = recipient.family_name
    cert['recipient']['pubkey'] = recipient.pubkey
    if config.hash_emails:
        # this is probably overkill, but if I'm generating a salt...
        salt = bcrypt.gensalt()
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
            raise Exception('there are fields in the csv file that are not expected by the additional_per_recipient_fields configuration')


def create_unsigned_certificates_from_roster(roster, template, output_dir, issued_on=str(date.today())):

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

            instantiate_assertion(cert, uid, issued_on)
            instantiate_recipient(cert, recipient)

            # validate certificate before writing
            schema_validator.validate_unsigned_v1_2_0(cert)

            with open(os.path.join(output_dir, uid + '.json'), 'w') as unsigned_cert:
                json.dump(cert, unsigned_cert)


if __name__ == "__main__":
    template_file = os.path.join(config.template_dir, config.template_file_name)
    create_unsigned_certificates_from_roster(config.roster, template_file, config.unsigned_certificates_dir)
