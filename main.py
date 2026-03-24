import tkinter as tk
from tkinter import messagebox
import random


class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабиринт")
        self.root.geometry("1000x700")

        # Фиксированный размер окна
        self.root.resizable(False, False)
        self.root.configure(bg='gray')

        # Отключаем кнопку развернуть
        self.root.attributes('-toolwindow', True)

        self.player_size = 20  # Размер игрока
        self.step = 20  # Шаг движения

        # Создаем Panel
        self.panel = tk.Frame(root, bg='white', relief=tk.SUNKEN, bd=3)
        self.panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Холст для рисования
        self.canvas = tk.Canvas(self.panel, bg='white', highlightthickness=2,
                                highlightbackground='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set()

        # Создаем ПРОХОДИМЫЙ лабиринт
        self.create_maze()

        # Создаем движущиеся шарики (враги)
        self.create_balls()

        # Создаем игрока
        self.create_player()

        # Запускаем движение шариков
        self.move_balls()

        # Обработчики событий
        self.canvas.bind('<Key>', self.key_press)

        # Устанавливаем игрока на старт
        self.root.after(100, self.set_initial_position)

    def create_maze(self):
        """Создание ПРОХОДИМОГО лабиринта"""

        self.walls = [
            # Внешние стены (с проходами!)
            (50, 50, 950, 70),  # Верхняя стена
            (50, 630, 950, 650),  # Нижняя стена
            (50, 50, 70, 300),  # Левая стена верхняя часть
            (50, 400, 70, 650),  # Левая стена нижняя часть (с проходом 300-400)
            (930, 50, 950, 300),  # Правая стена верхняя часть
            (930, 400, 950, 650),  # Правая стена нижняя часть (с проходом 300-400)

            # Внутренние стены - создают коридоры
            (200, 50, 220, 250),  # Вертикальная стена слева
            (400, 200, 420, 450),  # Вертикальная стена в центре
            (600, 100, 620, 350),  # Вертикальная стена
            (800, 300, 820, 550),  # Вертикальная стена справа

            (150, 200, 450, 220),  # Горизонтальная стена вверху
            (350, 350, 650, 370),  # Горизонтальная стена в центре
            (550, 450, 850, 470),  # Горизонтальная стена внизу
            (250, 500, 450, 520),  # Горизонтальная стена

            # Короткие стены для создания лабиринта
            (500, 200, 520, 300),  # Вертикальная короткая
            (300, 300, 320, 400),  # Вертикальная короткая
            (700, 400, 720, 500),  # Вертикальная короткая
            (150, 400, 170, 500),  # Вертикальная короткая
        ]

        # Отрисовываем стены
        for wall in self.walls:
            self.canvas.create_rectangle(wall, fill='gray', outline='black', width=2)

        # Старт и финиш (в доступных местах)
        self.start = (100, 100, 140, 140)  # Старт в левом верхнем углу
        self.finish = (860, 560, 900, 600)  # Финиш в правом нижнем углу

        self.start_rect = self.canvas.create_rectangle(self.start,
                                                       fill='lightgreen',
                                                       outline='darkgreen',
                                                       width=2)
        self.start_text = self.canvas.create_text(120, 80,
                                                  text="СТАРТ",
                                                  font=('Arial', 10, 'bold'),
                                                  fill='darkgreen')

        self.finish_rect = self.canvas.create_rectangle(self.finish,
                                                        fill='lightcoral',
                                                        outline='darkred',
                                                        width=2)
        self.finish_text = self.canvas.create_text(880, 540,
                                                   text="ФИНИШ",
                                                   font=('Arial', 10, 'bold'),
                                                   fill='darkred')

        self.obstacles = [
            (250, 250, 280, 280),
            (450, 150, 480, 180),
            (650, 350, 680, 380),
            (350, 450, 380, 480),
        ]

        for obs in self.obstacles:
            self.canvas.create_rectangle(obs, fill='yellow', outline='orange', width=2)

            x1, y1, x2, y2 = obs
            self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2)
            self.canvas.create_line(x1, y2, x2, y1, fill='red', width=2)

    def create_balls(self):
        """Создание движущихся шариков"""
        self.balls = []

        ball_data = [
            {'x': 300, 'y': 200, 'radius': 12, 'dx': 5, 'dy': 3, 'color': 'red'},
            {'x': 500, 'y': 300, 'radius': 15, 'dx': -4, 'dy': 4, 'color': 'orange'},
            {'x': 700, 'y': 400, 'radius': 10, 'dx': 6, 'dy': -3, 'color': 'purple'},
            {'x': 200, 'y': 500, 'radius': 12, 'dx': -5, 'dy': -4, 'color': 'blue'},
            {'x': 400, 'y': 150, 'radius': 14, 'dx': 4, 'dy': 5, 'color': 'green'},
            {'x': 600, 'y': 550, 'radius': 11, 'dx': -6, 'dy': 3, 'color': 'brown'},
        ]

        for ball in ball_data:
            ball_id = self.canvas.create_oval(
                ball['x'] - ball['radius'], ball['y'] - ball['radius'],
                ball['x'] + ball['radius'], ball['y'] + ball['radius'],
                fill=ball['color'], outline='black', width=2
            )

            highlight = self.canvas.create_oval(
                ball['x'] - ball['radius'] + 3, ball['y'] - ball['radius'] + 3,
                ball['x'] + ball['radius'] - 7, ball['y'] + ball['radius'] - 7,
                fill='white', outline='', stipple='gray50'
            )

            self.balls.append({
                'id': ball_id,
                'highlight': highlight,
                'x': ball['x'],
                'y': ball['y'],
                'radius': ball['radius'],
                'dx': ball['dx'],
                'dy': ball['dy'],
                'color': ball['color']
            })

    def create_player(self):
        """Создание игрока (синий шарик)"""
        self.player = self.canvas.create_oval(
            self.start[0] + 5, self.start[1] + 5,
            self.start[2] - 5, self.start[3] - 5,
            fill='deepskyblue', outline='darkblue', width=3
        )

        self.player_highlight = self.canvas.create_oval(
            self.start[0] + 10, self.start[1] + 10,
            self.start[0] + 20, self.start[1] + 20,
            fill='white', outline='', stipple='gray50'
        )

        # Глазки
        self.player_eye1 = self.canvas.create_oval(
            self.start[0] + 15, self.start[1] + 10,
            self.start[0] + 17, self.start[1] + 12,
            fill='black'
        )
        self.player_eye2 = self.canvas.create_oval(
            self.start[0] + 23, self.start[1] + 10,
            self.start[0] + 25, self.start[1] + 12,
            fill='black'
        )

    def set_initial_position(self):
        """Установка начальной позиции игрока"""
        self.move_player_to(120, 120)

    def key_press(self, event):
        """Обработка нажатий клавиш"""
        dx = dy = 0
        if event.keysym == 'Up':
            dy = -self.step
        elif event.keysym == 'Down':
            dy = self.step
        elif event.keysym == 'Left':
            dx = -self.step
        elif event.keysym == 'Right':
            dx = self.step
        else:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.player)
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        new_x = cx + dx
        new_y = cy + dy

        if new_x < 70 or new_x > 930 or new_y < 70 or new_y > 600:
            return

        player_bbox = (new_x - 15, new_y - 15, new_x + 15, new_y + 15)
        for wall in self.walls:
            if self.rect_overlap(player_bbox, wall):
                return

        self.move_player_to(new_x, new_y)

    def move_player_to(self, x, y):
        """Перемещение игрока"""
        self.canvas.coords(self.player,
                           x - 15, y - 15,
                           x + 15, y + 15)

        self.canvas.coords(self.player_highlight,
                           x - 5, y - 5,
                           x + 5, y + 5)

        self.canvas.coords(self.player_eye1,
                           x - 5, y - 5,
                           x - 3, y - 3)
        self.canvas.coords(self.player_eye2,
                           x + 3, y - 5,
                           x + 5, y - 3)

        self.check_collisions(x, y)

    def move_balls(self):
        """Движение шариков"""
        for ball in self.balls:
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']

            if ball['x'] < 80 or ball['x'] > 920:
                ball['dx'] = -ball['dx']
            if ball['y'] < 80 or ball['y'] > 600:
                ball['dy'] = -ball['dy']

            ball_bbox = (ball['x'] - ball['radius'], ball['y'] - ball['radius'],
                         ball['x'] + ball['radius'], ball['y'] + ball['radius'])

            for wall in self.walls:
                if self.rect_overlap(ball_bbox, wall):
                    if abs(ball['x'] - (wall[0] + wall[2]) / 2) > abs(ball['y'] - (wall[1] + wall[3]) / 2):
                        ball['dx'] = -ball['dx']
                    else:
                        ball['dy'] = -ball['dy']
                    break

            self.canvas.coords(ball['id'],
                               ball['x'] - ball['radius'], ball['y'] - ball['radius'],
                               ball['x'] + ball['radius'], ball['y'] + ball['radius'])

            self.canvas.coords(ball['highlight'],
                               ball['x'] - ball['radius'] + 3, ball['y'] - ball['radius'] + 3,
                               ball['x'] + ball['radius'] - 7, ball['y'] + ball['radius'] - 7)

        self.check_ball_collisions()

        self.root.after(50, self.move_balls)

    def check_ball_collisions(self):
        """Проверка столкновений игрока с шариками"""
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        pcx = (x1 + x2) // 2
        pcy = (y1 + y2) // 2

        for ball in self.balls:
            distance = ((pcx - ball['x']) ** 2 + (pcy - ball['y']) ** 2) ** 0.5
            if distance < (15 + ball['radius']):
                self.ball_collision()

    def ball_collision(self):
        """Обработка столкновения с шариком"""
        messagebox.showwarning("Столкновение!", "Вы столкнулись с шариком! Возврат на старт.")
        self.reset_to_start()

    def check_collisions(self, x, y):
        """Проверка столкновений"""
        player_bbox = (x - 15, y - 15, x + 15, y + 15)

        if self.rect_overlap(player_bbox, self.finish):
            self.show_victory()
            return

        for obs in self.obstacles:
            if self.rect_overlap(player_bbox, obs):
                messagebox.showwarning("Препятствие", "Вы наступили на препятствие!")
                self.reset_to_start()
                return

    def rect_overlap(self, r1, r2):
        """Проверка пересечения прямоугольников"""
        return not (r1[2] < r2[0] or r1[0] > r2[2] or
                    r1[3] < r2[1] or r1[1] > r2[3])

    def reset_to_start(self):
        """Возврат на старт"""
        self.move_player_to(120, 120)

    def show_victory(self):
        """Показ сообщения о победе"""
        if messagebox.askyesno("Победа!", "Вы достигли финиша! Хотите сыграть снова?"):
            self.reset_to_start()

    def create_info_panel(self):
        """Создание информационной панели"""
        info_frame = tk.Frame(self.root, bg='lightgray', height=60)
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        info_label = tk.Label(info_frame,
                              text=" УПРАВЛЕНИЕ: Стрелки |  ЦЕЛЬ: Дойти до красного финиша |  ДВИЖУЩИЕСЯ ШАРИКИ: Увернись от них! |  ЖЕЛТЫЕ БЛОКИ: Препятствия",
                              bg='lightgray', font=('Arial', 11), wraplength=950)
        info_label.pack(pady=5)


        hint_label = tk.Label(info_frame,
                              text="💡 ПОДСКАЗКА: Ищи проходы! Лабиринт проходимый, просто найди путь!",
                              bg='yellow', font=('Arial', 11, 'bold'))
        hint_label.pack(pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    game.create_info_panel()
    root.mainloop()
