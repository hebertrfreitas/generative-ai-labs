--verifica extensões ativas no banco de dados
select * from pg_extension

--cria uma tabela para armazenar embeddings adequado para um tamanho hipotético de três dimensões
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));

--insere dois arrays de embedding
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');

--distancia dos elementos (usando L2 distance)
SELECT embedding, embedding <-> '[3,1,2]' AS l2_distance 
FROM items 
ORDER BY l2_distance

--distancia dos elementos (usando similaridade de coseno)
SELECT embedding, 1- (embedding <=> '[3,2,3]') AS cosine_similarity 
FROM items 
ORDER BY cosine_similarity DESC

--cria o indice


SELECT phase, round(100.0 * tuples_done / nullif(tuples_total, 0), 1) AS "%" FROM pg_stat_progress_create_index;


select * from langchain_pg_collection

select * from langchain_pg_embedding

SELECT * FROM pg_indexes WHERE tablename = 'langchain_pg_embedding';

select embedding from langchain_pg_embedding



