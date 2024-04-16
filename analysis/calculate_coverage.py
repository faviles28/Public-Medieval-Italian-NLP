def load_words_from_file(filename):
    words = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            words.update(word.strip().lower() for word in line.split())
    return words

def calculate_coverage(text_file, dictionary_file):
    dictionary_words = load_words_from_file(dictionary_file)
    text_words = load_words_from_file(text_file)
    print(text_words)

    matching_words = text_words.intersection(dictionary_words)

    if len(text_words) > 0:
        percentage = (len(matching_words) / len(text_words)) * 100
    else:
        percentage = 0

    return percentage

text_file_path = '../texts/Decameron/lemmas/DecameronLemmatized.txt'
dictionary_file_path = '../texts/Dictionary/dictionary.txt'
coverage_percentage = calculate_coverage(text_file_path, dictionary_file_path)
print(f"Percentage of words in the text that are in the dictionary: {coverage_percentage:.2f}%")