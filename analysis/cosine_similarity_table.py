import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec

def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def calculate_cosine_similarity(model, word_list1, word_list2):
    similarities = []
    for word1 in word_list1:
        if word1 in model.wv:
            for word2 in word_list2:
                if word2 in model.wv:
                    sim = cosine_similarity(model.wv[word1].reshape(1, -1), model.wv[word2].reshape(1, -1))[0][0]
                    similarities.append((word1, word2, sim))
    return similarities

def main(file1, file2, topic1, topic2, model_file):
    model = Word2Vec.load(model_file)
    words_file1 = read_words_from_file(file1)
    words_file2 = read_words_from_file(file2)

    similarities = calculate_cosine_similarity(model, words_file1, words_file2)

    df = pd.DataFrame(similarities, columns=['First Word', 'Second Word', 'Similarity'])

    df['Similarity'] = df['Similarity'].round(3)

    average_similarity = df['Similarity'].mean()
    print(f'Average Similarity: {average_similarity}')

    df.to_csv(f'../texts/Divine Comedy/analysis/cosine-similarities/{topic1}-{topic2}-word_similarities.csv', index=False)

if __name__ == '__main__':
    topic1 = 'love&sexuality'
    # death, god, love&sexuality, punishment, sin, thebody, the self, politics&society
    topic2 = 'love'
    file1 = f'../texts/Divine Comedy/themes/manual/{topic1}.txt'
    file2 = f'../texts/Divine Comedy/themes/manual/{topic1}.txt'
    model_file = 'divine_comedy_final_word2vec.model'
    main(file1, file2, topic1, topic1, model_file)
