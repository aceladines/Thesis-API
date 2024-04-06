def search(pattern, text):
    windows = set()

    m = len(pattern)
    n = len(text)
    q = 256
    p = 0
    t = 0
    h = 1
    d = 193939

    for i in range(m-1):
        h = (h * d) % q

    # Calculate hash value for pattern and text
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Find the match and store the current window
    for i in range(n-m+1):
        windows.add(text[i:i+m])
        if p == t:
            for j in range(m):
                if text[i+j] != pattern[j]:
                    break
            else:  # No break occurred, pattern found
                return pattern, windows
        if i < n-m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i+m])) % q
            if t < 0:
                t = t + q

    return None, set()

def calculate_similarity_score(doc1: str, doc2: str) -> dict:
    patterns = doc1.split()
    windows = set()
    found_patterns = set()

    for pattern in patterns:
        found_pattern, found_windows = search(pattern, doc2)
        if found_pattern:
            found_patterns.add(found_pattern)
            windows.update(found_windows)

    intersection = found_patterns
    union = set(patterns).union(windows)

    jaccard_similarity = len(intersection) / len(union) if union else 0

    print(windows)

    data = {
        "percentage": jaccard_similarity * 100,
        "classification": f"Overall similarity score: {jaccard_similarity * 100:.2f}%",
        "breakdown": {
            "intersection": list(intersection),
            "union": list(union),
        }
    }

    return data
