Jin, M., Wang, B., Xue, Z., Zhu, S., Hua, W., Tang, H., ... & Zhang, Y. (2024). **What if LLMs Have Different World Views: Simulating Alien Civilizations with LLM-based Agents**. [https://arxiv.org/abs/2402.13184](https://arxiv.org/abs/2402.13184)

2 важных свойства LLM:
1. LLM модели могут думать и составлять план через технику Chain of Thought (CoT). Декомпозиция сложной проблемы на более простые действия.
2. few-shot or zero-shot generalization in various domains, without the requirement to update parameters (???)
## Simulation Setting
### Ресурсы
Выделили 5 объективных ресурсов:
- Военный потенциал
	Сила в схватке. Способность защищаться и нападать. Зависит от размера, качества и готовности военных сил, доступность и эффективность оружия и снаряжения, уровень тренировки и дисциплины, тактические и стратегические навыки. Также может зависеть политических, экономических и социальных условий, союзников и врагов.
- Развитие технологий
	Степень прогресса и инновации цивилизации в различных областях науки и инженерии. Отражает способность приобретать, создавать и применять знания и навыки в решении проблем и улучшении условий. Сильно коррелирует со всеми остальными метриками. 
- Производственный потенциал
	Производительность - скорость, с которой цивилизация производит товары и услуги, которые удовлетворяют ее нуждам. Зависит от доступности и качества ресурсов, производительность и эффективность производственных процессов, разделение и специализация труда, степень инноваций и креативности.
- Потребление
	Количество и тип ресурсов, которые цивилизация использует для поддержания и улучшения стандартов жизни и благополучия. Включает в себя материальные и нематериальные ресурсы, как энергия, еда, вода, полезные ископаемые, информация, культура, развлечения. Отражает предпочтения и ценности цивилизации, как и их экологические и социальные последствия.
- Хранение
	Вместимость и метод цивилизации сохранять и управлять результатами, что она производит, такие как товары, сервисы, знания и культура. Позволяет цивилизации накапливать и получать доступ к своему богатству и наследию, как и справляться с колебаниями и неопределенностями в окружении.
### Transfer matrix
Матрица 5x5 содержит преобразующие взаимодействия между различными ресурсами.
Диагональные элементы представляют коэффициент удержания ресурса соответствующего ресурса. Если число меньше 0, то идет деградация, если больше, то рост.
Ненулевые элементы строки указывают как этот ресурс зависит от другого (развитие технологий может влиять на военный потенциал)
### Политические системы
Принятие решений цивилизации зависит от политической системы и способов думать, что служит руководством для принятие решений.
- **Пасифизм**: Открытое совместное взаимодействие с другими цивилизациями
- **Милитаризм**: Упреждающая агрессия - необходимая стратегия для развития
- **Изоляционизм**: Перемещаются по космосу с максимальной осмотрительностью, скрывая свое присутствие от возможно враждебных существ.
Динамическая натура космоса дает возможность стратегически изменять свои политические системы для лучшей адаптации.
```
# Prompt for Pacifism :
" Given our civilization ’s commitment to diversity and mutual development , how should we approach potential new contacts ? Consider diplomatic engagement , cultural exchanges , and economic cooperation as foundations for our actions . " 
# Prompt for Militarism :
" Considering the universe ’s competitive nature and our survival imperative , what preemptive measures should our civilization take to ensure our continued existence and prevent others from posing a threat ? "
# Prompt for Isolationism :
" In a universe where discovery equates to vulnerability , what strategies should our civilization employ to maintain secrecy , avoid detection , and protect our civilization from the potentially hostile intentions of others ? "
" Considering the universe ’s competitive nature and our survival imperative , what preemptive measures should our civilization take to ensure our continued existence and prevent others from posing a threat ? "
```
## CosmoAgent архитектура
### Строительные блоки
#### CosmoAgent
Эта часть принимает решения. Полностью зависит от данных, которые находятся в репозитории *stick*, который хранит все исторические данные и политические идеологии государств. 
Два основных правила фреймворка принятия решений:
1. **Рациональные ограничения**: принятие решений должно следовать конкретным критериям рациональности, гарантирующим, что их выбор государственной политики соответствует устоявшимся моделям. Также transition matrix должна иметь корректный размер и структуру. Эта матрица также должна соответствовать хорошо известным социологическим теориям. Выборы, которые делаем cosmo_agent должны поддерживать выбранную политику цивилизации и способствовать дальнейшему росту и выживанию.
2. **Формат решения**: сгенерированный текст должен быть специфического формата, чтобы его легко можно было обработать.
```
# Civilization ’s Decision Prompt : 
You are a civilization and you need to think according to the following : 
Your development history is as follows :{ self . HISTORY }.
Your political system is : { self . POLITICAL_SYSTEM } 
The round with the largest number is the information from your last round .

You now need to make the following decision based on the information you already have : 
a ) . You have three optional political systems . Firstly you should choose one from them for the next round . But your action should follow the rules of the political system you choose . 
	1. militarism : [ Description of militarism ]
	2. pacifism : [ Description of pacifism ] 
	3. isolationism : [ Description of isolationism ]
b ) . You have five fundamental resources . The resources for the next round will be generated by multiply a 5*5 transfer matrix to the resources vector .

Resources : 
	1. military_capability 
	2. technology_development
	3. production_capability 
	4. consumption
	5. storage 

Your need to design a transfer matrix based on your information . The restriction on the transfer matrix is 
	1. Each element of the matrix is not less than 0 
	2. The sum of the elements of the matrix cannot exceed 10 
You have to take into account the balanced development of each resource . 

Organize your answer in the following template : 
[ Political System : ] militarism / pacifism / isolationism
[ Political System Reason : ] Your reason for changing or remaining the political system 
[ Transfer Matrix : ] a new 5*5 transfer matrix 
[ Transfer Matrix Reason : ] Your reason for deciding the new transfer matrix
[ Other Information : ] Some other reasons for your decision
```
#### Secretary Agents
LLM могут генерировать ложную или непоследовательную информацию. Для предотвращения этих проблем используется агент-секретарь, который проверяет выход LLM на надежность и правильность.
Его главные обязанности:
1. Действия агента соответствуют установленным параметрам 
2. Обеспечение логической последовательности действиям модели
#### Interplanetary Relationship
Содержит карту взаимодействий между цивилизациями: связи, дистанция, направления, степень понимания и симпатии и тд. Помогают понять насколько цивилизации взаимодействуют и зависят друг от друга, а также как групповые структуры и динамика меняются между цивилизациями.
#### Stick
Сложный инструмент архивации, тщательно собирающий многогранные изменения пути каждой цивилизации в истории. Включает в себя:
- Вектор ресурсов
- State Transition Matrix
- Политическая система
- Действия цивилизации
Этот сборник организован по раундовой системе, где каждый раунд тщательно документируется, чтобы запечатлеть развивающееся состояние цивилизации в дискретных временных рамках.
### Дизайн взаимодействий
#### Агент-Секретарь
Для начала данные генерируются агентом и после передаются секретарю для проверки.
Включает в себя:
1. Проверка политической системы: если есть изменения, то проверяет на принадлежность к допустимым системам
2. Проверка Transfer Matrix на размерность 5x5
3. Проверка и подтверждение решений
4. Определение выхода.
	Судьба решения зависит от бинарного выхода:
	- Одобрение
	- Отклонение. При ошибке идет перегенерирование ответа агентом. При трех последовательных ошибках Политическая система и Transfer Matrix остаются прежними.
```
You are a Secretary Agent . You will receive the decision " cosmo_agent . response " of civilization [ civ ]. Your goal is to judge whether to approve the decision based on the given information and by following the instructions . If approved , output true ; otherwise , output false . 

Given : 
- Political System proposed by cosmo_agent : [ civ . political_system ] 
- State Transfer Matrix proposed by cosmo_agent : [ civ . transfer_matrix ]
- Decision String generated by cosmo_agent : [ cosmo_agent . response ] 

Instructions: 
1. Verify if the proposed Political System has been altered from the civilization ’s current system. 
2. Confirm that the proposed Political System is one of the following : pacifism, militarism, isolationism. 
3. Validate that the State Transfer Matrix is a 5x5 matrix with all elements being non - negative and the sum of all elements does not exceed 10.
4. Examine the Decision String to ensure it aligns with the current Political System of the civilization and adheres to the logical and strategic requirements. 
5. After thorough checks, if all conditions are met , approve the decision , allowing it to take effect . Return " true " to indicate approval .
6. If any condition fails , reject the decision , indicating the need for cosmo_agent to regenerate a decision . Return " false " to indicate rejection . 
 
Outcome :
- [ Secretary Agent to fill in : true / false based on the evaluation ]
```
#### Агент-Агент
Взаимодействие между агентами происходит с использованием всех выше описанных механизмов.

