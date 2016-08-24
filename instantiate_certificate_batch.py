'''
Merges a certificate template with recipients defined in a roster file. The result is
unsigned certificates that can be given to cert-issuer.
'''
import json
import uuid
from datetime import date
import copy

import config
import helpers
import os
import hashlib
from collections import namedtuple
from cert_schema.schema_tools import schema_validator
import bcrypt

Recipient = namedtuple('Recipient', 'last_name first_name job_title date_range pubkey email')


def hash_and_salt_email_address(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest()

def instantiate_assertion(cert, uid, issued_on, evidence):
    cert['assertion']['issuedOn'] = issued_on
    cert['assertion']['uid'] = uid
    cert['assertion']['id'] = helpers.urljoin_wrapper(config.issuer_certs_url, uid)
    if evidence:
        cert['assertion']['evidence'] = evidence
    else:
        del cert['assertion']['evidence']
    return cert


def instantiate_recipient(cert, recipient):
    cert['recipient']['givenName'] = recipient.first_name
    cert['recipient']['familyName'] = recipient.last_name
    cert['recipient']['pubkey'] = recipient.pubkey
    if config.hash_emails:
        # this is probably overkill, but if I'm generating a salt...
        salt = bcrypt.gensalt()
        cert['recipient']['salt'] = salt
        cert['recipient']['identity'] = hash_and_salt_email_address(recipient.email, salt)
    else:
        cert['recipient']['identity'] = recipient.email


def create_unsigned_certificates_from_roster(roster, template, output_dir, issued_on=str(date.today())):

    recipients = []
    with open(roster) as roster:
        for line in roster.readlines():
            parts = line.split(',')
            r = Recipient(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
            recipients.append(r)

    with open(template) as template:
        cert_str = template.read()
        template = json.loads(cert_str)

        for recipient in recipients:
            uid = str(uuid.uuid4())

            cert = copy.deepcopy(template)

            # TODO: add evidence to csv. Also optional fields
            instantiate_assertion(cert, uid, issued_on, evidence=None)
            instantiate_recipient(cert, recipient)

            # validate certificate before writing
            schema_validator.validate_v1_2_0(cert)

            with open(os.path.join(output_dir, uid + '.json'), 'w') as unsigned_cert:
                json.dump(cert, unsigned_cert)


if __name__ == "__main__":
    template_file = os.path.join(config.template_dir, config.template_file_name)
    create_unsigned_certificates_from_roster(config.roster, template_file, config.unsigned_certificates_dir)
