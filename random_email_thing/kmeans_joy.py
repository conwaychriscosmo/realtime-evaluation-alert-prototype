import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA

# Load pre-trained word vectors (replace with your own method if different)
word_vectors = KeyedVectors.load_word2vec_format('path_to_your_vectors.bin', binary=True)

# Define the emotion words and get their vectors
emotion_words = ['joy', 'love', 'happiness']
emotion_vectors = np.array([word_vectors[word] for word in emotion_words])

# Get a subset of words for clustering (e.g., top 1000 most common words)
common_words = list(word_vectors.key_to_index.keys())[:1000]
word_vectors_array = np.array([word_vectors[word] for word in common_words])

# Perform k-means clustering
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(word_vectors_array)

# Find the closest cluster center to each emotion word
emotion_cluster_labels = kmeans.predict(emotion_vectors)

# Get the words closest to each emotion centroid
def get_closest_words(centroid, words, vectors, top_n=10):
    similarities = cosine_similarity([centroid], vectors)[0]
    sorted_indices = np.argsort(similarities)[::-1]
    return [words[i] for i in sorted_indices[:top_n]]

for emotion, label in zip(emotion_words, emotion_cluster_labels):
    centroid = kmeans.cluster_centers_[label]
    closest_words = get_closest_words(centroid, common_words, word_vectors_array)
    print(f"Words closest to {emotion} cluster:")
    print(", ".join(closest_words))
    print()

# Visualize the clusters (using PCA for dimensionality reduction)
pca = PCA(n_components=2)
reduced_vectors = pca.fit_transform(word_vectors_array)
reduced_centroids = pca.transform(kmeans.cluster_centers_)
reduced_emotions = pca.transform(emotion_vectors)

plt.figure(figsize=(12, 8))
scatter = plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], c=cluster_labels, alpha=0.6, cmap='viridis')
plt.scatter(reduced_centroids[:, 0], reduced_centroids[:, 1], c='red', s=200, alpha=0.8, marker='X')
for emotion, coord in zip(emotion_words, reduced_emotions):
    plt.annotate(emotion, coord, fontsize=12, fontweight='bold')
plt.colorbar(scatter)
plt.title('Word Clusters with Emotion Centroids')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()