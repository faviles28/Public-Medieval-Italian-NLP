def read_lemmatized_file(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        return file.readlines()

def get_token_statistics_and_unique_tokens(lines):
    all_tokens = []
    for line in lines:
        tokens = line.strip().split()
        all_tokens.extend(tokens)

    total_tokens = len(all_tokens)
    token_counts = {}
    for token in all_tokens:
        if token in token_counts:
            token_counts[token] += 1
        else:
            token_counts[token] = 1

    unique_tokens_set = set(all_tokens)
    unique_tokens = len(unique_tokens_set)
    ratio = unique_tokens / total_tokens

    average_appearances = sum(token_counts.values()) / unique_tokens

    return total_tokens, unique_tokens, ratio, unique_tokens_set, average_appearances

def write_unique_tokens_to_file(unique_tokens_set, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for token in unique_tokens_set:
            file.write(token + '\n')

def main(input_filename, output_filename):
    lemmatized_text = read_lemmatized_file(input_filename)
    total_tokens, unique_tokens, ratio, unique_tokens_set, average_appearances = get_token_statistics_and_unique_tokens(lemmatized_text)

    print(f"Total number of tokens: {total_tokens}")
    print(f"Number of unique tokens: {unique_tokens}")
    print(f"Ratio of unique tokens to total tokens: {ratio:.4f}")
    print(f"Average number of appearances for each unique token: {average_appearances:.4f}")

    write_unique_tokens_to_file(unique_tokens_set, output_filename)

if __name__ == '__main__':
    input_file = '../texts/Decameron/raw/CleanedDecameron.txt'
    output_file = '../texts/Decameron/analysis/uniqueTokensOG.txt'
    main(input_file, output_file)