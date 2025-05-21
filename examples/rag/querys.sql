select * from public.langchain_pg_collection

--listando os chunks e embeddings
select embedding.*
from public.langchain_pg_embedding as embedding
inner join public.langchain_pg_collection as collection ON (embedding.collection_id = collection.uuid)
where 
collection.name = 'fundos_investimento' 