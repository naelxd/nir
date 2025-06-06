# TODO

## Основные задачи
- [x] Реализовать базовую структуру проекта
- [x] Создать класс Persona с основными характеристиками
- [x] Реализовать ассоциативную память
- [x] Интегрировать LLM для общения персон
- [x] Реализовать систему слухов
- [x] Добавить механизм взаимодействия между персонами
- [x] Реализовать симуляцию мира

## Улучшения
- [ ] Добавить визуализацию социальных связей
- [ ] Реализовать более сложные сценарии взаимодействия
- [ ] Добавить анализ эмоционального состояния персон
- [ ] Улучшить систему генерации слухов
- [ ] Добавить возможность сохранения и загрузки состояния симуляции

## Оптимизация
- [ ] Оптимизировать работу с LLM
- [ ] Улучшить производительность симуляции
- [ ] Добавить кэширование результатов LLM
- [ ] Оптимизировать работу с памятью

## Документация
- [ ] Добавить подробное описание API
- [ ] Создать примеры использования
- [ ] Добавить документацию по установке и настройке
- [ ] Описать процесс разработки и тестирования

## Реализовать память
- [x] Реализовать reflection logic в Persona.reflect()
- [x] Реализовать semantic search для relevant thoughts в AssociativeMemory.retrieve_relevant_thoughts()
- [ ] Добавить долговременную память для важных событий
- [ ] Реализовать забывание неважных событий со временем
- [ ] Добавить эмоциональную окраску к воспоминаниям

## Реализовать сохранение слухов
- [x] Реализовать add_rumor() в RumorVisor
- [x] Реализовать get_rumor() в RumorVisor
- [ ] Добавить сохранение слухов в файл
- [ ] Реализовать загрузку слухов из файла
- [ ] Добавить статистику по слухам

## Реализовать генерацию слухов
- [x] Реализовать rumor generation logic в Persona.generate_rumor()
- [ ] Улучшить генерацию слухов с учетом контекста
- [ ] Добавить разные типы слухов (позитивные/негативные)
- [ ] Реализовать влияние черт характера на тип слухов

## Реализовать проверку распространения слухов
- [x] Реализовать distance calculation на основе social relationships в World._update_distances()
- [x] Реализовать interaction logic в World._simulate_interaction()
- [ ] Добавить визуализацию распространения слухов
- [ ] Реализовать анализ скорости распространения
- [ ] Добавить факторы, влияющие на скорость распространения

## Реализовать мир и общение между агентами
- [x] Реализовать полноценное общение между агентами с учетом социальных дистанций
- [x] Реализовать систему проверки знания слухов персонами
- [x] Реализовать анализ изменений слухов при передаче
- [ ] Добавить групповые взаимодействия
- [ ] Реализовать формирование социальных групп
- [ ] Добавить влияние окружения на поведение агентов

## Новые задачи
- [ ] Реализовать сохранение состояния симуляции
- [ ] Добавить возможность настройки параметров симуляции
- [ ] Реализовать экспорт результатов симуляции
- [ ] Добавить систему метрик для оценки эффективности симуляции