# CipherLab: Symmetric Encryption App
An interactive web application built with Python and Flask to demonstrate how symmetric cryptography works in a modern web environment.

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

# Project Features
CipherLab is a dynamic web application designed to simplify the complexities of symmetric cryptography through an interactive, user-friendly interface. Built with a focus on academic clarity, the app allows users to visualize the transformation of data in real-time, bridging the gap between theoretical security concepts and practical web implementation. By utilizing a Flask backend and Tailwind CSS, the project demonstrates how security protocols can be integrated into modern, responsive web environments.

- Secure User Authentication: Implements a professional login and registration system, ensuring that encryption tasks and history are managed within private user sessions.

- Interactive Symmetric Engine: Provides a streamlined interface to encrypt plaintext and decrypt ciphertext using a shared secret key, demonstrating the fundamental "same-key" logic of symmetric algorithms.

- Modular Code Architecture: Features a clean separation of concerns between the Flask application (app.py), the cryptographic logic (ciphers.py), and the data structures (models.py).

- Modern "Glassmorphism" UI: Employs a sleek, dark-themed aesthetic with backdrop blurs and responsive layouts, built entirely using Jinja2 templates and Tailwind CSS.

- Educational Focus: Designed specifically as a college learning tool to help students understand data integrity and the practical application of encryption libraries in Python.

# Tech Stack
- Backend: Python, Flask, SQLAlchemy
- Frontend: HTML5, Jinja2, Tailwind CSS
- Cryptography: Caesar & Vigenère algorithms
