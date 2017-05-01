import os
import uuid

from pip.req import parse_requirements
from setuptools import setup, find_packages

from cert_tools import __version__

here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'), session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='cert-tools',
    version=__version__,
    description='creates blockchain certificates',
    author='Blockcerts',
    tests_require=['tox'],
    url='https://github.com/blockchain-certificates/cert-tools',
    license='MIT',
    author_email='info@blockcerts.org',
    long_description=long_description,
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'create-certificate-template = cert_tools.create_v1_2_certificate_template:main',
            'instantiate-certificate-batch = cert_tools.instantiate_v1_2_certificate_batch:main',
            'create-revocation-addresses = cert_tools.create_revocation_addresses:main',
            'create-issuer = cert_tools.create_issuer:main'
        ]}
)