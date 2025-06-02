from typing import List, Dict, Optional
from datetime import datetime

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

class RumorVisor:
    def __init__(self):
        self.rumors: List[Rumor] = []
        self.rumor_id_counter = 0
        
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