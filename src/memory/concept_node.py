from typing import Tuple

class ConceptNode:
    def __init__(self, node_id: int, node_type: str, description: str, 
                 embedding_key: str, poignancy: int, subject: str, 
                 predicate: str, object: str):
        self.node_id = node_id
        self.node_type = node_type
        self.description = description
        self.embedding_key = embedding_key
        self.poignancy = poignancy
        self.subject = subject
        self.predicate = predicate
        self.object = object
        
    def spo_summary(self) -> Tuple[str, str, str]:
        """Get subject-predicate-object summary of the node"""
        return (self.subject, self.predicate, self.object) 