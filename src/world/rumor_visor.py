from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class Rumor:
    def __init__(self, content: str, creator: str, timestamp: int, node_id: int):
        self.content = content
        self.creator = creator
        self.timestamp = timestamp
        self.node_id = node_id
        self.spread_history: List[Dict] = []
        
    def add_spread(self, spreader: str, receiver: str, cycle: int) -> None:
        """Record the spread of the rumor"""
        self.spread_history.append({
            "spreader": spreader,
            "receiver": receiver,
            "timestamp": cycle
        })
            
    def get_spread_count(self) -> int:
        """Get the number of times the rumor has been spread"""
        return len(self.spread_history)
        
    def get_spread_path(self) -> List[Dict]:
        """Get the complete spread path of the rumor"""
        return self.spread_history
        
    def to_dict(self) -> Dict:
        """Convert rumor object to dictionary for JSON serialization"""
        return {
            "content": self.content,
            "creator": self.creator,
            "timestamp": self.timestamp,
            "node_id": self.node_id,
            "spread_history": self.spread_history
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Rumor':
        """Create rumor object from dictionary"""
        rumor = cls(
            content=data["content"],
            creator=data["creator"],
            timestamp=data["timestamp"],
            node_id=data["node_id"]
        )
        rumor.spread_history = data["spread_history"]
        return rumor

class RumorVisor:
    def __init__(self, save_path: str = "rumors_data"):
        self.rumors: List[Rumor] = []
        self.rumor_id_counter = 0
        self.save_path = save_path
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
    def add_rumor(self, content: str, creator: str, timestamp: int) -> int:
        """Add a new rumor to the system"""
        rumor = Rumor(content, creator, timestamp, self.rumor_id_counter)
        self.rumors.append(rumor)
        self.rumor_id_counter += 1
        return self.rumor_id_counter - 1
        
    def get_rumor(self, rumor_id: int) -> Optional[Rumor]:
        """Get a specific rumor by ID"""
        if 0 <= rumor_id < len(self.rumors):
            return self.rumors[rumor_id]
        return None
        
    def get_all_rumors(self) -> List[Rumor]:
        """Get all rumors in the system"""
        return self.rumors
        
    def track_rumor_spread(self, rumor_id: int, spreader: str, receiver: str, cycle: int) -> bool:
        """Track the spread of a specific rumor"""
        rumor = self.get_rumor(rumor_id)
        if rumor:
            rumor.add_spread(spreader, receiver, cycle)
            return True
        return False
        
    def get_rumor_stats(self, rumor_id: int) -> Optional[Dict]:
        """Get statistics for a specific rumor"""
        rumor = self.get_rumor(rumor_id)
        if not rumor:
            return None
            
        return {
            "spread_count": rumor.get_spread_count(),
            "creator": rumor.creator,
            "timestamp": rumor.timestamp,
            "content": rumor.content
        }
        
    def get_rumor_network(self, rumor_id: int) -> Optional[Dict]:
        """Get the spread network for a specific rumor"""
        rumor = self.get_rumor(rumor_id)
        if not rumor:
            return None
            
        network = {
            "nodes": set(),
            "edges": []
        }
        
        # Add creator as first node
        network["nodes"].add(rumor.creator)
        
        # Add all spreaders and receivers
        for spread in rumor.spread_history:
            network["nodes"].add(spread["spreader"])
            network["nodes"].add(spread["receiver"])
            network["edges"].append({
                "from": spread["spreader"],
                "to": spread["receiver"]
            })
            
        return network
        
    def save_rumor_stats(self, filename: str = "rumor_stats.json", persona_knowledge: Dict[str, List[int]] = None) -> None:
        """Save statistics for all rumors to a JSON file"""
        filepath = os.path.join(self.save_path, filename)
        stats = {
            "total_rumors": len(self.rumors),
            "rumors": {},
            "persona_knowledge": persona_knowledge or {}
        }
        
        for rumor in self.rumors:
            network = self.get_rumor_network(rumor.node_id)
            stats["rumors"][str(rumor.node_id)] = {
                "content": rumor.content,
                "creator": rumor.creator,
                "timestamp": rumor.timestamp,
                "spread_count": rumor.get_spread_count(),
                "spread_history": rumor.spread_history,
                "network": {
                    "nodes": list(network["nodes"]) if network else [],
                    "edges": network["edges"] if network else []
                }
            }
            
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2) 