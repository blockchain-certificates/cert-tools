#!/usr/bin/env

'''
Creates a certificate template with merge tags for recipient/assertion-specific data.
'''
import json
import os

from jsonpath_rw import parse, Root, Child, Fields

import helpers
import jsonpath_helpers


def get_path(match):
    """
    return an iterator based upon MATCH.PATH. Each item is a path component, start from outer most item.
    :param match:
    :return:
    """
    if match.context is not None:
        for path_element in get_path(match.context):
            yield path_element
        yield str(match.path)


def recurse(child, fields_reverse):
    if isinstance(child, Fields):
        fields_reverse.append(child.fields[0])
    else:
        if not isinstance(child, Child):
            raise Exception('unexpected input')
        if not isinstance(child.left, Root):
            recurse(child.left, fields_reverse)
        recurse(child.right, fields_reverse)


def update_json(json, path, value):
    '''Update JSON dictionnary PATH with VALUE. Return updated JSON'''
    try:
        first = next(path)
        # check if item is an array
        if first.startswith('[') and first.endswith(']'):
            try:
                first = int(first[1:-1])
            except ValueError:
                pass
        json[first] = update_json(json[first], path, value)
        return json
    except StopIteration:
        return value


def additional_global_fields(config, raw_json):
    if config.additional_global_fields:
        for field in config.additional_global_fields:
            jp = parse(field['path'])
            matches = jp.find(raw_json)
            if matches:
                for match in matches:
                    jsonpath_expr = get_path(match)
                    raw_json = update_json(raw_json, jsonpath_expr, field['value'])
            else:
                fields = []
                recurse(jp, fields)
                temp_json = raw_json
                for idx, f in enumerate(fields):
                    if f in temp_json:
                        temp_json = temp_json[f]
                    elif idx == len(fields) - 1:
                        temp_json[f] = field['value']
                    else:
                        print('path is not valid! : %s', '.'.join(fields))
    return raw_json


def create_certificate_section(config):
    data_dir = config.data_dir
    cert_image_path = helpers.normalize_data_path(data_dir, config.cert_image_file)
    issuer_image_path = helpers.normalize_data_path(data_dir, config.issuer_logo_file)
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
    data_dir = config.data_dir
    issuer_image_path = helpers.normalize_data_path(data_dir, config.issuer_signature_file)
    assertion = {
        'type': 'Assertion',
        'issuedOn': '*|DATE|*',
        'image:signature': helpers.encode_image(issuer_image_path),
        'uid': '*|CERTUID|*',
        'id': helpers.urljoin_wrapper(config.issuer_certs_url, '*|CERTUID|*')
    }
    return assertion


def create_certificate_template(config):
    certificate = create_certificate_section(config)
    verify = create_verification_section(config)
    assertion = create_assertion_section(config)
    recipient = create_recipient_section(config)

    data_dir = config.data_dir
    template_dir = config.template_dir
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

    template_path = helpers.normalize_data_path(data_dir, template_dir, template_file_name)

    with open(template_path, 'w') as cert_template:
        json.dump(raw_json, cert_template)

    return raw_json


def main():
    import config
    conf = config.get_config()
    template = create_certificate_template(conf)
    print('Created template!')


if __name__ == "__main__":
    main()
