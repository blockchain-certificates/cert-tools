import helpers

##############################
## TEMPLATE CREATION CONFIG ##
##############################
issuer_logo_file = 'data/images/issuer-logo.png'
issuer_signature_file = 'data/images/issuer-signature.png'
cert_image_file = 'data/images/cert-image.png'

# issuer information
issuer_url = 'http://issuer.org'
issuer_certs_url = 'http://certificates.issuer.org'  # where the certificates are hosted
issuer_public_key_url = 'https://issuer.org/keys/path-to-signing-public-key.asc'
issuer_signature = helpers.encode_image(issuer_signature_file)
issuer_email = 'contact@issuer.org'
issuer_name = 'Issuer Institution Name'
issuer_id = 'https://issuer.org/issuer/path-to-public-keys.json'
issuer_logo = helpers.encode_image(issuer_logo_file)


# certificate information
certificate_language = 'en-US'
certificate_description = 'This is the display description of the certificate.'
certificate_title = 'This is the certificate title'
certificate_id = helpers.urljoin_wrapper(issuer_certs_url, '/criteria/YYYY/mm/certificate_id.json') # e.g. /criteria/2016/01/alumni.json
certificate_image = helpers.encode_image(cert_image_file)

# whether to hash recipient emails
hash_emails = False

additional_global_fields = []
additional_per_recipient_fields = []
# can specify an array of additional global fields. For each additional field, you must indicate:
# - the jsonpath to the field
# - the global value to use
# additional_global_fields = [
#     {
#         'path': '$.certificate.subtitle',
#         'value': 'kim custom subtitle',
#     }
#]

# can specify an array of additional per-recipient fields. For each additional field, you must indicate:
# - the jsonpath to the field
# - the merge_tag placeholder to use
# - the csv column where the value (per recipient) can be found
# additional_per_recipient_fields = [
#     {
#         'path': '$.assertion.evidence',
#         'value': '*|EVIDENCE|*',
#         'csv_column': 'evidence'
#     }
# ]

###################
## TEMPLATE DATA ##
###################
# these are used by both
template_dir = 'data/certificate_templates'  # template output directory
template_file_name = 'test.json'

##############################
## INSTANTIATE BATCH CONFIG ##
##############################
unsigned_certificates_dir = 'data/unsigned_certificates'
roster = 'data/rosters/roster.csv'