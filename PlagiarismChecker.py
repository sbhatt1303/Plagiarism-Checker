from operator import itemgetter
import numpy as np
import random as rnd

len_buckets = 107
hash_table = [[] for i in xrange(len_buckets)]

def construct_shingles(doc,k):
    #converting the text to lower case
    doc = doc.lower()
    #making the shingles dictionary
    shingles = {}
    for i in xrange(len(doc)):
        substring = ''.join(doc[i:i+k])
        if len(substring) == k and substring not in shingles:
            shingles[substring] = 1

    return doc,shingles.keys()


#Pick a value of k and construct from each document the set of k-shingles
def make_shingles(docs,k):
    shingles = []
    for i in xrange(len(docs)):
        doc = docs[i]
        doc,sh = construct_shingles(doc,k)
        docs[i] = doc
        shingles.append(sh)
    return docs,shingles


def initialize_matrix(docs,shingles):
    # print(shingles)
    index = 0
    rows = {}
    for sh in shingles:
        for s in sh:
            if s not in rows:
                rows[s] = index
                index += 1

    return np.zeros((len(rows), len(docs))), rows

#Sorting the document-shingle pairs to order them by shingle.
def make_matrix(docs,shingles):
    matrix,rows = initialize_matrix(docs,shingles)

    #print rows
    #print matrix
    
    for col in xrange(len(docs)):
        for row in rows:
            if row in docs[col]:
                matrix[rows[row],col] = 1
    #print(matrix)
    return matrix

def get_hash(x,var,cons,n):
    return (var * x + cons) % n

def generate_hash_functions(n):
    hash_funcs = []
    for i in xrange(n):
        var = rnd.randint(0,1000)
        cons = rnd.randint(0,1000)
        hash_funcs.append([var,cons])
    return hash_funcs

def make_signature_matrix(matrix,n):
    #generating linear hash functions using random numbers
    hash_funcs = generate_hash_functions(n)
    # print(hash_funcs)
    hash_value = []
    for cur in hash_funcs:
        val = [get_hash(i,cur[0],cur[1],matrix.shape[0]) for i in xrange(matrix.shape[0])]
        hash_value.append(val)
    # print hash_value
    
    # making the signature matrix
    sign = np.zeros((n,matrix.shape[1])) + float('inf')

    for c in xrange(matrix.shape[1]):
        for r in xrange(matrix.shape[0]):
            if matrix[r,c] == 1:
                for i in xrange(n):
                    hf = hash_value[i]
                    sign[i,c] = min(sign[i,c],hf[r])
    return sign

def initialize_array_bucket(bands):
    global len_buckets
    array_buckets = []
    for band in xrange(bands):
        array_buckets.append([[] for i in xrange(len_buckets)])
    return array_buckets
    
def hash(substr):
    global lenBuckets
    return sum([ord(c) for c in substr]) % len_buckets

def euclidean_distance(x,y):
    return sum(((x[i] - y[i]) ** 2) for i in xrange(len(x))) ** (1.0/2.0)

def cosine_distance(x,y):
    productAB = sum([x[i]*y[i] for i in xrange(len(x))])
    zeros = [0 for i in xrange(len(x))]
    A = euclidean_distance(x,zeros)
    B = euclidean_distance(y,zeros)
    return productAB / (A * B)

#Picking a number of bands b and a number of rows r such that b*r = n,
#and the threshold t is approximately (1/b)^1/r

def LSH(SIG,t,bands,rows):

    array_buckets = initialize_array_bucket(bands)
    # print(array_buckets)

    hash_funcs = generate_hash_functions(bands)
    # print(hash_funcs)

    candidates = {}
    
    i = 0
    for b in xrange(bands):
        buckets = array_buckets[b]        
        band = SIG[i:i+rows,:]
        # print(band)
        for col in xrange(band.shape[1]):
            key = int(sum(band[:,col]) % len(buckets))
            buckets[key].append(col)
        
        i = i+rows

        for item in buckets:
            if len(item) > 1:
                pair = (item[0], item[1])
                if pair not in candidates:
                    A = SIG[:,item[0]]
                    B = SIG[:,item[1]]
                    similarity = cosine_distance(A,B)
                    if similarity >= t:
                        candidates[pair] = similarity

    sort = sorted(candidates.items(),key=itemgetter(1), reverse=True)
    return candidates,sort

#number of shingles   
k = 6

#reading file input
f = open("int1.txt")
g = open("int2.txt")
w = open("out1.txt","a+")
d0 = f.read()
d1 = g.read()

docs = [d0,d1]
newDocs,shingles = make_shingles(docs[:],k)

#making the boolean matrix
matrix = make_matrix(newDocs,shingles)

#making the signature matrix
sign = make_signature_matrix(matrix,1000)

candidates,sort = LSH(sign,0.85,100,10)

length = len(sort)
    
for i in xrange(length):
    pair = sort[i][0]
    val = sort[i][1]*100;
    w.write("%f\n"%val)