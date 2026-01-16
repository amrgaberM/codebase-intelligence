#!/bin/bash

# CodeBase RAG Setup Script

echo "🧠 CodeBase Intelligence RAG - Setup"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directories
mkdir -p data/repos data/vectors

# Check for .env
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "   Copy .env.example to .env and add your GROQ_API_KEY"
    cp .env.example .env
    echo "   Created .env from template"
fi

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add your GROQ_API_KEY to .env"
echo "  2. Activate: source venv/bin/activate"
echo "  3. Run UI: python app.py"
echo "  4. Or CLI: python cli.py --help"
echo ""
