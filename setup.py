import os
import uuid

from pip.req import parse_requirements
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'), session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='cert-tools',
    version='1.2.2',
    description='creates blockchain certificates',
    author='MIT Media Lab Blockchain Certificates',
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
            'create-certificate-template = cert_tools.create_certificate_template:main',
            'instantiate-certificate-batch = cert_tools.instantiate_certificate_batch:main',
            'create-revocation-addresses = cert_tools.create_revocation_addresses:main',
            'create-issuer = cert_tools.create_issuer:main'
        ]}
)
