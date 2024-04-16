from gensim import corpora, models

def read_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        documents = [line.strip().split() for line in file.readlines()]
    return documents

def create_lda_model(documents, num_topics=5, no_below=15, no_above=0.5):
    dictionary = corpora.Dictionary(documents)
    
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)

    corpus = [dictionary.doc2bow(document) for document in documents]
    
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lda_model = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, passes=15)
    
    return lda_model, dictionary

def print_top_words(lda_model, dictionary, num_words=10):
    for idx, topic in lda_model.print_topics(-1, num_words):
        print(f"Topic: {idx}\nWords: {topic}")

if __name__ == "__main__":
    file_path = '../texts/Decameron/lemmas/DecameronLemmatized.txt'
    
    # Read the corpus
    documents = read_corpus(file_path)
    
    # Create and train the LDA model
    lda_model, dictionary = create_lda_model(documents, num_topics=8, no_below=15, no_above=0.5)
    
    # Print the top words in each topic
    print_top_words(lda_model, dictionary)
