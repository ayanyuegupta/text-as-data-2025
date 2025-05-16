import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import json
import os
from tqdm import tqdm


def preprocess(d):
    
    docs = []
    for k in d:
        text = d[k]['content'].split('\n\n')
        for doc in text:
            #### remove new lines
            doc = doc.replace('\n', ' ').strip()
            if len(doc.split()) <= 5: continue
            docs.append(doc)

    return docs


def main():
    
    #### set up directory for saving our bertopic model
    model_dir = f'{os.getcwd()}/models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_name = 'gutenberg_bertopic'

    #### load gutenberg dictionary from last session
    data_dir = f'{os.getcwd()}/data'
    with open(f'{data_dir}/gutenberg_data.json', 'r') as f:
        d = json.load(f)
    
    #### split texts into docs
    docs = preprocess(d)
#    print(len(docs))

    #### embed docs
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = sentence_model.encode(docs, show_progress_bar=True)
    
    #### parameter tuning
    umap_model = UMAP(n_neighbors=15, n_components=10, metric='cosine')
    hdbscan_model = HDBSCAN(min_cluster_size=10)
    
    #### train model
    model = BERTopic(
            embedding_model=sentence_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            verbose=True
            ).fit(docs, embeddings)

    #### save model and topic info
    model.save(f'{model_dir}/{model_name}', serialization='pickle')
    topic_info = model.get_topic_info()
    topic_info.to_csv(f'{os.getcwd()}/{model_name}_info.csv', index=False)


if __name__ == '__main__':
    main()
