import json
import uuid
from datetime import date

import config
import helpers
import os
from collections import namedtuple

Recipient = namedtuple('Recipient', 'last_name first_name job_title date_range pubkey email')


def instantiate_assertion(cert, uid, issued_on):
    cert['assertion']['issuedOn'] = issued_on
    cert['assertion']['uid'] = uid
    cert['assertion']['id'] = helpers.urljoin_wrapper(config.issuer_certs_url, uid)
    return cert


def instantiate_recipient(cert, recipient):
    cert['recipient']['givenName'] = recipient.first_name
    cert['recipient']['familyName'] = recipient.last_name
    cert['recipient']['pubkey'] = recipient.pubkey
    cert['recipient']['identity'] = recipient.email


# TODO: this is digital-certs specific; recast as OBI extension
def create_extension(recipient):
    extension = {
        'recipient': {
            'degree': recipient['degree']
        }
    }
    return extension


def create_unsigned_certificates_from_roster(roster, template, output_dir, issued_on=str(date.today())):
    recipients = []
    with open(roster) as roster:
        for line in roster.readlines():
            parts = line.split(',')
            r = Recipient(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
            recipients.append(r)

    with open(template) as template:
        cert_str = template.read()
        cert = json.loads(cert_str)

        for recipient in recipients:
            uid = str(uuid.uuid4())

            instantiate_assertion(cert, uid, issued_on)
            instantiate_recipient(cert, recipient)

            # TODO: see create_extension
            #if recipient.XYZ:
            #    cert['extension'] = create_extension(recipient)

            with open(os.path.join(output_dir, uid + '.json'), 'w') as unsigned_cert:
                json.dump(cert, unsigned_cert)


if __name__ == "__main__":
    template_file = os.path.join(config.template_dir, config.template_file_name)
    create_unsigned_certificates_from_roster(config.roster, template_file, config.unsigned_certificates_dir)
