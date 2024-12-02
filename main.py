import psycopg2
from db import drop_table, create_vector_db, insert_vector, select_all
import google.generativeai as genai
from dotenv import load_dotenv
from os import environ

load_dotenv()
print(environ.get("API_KEY"))
genai.configure(api_key=environ.get("API_KEY"))
model = 'models/embedding-001'

def embed_fn(text, model):
  return genai.embed_content(model=model,
                             content=text,
                             task_type="retrieval_document",
                             )["embedding"]

def find_response(query, model):
    query_embedding = genai.embed_content(model=model,
                                            content=query,
                                            task_type="retrieval_query")
    return query_embedding['embedding']


conn = psycopg2.connect(
    database="vectordb",
    user="srini",
    password="my_password",
    port=5434
)

cur = conn.cursor()

def train_model():
  drop_table(cur)
  create_vector_db(cur)

  with open('responses.txt', 'r') as f:
    dataset = f.readlines()
    print(f"Completed Status: 0.00%", end='\r')

    for i, response in enumerate(dataset, start=1):
      vector = embed_fn(response, model)
      insert_vector(cur, response, vector)
      print(f"Completed Status: {(i / len(dataset) * 100):.2f}%", end='\r')

    
while True:
  try:
    query = input("How can I help you? ")
    query_vector = find_response(query, model)    
    print()
    for response in select_all(cur, query_vector):
      print(response[0])

  except KeyboardInterrupt:
    print("Exited!")
    break
    

conn.commit()
conn.close()
