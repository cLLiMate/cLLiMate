# cLLiMate

Large language models for sustainable climate data science.

## quickstart

Install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

### transferring data

Set up your gcloud credentials;

```bash
gcloud auth login
gcloud config set project cllimate
```

Then up and download data with gsutil at the root of the project:

```bash
# download data using rsync
gsutil -m rsync -r gs://cllimate/data/ data/

# upload data using rsync
gsutil rsync -r data/ gs://cllimate/data/
```

### setting up docker

You will need to add the artifact registry to your docker config:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

To build run all of the services:

```bash
docker compose build
docker compose up
```

The services will be available at:

- http://localhost:4001 for the api backend
- http://localhost:4002 for the frontend

### setting up secrets

Install sops and activate application-default credentials:

```bash
brew install sops
gcloud auth application-default login
```

Then decrypt the secrets:

```bash
sops -d conf/secrets/tokens.json
```

To edit secrets, remove the `-d` flag.

Source the following script to set up the environment variables:

```bash
source scripts/setup-secrets.sh
```

It might be useful to add the following to the top of your notebook if you need to add a secret to the environment:

```python
%load_ext autoreload
%autoreload 2

from cllimate.secrets import load_sops_secret
load_sops_secret()
```
