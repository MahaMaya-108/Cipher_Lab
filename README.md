# CipherLab

A Flask web app for Caesar and Vigenere ciphers with user accounts and a persistent activity log.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scriptsctivate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

## Files

- app.py        Flask app, routes, JSON cipher API
- models.py     SQLAlchemy User and Log models
- ciphers.py    Caesar + Vigenere encrypt/decrypt
- templates/    Jinja2 templates (Tailwind via CDN)
