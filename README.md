# tgpt
A streaming Python CLI leveraging OpenAI GPT for code assistance, including code verification, rewriting, and general queries.

## Quick & Easy Code Assistance
What follows assumes youve started a session with "tgpt".
Besides being able to answer arbitrary queries with `<query>`, you can also use the tool to verify and rewrite code. To verify code, simply type the `.verify` command followed by the full path of the file you want to verify:
```bash
.verify file_to_verify.py
```
Rewrite code with the .rewrite command:
```bash
.rewrite file_to_rewrite.py
```
Rewritten code will be saved as a .draft file, e.g., file_to_rewrite.py.draft. Just type your questions or commands to interact with the tool and enjoy real-time GPT-powered assistance!


## Quickstart

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
6. Open the `prompts.py` file and populate the `REWRITE_CODE_PROMPT` and `VERIFY_CODE_PROMPT` variables before running the script. You may also want to modify your system prompt in `system_prompt.py`

Now, you can use the `tgpt` command to start a session:

```bash
tgpt
```
