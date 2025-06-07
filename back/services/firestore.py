import os
from typing import Dict, List, Any, Optional, Union
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

class FirestoreService:
    def __init__(self):
        """Initialize Firestore client."""
        self.db = firestore.Client(
            database="tcgb-db"
        )
    
    # Document operations
    def get_document(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by ID.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document
            
        Returns:
            Document data as dictionary or None if not found
        """
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None
    
    def create_document(self, collection_name: str, data: Dict[str, Any], document_id: Optional[str] = None) -> str:
        """
        Create a new document.
        
        Args:
            collection_name: Name of the collection
            data: Document data
            document_id: Optional ID for the document (auto-generated if not provided)
            
        Returns:
            ID of the created document
        """
        collection_ref = self.db.collection(collection_name)
        if document_id:
            doc_ref = collection_ref.document(document_id)
            doc_ref.set(data)
            return document_id
        else:
            doc_ref = collection_ref.add(data)[1]
            return doc_ref.id
    
    def update_document(self, collection_name: str, document_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing document.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document
            data: Updated data
            
        Returns:
            True if update was successful
        """
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.update(data)
        return True
    
    def delete_document(self, collection_name: str, document_id: str) -> bool:
        """
        Delete a document.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the document
            
        Returns:
            True if deletion was successful
        """
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.delete()
        return True
    
    def query_documents(self, collection_name: str, filters: List[tuple] = None, 
                        order_by: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """
        Query documents with filters.
        
        Args:
            collection_name: Name of the collection
            filters: List of filter tuples (field, operator, value)
            order_by: Field to order results by
            limit: Maximum number of results
            
        Returns:
            List of document dictionaries
        """
        query = self.db.collection(collection_name)
        
        if filters:
            for field, op, value in filters:
                query = query.where(filter=FieldFilter(field, op, value))
        
        if order_by:
            query = query.order_by(order_by)
        
        if limit:
            query = query.limit(limit)
        
        return [doc.to_dict() for doc in query.stream()]
    
    # Sub-collection operations
    def get_sub_collection_document(self, collection_name: str, document_id: str, 
                                   sub_collection: str, sub_document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document from a sub-collection.
        
        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            sub_document_id: ID of the document in the sub-collection
            
        Returns:
            Document data or None if not found
        """
        doc_ref = self.db.collection(collection_name).document(document_id)\
                         .collection(sub_collection).document(sub_document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None
    
    def create_sub_collection_document(self, collection_name: str, document_id: str, 
                                      sub_collection: str, data: Dict[str, Any], 
                                      sub_document_id: Optional[str] = None) -> str:
        """
        Create a document in a sub-collection.
        
        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            data: Document data
            sub_document_id: Optional ID for the sub-collection document
            
        Returns:
            ID of the created document
        """
        sub_collection_ref = self.db.collection(collection_name).document(document_id)\
                                   .collection(sub_collection)
        
        if sub_document_id:
            doc_ref = sub_collection_ref.document(sub_document_id)
            doc_ref.set(data)
            return sub_document_id
        else:
            doc_ref = sub_collection_ref.add(data)[1]
            return doc_ref.id
    
    def update_sub_collection_document(self, collection_name: str, document_id: str, 
                                      sub_collection: str, sub_document_id: str, 
                                      data: Dict[str, Any]) -> bool:
        """
        Update a document in a sub-collection.
        
        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            sub_document_id: ID of the document in the sub-collection
            data: Updated data
            
        Returns:
            True if update was successful
        """
        doc_ref = self.db.collection(collection_name).document(document_id)\
                         .collection(sub_collection).document(sub_document_id)
        doc_ref.update(data)
        return True
    
    def delete_sub_collection_document(self, collection_name: str, document_id: str, 
                                      sub_collection: str, sub_document_id: str) -> bool:
        """
        Delete a document from a sub-collection.
        
        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            sub_document_id: ID of the document in the sub-collection
            
        Returns:
            True if deletion was successful
        """
        doc_ref = self.db.collection(collection_name).document(document_id)\
                         .collection(sub_collection).document(sub_document_id)
        doc_ref.delete()
        return True
    
    def query_sub_collection(self, collection_name: str, document_id: str, 
                            sub_collection: str, filters: List[tuple] = None, 
                            order_by: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """
        Query documents in a sub-collection.
        
        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            filters: List of filter tuples (field, operator, value)
            order_by: Field to order results by
            limit: Maximum number of results
            
        Returns:
            List of document dictionaries
        """
        query = self.db.collection(collection_name).document(document_id)\
                       .collection(sub_collection)
        
        if filters:
            for field, op, value in filters:
                query = query.where(filter=FieldFilter(field, op, value))
        
        if order_by:
            query = query.order_by(order_by)
        
        if limit:
            query = query.limit(limit)
        
        return [{**doc.to_dict(), '_id': doc.id} for doc in query.stream()]

    def get_collection_ref(self, collection_name: str):
        """
        Get Firestore ref of Firestore collection
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Firestore reference to the collection
        """
        return self.db.collection(collection_name)