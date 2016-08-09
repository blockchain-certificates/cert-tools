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
        # TODO: this is digital-certs specific; recast as OBI extension
        'subtitle': {
            'content': config.certificate_subtitle,
            'display': config.certificate_subtitle is not None
        },
        'title': config.certificate_title,
        'language': config.certificate_language,
        'image': config.certificate_image,
        'description': config.certificate_description,
        'id': config.certificate_id,
        'issuer': {
            'url': config.issuer_url,
            'image': config.issuer_logo,
            'email': config.issuer_email,
            'name': config.issuer_name,
            'id': config.issuer_id
        }
    }
    return certificate


def create_verification_section():
    verify = {
        'signer': config.issuer_public_key_url,
        'attribute-signed': 'uid',
        'type': 'ECDSA(secp256k1)'
    }
    return verify


def create_recipient_section():
    recipient = {
        'type': 'email',
        'familyName': '*|LNAME|*',
        'givenName': '*|FNAME|*',
        'pubkey': '*|PUBKEY|*',
        'identity': '*|EMAIL|*',
        'hashed': False
    }
    return recipient


def create_assertion_section():
    assertion = {
        'issuedOn': '*|DATE|*',
        'image:signature': config.issuer_signature,
        'uid': '*|CERTUID|*',
        'id': helpers.urljoin_wrapper(config.issuer_certs_url, '*|CERTUID|*'),
        'evidence': ''
    }
    return assertion


def create_certificate_template(template_dir, template_file_name):
    certificate = create_certificate_section()
    verify = create_verification_section()
    assertion = create_assertion_section()
    recipient = create_recipient_section()

    raw_json = {
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
