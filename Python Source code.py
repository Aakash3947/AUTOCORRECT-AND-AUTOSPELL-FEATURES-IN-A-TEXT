import re
from collections import Counter


# Function to preprocess a word
def preprocess_word(word):
    # Normalize case and remove non-alphanumeric characters
    word = word.lower()
    word = re.sub(r'\W+', '', word)
    return word


# Function to generate N-grams from a word
def generate_ngrams(word, n):
    return [word[i:i + n] for i in range(len(word) - n + 1)]


# Function to create an ASCII list from a word
def createList(word):
    return [ord(char) for char in word]


# Levenshtein Distance Calculation (Edit Distance)
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# Function to process the search term with N-gram and Levenshtein Distance
def process_search_with_ngrams(searchTerm, database, n=2, threshold_min=4, max_suggestions=1):
    # Preprocess the search term
    searchTerm = preprocess_word(searchTerm)
    search_ngrams = generate_ngrams(searchTerm, n)  # Generate N-grams for search term

    # Preprocess the database words and create ASCII lists
    processed_database = [preprocess_word(word) for word in database]
    lstAscii = [createList(word) for word in processed_database]

    candidate_indices = []

    # Step 2: Iterate through each string in the database
    for i in range(len(processed_database)):
        word = processed_database[i]
        word_ngrams = generate_ngrams(word, n)  # Generate N-grams for each word in the database

        # Compare the overlap in N-grams between the search term and the database word
        common_ngrams = set(search_ngrams) & set(word_ngrams)

        # If there are significant common N-grams, proceed with length difference check
        if len(common_ngrams) > 0:
            diff = abs(len(lstAscii[i]) - len(createList(searchTerm)))
            if diff < threshold_min:
                candidate_indices.append(i)

    # Calculate Levenshtein Distance and store results
    distances = []
    for i in candidate_indices:
        current_word = processed_database[i]
        cost = levenshtein_distance(current_word, searchTerm)
        distances.append((current_word, cost))

    # Sort by distance and select top max_suggestions
    distances.sort(key=lambda x: x[1])
    suggestions = [word for word, dist in distances[:max_suggestions]]

    return suggestions


# Expanded dictionary of valid words (database)
database = ["sample","hello", "world", "whatsapp", "feature", "suggestion", "test", "typing",
            "application", "weather", "system", "functionality", "development", "python",
            "programming", "code", "example", "reference", "suggestions"]

# List of input words with their corresponding number of suggestions
input_words = [("helllo", 1), ("examle", 2), ("functonality", 3)]

# Process each input word and get suggestions
for word, num_suggestions in input_words:
    suggestions = process_search_with_ngrams(word, database, max_suggestions=num_suggestions)
    print(f'Suggestions for "{word}": {", ".join(suggestions)}')