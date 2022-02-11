# pyOLOS - CLI for OLOS API

Command line interface supporting CRUD operations to make deposits on the OLOS preservation infrastructure.

More informations about [OLOS](https://olos.swiss)

Brought to you by Photo Élysée - Musée cantonal pour la photographie 
More informations about [Photo Élysée](http://elysee.ch) - Musée cantonal pour la photographie and [Plateforme 10](https://www.plateforme10.ch).

Enjoy !

## 1. Setup and configuration

### 1.1 Dev dir setup

```
$ mkdir pyolos
$ virtualenv venv
$ . venv/Script/activate
$ vim setup.py
$ pip install --editable .
```
For a good example on how to use Setuptools see :
    https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

### 1.2 Secret API Token

From your project directory

```
$ touch .env
$ echo "token=mySecretToken" >> .env
```
Pitfall: if your token is not valid anymore (they have a time limited validity), requests will fail silently. If your command fail without error message, be sure to check your ```.env``` file !

### 1.3 Adapting Configuration Files

Create configuration files using the following structure

1. File `./pyolos/conf/organisation_unit.ini` used to configure your organisation unit parameters. PITFALL: use double quote ONLY for value that contains spaces !

Sample content:
```
[Org]
name = "My organisation name"
org_unit_id = 01234567-1234-1234-1234-012345678901

[Agent]
first_name = "My first"
last_name = Mylast
orcid = 0000-1111-2222-3333
```
2. Adapt the file `./pyolos/conf/dlcm_ressources.ini` to the configuration of the dlcm server you are talking to. As well as the default access and sensitivity levels of the data you archive. Sample content: 
```
[Server]
protocol = https
root_context = sandbox.dlcm.ch

[Modules]
admin = administration/admin
preingest = ingestion/preingest
access = accession/access

[Deposit_DEFAULT]
access_level = PUBLIC
data_sensitivity = BLUE
```

## 2. CLI Commands Help

### 2.1 module `pyolos`
```
Usage: pyolos [OPTIONS] COMMAND [ARGS]...

  Command line interface to use OLOS preservation infrastructure.

Options:
  --verbose  Showing various details of the process.
  --help     Show this message and exit.

Commands:
  deposit-approve  Submit deposit for approval by passing its resource Id.
  deposit-create   POST new deposit, a resource used as a container to...
  deposit-delete   DELETE deposit by passing its resource Id.
  deposit-meta     GET deposit's metadata by passing its resource Id.
  deposit-upload   Add a new file to an existing deposit.
```

### 2.2 Deposit Action Commands

_Command `deposit-create`_
```
Usage: pyolos deposit-create [OPTIONS] [OUTPUT]

  POST new deposit, a resource used as a container to group several datasets
  (files) to be submited.  [OUTPUT] allows the output to be saved to a file.
  If no argument is provided, the output is send to stout.

Options:
  --access-level TEXT     The access level of the deposit. Values: PUBLIC,
                          RESTRICTED, CLOSED
  --datasensitivity TEXT  The data sensitivity of the deposit. Values:
                          UNDEFINED, BLUE, GREEN, YELLOW, ORANGE, RED, CRIMSON
  --description TEXT      The description of the deposit.
  --pubdate TEXT          The publication date of the deposit. Format: yyyy-
                          MM-dd
  --title TEXT            The title of the deposit.
  --help                  Show this message and exit.
```
_ Command `deposit-meta`
```
Usage: pyolos deposit-meta [OPTIONS] [OUTPUT]

  GET deposit's metadata by passing its resource Id.  [OUTPUT] allows the
  output to be saved to a file. If no argument is provided, the output is send
  to stout.

Options:
  --resid TEXT  Deposit resource ID.
  --help        Show this message and exit.
```
_Command `deposit-upload`_
```
Usage: pyolos deposit-upload [OPTIONS] DEPOSIT_ID FILE_PATH [OUTPUT]

  Add a new file to an existing deposit. [DEPOSIT-ID] Resource Id from the
  deposit.  [FILE-PATH] Full path to the file to add. [OUTPUT] allows the
  output to be saved to a file. If no argument is provided, the output is send
  to stout.

Options:
  --file-category TEXT  The category size of the data file. Values: Primary,
                        Secondary, Package, Software. Default: Primary
  --file-type TEXT      The sub-category size of the data file. Available
                        values depend on the category. See Data File Details:
                        https://sandbox.dlcm.ch/administration/docs/DLCM-
                        APIs.html#data-file. Default: Digitalized
  --help                Show this message and exit.
```
_Command `deposit-approve`_
```
Usage: pyolos deposit-approve [OPTIONS] [OUTPUT]

  Submit deposit for approval by passing its resource Id.  [OUTPUT] allows the
  output to be saved to a file. If no argument is provided, the output is send
  to stout.

Options:
  --resid TEXT  Deposit resource ID.
  --help        Show this message and exit.
```
_Command `deposit-delete`_
```
Usage: pyolos deposit-delete [OPTIONS] [OUTPUT]

  DELETE deposit by passing its resource Id.  [OUTPUT] allows the output to be
  saved to a file. If no argument is provided, the output is send to stout.

Options:
  --resid TEXT  Deposit resource ID.
  --help        Show this message and exit.
```
## 3. Examples

### Create a deposit

```
pyolos --verbose deposit-create --title "Test Deposit" --description "This is a test deposit" --pubdate 2022-02-01 --access-level CLOSED --datasensitivity BLUE
```
### Get deposit metadata to a file (JSON)
```
pyolos --verbose deposit-meta --resid f161207d-68c8-46aa-a757-ac78622490fd output.json
```

### Upload a primary data file into a deposit
```
pyolos --verbose deposit-upload --file-category Primary --file-type Digitalized f161207d-68c8-46aa-a757-ac78622490fd DJ_007517_modele.tif upload_result_metadata.json
```

### Upload a DataCite metadata file into a deposit
```
pyolos --verbose deposit-upload --file-category Package --file-type Metadata f161207d-68c8-46aa-a757-ac78622490fd descriptive_metadata_file_DataCite44.xml upload_result_metadata.json
```

### Approve a deposit (queues the deposit to be asynchronously archived)
```
 pyolos --verbose deposit-approve --resid f161207d-68c8-46aa-a757-ac78622490fd

```

### Delete a deposit
```
pyolos --verbose deposit-delete --resid bb7c3631-7dcd-4e77-9a17-62ed7f28401b
```

License [MIT](https://opensource.org/licenses/MIT) see LICENSE file for more information.