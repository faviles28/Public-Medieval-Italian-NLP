from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import nltk
import spacy

def train_model(filename, vector_size=200, window=15, min_count=5, epochs=25):
    nlp = spacy.load('it_core_news_lg')

    def tokenize_text(text):
        doc = nlp(text)
        return [token.text for token in doc]

    sentences = []
    with open(filename, "r", encoding="UTF-8") as file:
        for line in file:
            if line.strip():
                sentences.append(tokenize_text(line))

    print(sentences)
    model = Word2Vec(sentences=sentences, vector_size=vector_size, window=window, min_count=min_count, workers=4)
    model.train(sentences, total_examples=len(sentences), epochs=epochs)

    model.save("decameron_final_word2vec.model")

def load_model():
    loaded_model = Word2Vec.load("decameron_final_word2vec.model")
    return loaded_model

def get_word_vector(model, word):
    if word in model.wv:
        return model.wv[word]
    else:
        return None

def main(input_filename):
    model = train_model(input_filename)
    model = load_model()

    word1 = "essere"
    word2 = "fare"

    word_vector1 = model.wv[word1]
    word_vector2 = model.wv[word2]

    word_vector1_reshaped = word_vector1.reshape(1, -1)
    word_vector2_reshaped = word_vector2.reshape(1, -1)

    print(cosine_similarity(word_vector1_reshaped, word_vector2_reshaped))


if __name__ == '__main__':
    input_file = '../texts/Decameron/lemmas/DecameronLemmatized.txt'
    main(input_file)