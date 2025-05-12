select * from pg_extension


CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');

SELECT * FROM items ORDER BY embedding <-> '[1,2,4]' LIMIT 5;

--distancia dos elementos (usando L2 distance)
SELECT embedding, embedding <-> '[3,1,2]' AS l2_distance FROM items;



--distancia dos elementos (usando similaridade de coseno)
SELECT embedding,  1 - (embedding <=> '[3,1,2]') AS cosine_similarity FROM items;



