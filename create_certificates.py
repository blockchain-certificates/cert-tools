import argparse
import base64
import json
import random
from collections import namedtuple

import config

Recipient = namedtuple('Recipient', 'last_name first_name job_title date_range pubkey email')


def create_certificate_template(template_name):
    with open(config.issuer_logo, "rb") as logo_png:
        encoded = base64.b64encode(logo_png.read())
        logo_base64 = "data:image/png;base64," + encoded

    with open(config.issuer_signature, "rb") as signature_png:
        encoded = base64.b64encode(signature_png.read())
        signature_base64 = "data:image/png;base64," + encoded

    with open(config.cert_image, "rb") as cert_image_png:
        encoded = base64.b64encode(cert_image_png.read())
        cert_image_base64 = "data:image/png;base64," + encoded

    with open('generic_certificate_template.json') as template:
        cert_str = template.read()
        cert = json.loads(cert_str)

    cert['verify']['signer'] = config.verify_signer
    cert['assertion']['image:signature'] = signature_base64
    cert['certificate']['image'] = cert_image_base64
    cert['certificate']['id'] = config.cert_id

    cert['certificate']['issuer']['url'] = config.issuer_url
    cert['certificate']['issuer']['image'] = logo_base64
    cert['certificate']['issuer']['email'] = config.issuer_email
    cert['certificate']['issuer']['name'] = config.issuer_name
    cert['certificate']['issuer']['id'] = config.issuer_id

    sorted_cert = json.dumps(cert, sort_keys=True)

    with open(template_name + '.json', 'wb') as cert_template:
        s = sorted_cert.encode('utf-8')
        cert_template.write(s)


def create_unsigned_certificates_from_roster(roster, template):
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
            uid = '%024x' % random.randrange(16 ** 24)

            cert['assertion']['issuedOn'] = config.issued_on

            # recipient
            cert['recipient']['givenName'] = recipient.first_name
            cert['recipient']['familyName'] = recipient.last_name
            cert['recipient']['pubkey'] = recipient.pubkey
            cert['recipient']['identity'] = config.email

            # assertion
            cert['assertion']['uid'] = uid
            cert['assertion']['id'] = config.recipient_id_prefix + uid

            # certificate
            cert['certificate']['title'] = recipient.job_title
            cert['certificate']['description'] = config.description
            cert['certificate']['subtitle']['content'] = recipient.date_range
            cert['certificate']['subtitle']['display'] = True

            sorted_cert = json.dumps(cert, sort_keys=True)

            with open('unsigned_certs/' + uid + '.json', 'wb') as unsigned_cert:
                s = sorted_cert.encode('utf-8')
                unsigned_cert.write(s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates digital certificates from a template')
    parser.add_argument('--input_dir', nargs='?', const='data', type=str, default='data',
                        help='certificate data to populate into template. Default is data/')

    args = parser.parse_args()
    create_certificate_template('test')
