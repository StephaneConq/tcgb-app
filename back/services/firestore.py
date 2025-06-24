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
    
    def batch_query_documents(self, collection_name: str, filter_groups: List[List[tuple]], 
                          order_by: str = None, direction: str = "ASCENDING", limit: int = None) -> List[Dict[str, Any]]:
        """
        Execute multiple queries with different filter conditions and combine the results.
        This allows for implementing "OR" logic across different filter groups.

        Args:
            collection_name: Name of the collection to query
            filter_groups: List of filter groups, where each group is a list of filter tuples (field, operator, value)
                        Each filter group is executed as a separate query with AND logic within the group
                        Results from all groups are combined (OR logic between groups)
            order_by: Field to order results by (applied after combining results)
            direction: Direction to order results ("ASCENDING" or "DESCENDING")
            limit: Maximum number of results in the final combined result

        Returns:
            List of document dictionaries matching any of the filter groups
        """
        all_results = []
        seen_ids = set()  # To track duplicate documents

        # Execute each query separately
        for filters in filter_groups:
            query = self.db.collection(collection_name)
            
            # Apply filters for this query (AND logic within a filter group)
            if filters:
                for field, op, value in filters:
                    query = query.where(filter=FieldFilter(field, op, value))
            
            # Get results for this query
            query_results = [{**doc.to_dict(), '_id': doc.id, 'ref': doc.reference} for doc in query.stream()]
            
            # Add unique results to the combined results
            for result in query_results:
                if result['_id'] not in seen_ids:
                    all_results.append(result)
                    seen_ids.add(result['_id'])
        
        # Sort the combined results if order_by is specified
        if order_by and all_results:
            reverse = direction.upper() == "DESCENDING"
            all_results.sort(key=lambda x: x.get(order_by, ''), reverse=reverse)
        
        # Apply limit if specified
        if limit is not None and limit < len(all_results):
            all_results = all_results[:limit]
        
        return all_results


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
                        order_by: str = None, direction: str = "ASCENDING", limit: int = None) -> List[Dict[str, Any]]:
        """
        Query documents with filters.

        Args:
            collection_name: Name of the collection
            filters: List of filter tuples (field, operator, value)
            order_by: Field to order results by
            direction: Direction to order results ("ASCENDING" or "DESCENDING")
            limit: Maximum number of results

        Returns:
            List of document dictionaries
        """
        query = self.db.collection(collection_name)

        if filters:
            for field, op, value in filters:
                query = query.where(filter=FieldFilter(field, op, value))

        if order_by:
            # Convert direction string to Firestore direction enum
            if direction.upper() == "DESCENDING":
                query = query.order_by(
                    order_by, direction=firestore.Query.DESCENDING)
            else:
                query = query.order_by(
                    order_by, direction=firestore.Query.ASCENDING)

        if limit:
            query = query.limit(limit)

        return [{**doc.to_dict(), '_id': doc.id} for doc in query.stream()]

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
            test = doc.to_dict().get('card_ref').get().to_dict()
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
        
    def batch_delete_sub_collection_documents(self, collection_name: str, document_id: str,
                                         sub_collection: str, sub_document_ids: List[str]) -> bool:
        """
        Delete multiple documents from a sub-collection using a batch operation.

        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            sub_document_ids: List of document IDs to delete from the sub-collection

        Returns:
            True if batch deletion was successful
        """
        if not sub_document_ids:
            return True  # Nothing to delete
            
        batch = self.db.batch()
        sub_collection_ref = self.db.collection(collection_name).document(document_id)\
            .collection(sub_collection)
        
        for sub_doc_id in sub_document_ids:
            doc_ref = sub_collection_ref.document(sub_doc_id)
            batch.delete(doc_ref)
        
        # Commit the batch
        batch.commit()
        
        return True


    def batch_create_sub_collection_documents(self, collection_name: str, document_id: str,
                                              sub_collection: str, documents_data: List[Dict[str, Any]],
                                              document_ids: Optional[List[str]] = None) -> List[str]:
        """
        Create multiple documents in a sub-collection using a batch operation.

        Args:
            collection_name: Name of the parent collection
            document_id: ID of the parent document
            sub_collection: Name of the sub-collection
            documents_data: List of document data dictionaries
            document_ids: Optional list of IDs for the sub-collection documents
                         (must match length of documents_data if provided)

        Returns:
            List of IDs of the created documents
        """
        batch = self.db.batch()
        sub_collection_ref = self.db.collection(collection_name).document(document_id)\
            .collection(sub_collection)
        created_ids = []

        # Check if document_ids is provided and has the correct length
        if document_ids and len(document_ids) != len(documents_data):
            raise ValueError(
                "Length of document_ids must match length of documents_data")

        for i, data in enumerate(documents_data):
            if document_ids:
                doc_ref = sub_collection_ref.document(document_ids[i])
                created_ids.append(document_ids[i])
            else:
                doc_ref = sub_collection_ref.document()
                created_ids.append(doc_ref.id)

            batch.set(doc_ref, data)

        # Commit the batch
        batch.commit()

        return created_ids

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
                             order_by: str = None, limit: int = None, get_ref: bool = False) -> List[Dict[str, Any]]:
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

        return [{**doc.to_dict(), '_id': doc.id, 'ref': doc.reference} for doc in query.stream()]

    def get_collection_ref(self, collection_name: str):
        """
        Get Firestore ref of Firestore collection

        Args:
            collection_name: Name of the collection

        Returns:
            Firestore reference to the collection
        """
        return self.db.collection(collection_name)

    def get_document_ref_by_path(self, ref_path: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its reference path.
        
        Args:
            ref_path: Full path to the document, e.g. "series/IaSmT9uI8EJseYJDAtPB/cards/Qf93tBIlH4kzSp5QlAkW"
            
        Returns:
            Document data as dictionary or None if not found
        """
        # Split the path into components
        path_components = ref_path.split('/')
        
        # Check if we have a valid path (must have at least collection/document)
        if len(path_components) < 2 or len(path_components) % 2 != 0:
            raise ValueError(f"Invalid reference path: {ref_path}. Path must have even number of segments.")
        
        # Build the document reference
        doc_ref = self.db
        for i in range(0, len(path_components), 2):
            collection_name = path_components[i]
            document_id = path_components[i+1]
            doc_ref = doc_ref.collection(collection_name).document(document_id)
        
        # Get the document
        doc = doc_ref.get()
        if doc.exists:
            return doc.reference
        return None
