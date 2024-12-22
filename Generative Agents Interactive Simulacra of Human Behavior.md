Generative Agents: Interactive Simulacra of Human Behavior (2023) [https://github.com/joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents)

# Архитектура агента

## Память и извлечение
**Поток памяти** содержит обширную запись опыта агента.
Запись включает описание, время создания и недавнее время обращения.
Самый базовый элемент - наблюдение (действия самого агента и наблюдаемые действия других агентов и объектов)

**Извлечение** имплементировано с фокусом на 3 важных компонента
- Новизна
	Используется функция exponential decay над количеством часов последнего обращения к записи. 
- Важность
	Разделяет рутинные действия от важных событий. К примеру потребление завтрака будет иметь меньшую оценку, чем расставание с близким человеком.	
	```
	On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory. 
	Memory: buying groceries at The Willows Market and Pharmacy
	Rating: <fill in>
	```
- Релевантность
	Присваивает большую оценку к тем событиям, которые сильнее относятся к текущей ситуации.
	Они используют модель для генерации эмбединга для описания событий и считают релевантность с помощью косинусного подобия между ними.
Для посчета используется min-max scaling для нормализации новизны, важности и релевантности.
Итоговая оценка выглядит как 𝑠𝑐𝑜𝑟𝑒 = 𝛼𝑟𝑒𝑐𝑒𝑛𝑐𝑦 · 𝑟𝑒𝑐𝑒𝑛𝑐𝑦 + 𝛼𝑖𝑚𝑝𝑜𝑟𝑡𝑎𝑛𝑐𝑒 ·𝑖𝑚𝑝𝑜𝑟𝑡𝑎𝑛𝑐𝑒 +𝛼𝑟𝑒𝑙𝑒𝑣𝑎𝑛𝑐𝑒 ·𝑟𝑒𝑙𝑒𝑣𝑎𝑛𝑐𝑒, 
где 𝛼s равно 1

## Рефлексия
Второй тип записей в памяти - рефлексия. Это более высокоуровневые, абстрактные мысли агента. Генерируются периодически (в данной исплементации генерируются когда сумма важностей последних событий превосходит определенного порога, в данном случае 150)
```
Statements about Klaus Mueller 
1. Klaus Mueller is writing a research paper 
2. Klaus Mueller enjoys reading a book on gentrification 
3. Klaus Mueller is conversing with Ayesha Khan about exercising [...] 
What 5 high-level insights can you infer from the above statements? (example format: insight (because of 1, 5, 3))
```
Пример ответа 
```
Klaus Mueller is dedicated to his research on gentrification (because of 1, 2, 8, 15)
```
Агенты могут рефлексировать не только над наблюдениями, но и над другими рефлексиями, делая их более высокоуровневыми.

## Планирование и реагирование
Планы описывают будущие действия агента, чтобы сохранить поведение агента постоянным. План состоит из места, времени начала и продолжительности.
Как и рефлексии планы хранятся в потоке памяти и включены в процесс извлечения. Агенты могут менять свои планы.
```
Name: Eddy Lin (age: 19) Innate traits: friendly, outgoing, hospitable 
Eddy Lin is a student at Oak Hill College studying music theory and composition. He loves to explore different musical styles and is always looking for ways to expand his knowledge. Eddy Lin is working on a composition project for his college class. He is taking classes to learn more about music theory. Eddy Lin is excited about the new composition he is working on but he wants to dedicate more hours in the day to work on it in the coming days 
On Tuesday February 12, Eddy 1) woke up and completed the morning routine at 7:00 am, [. . . ] 6) got ready to sleep around 10 pm. 
Today is Wednesday February 13. Here is Eddy’s plan today in broad strokes: 1)
```
Пример вывода:
```
“1) wake up and complete the morning routine at 8:00 am, 2) go to Oak Hill College to take classes starting 10:00 am, [. . . ] 5) work on his new music composition from 1:00 pm to 5:00 pm, 6) have dinner at 5:30 pm, 7) finish school assignments and go to bed by 11:00 pm.”
```
Все сохраняется в поток памяти и рекурсивно декомпозируется на более мелкие куски, к примеру
```
1:00 pm: start by brainstorming some ideas for his music composition [...] 4:00 pm: take a quick break and recharge his creative energy before reviewing and polishing his composition
```
Далее
```
4:00 pm: grab a light snack, such as a piece of fruit, a granola bar, or some nuts. 4:05 pm: take a short walk around his workspace [...] 4:50 pm: take a few minutes to clean up his workspace
```

### Реагирование и изменение планов
Агенты оперируют в цикле, где в каждый промежуток времени они воспринимают мир вокруг и эти наблюдения сохраняются в потоке памяти.
```
[Agent’s Summary Description]
It is February 13, 2023, 4:56 pm. John Lin’s status: John is back home early from work. 
Observation: John saw Eddy taking a short walk around his workplace. 
Summary of relevant context from John’s memory: Eddy Lin is John’s Lin’s son. Eddy Lin has been working on a music composition for his class. Eddy Lin likes to walk around the garden when he is thinking about or listening to music. 
Should John react to the observation, and if so, what would be an appropriate reaction?
```
Контекст генерируется использую два вопроса, которые извлекают информацию из памяти: 
```
What is [observer]’s relationship with the [observed entity]?” and 
“[Observed entity] is [action status of the observed entity]”
```
И эти ответы резюмируются.

Результатом может быть
```
John could consider asking Eddy about his music composition project.
```
### Диалог
Инициализация разговора
```
[Agent’s Summary Description] 
It is February 13, 2023, 4:56 pm.
John Lin’s status: John is back home early from work. 
Observation: John saw Eddy taking a short walk around his workplace. 
Summary of relevant context from John’s memory: Eddy Lin is John’s Lin’s son. Eddy Lin has been working on a music composition for his class. Eddy Lin likes to walk around the garden when he is thinking about or listening to music. 
John is asking Eddy about his music composition project. What would he say to Eddy?
```
Результат:
```
“Hey Eddy, how’s the music composition project for your class coming along?”
```
Ответ генерируется используя историю данного диалога
```
[Agent’s Summary Description] 
It is February 13, 2023, 4:56 pm. 
Eddy Lin’s status: Eddy is taking a short walk around his workplace. 
Observation: John is initiating a conversation with Eddy. 
Summary of relevant context from Eddy’s memory: John Lin is Eddy Lin’s father. John Lin is caring and is interested to learn more about Eddy Lin’s school work. John Lin knows that Eddy Lin is working on a music composition. 
Here is the dialogue history: 
John: Hey Eddy, how’s the music composition project for your class coming along?
How would Eddy respond to John?
```
Результат: 
```
“Hey Dad, it’s going well. I’ve been taking walks around the garden to clear my head and get some inspiration.”
```
Далее продолжается, пока кто-либо не захочет закончить диалог

# Архитектура окружения
Агенты оперируют используя словесный язык. 
Чтобы представлять окружение используется структура дерева, где связи между объектами реализована с помощью ребер (например плита является ребенком кухни и рендерится в "плита на кухне")
Агенты строят деревья, когда попадают в окружение. Каждый агент инициализируется с соответствующими графами, его дом, работа, посещенные магазины и тд.
Во время перемещения по среде они обновляют дерево. Но когда выходят из зоны, эти данные не обновляются, пока они снова ее не посетят.
Промпт, если Эдди хочет пройтись по своему рабочему месту
```
[Agent’s Summary Description] Eddy Lin is currently in The Lin family’s house: Eddy Lin’s bedroom: desk) that has Mei and John Lin’s bedroom, Eddy Lin’s bedroom, common room, kitchen, bathroom, and garden. 
Eddy Lin knows of the following areas: The Lin family’s house, Johnson Park, Harvey Oak Supply Store, The Willows Market and Pharmacy, Hobbs Cafe, The Rose and Crown Pub. 
* Prefer to stay in the current area if the activity can be done there. 
* Eddy Lin is planning to take a short walk around his workspace. Which area should Eddy Lin go to?
```
Это выводит The Lin family’s house. Далее рекурсивно The Lin family’s house: garden: house garden