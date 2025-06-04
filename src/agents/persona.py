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
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

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
                 model_type: str = "llama", api_key: str = None,
                 reflection_enabled: bool = True):
        self.name = name
        self.scratch = Scratch(name, first_name, last_name, age, 
                             innate_traits, lifestyle)
        self.associative_memory = AssociativeMemory()
        self.message_count = 0  # Счетчик сообщений
        self.REFLECTION_THRESHOLD = 20  # Порог для рефлексии
        self.reflection_enabled = reflection_enabled  # Флаг включения рефлексии
        
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
        history_with = self.scratch.get_history_with(name)
        prompt = f'''Ты — персонаж в симуляции. Вот твои данные:
[ПЕРСОНАЖ]
{self.scratch.get_summary()}

Ты общаешься с другим персонажем ({name}).  
Что ты о нем знаешь (из памяти):
[ИНФОРМАЦИЯ О СОБЕСЕДНИКЕ]
{relevant_thoughts if relevant_thoughts else "ничего"}

Последние сообщения между вами:
[ИСТОРИЯ ДИАЛОГА С {name.upper()}]
{history_with}

Слухи, которые тебе доступны сейчас:
[СЛУХИ]
{rumor if rumor else "Слухов нет, возвращай []"}

Твоя задача: продолжить диалог с учётом твоего характера и доступных слухов.  
— Оформи ответ в стиле твоего персонажа.  
— Если ты используешь один или несколько слухов, после текста укажи номера слухов в формате [1,2] (без пробелов внутри).  
— Если не используешь ни один слух, просто напиши «[]» после реплики.

Пример формата:
«Конечно, я тоже слышал об этом, но не уверен, правда ли это. []»

Важно:
— Не обрывай мысль на полуслове: напиши развернутую, логичную фразу (до 200 символов, но без искусственных ограничений).  
— Квадратные скобки «[» и «]» используй только для нумерации слухов.

Ответ:
'''
        
        answer = self.model.ask(prompt)
        
        rumor_part = answer[answer.find('[')+1:answer.find(']')]

        used_rumors = [int(x.strip()) for x in rumor_part.split(',') if x.strip().isdigit()]

        answer = answer[:answer.find('[')].strip()
        
        self.scratch.add_chat_message(answer, self.name, name)
       
        return answer, used_rumors
        
    def generate_rumor(self) -> str:
        """Generate a new rumor"""
        # Get existing rumors from memory
        existing_rumors = self.associative_memory.get_str_desc_rumors()
        
        prompt = f'''Ты персонаж {self.name}. Вот твои характеристики:
{self.scratch.get_summary()}

Придумай новый слух. Слух должен быть интересным и правдоподобным.
Важно: слух должен быть уникальным и не похожим на уже существующие.

Вот уже существующие слухи:
{existing_rumors if existing_rumors else "Слухов пока нет"}

Напиши только новый уникальный слух.'''
        
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
        
        # Add to memory using the new rumor-specific method
        self.associative_memory.add_rumor(rumor_node)
        return rumor
        
    def get_answer(self, answer: str, name: str) -> None:
        """Process and store the answer in memory"""
        self.scratch.add_chat_message(answer, name, self.name)
        
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
        
        # Увеличиваем счетчик сообщений
        self.message_count += 1
        
        # Проверяем, нужно ли запустить рефлексию
        if self.reflection_enabled and self.message_count >= self.REFLECTION_THRESHOLD:
            print(f"\n{self.name} размышляет о последних событиях...")
            self.reflect()
            self.message_count = 0  # Сбрасываем счетчик
        
    def get_name(self) -> str:
        """Get the persona's name"""
        return self.name 

    def enable_reflection(self) -> None:
        """Включить механизм рефлексии"""
        self.reflection_enabled = True
        print(f"Рефлексия для {self.name} включена")
        
    def disable_reflection(self) -> None:
        """Отключить механизм рефлексии"""
        self.reflection_enabled = False
        print(f"Рефлексия для {self.name} отключена") 