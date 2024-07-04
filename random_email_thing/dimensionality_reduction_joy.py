import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors

# Load pre-trained word vectors
word_vectors = KeyedVectors.load_word2vec_format('path_to_your_vectors.bin', binary=True)

# Define emotion words
emotion_words = ['joy', 'love', 'happiness']

# Function to get k nearest neighbors
def get_nearest_neighbors(word, k=10):
    if word not in word_vectors:
        print(f"'{word}' not found in the vocabulary.")
        return []
    
    neighbors = word_vectors.most_similar(word, topn=k)
    return [word for word, _ in neighbors]

# Get nearest neighbors for each emotion word
k = 20  # Number of neighbors for each emotion word
emotion_neighbors = []
for word in emotion_words:
    emotion_neighbors.extend(get_nearest_neighbors(word, k))

# Remove duplicates and add original emotion words
emotion_neighbors = list(set(emotion_neighbors + emotion_words))

# Get vectors for these words
vectors = np.array([word_vectors[word] for word in emotion_neighbors])

# Perform k-means clustering
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(vectors)

# Dimensionality reduction
def plot_reduction(reduction, title):
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(reduction[:, 0], reduction[:, 1], c=cluster_labels, cmap='viridis')
    for i, word in enumerate(emotion_neighbors):
        plt.annotate(word, (reduction[i, 0], reduction[i, 1]))
    plt.colorbar(scatter)
    plt.title(title)
    plt.show()

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(vectors)
plot_reduction(pca_result, 'PCA of Emotion-Related Words')

# t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=5)
tsne_result = tsne.fit_transform(vectors)
plot_reduction(tsne_result, 't-SNE of Emotion-Related Words')

# Print words in each cluster
for i in range(n_clusters):
    cluster_words = [word for word, label in zip(emotion_neighbors, cluster_labels) if label == i]
    print(f"Cluster {i}: {', '.join(cluster_words)}")