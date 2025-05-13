import time
from together import Together
from together.types.chat_completions import ChatCompletionResponse

class TogetherAPI:
    '''
    Working with Together API

    Example of usage:
    -------
    chat = TogetherAPI("meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")
    message = chat.ask("do u like cookies?")
    -------
    '''
    def __init__(self, model):
        self.client = Together()
        self.model = model

    def ask(self, message: str):
        return self._process_request(self._get_request(message))


    def _get_request(self, message: str):
        return self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                )

    def _process_request(self, request: ChatCompletionResponse):
        return request.choices[0].message.content


class LlamaAPI(TogetherAPI):
    '''
    Initialise Llama Model with Together API

    Example of usage:
    -------
    chat = LlamaAPI("meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")
    message = chat.ask("do u like cookies?")
    -------
    '''
    def __init__(self):
        self.client = Together()
        self.model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"



class Persona:
    def __init__(self, name: str, first_name: str, last_name: str, 
                 age: int, innate_traits: str, lifestyle: str, 
                 mendacity_level: int = 0.5):
        self.name = name
        self.scratch = Scratch(name, first_name, last_name, age, 
                               innate_traits, lifestyle, mendacity_level)
        self.associative_memory = AssociativeMemory()
        self.model = LlamaAPI()

    def reflect(self):
        pass

    def retrieve(self):
        pass

    def answer(self, name):
        prompt = f'''Представь, что ты персонаж и вот твои данные:
{self.scratch.get_summary()}
Ты говоришь с {name}.
Ты знаешь о нем: .
Ваша история диалога: 
{self.scratch.get_summary_chat()}
Что ты ему скажешь? Напиши только ответ. (Максимальная длина 100 символов)'''
        answer = self.model.ask(prompt)
        self.scratch.add_chat_message(answer, self.name)
        return answer


    def generate_rumor(self):
        pass

    def get_answer(self, answer, name):
        self.scratch.add_chat_message(answer, name)

    def get_name(self):
        return self.name


class AssociativeMemory:
    def __init__(self):
        pass


class ConceptNode:
    def __init__(self):
        pass


class Scratch:
    def __init__(self, name: str, first_name: str, last_name: str, 
                 age: int, innate_traits: str, lifestyle: str, 
                 mendacity_level: int = 0.5):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.innate_traits = innate_traits
        self.lifestyle = lifestyle
        self.mendacity_level = mendacity_level
        self.chatting_with = None
        self.chat = []  #[["name", "message"], ...]
        self.learned_traits = ""

    def is_chat(self):
        return self.chat == []

    def get_summary(self):
        summary = ""
        summary += f'Name: {self.name}'
        summary += f'Age: {self.age}'
        summary += f'Innate Traits: {self.innate_traits}'
        summary += f'Learned Traits: {self.learned_traits}'
        summary += f'Lifestyle: {self.lifestyle}'
        return summary

    def get_summary_mendlevel(self):
        return f"Mendacity Level: {self.mendacity_level}"

    def get_summary_chat(self):
        summary = ""
        if not self.is_chat():
            summary += f"Chatting with {self.chatting_with}"
            for message in self.chat:
                summary += f'{message[0]}: {message[1]}'
        else:
            summary += "Currently not chatting"

        return summary

    def add_chat_message(self, message: str, author: str):
        self.chat.append([author, message])
    

class World:
    def __init__(self):
        self.personas = {}
        self.distances = []
        self.rumor_visor = RumorVisor()
    
    def start(self, presonas_info: list[dict]):
        names = []
        for info in presonas_info:
            p = Persona(name=info['name'], first_name=info['first_name'], 
                        last_name=info['last_name'], age=info['age'], 
                        innate_traits=info['innate_traits'], 
                        lifestyle=info['lifestyle'], mendacity_level=info['mendacity_level'])
            self.personas[info['name']] = p
            names.append(info['name'])

        while True:
            answer = self.personas[names[0]].answer(names[1])
            self.personas[names[1]].get_answer(answer, names[0])
            print(f'{names[0]}: {answer}')
            time.sleep(5)
            answer = self.personas[names[1]].answer(names[0])
            self.personas[names[0]].get_answer(answer, names[1])
            print(f'{names[1]}: {answer}')
            time.sleep(5)


    def shuffle(self):
        pass


class RumorVisor:
    def __init__(self):
        self.rumors = []

    def add_rumor(self):
        pass

    def get_rumor(self):
        pass


if __name__ == '__main__':
    world = World()
    personas_info = [
    {
        "name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "age": 32,
        "innate_traits": ["charismatic", "intelligent"],
        "lifestyle": "active",
        "mendacity_level": 2
    },
    {
        "name": "Alice Smith",
        "first_name": "Alice",
        "last_name": "Smith",
        "age": 28,
        "innate_traits": ["creative", "perceptive"],
        "lifestyle": "bohemian",
        "mendacity_level": 4
    }
]
    world.start(personas_info)

