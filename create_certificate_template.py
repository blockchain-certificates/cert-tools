'''
Creates a certificate template with merge tags for recipient/assertion-specific data.
'''
import json

import config
import helpers
import os
from collections import namedtuple

Recipient = namedtuple('Recipient', 'last_name first_name job_title date_range pubkey email')


def create_certificate_section():
    certificate = {
        '@type': 'Certificate',
        'title': config.certificate_title,
        'image:certificate': config.certificate_image,
        'description': config.certificate_description,
        'id': config.certificate_id,
        'issuer': {
            '@type': 'Issuer',
            'url': config.issuer_url,
            'image:logo': config.issuer_logo,
            'email': config.issuer_email,
            'name': config.issuer_name,
            'id': config.issuer_id
        }
    }

    if config.certificate_language:
        certificate['language'] = config.certificate_language

    if config.certificate_subtitle:
        certificate['subtitle'] = config.certificate_subtitle

    return certificate


def create_verification_section():
    verify = {
        '@type': 'VerificationObject',
        'signer': config.issuer_public_key_url,
        'attribute-signed': 'uid',
        'type': 'ECDSA(secp256k1)'
    }
    return verify


def create_recipient_section():
    recipient = {
        '@type': 'Recipient',
        'type': 'email',
        'familyName': '*|LNAME|*',
        'givenName': '*|FNAME|*',
        'pubkey': '*|PUBKEY|*',
        'identity': '*|EMAIL|*',
        'hashed': config.hash_emails
    }
    return recipient


def create_assertion_section():
    assertion = {
        '@type': 'Assertion',
        'issuedOn': '*|DATE|*',
        'image:signature': config.issuer_signature,
        'uid': '*|CERTUID|*',
        'id': helpers.urljoin_wrapper(config.issuer_certs_url, '*|CERTUID|*'),
        'evidence': '*|EVIDENCE|*'
    }
    return assertion


def create_certificate_template(template_dir, template_file_name):
    certificate = create_certificate_section()
    verify = create_verification_section()
    assertion = create_assertion_section()
    recipient = create_recipient_section()

    raw_json = {
        '@context': 'https://raw.githubusercontent.com/digital-certificates#', # TODO
        '@type': 'DigitalCertificate',
        'recipient': recipient,
        'assertion': assertion,
        'certificate': certificate,
        'verify': verify
    }

    with open(os.path.join(template_dir, template_file_name), 'w') as cert_template:
        json.dump(raw_json, cert_template)

    return raw_json


if __name__ == "__main__":
    template = create_certificate_template(config.template_dir, config.template_file_name)
