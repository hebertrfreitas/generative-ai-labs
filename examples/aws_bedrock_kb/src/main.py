from query_kb import query_kb, list_kbs


if __name__ == '__main__':
    list = list_kbs()
    query_kb(kb_id=list[0].knowledgeBaseId, query='O que são Derivativos de Crédito')

