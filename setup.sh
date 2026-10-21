#!/usr/bin/env bash
set -e

echo "Setting up CampusAccessCard..."

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo ""
echo "Setup complete."
echo "Edit .env and add your Gemini API key."
echo "Then run: python main.py"
