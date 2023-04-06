#!/bin/bash

# Install Poetry
echo "Installing Poetry..."
pip install poetry

# Find the tgpt directory, suppressing error messages
echo "Searching for 'tgpt' directory..."
TGPT_DIR=$(find ~ -type d -iname "tgpt" -print -quit 2>/dev/null)

# Check if the tgpt directory was found
if [ -z "$TGPT_DIR" ]; then
  echo "Error: 'tgpt' directory not found."
  exit 1
fi

echo "Found 'tgpt' directory at: $TGPT_DIR"

# Navigate to the tgpt directory
cd "$TGPT_DIR"

# Set the Python version to be used with Poetry
echo "Setting Python version for Poetry environment..."
poetry env use python3.11

# Install dependencies with Poetry
echo "Installing dependencies using Poetry..."
poetry install

# Check if the OPENAI_API_KEY already exists in .zshrc
if ! grep -q '^export OPENAI_API_KEY=' ~/.zshrc; then
  # Prompt the user for the OpenAI API key
  echo "Get your OpenAI API Key from https://platform.openai.com/account/api-keys and enter it here:"
  read OPENAI_API_KEY
  echo "export OPENAI_API_KEY=${OPENAI_API_KEY}" >> ~/.zshrc
  echo "OPENAI_API_KEY added to .zshrc."
else
  echo "OPENAI_API_KEY already exists in .zshrc. Won't prompt user for key."
fi
# Check if the tgpt alias already exists in .zshrc
grep -q '^alias tgpt=' ~/.zshrc || {
  echo "Adding 'tgpt' alias to .zshrc..."
  echo "alias tgpt='python ${TGPT_DIR}/tgpt.py --input \$*'" >> ~/.zshrc
  echo "'tgpt' alias added successfully."
}

echo "Done. Now run "source ~/.zshrc" and you can use the 'tgpt' command."