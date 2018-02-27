# salt-aws-boto3

Use boto3 for AWS orchestration with Salt.

* [Install](#install)
* [Salt Setup](#salt-setup)
* [Python Package Setup](#py-setup)
* [Documentation](#docs)
* [Tests](#tests)

---

## <a name="install"></a> Install

```bash
pip install salt-aws-boto3
```


## <a name="salt-setup"></a> Salt Setup

* set an environment variable for `AWS_REGION` (Default is `us-east-1`)
* copy `aws_boto3` to your salt modules directory
* copy `pip_deps.sls` to your salt states directory
* run `salt '*' state.apply pip_deps`
* run `salt '*' saltutil.sync_modules`


## <a name="py-setup"></a> Use at as a python package

```bash
[sudo] pip install virtualenv
virtualenv .venv
source .venv/bin/activate
pip install --editable .
```


## <a name="docs"></a> Documentation

### Run any boto3 client

[See the boto3 docs](http://boto3.readthedocs.io/en/latest/reference/services/index.html)


```python
from aws_boto3 import run_client
# run_client(service, function, region=None, payload=None)
run_client('ec2', 'create_key_pair', payload={'KeyName': 'foo'})
```

### More docs

* [DynamoDB](./docs/dynamodb.md)
* [ECR](./docs/ecr.md)
* [ECS](./docs/ecs.md)
* [IAM](./docs/iam.md)
* [KMS](./docs/kms.md)
* [Lambda](./docs/lambda.md)
* [S3](./docs/s3.md)


## <a name="tests"></a> Tests

Run the tests:

```bash
sh run-tests.sh
```
