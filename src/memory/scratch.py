from typing import List, Dict, Optional

class Scratch:
    def __init__(self, name: str, first_name: str, last_name: str, 
                 age: int, innate_traits: str, lifestyle: str):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.innate_traits = innate_traits
        self.lifestyle = lifestyle
        self.chatting_with = None
        self.chat: List[List[str]] = []  # [["name", "message"], ...]
        self.learned_traits = ""
        
    def is_chat(self) -> bool:
        """Check if there is an active chat"""
        return len(self.chat) == 0
        
    def get_summary(self) -> str:
        """Get a summary of the persona's current state"""
        summary = ""
        summary += f'Имя: {self.name}\n'
        summary += f'Возраст: {self.age}\n'
        summary += f'Изначальные черты: {self.innate_traits}\n'
        summary += f'Приобретенные черты: {self.learned_traits}\n'
        summary += f'Жизненный стиль: {self.lifestyle}\n'
        return summary
        
    def get_summary_chat(self) -> str:
        """Get a summary of the current chat"""
        summary = ""
        if not self.is_chat():
            for message in self.chat:
                summary += f'{message[0]}: {message[1]}\n'
        else:
            summary += "Сейчас нет диалога"
        return summary
        
    def add_chat_message(self, message: str, author: str, recipient: str) -> None:
        """Add a message to the chat history"""
        self.chat.append([author, message, recipient])
        
    def get_summary_dict(self) -> Dict:
        """Get a dictionary summary of the persona's current state"""
        return {
            "name": self.name,
            "age": self.age,
            "innate_traits": self.innate_traits,
            "learned_traits": self.learned_traits,
            "lifestyle": self.lifestyle
        }
    
    def get_history_with(self, interlocutor: str, max_messages: int = 20) -> str:
        """
        Возвращает строки вида "Автор: текст" только тех сообщений,
        где автор == interlocutor и recipient == self.name,
        или автор == self.name и recipient == interlocutor.
        """
        filtered = []
        for author, msg, recipient in self.chat[-max_messages:]:
            if (author == interlocutor and recipient == self.name) or \
               (author == self.name and recipient == interlocutor):
                filtered.append(f"{author}: {msg}")
        return "\n".join(filtered) if filtered else ""