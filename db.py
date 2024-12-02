
def create_vector_db(cur):
  cur.execute("""
  CREATE TABLE vectors (id bigserial PRIMARY KEY, response text, embedding vector(768));
              """)

def insert_vector(cur, text, vector):
  cur.execute("""
  INSERT INTO vectors (response, embedding) VALUES (%s, %s);
              """,
              (text, vector))

def select_all(cur, vector):
  cur.execute("""
  SELECT response FROM vectors ORDER BY embedding <-> %s::vector LIMIT 1;
              """,
              (vector,))
  return cur.fetchall() 

def drop_table(cur):
  cur.execute("""
  DROP TABLE vectors;
              """)
