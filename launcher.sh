#!/bin/bash

# Packagemaxxing Environment Setup Script
# Prepares dependencies for the AI camera art system
# Run this after activating your virtual environment

set -e  # Exit on any error

echo "🚀 Packagemaxxing Environment Setup"
echo "==================================="
echo ""

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected!"
    echo "   Please activate your virtual environment first:"
    echo "   source venv/bin/activate  # or your venv path"
    echo ""
    echo "   Then run this script again."
    exit 1
else
    echo "✅ Virtual environment active: $(basename $VIRTUAL_ENV)"
fi

# Check if requirements.txt exists
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if packagemaxxing.py exists
if [[ ! -f "packagemaxxing.py" ]]; then
    echo "❌ Error: packagemaxxing.py not found!"
    exit 1
fi

echo ""
echo "🎉 Environment setup complete!"
echo ""
echo "To run the Packagemaxxing AI Camera Art system:"
echo "  python packagemaxxing.py"
echo ""
echo "The system will launch a Gradio web interface with:"
echo "• Real-time camera feed processing"
echo "• AI-powered visual effects (scanner art, matrix rain, etc.)"
echo "• Live audio transcription"
echo "• Gallery of generated art pieces"

