import faiss
import numpy as np

# Create 100 random 128-dimensional vectors. a 100×128 NumPy array of float32 values, randomly generated. (100 rows)
d = 128
vectors = np.random.random((100, d)).astype('float32')

# Adds the 100 vectors to the FAISS index.
index = faiss.IndexFlatL2(d)
index.add(vectors)

# Search for nearest neighbors of a random query vector
query = np.random.random((1, d)).astype('float32')
distances, indices = index.search(query, k=5)

print("Closest matches:", indices)
