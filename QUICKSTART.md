# Quickstart

## No-model path (primary)

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r environment/requirements.txt
bash scripts/reproduce_offline.sh
```

Outputs appear under `outputs/`. This path verifies frozen key quantities and regenerates Figures 1–5 and Extended Data Figures 1–8.

## Container path

```bash
docker build -t maofield-repro -f environment/Dockerfile .
docker run --rm -v "$PWD/outputs:/work/outputs" maofield-repro
```

## Full provider rerun

Not required to reproduce the reported paper. See `REPRODUCIBILITY.md`; it requires author-controlled credentials, exact provider availability and restricted evidence.
