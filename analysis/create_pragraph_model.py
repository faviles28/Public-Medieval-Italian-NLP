from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def tokenize_text(text):
    return text.split()

def train_doc2vec_model(input_filename, vector_size=300, epochs=30):
    with open(input_filename, "r", encoding="UTF-8") as file:
        paragraphs = [line.strip() for line in file if line.strip()]

    tagged_documents = [TaggedDocument(tokenize_text(para), [str(i)]) for i, para in enumerate(paragraphs)]

    model = Doc2Vec(vector_size=vector_size, min_count=2, epochs=epochs)
    model.build_vocab(tagged_documents)
    model.train(tagged_documents, total_examples=model.corpus_count, epochs=model.epochs)

    model.save("decameron_doc2vec.model")
    return model

def get_paragraph_vector(model, paragraph):
    tokens = tokenize_text(paragraph)
    return model.infer_vector(tokens)

def load_model():
    loaded_model = Doc2Vec.load("decameron_doc2vec.model")
    return loaded_model

def read_txt_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def calculate_cosine_similarity(model, paragraphs):
    similarity_matrix = np.zeros((len(paragraphs), len(paragraphs)))
    for i, para1 in enumerate(paragraphs):
        for j, para2 in enumerate(paragraphs):
            vector1 = get_paragraph_vector(model, para1)
            vector2 = get_paragraph_vector(model, para2)
            similarity_matrix[i, j] = cosine_similarity([vector1], [vector2])[0][0]
    return similarity_matrix

def main(input_filename):
    # model = train_doc2vec_model(input_filename)
    model = load_model()

    decameron_files = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    paragraphs = [read_txt_file(f'../texts/Decameron/lemmas/Decameron{roman}.txt') for roman in decameron_files]

    similarity_matrix = calculate_cosine_similarity(model, paragraphs)
    print(similarity_matrix)

if __name__ == '__main__':
    input_file = "../texts/Decameron/lemmas/DecameronLemmatized.txt"
    main(input_file)
