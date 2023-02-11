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

## setting up docker

You will need to add the artifact registry to your docker config:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```
