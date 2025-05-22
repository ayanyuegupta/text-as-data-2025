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


#### define functions here
def preprocess(d, separators=['\n\n', '. ', '.--'], titles=['mr', 'mrs', 'ms', 'dr']):
    
    #### split into sentences
    sentences = []
    for k in d:
        text = d[k]['content']
        #### examine the text
#        print(repr(text))
#        quit()
        text = text.lower()
        for sep in separators:
            text = text.replace(sep, '<SEP>')
        
        #### handle titles
        for title in titles:
            text = text.replace(f'{title}<SEP>', f'{title} ')
        #### split into sentences
        sentences += text.split('<SEP>')
    

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
#        stop_words = set(stopwords.words('english'))
#        print(stop_words)
#        quit()
        cleaned = []
        for t in tokens:
            t = re.sub(r'[^a-z]', '', t)
#            if t in stop_words: continue
            if len(t) == 0: continue
            cleaned.append(t) 
        token_count += len(cleaned)
        processed.append(cleaned)
    
    return processed


#### call functions here
def main():
 
    data_dir = f'{os.getcwd()}/data'
    with open(f'{data_dir}/gutenberg_data.json', 'r') as f:
        d = json.load(f)
    
    #### call preprocessing function here
    sentences = preprocess(d)

    #### initialise and train w2v model
    model = Word2Vec(sentences=sentences, vector_size=300, workers=4) 
    model.train(sentences, total_examples=model.corpus_count, epochs=3)

    ####explore similar words
    words = ['marriage', 'husband', 'wife', 'child']
    for w in words:
        print('\n####')
        print(w)
        print(model.wv.most_similar(w, topn=10))


if __name__ == '__main__':
    main()


