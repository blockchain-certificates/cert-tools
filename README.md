[![Build Status](https://travis-ci.org/blockchain-certificates/cert-tools.svg?branch=master)](https://travis-ci.org/blockchain-certificates/cert-tools)

# cert-tools
Command line tools for designing certificate templates, instantiating a certificate batch, and import/export tasks

see example of certificate template and batch creation in sample_data 

## Install

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/developer-common-docs/blob/master/virtualenv.md)

2. Git clone the repository and change to the directory

  ```bash
  git clone https://github.com/blockchain-certificates/cert-tools.git && cd cert-tools
  ```

3. Run the setup script

  ```bash
  pip install .
  ```

## Scripts

The cert-tools setup script installs 2 scripts, which are described below:


### create_certificate_template.py

#### Run

```
create-certificate-template -c conf.ini
```

#### About

Creates a certificate template populated with the setting you provide in the conf.ini file. This will not contain recipient-specific data; such fields will be populated with merge tags.
 
You can specify additional global fields (fields that apply for every certificate in the batch) and additional per-recipient fields (fields that you will specify per-recipient).

additional_global_fields:  For each additional global field, you must indicate:

- the jsonpath to the field
- the global value to use

Example:

conf.ini version:
```
additional_global_fields = {"fields": [{"path": "$.certificate.subtitle","value": "custom subtitle"}]}
```

above expanded for readability:
```
    additional_global_fields = {
        "fields": 
            [
                {
                    "path": "$.certificate.subtitle",
                    "value": "custom subtitle"
                }
            ]
    }

```

additional_per_recipient_fields: Although these are per-recipient, we still use these for the template creation process. Except in this case, we apply merge tags as values. This is to allow additional tooling to replace instantiate_certificate_batch.py. For each additional per-recipient field, you must indicate:

- the jsonpath to the field
- the merge_tag placeholder to use
- the csv column where the value (per recipient) can be found. This is used by instantiate_certificate_batch

Example:

conf.ini version:
```
    additional_per_recipient_fields = {"fields": [{"path": "$.assertion.evidence","value": "*|EVIDENCE|*","csv_column": "evidence"}]}
```

above expanded for readability:
```
    additional_per_recipient_fields = {
        "fields": 
            [
                {
                    "path": "$.assertion.evidence",
                    "value": "*|EVIDENCE|*",
                    "csv_column": "evidence"
                }
            ]
    }
```
   
   
### instantiate_certificate_batch.py

#### Run
```
instantiate-certificate-batch -c conf.ini
```

#### About

Populates the certificate template (created by the previous script) with recipient data from a csv file. It generates a certificate per recipient based on the values in the csv file.

The csv file location is configurable via the conf.ini file.

The csv file must always contain:

- familyName
- givenName
- pubkey
- identity

It may also contain custom fields per-recipient. The create_certificate_template.py script populated the template with merge tags for these fields. This script will now populate each recipient's certificate with the value in the corresponding csv file. So in this example, we'll get the value in the csv column 'revkey' to populate the 'revocationKey' field on the certificate's recipient section.


```
additional_per_recipient_fields = {"fields": [{"path": "$.recipient.revocationKey","value": "*|REVKEY|*","csv_column": "revkey"}]}
```
   
### create_revocation_addresses.py
   
#### Run (optional)
```
create-revocation-addresses -k tpubD6NzV...H66KUZEBkf
```

#### About

Generates Bitcoin addresses using an HD extended public (or private) key to be used as the issuer's revocation addresses for the certificates. This would be useful only if the issuer requires to be able to revoke specific certificates later on. It creates a list of addresses that could then be easily merged with the roster file, e.g. using unix's paste command.

To create 20 revocation address for a testnet extended public key for the first batch of 2016 certificates run:

```
echo "revkey" > rev_addresses.txt

create-revocation-addresses -n 20 -p "2016/1" -k tpubD6NzV...H66KUZEBkf >> rev_addresses.txt
```

To merge to roster (in unix) run:

```
paste -d , roster.txt rev_addresses.txt > roster_with_rev.txt
```

## Example

See sample_data for example configuration and output. `conf-mainnet.ini` was used to create a batch of 2 unsigned certificates on the Bitcoin blockchain. 

The steps were:
- Create the template
    - Update the config file to contain the correct data to populate the certificates
    - Place the needed images in `images/` and point to them in the config file
    - Run `create_certificate_template.py`, which resulted in the certificate template `/certificate_templates/game_of_thrones_live_template.json`
- Instantiate the batch
    - Add the recipient roster (in this case `rosters/roster_testnet.csv`) with the recipient's Bitcoin addresses.
    - Run 'instantiate_certificate_batch.py', which resulted in the files in `unsigned_certificates`
    
Then the unsigned certificates were copied to cert-issuer for signing and issuing on the blockchain.

## Contact

Contact [info@blockcerts.org](mailto:info@blockcerts.org) with questions
