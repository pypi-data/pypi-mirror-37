# Certificate Pruner

Prune IAM Server Certificates that are not attached to an ELB


## Requirements
Python 2.7 or 3.6

## Installation
```
pip install cert-pruner
```

## Usage

Determine which certificates will be pruned:
```
cert-pruner
```

Find unattached certificates that were uploaded at least 60 days ago:
```
cert-pruner --days 60
```

Find unattached, expired certificates:
```
cert-pruner --days -1
```

Perform the pruning operation:
```
cert-pruner --delete
```

## Credentials

AWS credentials can be passed in using the `--profile` command line argument:

```
cert-pruner --profile profile-name
```

or by setting the `AWS_PROFILE` environment variable:

```
export AWS_PROFILE=profile-name
cert-pruner
```

If a profile is not configured, the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION`
environment variables can be set and used for authentication.
