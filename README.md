# 🐍 Snake AI: Deep Q-Learning Project

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)

Проект по созданию самообучающегося искусственного интеллекта для игры в «Змейку». Агент обучается с нуля, используя алгоритм **Deep Q-Learning (DQN)** на базе библиотеки **PyTorch**.

---

## 📺 Демонстрация
Проект включает в себя веб-панель управления, где можно в реальном времени наблюдать за процессом обучения и графиком эффективности (наград).

- **Game Stream**: Прямая трансляция игры из виртуального кадра.
- **Reward Graph**: Динамический график прогресса обучения.
- **Archive**: Видео готового результата и финальный график.

---

## 🧠 Обучение (Reinforcement Learning)

Агент (змейка) получает информацию о состоянии среды (11 параметров) и обучается максимизировать награду:
- **Еда (Красный)**: `+10` очков.
- **Выход (Синий)**: `+50` очков (переход на новый уровень).
- **Смерть**: `-10` очков.
- **Шаг**: `-0.1` (стимул не ходить кругами).

### Архитектура нейросети:
- **Input Layer**: 11 нейронов (состояние среды).
- **Hidden Layer**: 256 нейронов (ReLU активация).
- **Output Layer**: 3 нейрона (влево, прямо, вправо).

---

## 🛠 Инструкция по запуску

### 1. Склонируйте репозиторий:
```bash
git clone [https://github.com/ВАШ_НИК/snake-ai.git](https://github.com/ВАШ_НИК/snake-ai.git)
cd snake-ai




pip install torch pygame flask matplotlib opencv-python numpy
python app.py
python game.py




Структура 
app.py — Flask-сервер и стриминг видео.

game.py — Логика игры на Pygame (среда обучения).

agent.py — Логика DQN агента и работа с памятью.

model.py — Архитектура нейронной сети и тренер.

static/ — Статические файлы (графики, видео).

templates/ — HTML интерфейс.


