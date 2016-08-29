import helpers

##############################
## TEMPLATE CREATION CONFIG ##
##############################
issuer_logo_file = 'sample_data/images/issuer-logo.png'
issuer_signature_file = 'sample_data/images/issuer-signature.png'
cert_image_file = 'sample_data/images/cert-image.png'

# issuer information
issuer_url = 'http://www.blockcerts.org/mockissuer/'
issuer_certs_url = 'http://certificates.gamoeofthronesxyz.org'  # site where the certificates are hosted
issuer_public_key_url = 'http://www.blockcerts.org/mockissuer/keys/got_public_key.asc'
issuer_signature = helpers.encode_image(issuer_signature_file)
issuer_email = 'fakeEmail@gamoeofthronesxyz.org'
issuer_name = 'Game of thrones characters'
issuer_id = 'http://www.blockcerts.org/mockissuer/issuer/got-issuer.json'
issuer_logo = helpers.encode_image(issuer_logo_file)

# certificate information
certificate_language = 'en-US'
certificate_description = 'This certifies that the named character is an official Game of Thrones character.'
certificate_title = 'Game of Thrones Character'
certificate_id = helpers.urljoin_wrapper(issuer_certs_url, '/criteria/2016/08/got.json')
certificate_image = helpers.encode_image(cert_image_file)

# whether to hash recipient emails
hash_emails = False

additional_global_fields = []
additional_per_recipient_fields = []

###################
## TEMPLATE DATA ##
###################
# these are used by both
template_dir = 'sample_data/certificate_templates'  # template output directory
template_file_name = 'game_of_thrones_template.json'

##############################
## INSTANTIATE BATCH CONFIG ##
##############################
unsigned_certificates_dir = 'sample_data/unsigned_certificates'
roster = 'sample_data/rosters/game_of_thrones_roster.csv'