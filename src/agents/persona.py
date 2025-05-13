from typing import List, Dict, Optional
from memory.associative_memory import AssociativeMemory
from memory.scratch import Scratch
from memory.concept_node import ConceptNode
from together import Together
from together.types.chat_completions import ChatCompletionResponse
from abc import ABC, abstractmethod
import openai

class LLMAPI(ABC):
    @abstractmethod
    def ask(self, message: str) -> str:
        pass

class LlamaAPI(LLMAPI):
    def __init__(self):
        self.client = Together()
        self.model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

    def ask(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content

class ChatGPTAPI(LLMAPI):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4.1-nano"

    def ask(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message.content

class Persona:
    def __init__(self, name: str, first_name: str, last_name: str, 
                 age: int, innate_traits: str, lifestyle: str,
                 model_type: str = "llama", api_key: str = None):
        self.name = name
        self.scratch = Scratch(name, first_name, last_name, age, 
                             innate_traits, lifestyle)
        self.associative_memory = AssociativeMemory()
        
        # Initialize appropriate model
        if model_type.lower() == "chatgpt":
            if not api_key:
                raise ValueError("API key is required for ChatGPT")
            self.model = ChatGPTAPI(api_key)
        else:
            self.model = LlamaAPI()
        
    def reflect(self) -> None:
        """Process recent events and update memory"""
        # Get recent events
        recent_events = self.associative_memory.get_summarized_last_events()
        
        if not recent_events:
            return
            
        # Create reflection prompt
        reflection_prompt = f'''Ты персонаж {self.name}. Вот твои характеристики:
{self.scratch.get_summary()}

Недавние события:
{recent_events}

Подумай о том, что произошло и как это повлияло на тебя. Напиши свои мысли.'''
        
        # Get reflection from LLM
        reflection = self.model.ask(reflection_prompt)
        
        # Create thought node
        thought_node = ConceptNode(
            node_id=len(self.associative_memory.id_to_node),
            node_type="thought",
            description=reflection,
            embedding_key="thought",
            poignancy=5,  # High importance for reflections
            subject=self.name,
            predicate="reflects",
            object="recent events"
        )
        
        # Add to memory
        self.associative_memory.add_thought(thought_node)
        
    def retrieve(self) -> Dict:
        """Retrieve relevant information from memory"""
        return {
            "chats": self.associative_memory.get_str_desc_chats(),
            "thoughts": self.associative_memory.get_str_desc_thoughts()
        }
        
    def answer(self, name: str, rumor: str = None) -> tuple[str, list[int]]:
        """Generate response to a query using LLM, optionally including a rumor.
        Returns tuple of (answer, list of used rumor numbers)"""
        # Get relevant thoughts for context
        relevant_thoughts = self.associative_memory.retrieve_relevant_thoughts(name)
        prompt = f'''Ты — персонаж в симуляции. Вот твои данные:
[ПЕРСОНАЖ]
{self.scratch.get_summary()}

Ты общаешься с другим персонажем.  
Вот, что ты знаешь о нем:
[ИНФОРМАЦИЯ О СОБЕСЕДНИКЕ]
{relevant_thoughts if relevant_thoughts else "ничего"}

Ваша история диалога:
[ИСТОРИЯ ДИАЛОГА]
{self.scratch.get_summary_chat()}

Слухи:
[СЛУХИ]
{rumor if rumor else "Слухов нет, требуется вывести []"}

Твоя задача: продолжить диалог.  
Составь логичный и связный ответ в стиле персонажа.  
Если ты используешь слухи, укажи номера слухов в квадратных скобках после ответа.  
Пример: Ответ текста. [1,3]  
Если слухи не использованы, укажи [].

Важно:
- Максимальная длина ответа — 100 символов.
- Используй символы [ и ] **только** для обозначения номеров слухов.

Ответ:
'''
        
        answer = self.model.ask(prompt)
        
        # Извлекаем содержимое между []
        rumor_part = answer[answer.find('[')+1:answer.find(']')]
        # Разбиваем на числа и конвертируем в int
        used_rumors = [int(x.strip()) for x in rumor_part.split(',') if x.strip().isdigit()]
        # Удаляем часть с номерами слухов из ответа
        print(answer)
        answer = answer[:answer.find('[')].strip()
        
        self.scratch.add_chat_message(answer, self.name)
        print(prompt)
       
        return answer, used_rumors
        
    def generate_rumor(self) -> str:
        """Generate a new rumor"""
        prompt = f'''Ты персонаж {self.name}. Вот твои характеристики:
{self.scratch.get_summary()}

Придумай слух. Слух должен быть интересным и правдоподобным. Напиши только слух.'''
        
        rumor = self.model.ask(prompt)
        
        # Create rumor node
        rumor_node = ConceptNode(
            node_id=len(self.associative_memory.id_to_node),
            node_type="rumor",
            description=rumor,
            embedding_key="rumor",
            poignancy=3,  # Medium importance for rumors
            subject=self.name,
            predicate="creates",
            object="rumor"
        )
        
        # Add to memory
        self.associative_memory.add_thought(rumor_node)
        return rumor
        
    def get_answer(self, answer: str, name: str) -> None:
        """Process and store the answer in memory"""
        self.scratch.add_chat_message(answer, name)
        
        # Create chat node
        chat_node = ConceptNode(
            node_id=len(self.associative_memory.id_to_node),
            node_type="chat",
            description=f"{name}: {answer}",
            embedding_key="chat",
            poignancy=2,  # Low importance for regular chat
            subject=name,
            predicate="says",
            object=answer
        )
        
        # Add to memory
        self.associative_memory.add_chat(chat_node)
        
    def get_name(self) -> str:
        """Get the persona's name"""
        return self.name 