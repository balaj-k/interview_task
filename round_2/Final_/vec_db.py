from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import VectorParams, Distance, Record
import pandas as pd


encoder = SentenceTransformer('all-MiniLM-L6-v2')

doc_ = pd.read_csv("./splited_resume_doc.csv")
data = []

for index, row in doc_.iterrows():
    data.append({
        "data": row.values[0]  # Assuming there's only one column in your CSV file
    })

qdrant = QdrantClient(":memory:")

qdrant.recreate_collection(
    collection_name="resume_data",
    vectors_config=VectorParams(
        size = encoder.get_sentence_embedding_dimension(),
        distance = Distance.COSINE
    )
)

qdrant.upload_records(
    collection_name="resume_data",
    records=[
        Record(
            id= idx,
            vector=encoder.encode(doc_["data"]).tolist(),
            payload=doc_

        )for idx, doc_ in enumerate(data)
    ]
)

hits = qdrant.search(
    collection_name="resume_data",
    query_vector=encoder.encode(input("Ask something: ")).tolist(),
    limit=5
)

for hit in hits:
    print(hit.payload, "score: ", hit.score )