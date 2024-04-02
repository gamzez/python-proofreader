# LLM-Based Proofreader

This repository contains a Python-based proofreading tool that leverages OpenAI's GPT-3.5 model to correct grammatical errors in German texts. The tool not only identifies and corrects errors but also highlights the differences between the original and corrected texts.

## Prerequisites

To use this proofreader, you will need:
- Python installed on your system.
- An active OpenAI API key.

## Usage

The proofreader is encapsulated in a function named `grammarly` which takes a string of text as input and returns three pieces of information:
- A boolean indicating whether an error was detected in the input text.
- The original text with erroneous words highlighted by `-` signs.
- The corrected text with replacements highlighted by `<` and `>` signs.

To use the proofreader, you can directly call the `grammarly` function from your Python code like so:

```python
text_with_errors = "Your text with potential errors."
is_error, original, corrected = grammarly(text_with_errors)
print("Error Detected:", is_error)
print("Original Text:", original)
print("Corrected Text:", corrected)
