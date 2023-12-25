import tkinter as tk
from collections import deque
from tkinter import *
from tkinter import messagebox


class MazeDrawer:
    def __init__(self, rows, cols):
        self.start_cell = None
        self.goal_cells = []
        self.rows = rows
        self.cols = cols
        self.root = tk.Tk()
        self.root.state("zoomed")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window closing
        self.canvas = tk.Canvas(self.root, width=w.winfo_width(), height=w.winfo_height(), bg="white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.draw_wall)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<Button-3>", self.set_start_or_goal)
        self.drawing = False
        self.count_initial_goal = 0
        self.start = False
        self.is_running = False
        self.delete = False
        run_button = tk.Button(self.root, text="Run BFS", command=self.bfs_search)
        dfs_button = tk.Button(self.root, text="Run DFS", command=self.dfs_search)
        greedy_button = tk.Button(self.root, text="Run Greedy", command=self.greedy_search)
        edit_button = tk.Button(self.root, text="Delete", command=self.Delete)
        dfs_button.place(x=w.winfo_width() - 150, y=70)
        run_button.place(x=w.winfo_width() - 150, y=105)
        greedy_button.place(x=w.winfo_width() - 150, y=140)
        edit_button.place(x=w.winfo_width() - 150, y=175)
        self.width = w.winfo_width() // cols
        self.height = (w.winfo_height() - 100) // rows
        if self.width > self.height:
            self.width = self.height

        self.maze = [[0 if row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1 else 1
                      for col in range(self.cols)] for row in range(self.rows)]
        # Draw the borders as black
        for row in range(self.rows):
            for col in range(self.cols):
                fill_color = "black" if self.maze[row][col] == 0 else "white"
                self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                             (row + 1) * self.height, fill=fill_color)

    def draw_wall(self, event):
        if self.drawing and not self.delete:
            col = event.x // self.width
            row = event.y // self.height
            if 1 <= row < self.rows - 1 and 1 <= col < self.cols - 1 and self.maze[row][col] != 2 and self.maze[row][
                col] != 3:
                self.maze[row][col] = 0
                self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                             (row + 1) * self.height, fill="black")
        elif self.delete:
            col = event.x // self.width
            row = event.y // self.height
            if self.maze[row][col] == 0 and 1 <= row < self.rows - 1 and 1 <= col < self.cols - 1:
                self.maze[row][col] = 1
                self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                             (row + 1) * self.height, fill="white")

    def Delete(self):
        if not self.delete:
            self.redraw_maze()
            self.delete = True
        else:
            self.delete = False

    def set_start_or_goal(self, event):
        col = event.x // self.width
        row = event.y // self.height
        if not self.delete:
            if 1 <= row < self.rows - 1 and 1 <= col < self.cols - 1:
                current_color = self.canvas.itemcget(self.canvas.find_closest(event.x, event.y), "fill")

                if event.num == 3 and not self.start:  # Left click for setting start cell
                    if current_color == "white" or current_color == "red":
                        if current_color == "red":
                            self.maze[row][col] = 3
                        else:
                            self.maze[row][col] = 2
                        self.start_cell = (row, col)
                        self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                     (row + 1) * self.height, fill="green")
                        self.canvas.create_text((col + 0.5) * self.width, (row + 0.5) * self.height, text="S",
                                                font=("Arial", self.width // 3),
                                                fill="white")
                        self.count_initial_goal += 1
                        self.start = True
                elif event.num == 3 and self.start:  # Right click for setting goal cell(s)
                    if current_color == "white" or current_color == "green":
                        self.maze[row][col] = 3
                        self.goal_cells.append((row, col))
                        self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                     (row + 1) * self.height, fill="red")
                        self.canvas.create_text((col + 0.5) * self.width, (row + 0.5) * self.height, text="G",
                                                font=("Arial", self.width // 3),
                                                fill="white")
        else:
            if 1 <= row < self.rows - 1 and 1 <= col < self.cols - 1 and event.num == 3:
                if (row, col) in self.goal_cells:
                    self.goal_cells.remove((row, col))
                    if self.start_cell[0] == row and self.start_cell[1] == col:
                        self.maze[row][col] = 2
                        self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                     (row + 1) * self.height, fill="green")
                        self.canvas.create_text((col + 0.5) * self.width, (row + 0.5) * self.height, text="S",
                                                font=("Arial", self.width // 3),
                                                fill="white")
                    else:
                        self.maze[row][col] = 1
                        self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                     (row + 1) * self.height, fill="white")
                elif self.start_cell[0] == row and self.start_cell[
                    1] == col and self.start:  # right click for setting start cell
                    self.maze[row][col] = 1
                    self.start_cell = None
                    self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                 (row + 1) * self.height, fill="white")
                    self.start = False

    def redraw_maze(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.start_cell:
                    fill_color = "green"
                elif (row, col) in self.goal_cells:
                    fill_color = "red"
                elif self.maze[row][col] == 0:
                    fill_color = "black"
                else:
                    fill_color = "white"
                self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                             (row + 1) * self.height, fill=fill_color)
                if (row, col) in self.start_cell:
                    self.canvas.create_text((col + 0.5) * self.width, (row + 0.5) * self.height, text="S",
                                            font=("Arial", self.width // 3),
                                            fill="white")
                elif (row, col) in self.goal_cells:
                    self.canvas.create_text((col + 0.5) * self.width, (row + 0.5) * self.height, text="G",
                                            font=("Arial", self.width // 3),
                                            fill="white")
        self.canvas.update()

    def bfs_search(self):
        if not self.is_running:
            if self.start_cell != None:
                queue = deque([(self.start_cell, [])])
                visited = set()
                if self.goal_cells.__len__() > 0:
                    ff = False
                    self.redraw_maze()
                    self.is_running = True
                    while queue:
                        (current_cell, path) = queue.popleft()
                        row, col = current_cell

                        if current_cell in self.goal_cells:
                            ff = True
                            # Draw the final path
                            for cell in path:
                                self.canvas.create_rectangle(cell[1] * self.width, cell[0] * self.height,
                                                             (cell[1] + 1) * self.width, (cell[0] + 1) * self.height,
                                                             fill="blue")
                                self.canvas.update()
                                self.root.after(100)
                            self.canvas.create_rectangle(col * self.width, row * self.height,
                                                         (col + 1) * self.width, (row + 1) * self.height,
                                                         fill="blue")
                            self.canvas.update()
                            self.root.after(100)
                            self.is_running = False
                            return

                        if current_cell not in visited:
                            visited.add(current_cell)
                            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

                            for neighbor in neighbors:
                                n_row, n_col = neighbor
                                if self.rows > n_row >= 0 != self.maze[n_row][n_col] and 0 <= n_col < self.cols:
                                    queue.append(((n_row, n_col), path + [current_cell]))
                                    # Visualize exploration path
                                    self.canvas.create_rectangle(n_col * self.width, n_row * self.height,
                                                                 (n_col + 1) * self.width, (n_row + 1) * self.height,
                                                                 fill="yellow")
                                    self.canvas.update()
                                    self.root.after(50)  # Delay for visualization

                    queue = deque([(self.start_cell, [])])
                    visited = set()

                    while queue:
                        (current_cell, path) = queue.popleft()
                        row, col = current_cell

                        if current_cell in self.goal_cells:
                            # Draw the final path
                            for cell in path:
                                self.canvas.create_rectangle(cell[1] * self.width, cell[0] * self.height,
                                                             (cell[1] + 1) * self.width, (cell[0] + 1) * self.height,
                                                             fill="blue")
                                self.canvas.update()
                                self.root.after(50)
                            return

                        if current_cell not in visited:
                            visited.add(current_cell)
                            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

                            for neighbor in neighbors:
                                n_row, n_col = neighbor
                                if self.rows > n_row >= 0 != self.maze[n_row][n_col] and 0 <= n_col < self.cols:
                                    queue.append(((n_row, n_col), path + [current_cell]))
                                    # Visualize exploration path
                                    self.canvas.create_rectangle(n_col * self.width, n_row * self.height,
                                                                 (n_col + 1) * self.width, (n_row + 1) * self.height,
                                                                 fill="yellow")
                                    self.canvas.update()
                                    self.root.after(50)  # Delay for visualization
                    if ff == False:
                        messagebox.showwarning("warning", "No solution path")
                else:
                    messagebox.showwarning("warning", "Please determine the goal cell")
            else:
                messagebox.showwarning("warning", "Please determine the start cell")
            self.is_running = False

    def dfs_search(self):
        if not self.is_running:
            if self.start_cell != None:
                if self.goal_cells.__len__() > 0:
                    # Initialize visited matrix and path
                    visited = [[False] * self.cols for _ in range(self.rows)]
                    exploration_path = []  # To store the cells explored during the search
                    self.is_running = True
                    self.redraw_maze()

                    def dfs(row, col):
                        # Base case: check if the current cell is a goal cell
                        if (row, col) in self.goal_cells:
                            # Mark the goal cell and add it to the final path
                            self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                         (row + 1) * self.height, fill="blue")
                            self.is_running = False
                            return [(row, col)]  # Goal found

                        # Mark the current cell as visited and add it to the exploration path
                        visited[row][col] = True
                        exploration_path.append((row, col))
                        self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                     (row + 1) * self.height, fill="yellow")
                        self.canvas.update()
                        self.root.after(30)

                        # Explore neighbors in a depth-first manner
                        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                        for neighbor_row, neighbor_col in neighbors:
                            if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols and not \
                            visited[neighbor_row][
                                neighbor_col] and self.maze[neighbor_row][neighbor_col] != 0:
                                # Recursive DFS call for the neighbor
                                path_from_neighbor = dfs(neighbor_row, neighbor_col)
                                if path_from_neighbor:
                                    # Goal found, add the current cell to the path and propagate the success back
                                    return [(row, col)] + path_from_neighbor

                        return []  # No goal found from this cell

                    # Start DFS from the initial cell
                    start_row, start_col = self.start_cell
                    final_path = dfs(start_row, start_col)
                    if final_path.__len__() > 0:
                        # Visualize the final path
                        for cell in final_path:
                            row, col = cell
                            self.canvas.create_rectangle(col * self.width, row * self.height, (col + 1) * self.width,
                                                         (row + 1) * self.height, fill="blue")
                            self.canvas.update()
                            self.root.after(50)
                    else:
                        messagebox.showwarning("warning", "No solution path")
                else:
                    messagebox.showwarning("warning", "Please determine the goal cell")
            else:
                messagebox.showwarning("warning", "Please determine the start cell")
            self.is_running = False

    def greedy_search(self):
        if not self.is_running:
            if self.start_cell != None:
                if self.goal_cells.__len__() > 0:
                    queue = deque([(self.start_cell, [])])
                    visited = set()
                    ff = False
                    self.is_running = True
                    self.redraw_maze()
                    while queue:
                        # Sort the queue based on a heuristic (e.g., Euclidean or Manhattan distance to goal)
                        queue = deque(sorted(queue, key=lambda x: self.heuristic(x[0])))
                        (current_cell, path) = queue.popleft()
                        row, col = current_cell

                        if current_cell in self.goal_cells:
                            ff = True
                            # Draw the final path
                            for cell in path:
                                self.canvas.create_rectangle(cell[1] * self.width, cell[0] * self.height,
                                                             (cell[1] + 1) * self.width, (cell[0] + 1) * self.height,
                                                             fill="blue")
                                self.canvas.update()
                                self.root.after(100)
                            self.canvas.create_rectangle(current_cell[1] * self.width, current_cell[0] * self.height,
                                                         (current_cell[1] + 1) * self.width,
                                                         (current_cell[0] + 1) * self.height,
                                                         fill="blue")
                            self.canvas.update()
                            self.root.after(100)
                            self.is_running = False
                            return

                        if current_cell not in visited:
                            visited.add(current_cell)
                            neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

                            for neighbor in neighbors:
                                n_row, n_col = neighbor
                                if self.rows > n_row >= 0 != self.maze[n_row][n_col] and 0 <= n_col < self.cols:
                                    queue.append(((n_row, n_col), path + [current_cell]))
                                    # Visualize exploration path
                                    self.canvas.create_rectangle(n_col * self.width, n_row * self.height,
                                                                 (n_col + 1) * self.width, (n_row + 1) * self.height,
                                                                 fill="yellow")
                                    self.canvas.update()
                                    self.root.after(50)  # Delay for visualization
                    if ff == False:
                        messagebox.showwarning("warning", "No solution path")
                else:
                    messagebox.showwarning("warning", "Please determine the goal cell")
            else:
                messagebox.showwarning("warning", "Please determine the start cell")
            self.is_running = False

    def heuristic(self, cell):
        min_distance = float('inf')
        for goal_cell in self.goal_cells:
            distance = abs(cell[0] - goal_cell[0]) + abs(cell[1] - goal_cell[1])
            min_distance = min(min_distance, distance)
        return min_distance

    def start_drawing(self, event):
        self.drawing = True

    def on_closing(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def set_maze():
    r = tbox1.get()
    c = tbox2.get()
    if r == "" or c == "":
        messagebox.showwarning("warning", "Please enter the size of matrix")
    else:
        if r.isnumeric() and c.isnumeric() and int(r) and int(c) > 0:
            maze_drawer = MazeDrawer(int(r) + 2, int(c) + 2)
            maze_drawer.run()
        else:
            messagebox.showwarning("warning", "Please enter valid size of matrix")


w = Tk()
w.state("zoomed")
w.title("Maze")  # ?
w.config(background="Grey")  # ?
tbox1 = Entry(w, font=('Arial', 10), fg='Black', background='White')
tbox1.place(x=0, y=40)  # ?
tbox2 = Entry(w, font=('Arial', 10), fg='Black', background='White')
tbox2.place(x=160, y=40)  # ?
b1 = Button(w, text="Submit", font=('Arial', 10, 'bold'), fg='White', background='Black', command=set_maze)  # ?
b1.place(x=125, y=70)  # ?
l1 = Label(w, text="Please enter the size of maze", font=('Arial', 10, 'bold'), fg='Black', background='Grey')  # ?
l1.place(x=0, y=20)  # ?
w.mainloop()
