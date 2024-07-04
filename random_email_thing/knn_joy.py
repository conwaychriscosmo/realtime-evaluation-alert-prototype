import numpy as np
from sklearn.neighbors import NearestNeighbors
from gensim.models import KeyedVectors

# Load pre-trained word vectors (replace with your own method if different)
word_vectors = KeyedVectors.load_word2vec_format('path_to_your_vectors.bin', binary=True)

# Convert the word vectors to a numpy array and create a word list
words = []
vectors = []
for word, vector in word_vectors.items():
    words.append(word)
    vectors.append(vector)

vectors = np.array(vectors)

# Initialize the NearestNeighbors model
k = 10  # Number of neighbors to find
nn = NearestNeighbors(n_neighbors=k+1, metric='cosine')  # +1 because the word itself will be included
nn.fit(vectors)

# Get the vector for "joy"
joy_vector = word_vectors['joy']

# Find the k+1 nearest neighbors
distances, indices = nn.kneighbors([joy_vector])

# Print the k nearest neighbors (excluding "joy" itself)
print(f"The {k} nearest neighbors of 'joy' are:")
for i in range(1, k+1):  # Start from 1 to skip "joy" itself
    word = words[indices[0][i]]
    distance = distances[0][i]
    print(f"{i}. {word} (cosine distance: {distance:.4f})")

# Function to find nearest neighbors for any word
def get_nearest_neighbors(word, k=10):
    if word not in word_vectors:
        print(f"'{word}' not found in the vocabulary.")
        return
    
    word_vector = word_vectors[word]
    distances, indices = nn.kneighbors([word_vector])
    
    print(f"The {k} nearest neighbors of '{word}' are:")
    for i in range(1, k+1):  # Start from 1 to skip the word itself
        neighbor = words[indices[0][i]]
        distance = distances[0][i]
        print(f"{i}. {neighbor} (cosine distance: {distance:.4f})")

# Example usage of the function
get_nearest_neighbors('happiness', k=15)