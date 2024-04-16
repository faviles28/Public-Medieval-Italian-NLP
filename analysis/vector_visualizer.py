from gensim.models.doc2vec import Doc2Vec
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def tokenize_text(text):
    return text.split()

def load_model():
    loaded_model = Doc2Vec.load("decameron_doc2vec.model")
    return loaded_model

def get_paragraph_vector(model, paragraph):
    tokens = tokenize_text(paragraph)
    return model.infer_vector(tokens)

def read_txt_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def plot_texts(model, filenames):
    vectors = np.array([get_paragraph_vector(model, read_txt_file(filename)) for filename in filenames])
    
    perplexity_value = 5
    learning_rate_value = 2000 
    n_iter_value = 10000

    tsne = TSNE(n_components=2, random_state=0, 
                perplexity=perplexity_value, 
                learning_rate=learning_rate_value, 
                n_iter=n_iter_value)

    vectors_2d = tsne.fit_transform(vectors)

    plt.figure(figsize=(12, 8))
    for i, label in enumerate(filenames):
        x, y = vectors_2d[i]
        plt.scatter(x, y)
        plt.annotate(label.split('/')[-1], (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    plt.title('2D Visualization of Day Similarities')
    plt.grid(True)
    plt.show()

def main():
    model = load_model()
    decameron_files = [f'../texts/Decameron/lemmas/Decameron{roman}.txt' for roman in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']]
    plot_texts(model, decameron_files)

if __name__ == '__main__':
    main()
