import openai
import fitz
import pandas as pd
import numpy as np
from numpy.linalg import norm
# from openai.embeddings_utils import cosine_similarity
# from.qdrant_db import vector_db

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.

    Args:
    vec1 (numpy.ndarray or str): First vector.
    vec2 (numpy.ndarray or str): Second vector.

    Returns:
    float: Cosine similarity between vec1 and vec2.
    """
    # Convert vec1 to numpy array if it's a string
    if isinstance(vec1, str):
        vec1 = np.array(eval(vec1))

    # Convert vec2 to numpy array if it's a string or a list
    if isinstance(vec2, str):
        vec2 = np.array(eval(vec2))
    elif isinstance(vec2, list):
        vec2 = np.array(vec2)

    # Compute dot product
    dot_product = np.dot(vec1, vec2)

    # Compute norms
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)

    # Compute cosine similarity
    similarity = dot_product / norm_product if norm_product != 0 else 0

    return similarity

def files(pdf):
    doc = fitz.open(pdf)
    data = ""
    for page in doc:
        data += page.get_text("text")
    return data

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ").strip()
   return openai.embeddings.create(input = [text], model=model).data[0].embedding

if __name__ == "__main__":
    # OPENAI API KEY
    openai.api_key = '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'

    # Input file directory
    # pdf_file = "/home/vybog/Documents/Personal_Mar_29/vec_search/files/BalajiCV_demo (1).pdf"
    # data = files(pdf_file)
    # c = data.strip().split("\n")
    
    # with open('splited_resume_doc.csv', 'w') as file:
    #     # file.write(f'{text} \n')
    #     for x in c:
#             file.write(f'"{x}"\n')

    
    # Now read the reframed CSV file into a DataFrame
    df = pd.read_csv('splited_resume_doc.csv', header=None, names=['text'])
   
    # Storing the output DataFrame CSV file
    df['embedding'] = df['text'].apply(lambda x: get_embedding(x))
    df.to_csv('resume_out.csv')

    df = pd.read_csv('resume_out.csv')
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)

    print(df)

    # Input search 
    to_ask = input("Ask something :")

    # Compute embeddings for the input query
    query_embedding = get_embedding(to_ask)

    # Load DataFrame from the CSV file
    df = pd.read_csv('resume_out.csv')

    # Compute cosine similarity between each embedding and the query embedding
    df['similarities'] = df['embedding'].apply(lambda x: cosine_similarity(x, query_embedding))

    # Sort DataFrame by similarity scores in descending order
    df = df.sort_values("similarities", ascending=False)

    # Set display options to show all columns
    pd.set_option('display.max_columns', None)

    # Print the top 20 results
    print(df.head(20))