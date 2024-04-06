import spacy
import nltk
from nltk.tokenize import word_tokenize
import re


nltk.download('punkt')
nltk.download('stopwords')

def remove_stopwords(input_text):
    if isinstance(input_text, str):
        sp = spacy.load('en_core_web_sm')
        all_stopwords = sp.Defaults.stop_words

        # Tokenize the input text
        text_tokens = word_tokenize(input_text)
        
        # Remove stopwords
        tokens_without_sw = [word for word in text_tokens if word.lower() not in all_stopwords]

        return tokens_without_sw

    else:
        raise ValueError("Input must be a string")

def calculate_similarity_score(doc1: str, doc2: str) -> dict:
    # Remove non-alphanumeric characters and split by spaces
    patterns = set(doc1.split())
    # patterns = set(re.sub(r'[^A-Za-z0-9\s]+', '', doc1).split())
    # patterns = set(re.sub(r'[^A-Za-z0-9\s]+', '', " ".join(remove_stopwords(doc1))).split())


    # Remove elements with length <= 2
    # patterns = [item for item in patterns if len(item) > 2]

    text = doc2
    # text = re.sub(r'[^A-Za-z0-9\s]+', '', doc2)
    # text = re.sub(r'[^A-Za-z0-9\s]+', '', " ".join(remove_stopwords(doc2)))

    text_words = set(text.split())

    n = len(text)

    found_patterns = set()

    for pattern in patterns:
        d = 256
        p = 0
        t = 0
        h = 1
        q = 193939
        i = 0
        j = 0
         
        m = len(pattern)

        for i in range(m-1):      
            h = (h*d) % q

        # Calculate hash value for pattern and text
        for i in range(m):
            p = (d*p + ord(pattern[i])) % q
            t = (d*t + ord(text[i])) % q

        # Find the match
        for i in range(n-m+1):
            if p == t:
                for j in range(m):
                    if text[i+j] != pattern[j]:
                        break

                j += 1
                if j == m:
                    found_patterns.add(pattern)                    
                    

            if i < n-m:
                t = (d*(t-ord(text[i])*h) + ord(text[i+m])) % q

                if t < 0:
                    t = t+q


    found_patterns.intersection_update(text_words)
    intersection = found_patterns

    union = set(patterns).union(set(text_words))

    jaccard_similarity = float(len(intersection)) / float(len(union))
        
    data = {
        "percentage": (jaccard_similarity * 100),
        "classification": f"Overall similarity score: {jaccard_similarity * 100:.2f}%",
        "breakdown": {
            "intersection": list(intersection),
            "union": list(union),
        }
    }

    return data
