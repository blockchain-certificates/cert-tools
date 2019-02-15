#!/usr/bin/env python

'''
Creates a certificate template with merge tags for recipient/assertion-specific data.
'''
import json
import os
import uuid

import configargparse

from cert_tools import helpers
from cert_tools import jsonpath_helpers

from cert_core.cert_model.model import scope_name
from cert_schema import OPEN_BADGES_V2_CANONICAL_CONTEXT, BLOCKCERTS_V2_CANONICAL_CONTEXT

OPEN_BADGES_V2_CONTEXT = OPEN_BADGES_V2_CANONICAL_CONTEXT
BLOCKCERTS_V2_CONTEXT = BLOCKCERTS_V2_CANONICAL_CONTEXT


def create_badge_section(config):
    cert_image_path = os.path.join(config.abs_data_dir, config.cert_image_file)
    issuer_image_path = os.path.join(config.abs_data_dir, config.issuer_logo_file)
    badge = {
        'type': 'BadgeClass',
        'id': helpers.URN_UUID_PREFIX + config.badge_id,
        'name': config.certificate_title,
        'description': config.certificate_description,
        'image': helpers.encode_image(cert_image_path),
        'issuer': {
            'id': config.issuer_id,
            'type': 'Profile',
            'name': config.issuer_name,
            'url': config.issuer_url,
            'email': config.issuer_email,
            'image': helpers.encode_image(issuer_image_path),
            'revocationList': config.revocation_list
        }
    }

    badge['criteria'] = {}
    badge['criteria']['narrative'] = config.criteria_narrative

    if config.issuer_signature_lines:
        signature_lines = []
        signature_lines = []
        for signature_line in config.issuer_signature_lines:
            signature_image_path = os.path.join(config.abs_data_dir, signature_line['signature_image'])
            signature_lines.append(
                {
                    'type': [
                        'SignatureLine',
                        'Extension'
                    ],
                    'jobTitle': signature_line['job_title'],
                    'image': helpers.encode_image(signature_image_path),
                    'name': signature_line['name']
                }
            )
        badge[scope_name('signatureLines')] = signature_lines

    return badge


def create_verification_section(config):
    verification = {
        'type': ['MerkleProofVerification2017', 'Extension'],
        'publicKey': config.issuer_public_key

    }
    return verification


def create_recipient_section(config):
    recipient = {
        'type': 'email',
        'identity': '*|EMAIL|*',
        'hashed': config.hash_emails
    }
    return recipient


def create_recipient_profile_section():
    return {
        'type': ['RecipientProfile', 'Extension'],
        'name': '*|NAME|*',
        'publicKey': 'ecdsa-koblitz-pubkey:*|PUBKEY|*'
    }


def create_assertion_section(config):
    assertion = {
        '@context': [
            OPEN_BADGES_V2_CONTEXT,
            BLOCKCERTS_V2_CONTEXT,
            {
                "displayHtml": {"@id": "schema:description"}
            }
        ],
        'type': 'Assertion',
        'displayHtml': config.display_html,
        'issuedOn': '*|DATE|*',
        'id': helpers.URN_UUID_PREFIX + '*|CERTUID|*'
    }
    return assertion


def create_certificate_template(config):

    if not config.badge_id:
        badge_uuid = str(uuid.uuid4())
        print('Generated badge id {0}'.format(badge_uuid))
        config.badge_id = badge_uuid

    badge = create_badge_section(config)
    verification = create_verification_section(config)
    assertion = create_assertion_section(config)
    recipient = create_recipient_section(config)
    recipient_profile = create_recipient_profile_section()

    assertion['recipient'] = recipient
    assertion[scope_name('recipientProfile')] = recipient_profile

    assertion['badge'] = badge
    assertion['verification'] = verification

    if config.additional_global_fields:
        for field in config.additional_global_fields:
            assertion = jsonpath_helpers.set_field(assertion, field['path'], field['value'])

    if config.additional_per_recipient_fields:
        for field in config.additional_per_recipient_fields:
            assertion = jsonpath_helpers.set_field(assertion, field['path'], field['value'])

    return assertion


def write_certificate_template(config):
    template_dir = config.template_dir
    if not os.path.isabs(template_dir):
        template_dir = os.path.join(config.abs_data_dir, template_dir)
    template_file_name = config.template_file_name

    assertion = create_certificate_template(config)
    template_path = os.path.join(config.abs_data_dir, template_dir, template_file_name)

    print('Writing template to ' + template_path)
    with open(template_path, 'w') as cert_template:
        json.dump(assertion, cert_template)


def get_config():
    cwd = os.getcwd()
    config_file_path = os.path.join(cwd, 'conf.ini')
    p = configargparse.getArgumentParser(default_config_files=[config_file_path])

    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')

    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--issuer_logo_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--cert_image_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--issuer_url', type=str, help='issuer URL')
    p.add_argument('--issuer_certs_url', type=str, help='issuer certificates URL')
    p.add_argument('--issuer_email', required=True, type=str, help='issuer email')
    p.add_argument('--issuer_name', required=True, type=str, help='issuer name')
    p.add_argument('--issuer_id', required=True, type=str, help='issuer profile')
    p.add_argument('--issuer_key', type=str, help='issuer issuing key')
    p.add_argument('--certificate_description', type=str, help='the display description of the certificate')
    p.add_argument('--certificate_title', required=True, type=str, help='the title of the certificate')
    p.add_argument('--criteria_narrative', required=True, type=str, help='criteria narrative')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--hash_emails', action='store_true',
                   help='whether to hash emails in the certificate')
    p.add_argument('--revocation_list', type=str, help='issuer revocation list')
    p.add_argument('--issuer_public_key', type=str, help='issuer public key')
    p.add_argument('--badge_id', required=True, type=str, help='badge id')
    p.add_argument('--issuer_signature_lines', action=helpers.make_action('issuer_signature_lines'),
                   help='issuer signature lines')
    p.add_argument('--additional_global_fields', action=helpers.make_action('global_fields'),
                   help='additional global fields')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'),
                   help='additional per-recipient fields')
    p.add_argument('--display_html', type=str, help='html content to display')

    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))
    return args


def main():
    conf = get_config()
    write_certificate_template(conf)
    print('Created template!')


if __name__ == "__main__":
    main()
