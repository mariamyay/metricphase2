# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:44:59 2024

@author: Mariam
"""

import faiss
import numpy as np

class VectorDB:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

    def add_vector(self, vector):
        self.index.add(np.array(vector).reshape(1, -1))

    def search(self, query_vector, k=5):
        distances, indices = self.index.search(np.array(query_vector).reshape(1, -1), k)
        return distances, indices
    
vector_db = VectorDB(200)