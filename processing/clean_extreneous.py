import re

def clean_decameron(input_file_path, output_file_path):
    header_patterns = [
        re.compile(r'^\f.*Giornata.*$', re.I),
        re.compile(r'^\fConclusione dell’Autore$'),
        re.compile(r'^\fProemio$'),
    ]
    # More general pattern for verse number indicators
    verse_number_pattern = re.compile(r'\[\d+\]\s*')
    
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            if any(pattern.match(line) for pattern in header_patterns):
                continue
            line = verse_number_pattern.sub('', line)
            output_file.write(line)
    
    print("Cleaned content written to CleanedDecameron.txt")

def clean_commedia(input_file_path, output_file_path):
    with open(input_file_path, encoding="ISO 8859-1") as file:
        content = file.read()

    # Remove sequences enclosed with []
    pattern_brackets = re.compile(r'\[.*?\]', re.DOTALL)
    cleaned_content = re.sub(pattern_brackets, '', content)

    # Remove headers
    pattern_headers = re.compile(r'^\s*(Inferno|Paradiso|Purgatorio)(:\s*Canto)?(\s*[IVXLCDM]+)?\s*$', re.MULTILINE)
    cleaned_content = re.sub(pattern_headers, '', cleaned_content)

    # Writing cleaned content to a new file
    with open(output_file_path, 'w', encoding="ISO 8859-1") as output_file:
        output_file.write(cleaned_content)

    print("Cleaned content written to CleanedDivinaCommedia.txt")

if __name__ == "__main__":
    input = '../texts/Decameron/raw/Decameron.txt'
    output = '../texts/Decameron/raw/CleanedDecameron.txt'
    clean_decameron(input, output)
    # clean_commedia(input, output)