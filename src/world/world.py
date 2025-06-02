from typing import Dict, List, Tuple
import numpy as np
import time
import random
from world.rumor_visor import RumorVisor
from agents.persona import Persona

class World:
    def __init__(self):
        self.personas: Dict[str, Persona] = {}
        self.distances: List[List[int]] = []
        self.rumor_visor = RumorVisor()
        self.current_cycle = 0
        self.rumor_knowledge: Dict[str, List[int]] = {}  # persona -> list of known rumor IDs
        self.epoch_to_shuffle_distance = 5  # N эпох для изменения дистанции
        self.RUMOR_PERIOD = 10  # N эпох для генерации нового слуха
        self.SHUFFLE_PERIOD = 10  # N эпох для перемешивания пар
        
    def add_persona(self, persona_data: dict) -> None:
        """Add a persona to the world"""
        persona = Persona(
            name=persona_data["name"],
            first_name=persona_data["first_name"],
            last_name=persona_data["last_name"],
            age=persona_data["age"],
            innate_traits=persona_data["innate_traits"],
            lifestyle=persona_data["lifestyle"],
            model_type=persona_data.get("model_type", "llama"),
            api_key=persona_data.get("api_key")
        )
        self.personas[persona_data["name"]] = persona
        self.rumor_knowledge[persona.name] = []
        self._update_distances()
        
    def _update_distances(self) -> None:
        """Update the social distance matrix with random distances"""
        n = len(self.personas)
        self.distances = [[0] * n for _ in range(n)]  # Initialize n x n matrix
        
        # Get persona names in order
        names = list(self.personas.keys())
        
        for i, name1 in enumerate(names):
            for j, name2 in enumerate(names):
                if i != j:  # Skip self-distance
                    # Generate random distance between 1 and 10
                    distance = random.randint(1, 10)
                    self.distances[i][j] = distance
                
    def start(self, personas_info: List[Dict], max_cycles: int = 100) -> None:
        """Start the simulation with given personas
        
        Args:
            personas_info: List of dictionaries with persona information
            max_cycles: Maximum number of simulation cycles to run
        """
        # Initialize personas
        for info in personas_info:
            p = Persona(
                name=info['name'],
                first_name=info['first_name'],
                last_name=info['last_name'],
                age=info['age'],
                innate_traits=info['innate_traits'],
                lifestyle=info['lifestyle'],
                model_type=info.get("model_type", "llama"),
                api_key=info.get("api_key")
            )
            self.personas[info['name']] = p
            self.rumor_knowledge[p.name] = []
            
        # Initialize distance matrix
        self.shuffle()
        
        print("\nНачальная матрица социальных дистанций:")
        names = list(self.personas.keys())
        for i, name1 in enumerate(names):
            for j, name2 in enumerate(names):
                if i != j:
                    print(f"{name1} -> {name2}: {self.distances[i][j]}")

        print(f"\nЗапуск симуляции на {max_cycles} циклов...")
        while self.current_cycle < max_cycles:
            self.run_cycle()
            time.sleep(5)
            
        print(f"\nСимуляция завершена после {self.current_cycle} циклов")
        
        # Вывод информации о слухах
        print("\nСтатистика по слухам:")
        print("=" * 50)
        
        all_rumors = self.rumor_visor.get_all_rumors()
        if not all_rumors:
            print("За время симуляции не было создано ни одного слуха")
            return
        else:
            print(f"Всего создано слухов: {len(all_rumors)}")
        
        # Статистика по каждому слуху
        for i, rumor in enumerate(all_rumors, 1):
            stats = self.rumor_visor.get_rumor_stats(rumor.node_id)
            network = self.rumor_visor.get_rumor_network(rumor.node_id)
            
            print(f"\nСлух #{i}:")
            print(f"Создатель: {stats['creator']}")
            print(f"Содержание: {stats['content']}")
            print(f"Количество передач: {stats['spread_count']}")
            
            if network and network["edges"]:
                print("\nПуть распространения:")
                for spread in rumor.spread_history:
                    print(f"Итерация {spread['timestamp']}: {spread['spreader']} -> {spread['receiver']}")
            else:
                print("\nСлух не был передан другим агентам")
            
            print("-" * 30)
        
    def shuffle(self) -> None:
        """Shuffle the order of personas for interaction based on minimum distances"""
        self._update_distances()
        names = list(self.personas.keys())
        n = len(names)
        
        # Создаем список всех возможных пар с их дистанциями
        all_pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                all_pairs.append((i, j, self.distances[i][j]))
        
        # Сортируем пары по возрастанию дистанции
        all_pairs.sort(key=lambda x: x[2])
        
        # Жадный алгоритм: выбираем пары с минимальной дистанцией,
        # избегая повторного использования агентов
        used = set()
        self.pairs = []
        
        for i, j, dist in all_pairs:
            if i not in used and j not in used:
                self.pairs.append((i, j))
                used.add(i)
                used.add(j)
                
        print("\nНовые пары для взаимодействия:")
        for idx1, idx2 in self.pairs:
            print(f"{names[idx1]} <-> {names[idx2]} (дистанция: {self.distances[idx1][idx2]})")
        
    def run_cycle(self) -> None:
        """Run one cycle of the simulation"""
        self.current_cycle += 1
        if self.current_cycle % self.SHUFFLE_PERIOD == 0:
            self.shuffle()

        if self.current_cycle % self.RUMOR_PERIOD == 0:
            self._generate_new_rumor()

        names = list(self.personas.keys())
        # Если нечетное количество, один агент не общается
        for idx1, idx2 in self.pairs:
            self._simulate_interaction(self.personas[names[idx1]], self.personas[names[idx2]])
        
    def _generate_new_rumor(self) -> None:
        """Generate a new rumor from a random persona"""
        if not self.personas:
            return
            
        creator = np.random.choice(list(self.personas.values()))
        rumor_content = creator.generate_rumor()
        rumor_id = self.rumor_visor.add_rumor(rumor_content, creator.name, self.current_cycle)
        
        # Add rumor to creator's knowledge
        self.rumor_knowledge[creator.name].append(rumor_id)
        print(f"\nНовый слух от {creator.name}: {rumor_content}")
        
    def _simulate_interaction(self, persona1: Persona, persona2: Persona) -> None:
        """Simulate an interaction between two personas"""
        print(f"\nВзаимодействие между {persona1.name} и {persona2.name}")
        
        # Получаем слухи для передачи
        rumors1 = [self.rumor_visor.get_rumor(rid) for rid in self.rumor_knowledge[persona1.name]]
        rumors2 = [self.rumor_visor.get_rumor(rid) for rid in self.rumor_knowledge[persona2.name]]
        
        # Выбираем случайное количество слухов для передачи (1-3)
        num_rumors1 = min(random.randint(1, 3), len(rumors1))
        num_rumors2 = min(random.randint(1, 3), len(rumors2))
        
        # Выбираем случайные слухи для передачи
        rumors_to_share1 = random.sample(rumors1, num_rumors1) if rumors1 else []
        rumors_to_share2 = random.sample(rumors2, num_rumors2) if rumors2 else []
        
        # Агент 1 отвечает, вставляя свои слухи
        rumor_text1 = "\n".join([f"{i+1}. Кстати, я слышал: {r.content}" for i, r in enumerate(rumors_to_share1)])
        answer1, used_rumors1 = persona1.answer(persona2.name, rumor=rumor_text1 if rumor_text1 else None)
        persona2.get_answer(answer1, persona1.name)
        print(f'{persona1.name}: {answer1}')
        
        # Передаем только использованные слухи от persona1 к persona2
        for rumor_idx in used_rumors1:
            if 0 <= rumor_idx - 1 < len(rumors_to_share1):
                rumor = rumors_to_share1[rumor_idx - 1]
                if rumor.node_id not in self.rumor_knowledge[persona2.name]:
                    self.rumor_visor.track_rumor_spread(rumor.node_id, persona1.name, persona2.name, self.current_cycle)
                    self.rumor_knowledge[persona2.name].append(rumor.node_id)
                    print(f"{persona1.name} передал слух {persona2.name}: {rumor.content}")
        
        # Агент 2 отвечает, вставляя свои слухи
        rumor_text2 = "\n".join([f"{i+1}. Кстати, я слышал: {r.content}" for i, r in enumerate(rumors_to_share2)])
        answer2, used_rumors2 = persona2.answer(persona1.name, rumor=rumor_text2 if rumor_text2 else None)
        persona1.get_answer(answer2, persona2.name)
        print(f'{persona2.name}: {answer2}')
        
        # Передаем только использованные слухи от persona2 к persona1
        for rumor_idx in used_rumors2:
            if 0 <= rumor_idx - 1 < len(rumors_to_share2):
                rumor = rumors_to_share2[rumor_idx - 1]
                if rumor.node_id not in self.rumor_knowledge[persona1.name]:
                    self.rumor_visor.track_rumor_spread(rumor.node_id, persona2.name, persona1.name, self.current_cycle)
                    self.rumor_knowledge[persona1.name].append(rumor.node_id)
                    print(f"{persona2.name} передал слух {persona1.name}: {rumor.content}")
