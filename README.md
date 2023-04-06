# tgpt
A Python command-line interface that uses OpenAI GPT to provide various code-related assistance. Features include code rewriting, verification, and general answers to code-related questions. You can interact with the tool by typing questions or commands, and it streams responses from GPT. To use it, obtain an API key from OpenAI, run `install_tgpt.sh`, and then `tgpt`.

# Quickstart

This quickstart guide walks you through setting up the `tgpt` project on your machine using the provided `install_tgpt.sh`.

To set up and run the `tgpt` project, follow these steps:

1. Download or clone the `tgpt` repository to your local machine.
2. Open your terminal and navigate to the location where you saved the `install_tgpt.sh` script.
3. Make the script executable by running:
   ```bash
   chmod +x install_tgpt.sh
   ```
4. Run the script:
   ```bash
   ./install_tgpt.sh
   ```
   The script will prompt you for your OpenAI API key if it's not already set in your `.zshrc` file.
5. Restart your terminal or source your `.zshrc` configuration by running:
   ```bash
   source ~/.zshrc
   ```

**6. Open the `prompts.py` file and populate the `CODE_PROMPT`, `REWRITE_CODE_PROMPT`, and `VERIFY_CODE_PROMPT` variables before running the script.**

Now, you can use the `tgpt` command as an alias for running the `tgpt.py` script with user input:

```bash
tgpt your_input_here
```

This script performs the following tasks:

1. Installs Poetry, a Python dependency management tool.
2. Searches for the 'tgpt' directory and navigates to it.
3. Sets Python 3.11 as the version for the Poetry environment.
4. Installs Python dependencies using Poetry.
5. If not already set, prompts for your OpenAI API Key and adds it to .zshrc.
6. Adds an alias 'tgpt' in .zshrc for easy script execution.

After running this script, reload your shell with `source ~/.zshrc`. Now you can use the 'tgpt' command.