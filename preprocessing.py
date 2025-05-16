import nltk
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import gutenberg, stopwords
from nltk.tokenize import word_tokenize
import json
import os
import re


def convert_to_dict():

    d = {}
    for file_id in gutenberg.fileids():
        d[file_id] = {}
        d[file_id]['title'] = file_id
        d[file_id]['content'] = gutenberg.raw(file_id)
        d[file_id]['word_count'] = len(gutenberg.words(file_id))

    return d


def preprocess_text(text):
    
    #### Preprocess text by applying several cleaning steps:
    #### 1. Convert to lowercase
    #### 2. Tokenize
    #### 3. Remove punctuation and numbers
    #### 4. Remove stop words
   
    #### convert to lowercase
    text = text.lower()
    
    #### tokenize
    #### first, let's see what basic split() does
    basic_tokens = text.split()
    
    #### now, let's use NLTK's word_tokenize
    tokens = word_tokenize(text)
    
    #### remove punctuation and numbers
    #### we'll use a regular expression to keep only alphabetic characters
    cleaned = []
    for token in tokens:
       cleaned.append(re.sub(r'[^a-z]', '', token))
    tokens = cleaned
    
    #### remove empty strings that might result from the previous step
    cleaned = []
    for token in tokens:
        if token:
            cleaned.append(token)
    tokens = cleaned
    
    #### remove stop words
    stop_words = set(stopwords.words('english'))
    cleaned = []
    for token in tokens:
        if token not in stop_words:
            cleaned.append(token)
    
    return tokens


def main():


    #### 6. EXAMINING THE DATA
    print(gutenberg.fileids())
    for file_id in gutenberg.fileids():
        print('####')
        print(gutenberg.raw(file_id)[:100])
    

    #### 7. LISTS AND DICTIONARIES
    d = convert_to_dict()
    print(d['austen-emma.txt']['content'][:50])


    #### 8. SAVING AND LOADING WITH JSON
    save_dir = f'{os.getcwd()}/data'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    #### save d as JSON file in save_dir
    with open(f'{save_dir}/gutenberg_data.json', 'w') as f:
        json.dump(d, f)
    #### load d from JSON file we just created
    with open(f'{save_dir}/gutenberg_data.json', 'r') as f:
        d = json.load(f)
    

    #### 9. PREPROCESSING TEXT
    text_id = 'shakespeare-macbeth.txt'  
    text_content = d[text_id]['content'] 
    #### preprocess with our function
    tokens = preprocess_text(text_content)


if __name__ == '__main__':
    main()
