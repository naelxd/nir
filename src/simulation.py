import os
import sys
import argparse

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from world.world import World

def assign_models(personas: list[dict], model_type: str, api_key: str = None) -> list[dict]:
    """Assign the specified model to all personas"""
    if model_type not in ["llama", "chatgpt"]:
        raise ValueError("Model type must be either 'llama' or 'chatgpt'")
    
    for persona in personas:
        persona["model_type"] = model_type
        persona["api_key"] = api_key if model_type == "chatgpt" else None
    
    return personas

def create_personas() -> list[dict]:
    """Create a list of 5 personas with different characteristics"""
    return [
        {
            "name": "Алексей Петров",
            "first_name": "Алексей",
            "last_name": "Петров",
            "age": 25,
            "innate_traits": "общительный,энергичный,любознательный",
            "lifestyle": "активный"
        },
        {
            "name": "Мария Иванова",
            "first_name": "Мария",
            "last_name": "Иванова",
            "age": 30,
            "innate_traits": "аналитичный,осторожный,наблюдательный",
            "lifestyle": "спокойный"
        },
        {
            "name": "Дмитрий Соколов",
            "first_name": "Дмитрий",
            "last_name": "Соколов",
            "age": 28,
            "innate_traits": "креативный,импульсивный,эмоциональный",
            "lifestyle": "творческий"
        },
        {
            "name": "Елена Кузнецова",
            "first_name": "Елена",
            "last_name": "Кузнецова",
            "age": 35,
            "innate_traits": "практичный,организованный,ответственный",
            "lifestyle": "деловой"
        },
        {
            "name": "Иван Морозов",
            "first_name": "Иван",
            "last_name": "Морозов",
            "age": 22,
            "innate_traits": "общительный,импульсивный,любопытный",
            "lifestyle": "активный"
        }
    ]

def main():
    """Main function to run the simulation"""
    parser = argparse.ArgumentParser(description='Run the social simulation')
    parser.add_argument('--model', type=str, default='llama',
                      choices=['llama', 'chatgpt'],
                      help='Model to use for all personas (llama or chatgpt)')
    parser.add_argument('--api-key', type=str,
                      help='API key for ChatGPT (required if model is chatgpt)')
    
    args = parser.parse_args()
    
    # Создаем персон и назначаем модель
    personas = create_personas()
    personas = assign_models(personas, args.model, args.api_key)
    
    if args.model == "chatgpt" and not args.api_key:
        print("Error: API key is required for ChatGPT model")
        sys.exit(1)
    
    print(f"Запуск симуляции с 5 агентами (модель: {args.model})...")
    
    # Create world and personas
    world = World()
    
    print("\nХарактеристики агентов:")
    for persona in personas:
        print(f"\n{persona['name']} ({persona['age']} лет)")
        print(f"Черты характера: {persona['innate_traits']}")
        print(f"Образ жизни: {persona['lifestyle']}")
        print(f"Модель: {persona['model_type']}")
    
    print("\nНачало симуляции...")
    print("=" * 50)
    
    # Start the simulation
    world.start(personas)

if __name__ == "__main__":
    main() 