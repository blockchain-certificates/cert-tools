import unittest

from cert_tools import create_v3_certificate_template

class Options:
    def __init__(self):
        self.issuer_id = 'did:example:0123456789'

class TestV3CertificateTemplate(unittest.TestCase):
    def test_create_v3_assertion(self):
        options = Options()
        output = create_v3_certificate_template.create_v3_assertion(options)
        self.assertEqual(output, {
            '@context': [
                'https://www.w3.org/2018/credentials/v1',
                'https://w3id.org/blockcerts/v3'
            ],
            'type': ["VerifiableCredential", "BlockcertsCredential"],
            "issuer": 'did:example:0123456789',
            'issuanceDate': '*|DATE|*',
            'id': 'urn:uuid:*|CERTUID|*'
        })
