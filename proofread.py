import openai
import re
import string
import numpy as np
import difflib

# Load the OpenAI API key from the file
with open('openai_api_key.txt') as f:
    api_key = f.readline().strip()
openai.api_key = api_key

def text_correcter(text):
    # Define the prompt for the AI, instructing it to correct the provided text.
    system_role = "Korrigiere den folgenden deutschen Text und gib mir die korrigierte Version. Mach keine Erklärungen, gib nur den korrigierten Text zurück. Wenn der Text bereits korrekt ist, gib den Originaltext zurück."
    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": text}
    ]
    
    # Send the correction request to the API.
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the corrected text from the response.
    chat_response = completion.choices[0].message.content
    return chat_response

# Remove commas and dots from the given text.
def remove_commas_and_dots(text):
    return text.replace(',', '').replace('.', '')

# Remove spaces before punctuation in the given text.
def remove_space_before_punctuation(text):
    pattern = r'\s+([.?!,:;])'
    return re.sub(pattern, r'\1', text)

# Counts the number of words in the given string, ignoring punctuation.
def count_words(s):
    return sum([i.strip(string.punctuation).isalpha() for i in s.split()])

def proofreader(text_wErrors):
    # Preprocess the text for better comparison and correction.
    text_wErrors = remove_space_before_punctuation(text_wErrors)
    text_corrected = text_correcter(text_wErrors)
    
    # Remove punctuation for comparison purposes.
    text_wErrors_no_commas_dots = remove_commas_and_dots(text_wErrors)
    text_corrected_no_commas_dots = remove_commas_and_dots(text_corrected)
    
    # Check if the corrected text differs significantly from the original.
    isWordCountSame = np.abs(count_words(text_wErrors_no_commas_dots) - count_words(text_corrected_no_commas_dots)) < 2
    isError = isWordCountSame and (text_corrected_no_commas_dots.lower() != text_wErrors_no_commas_dots.lower())
    text_corrected = remove_space_before_punctuation(text_corrected)

    # Tokenize texts for detailed comparison.
    tokens1 = re.findall(r'\w+(?:-\w+)*\.?|\.', text_wErrors)
    tokens2 = re.findall(r'\w+(?:-\w+)*\.?|\.', text_corrected)

    # Use difflib to compare and highlight differences.
    d = difflib.Differ()
    diff = list(d.compare(tokens1, tokens2))

    # Mark differences for visualization.
    text_with_removed_markers = []
    text_with_added_markers = []
    for token in diff:
        if token.startswith('- '):
            text_with_removed_markers.append('-' + token[2:] + '-')
        elif token.startswith('+ '):
            text_with_added_markers.append('<' + token[2:] + '>')
        elif token.startswith('  '):
            text_with_removed_markers.append(token[2:])
            text_with_added_markers.append(token[2:])
            
    # Reconstruct the original and corrected texts with markers.
    reconstructed_original = ' '.join(text_with_removed_markers)
    reconstructed_corrected = ' '.join(text_with_added_markers)
    return bool(isError), reconstructed_original, reconstructed_corrected


    
if __name__ == "__main__":
    text_with_errors = "Dies sind ein Beispielsatz mit einem Fehler."
    is_error, original, corrected = proofreader(text_with_errors)
    print("Error Detected:", is_error)
    print("Original Text:", original)
    print("Corrected Text:", corrected)