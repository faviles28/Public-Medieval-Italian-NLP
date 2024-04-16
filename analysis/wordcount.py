def count_words(text_file, word_list_file, output_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()

    words_in_text = text.split()

    word_counts = {}

    # Read each word from the second file and count occurrences
    with open(word_list_file, 'r', encoding='utf-8') as file:
        for word in file:
            word = word.strip()
            count = words_in_text.count(word)
            word_counts[word] = count

    # Sort the dictionary by count in descending order
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        for word, count in sorted_word_counts:
            file.write(f"{word} - {count}\n")

def filter_words(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            word, count = line.split(' - ')
            if int(count) >= 10:
                outfile.write(word + '\n')

text_file = '../texts/Decameron/lemmas/DecameronLemmatized.txt'
word_list_file = '../texts/Decameron/analysis/uniqueTokens.txt'
output_file = '../texts/Decameron/analysis/wordCounts.txt'
final_file = '../texts/Decameron/analysis/filteredWords.txt'

count_words(text_file, word_list_file, output_file)
filter_words(output_file, final_file)

