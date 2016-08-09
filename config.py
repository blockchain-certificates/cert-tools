import helpers
import os

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
certificate_subtitle = ''
certificate_title = 'This is the certificate title'
certificate_id = helpers.urljoin_wrapper(issuer_certs_url, '/criteria/YYYY/mm/certificate_id.json') # e.g. /criteria/2016/01/alumni.json
certificate_image = helpers.encode_image(cert_image_file)

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

#########################
## IMPORT/EXPORT TOOLS ##
#########################
mongo_host_string = 'mongodb://localhost:27017'
signed_certificates_dir = 'signed_certificates'
transaction_ids_dir = 'transaction_ids'
receipts_dir = 'receipts'
signed_certificates_glob = os.path.join(signed_certificates_dir, '*.json')
transaction_ids_glob = os.path.join(transaction_ids_dir, '*.txt')
receipts_glob = os.path.join(receipts_dir, '*.json')