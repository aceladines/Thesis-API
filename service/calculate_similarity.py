import xxhash
from pyxorfilter import Xor16
import spacy
import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def lemmatize_text(input_text):
    if isinstance(input_text, str):
        sp = spacy.load('en_core_web_sm')
        all_stopwords = sp.Defaults.stop_words

        # Tokenize the input text
        text_tokens = word_tokenize(input_text)
        
        # Remove stopwords
        tokens_without_sw = [word for word in text_tokens if word.lower() not in all_stopwords]
        
        # Lemmatize the tokens
        lemmatized_text = sp(" ".join(tokens_without_sw))
        lemmatized_tokens = [word.lemma_ for word in lemmatized_text]
        
        # Remove non-alphanumeric tokens
        clean_tokens = [token for token in lemmatized_tokens if re.match(r'\b[a-zA-Z0-9]+\b', token)]
        
        return clean_tokens
        
    else:
        raise ValueError("Input must be a string")

def calculate_similarity_score(doc1: str, doc2: str) -> dict:

    # Lemmatized 2 inputs
    pattern = lemmatize_text(doc1.lower())
    text = " ".join(lemmatize_text(doc2.lower()))

    text_words = set(text.split(" "))

    xor = Xor16(len(set(pattern)))
    xor.populate(set(pattern))

    found_patterns = set()

    # Patterns that in the filter will remain, others will be removed
    cleaned_patterns = [text for text in text_words if xor.contains(text)]

    for x in cleaned_patterns:

        pattern_hash = xxhash.xxh3_128(x).hexdigest()

        for i in text_words:
            substring_hash = xxhash.xxh3_128(i).hexdigest()

            if pattern_hash == substring_hash:
                    found_patterns.add(x) 

    intersection = found_patterns
    union = set(pattern).union(text_words)

    jaccard_similarity = float(len(intersection)) / float(len(union))

    data = {
        "percentage": jaccard_similarity * 100,
        "classification": f"Overall similarity score: {jaccard_similarity * 100:.2f}%",
        "breakdown": {
            "intersection": list(intersection),
            "union": list(union),
        }
    }


    return data

