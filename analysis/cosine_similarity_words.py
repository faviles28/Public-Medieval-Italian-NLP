import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec

def read_words_and_frequencies_from_file(file_path):
    words_and_freqs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) == 2 and parts[1].isdigit():
                word, freq = parts[0], int(parts[1])
                if freq >= 5:
                    words_and_freqs.append(word)
    return words_and_freqs

def calculate_similarity_with_input_word(model, input_word, word_list):
    similarities = []
    if input_word in model.wv:
        for word in word_list:
            if word in model.wv:
                sim = cosine_similarity(model.wv[input_word].reshape(1, -1), model.wv[word].reshape(1, -1))[0][0]
                similarities.append((input_word, word, sim))
    return similarities

def similarity_analysis(input_word, file_path, model_file):
    model = Word2Vec.load(model_file)
    words_list = read_words_and_frequencies_from_file(file_path)

    similarities = calculate_similarity_with_input_word(model, input_word, words_list)

    # Sort the similarities and select the top 20
    top_20_similarities = sorted(similarities, key=lambda x: x[2], reverse=True)[:20]

    # Print the top 20 most similar words
    print(f'Top 20 words most similar to "{input_word}":')
    for i, (input_word, compared_word, similarity) in enumerate(top_20_similarities, start=1):
        print(f'{i}. {compared_word} - Similarity: {similarity:.3f}')

# Example usage
if __name__ == '__main__':
    input_word = 'diritta via essere smarrito'
    file_path = '../texts/Divine Comedy/analysis/wordCounts.txt'
    model_file = 'divine_comedy_final_word2vec.model'
    similarity_analysis(input_word, file_path, model_file)
