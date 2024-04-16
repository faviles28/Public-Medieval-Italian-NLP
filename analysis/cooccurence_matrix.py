from collections import defaultdict
import pandas as pd

def read_file(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        return file.readlines()

def build_cooccurrence_matrix(lines):
    cooccurrence = defaultdict(int)

    for line in lines:
        words = line.strip().split()
        word_len = len(words)
        
        # Consider all pairs of words in the same line
        for i in range(word_len):
            for j in range(i + 1, word_len):
                pair = tuple(sorted([words[i], words[j]]))
                cooccurrence[pair] += 1

    return cooccurrence

def main(input_filename):
    lines = read_file(input_filename)
    matrix = build_cooccurrence_matrix(lines)
    
    # Convert the defaultdict to a DataFrame for better visualization
    df = pd.DataFrame(list(matrix.items()), columns=['Word Pair', 'Count'])
    
    print(df.head())

    # Print the top 100 most common co-occurring pairs
    print(df.nlargest(30, 'Count'))

    output_filename = "../texts/Decameron/analysis/cooccurrence_matrix_X.csv" 
    df.to_csv(output_filename, index=False)

if __name__ == '__main__':
    input_file = '../texts/Decameron/lemmas/DecameronX.txt'
    main(input_file)