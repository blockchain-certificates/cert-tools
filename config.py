import helpers


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

# output directories
template_dir = 'data/certificate_templates'
unsigned_certificates_dir = 'data/unsigned_certificates'
roster = 'data/rosters/roster.csv'

template_file_name = 'test.json'

