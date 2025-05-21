import numpy as np
import math

def exercise1(A):
    A = np.array(A)
    col_sums = [sum(abs(A[:,j])) for j in range(A.shape[1])]
    return max(col_sums)

def exercise2(B):
    B = np.array(B)
    row_sums = [sum(abs(row)) for row in B]
    return max(row_sums)

def exercise3(C):
    C = np.array(C)
    return math.sqrt(sum(sum(C * C)))

def exercise4(u, v):
    u = np.array(u)
    v = np.array(v)
    dot_product = np.dot(u, v)
    u_norm = np.sqrt(np.dot(u, u))
    v_norm = np.sqrt(np.dot(v, v))
    cos_theta = dot_product / (u_norm * v_norm)
    return np.arccos(cos_theta) * 180 / np.pi

def exercise5(u):
    u = np.array(u)
    norm = np.sqrt(np.dot(u, u))
    return u / norm

def exercise6(v1, s2, s3):
    v1 = np.array(v1)
    s2 = np.array(s2)
    s3 = np.array(s3)
    
    d12 = np.sqrt(np.sum((v1 - s2) ** 2))
    d13 = np.sqrt(np.sum((v1 - s3) ** 2))
    d23 = np.sqrt(np.sum((s2 - s3) ** 2))
    
    return d12, d13, d23

def exercise7(E, A):
    A_inv = np.linalg.inv(A)
    D = np.dot(A_inv, E)
    D = np.round(D).astype(int)
    
    lookup = {
        0: ' ', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I',
        10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R',
        19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'
    }
    
    message = ""
    for col in range(D.shape[1]):
        for row in range(D.shape[0]):
            if D[row, col] in lookup:
                message += lookup[D[row, col]]
    
    return message

def exercise8(message, A):
    lookup = {
        ' ': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18,
        'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26
    }
    
    message = message.upper()
    rows = A.shape[0]
    cols = math.ceil(len(message) / rows)
    D = np.zeros((rows, cols))
    
    idx = 0
    for col in range(cols):
        for row in range(rows):
            if idx < len(message):
                D[row, col] = lookup.get(message[idx], 0)
                idx += 1
    
    E = np.dot(A, D)
    return E

def exercise9(doc_term_matrix):
    doc_term_matrix = np.array(doc_term_matrix)
    num_docs = doc_term_matrix.shape[0]
    similarity_matrix = np.zeros((num_docs, num_docs))
    
    for i in range(num_docs):
        for j in range(num_docs):
            doc_i = doc_term_matrix[i]
            doc_j = doc_term_matrix[j]
            
            dot_product = np.dot(doc_i, doc_j)
            norm_i = np.sqrt(np.dot(doc_i, doc_i))
            norm_j = np.sqrt(np.dot(doc_j, doc_j))
            
            if norm_i > 0 and norm_j > 0:
                similarity_matrix[i, j] = dot_product / (norm_i * norm_j)
            else:
                similarity_matrix[i, j] = 0
    
    return similarity_matrix

def exercise10(docs, query):
    query = np.array(query)
    query_norm = np.sqrt(np.dot(query, query))
    
    if query_norm == 0:
        return []
    
    similarities = []
    for i, doc in enumerate(docs):
        doc = np.array(doc)
        doc_norm = np.sqrt(np.dot(doc, doc))
        
        if doc_norm > 0:
            similarity = np.dot(query, doc) / (query_norm * doc_norm)
            similarities.append((i+1, similarity))
        else:
            similarities.append((i+1, 0))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities