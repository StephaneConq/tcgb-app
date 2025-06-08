
from services.firestore import FirestoreService


firestore_service = FirestoreService()

documents = firestore_service.query_documents('series')

for i, document in enumerate(documents):
    print(f"{i + 1}/{len(documents)}: {document.get('serie_name')}")
    subdocuments = firestore_service.query_sub_collection(
        'series',
        document.get('_id'),
        'cards'
    )
    ids = [subdoc.get('_id') for subdoc in subdocuments]
    
    firestore_service.batch_delete_sub_collection_documents(
        'series',
        document.get('_id'),
        'cards',
        ids
    )
    print(f"Deleted cards from serie: {document.get('serie_name')}")
    firestore_service.delete_document(
        'series',
        document.get('_id')
    )
    print(f"Serie deleted: {document.get('serie_name')}")
    