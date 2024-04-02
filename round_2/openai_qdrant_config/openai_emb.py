# import openai
# import pandas as pd
# import numpy as np
# from qdrant_client import QdrantClient


# class QdrantDatabase:
#     def __init__(self, path=r"C:\Users\BALAJI\Documents\openai_embeddings\files\Final_data\qdrant_database"):
#         self.client = QdrantClient(path=path)

#     def insert_vectors(self, vectors):
#         points = [{"id": vector["id"], "vector": vector["vector"]} for vector in vectors]
#         self.client.upsert(collection_name="resume_details", points=points)

#     def search_vectors(self, query_vector, top_k=10):
#         result = self.client.search(collection_name="resume_details", payload={"vector": query_vector, "top": top_k})
#         return result['hits']


# def get_embedding(text, model="text-embedding-3-small"):
#     text = text.replace("\n", " ").strip()
#     return openai.embeddings.create(input=[text], model=model).data[0].embedding

# if __name__ == "__main__":
#     # OPENAI API KEY
#     openai.api_key = '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'

#     try:
#         # Initialize QdrantDatabase
#         qdrant_db = QdrantDatabase()

#         # Read the reframed CSV file into a DataFrame
#         df = pd.read_csv('splited_resume_doc.csv', header=None, names=['text'])

#         # Store embeddings in Qdrant vector database
#         vectors = [{"vector": get_embedding(text), "id": idx} for idx, text in enumerate(df['text'])]
#         qdrant_db.insert_vectors(vectors)

#         # Input search
#         to_ask = input("Ask something: ")

#         # Compute embedding for the input query
#         query_embedding = get_embedding(to_ask)

#         # Search vectors in Qdrant
#         search_results = qdrant_db.search_vectors(query_embedding)

#         # Display search results
#         for result in search_results:
#             print(result)
#     except Exception as e:
#         print("An error occurred:", e)





import openai
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.http import models

class QdrantDatabase:
    def __init__(self, path):
        self.client = QdrantClient(path=path)

    def create_collection(self, collection_name):
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
        )

    def insert_vectors(self, collection_name, vectors, ids):
        if len(vectors) != len(ids):
            raise ValueError("Length of vectors and ids should be the same.")

        if not all(isinstance(id, (str, int)) for id in ids):
            raise ValueError("IDs should be either string or integer type.")
        # breakpoint() 
        points = []
        for id, vector in zip(ids, vectors):
            print(f"Id :{id}, type of id: {type(id)}")
            print(f"Id :{vectors}, type of id: {type(vectors)}")
            points.append({"id": str(id), "vector": vector})
            # print(points)

        
        # points = [{"id": str(id), "vector": vector} for id, vector in zip(ids, vectors)]
        # print("type points :", points)
        # print(type(points))
        # breakpoint()
        self.client.upsert(collection_name=collection_name, points=points)

    def query(self, collection_name, query_vector, top_k=10):
        result = self.client.search(collection_name=collection_name, payload={"vector": query_vector, "top": top_k})
        return result['hits']

def get_openai_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return openai.embeddings.create(input=[text], model=model).data[0].embedding

if __name__ == "__main__":
    # Initialize QdrantDatabase
    qdrant_db = QdrantDatabase(path=":memory:")

    # OPENAI API KEY
    openai.api_key = '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'

    try:
        # Create a collection
        qdrant_db.create_collection(collection_name="resume_details")

        # Read the reframed CSV file into a DataFrame
        df = pd.read_csv('splited_resume_doc.csv', header=None, names=['text'])

        # Prepare documents and IDs
        documents = df['text'].tolist()
        ids = df.index.tolist()
        print(type(documents))
        print("ids : ",ids)
        # breakpoint()
        # Compute and store embeddings
        embeddings = [get_openai_embedding(text) for text in documents]
        qdrant_db.insert_vectors(collection_name="resume_details", vectors=embeddings, ids=ids)

        # Input search
        to_ask = input("Ask something: ")
        

        # Compute OpenAI embedding for the input query
        query_embedding = get_openai_embedding(to_ask)

        # Perform semantic search
        search_results = qdrant_db.query(collection_name="resume_details", query_vector=query_embedding)

        # Display search results
        print(search_results)
    except Exception as e:
        print("An error occurred:", e)
