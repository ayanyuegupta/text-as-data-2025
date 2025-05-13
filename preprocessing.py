import nltk
nltk.download('movie_reviews')
from nltk.corpus import movie_reviews


def convert_to_dict():

    sentiment = ['pos', 'neg']
    d = {}
    for s in sentiment:
        file_ids = movie_reviews.fileids(s)
        for i, file_id in enumerate(file_ids):
            d[f'{s}_{i}'] = {}
            d[f'{s}_{i}']['content'] = ' '.join(movie_reviews.words(file_id))
            d[f'{s}_{i}']['sentiment'] = s
    
    return d


def main():
    
#    print(movie_reviews.fileids('pos'))
#    print(movie_reviews.fileids('neg'))
#    file_ids = movie_reviews.fileids('pos') + movie_reviews.fileids('neg')
#    for file_id in file_ids:
#        print(movie_reviews.words(file_id)) 
    d = convert_to_dict()
    print(d['neg_0'])


if __name__ == '__main__':
    main()