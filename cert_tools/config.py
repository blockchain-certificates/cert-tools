import configargparse
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def make_action(additional_arg):
    class customAction(configargparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            print(additional_arg)
            json_obj = json.loads(values)['fields']
            setattr(args, self.dest, json_obj)
    return customAction


def create_config():

    p = configargparse.getArgumentParser(default_config_files=[os.path.join(BASE_DIR, 'conf.ini')])

    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')

    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--issuer_logo_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--issuer_signature_file', type=str, help='issuer signature image file, png format')
    p.add_argument('--cert_image_file', type=str, help='issuer logo image file, png format')
    p.add_argument('--issuer_url', type=str, help='issuer URL')
    p.add_argument('--issuer_certs_url', type=str, help='issuer certificates URL')
    p.add_argument('--issuer_email', type=str, help='issuer email')
    p.add_argument('--issuer_name', type=str, help='issuer name')
    p.add_argument('--issuer_id', type=str, help='path to issuer public keys')
    p.add_argument('--certificate_language', type=str, required=False, help='certificate language')
    p.add_argument('--certificate_description', type=str, help='the display description of the certificate')
    p.add_argument('--certificate_title', type=str, help='the title of the certificate')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--hash_emails', action='store_true',
                   help='whether to hash emails in the certificate')
    p.add_argument('--additional_global_fields', action=make_action('per_recipient_fields'), help='additional global fields')
    p.add_argument('--additional_per_recipient_fields', action=make_action('per_recipient_fields'), help='additional per-recipient fields')

    p.add_argument('--unsigned_certificates_dir', type=str, help='output directory for unsigned certificates')
    p.add_argument('--roster', type=str, help='roster file name')
    args, _ = p.parse_known_args()
    return args


parsed_config = None


def get_config():
    global parsed_config
    if parsed_config:
        return parsed_config
    parsed_config = create_config()
    return parsed_config
