def process_parsed_file(file_path):
    reconstructed_text_forms = []
    reconstructed_text_lemmas = []
    current_line_forms = []
    current_line_lemmas = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('<doc') or not line.strip():
                if current_line_forms:
                    reconstructed_text_forms.append(' '.join(current_line_forms))
                    reconstructed_text_lemmas.append(' '.join(current_line_lemmas))
                    current_line_forms = []
                    current_line_lemmas = []
                continue

            # Extract necessary parts (word form, lemma, and tag)
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                tag = parts[3]
                if (tag not in ['E', 'P', 'R', 'C', 'F', 'I', 'D', 'B']) or (parts[2] == 'non'):
                    word_form = parts[1]
                    lemma = parts[2]
                    current_line_forms.append(word_form)
                    current_line_lemmas.append(lemma)

    # Add the last line if it exists
    if current_line_forms:
        reconstructed_text_forms.append(' '.join(current_line_forms))
        reconstructed_text_lemmas.append(' '.join(current_line_lemmas))

    return '\n'.join(reconstructed_text_forms), '\n'.join(reconstructed_text_lemmas)

def save_to_file(text, file_path):
    """
    Save the given text to a file.

    Args:
    text (str): The text to be saved.
    file_path (str): The path to the file where the text will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    file_path = 'output.parsed'
    forms_output_file_path = 'DecameronOriginalWordForms.txt'
    lemmas_output_file_path = 'DecameronLemmatized.txt'
    
    reconstructed_text_forms, reconstructed_text_lemmas = process_parsed_file(file_path)
    save_to_file(reconstructed_text_forms, forms_output_file_path)
    save_to_file(reconstructed_text_lemmas, lemmas_output_file_path)
    
    print(f"Original word forms text has been saved to {forms_output_file_path}")
    print(f"Lemmatized text has been saved to {lemmas_output_file_path}")

if __name__ == '__main__':
    main()
