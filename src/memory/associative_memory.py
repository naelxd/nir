from typing import List, Set, Dict
import numpy as np
from .concept_node import ConceptNode
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class AssociativeMemory:
    def __init__(self):
        self.id_to_node: Dict[int, ConceptNode] = {}
        self.seq_chat: List[ConceptNode] = []
        self.seq_thought: List[ConceptNode] = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def add_chat(self, node: ConceptNode) -> None:
        """Add a chat node to memory"""
        self.id_to_node[node.node_id] = node
        self.seq_chat.append(node)
        
    def add_thought(self, node: ConceptNode) -> None:
        """Add a thought node to memory"""
        self.id_to_node[node.node_id] = node
        self.seq_thought.append(node)
        
    def get_summarized_last_events(self) -> Set[str]:
        """Get a summary of recent events"""
        recent_events = set()
        for node in self.seq_chat[-5:]:  # Last 5 chat events
            recent_events.add(node.description)
        return recent_events
        
    def get_str_desc_chats(self) -> str:
        """Get string description of chat history"""
        return "\n".join([node.description for node in self.seq_chat[-10:]])
        
    def get_str_desc_thoughts(self) -> str:
        """Get string description of thought history"""
        return "\n".join([node.description for node in self.seq_thought[-10:]])
        
    def retrieve_relevant_thoughts(self, query: str, threshold: float = 0.7) -> Set[str]:
        """Retrieve relevant thoughts based on semantic similarity"""
        if not self.seq_thought:
            return set()
            
        # Get embeddings for query and all thoughts
        query_embedding = self.model.encode([query])[0]
        thought_embeddings = self.model.encode([node.description for node in self.seq_thought])
        
        # Calculate similarities
        similarities = cosine_similarity([query_embedding], thought_embeddings)[0]
        
        # Get relevant thoughts above threshold
        relevant_indices = np.where(similarities > threshold)[0]
        relevant_thoughts = set()
        
        for idx in relevant_indices:
            relevant_thoughts.add(self.seq_thought[idx].description)
            
        return relevant_thoughts 