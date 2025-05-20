#from tqdm import tqdm
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from gensim.models import Word2Vec
import gensim
import json
import os


def preprocess(d, separators=['\n\n', '. ', '.--'], titles=['mr', 'mrs', 'ms', 'dr']):
    
    #### split into sentences
    sentences = []
    for k in d:
        text = d[k]['content']
#        #### examine the text
#        print(repr(text))
#        quit()

        #### lower case
        text = text.lower()

        #### split into sentences
        for sep in separators:
            text = text.replace(sep, '<SEP>')
        
        #### handle titles
        for title in titles:
            text = text.replace(f'{title}<SEP>', f'{title} ')
        
        #### split into sentences
        sentences += text.split('<SEP>')
    
    ####clean sentences
    processed = []
#    sentences = sentences[:10]
    token_count = 0
    for s in sentences:
        #### remove new lines
        s = s.replace('\n', ' ')
        
        #### tokenize
        tokens = word_tokenize(s)
#        print(tokens)
#        quit()

        #### remove non alphabetic characters
        #### remove stop words
        stop_words = set(stopwords.words('english'))
#        print(stop_words)
#        quit()
        cleaned = []
        for t in tokens:
            t = re.sub(r'[^a-z]', '', t)
#            if t in stop_words: continue
            cleaned.append(t) 
        token_count += len(cleaned)
        processed.append(cleaned)
    
    print(f'Total number of tokens: {token_count}')

    return processed


def main():
    
    #### set up directory for saving our word2vec model
    model_dir = f'{os.getcwd()}/models'
    if not os.path.exists(model_dir): 
        os.makedirs(model_dir)
    model_name = 'gutenberg_w2v.model'

    #### load gutenberg dictionary from last session
    data_dir = f'{os.getcwd()}/data'
    with open(f'{data_dir}/gutenberg_data.json', 'r') as f:
        d = json.load(f)
 
    #### if we have already trained a model, we just load it instead of preprocessing
    #### and training repeatedly.
    if not os.path.exists(f'{model_dir}/{model_name}'):
        #### preprocess data
        sentences = preprocess(d)
#        print(len(sentences))

        #### initialise and train w2v model
        model = Word2Vec(sentences=sentences, vector_size=300, workers=4) 
        model.train(sentences, total_examples=model.corpus_count, epochs=3)
        
        #### save model
        model.save(f'{model_dir}/{model_name}')
    else:
        model = Word2Vec.load(f'{model_dir}/{model_name}')


    #### explore similar words
    words = ['marriage', 'family', 'man', 'woman', 'love', 'king', 'queen']
    for w in words:
        print('\n####')
        print(w)
        print(model.wv.most_similar(w, topn=10))


if __name__ == '__main__':
    main()
