import os

from setuptools import setup, find_packages

from cert_tools import __version__

here = os.path.abspath(os.path.dirname(__file__))

with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]

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
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'create-certificate-template = cert_tools.create_v2_certificate_template:main',
            'create-certificate-template_v3 = cert_tools.create_v3_alpha_certificate_template:main',
            'instantiate-certificate-batch = cert_tools.instantiate_v2_certificate_batch:main',
            'instantiate-certificate-batch_v3 = cert_tools.instantiate_v3_alpha_certificate_batch:main',
            'create-issuer = cert_tools.create_v2_issuer:main'
        ]}
)
