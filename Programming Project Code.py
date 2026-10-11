import openpyxl
import heapq
from tkinter import Tk, filedialog
from guizero import App, Box, PushButton, Text, TextBox, Waffle
from time import sleep

def load_maze(filename):

#    Load the maze from an Excel file and return it as a list of lists.
#    Replace None or Null values with 0.

    maze = []
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active
    for row in sheet.iter_rows(values_only=True):
        row_list = []
        for cell in row:
            if cell is None:  # Check for None values
                row_list.append(0)
            else:
                row_list.append(cell)
        maze.append(row_list)
    return maze

def display_grid():

    maze = read_maze('maze.xlsx')
    global waf_board
    app = App()    
    waf_board = Waffle(app, dotty=False, dim=20, height=COLS, width=ROWS)
    
    for row in range(ROWS):
        for col in range(COLS):
            if maze[col][row] == 1:
                waf_board[row,col].color = "black"
            elif maze[col][row] == start:
                waf_board[row,col].color = "green"
            elif maze[col][row] == end:
                waf_board[row,col].color = "red"
            else:
                waf_board[row,col].color = "white"                



def dijkstra(maze, start, end):

 #   Dijkstra's algorithm to find the shortest path from start to end in the maze.

    rows = len(maze)
    cols = len(maze[0])
    
    # Initialize distances to infinity for all cells
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = 0
    # Initialize a parent dictionary to keep track of the path
    parent = {}
    # Priority queue to store cells to explore
    queue = [(0, start)]
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        distance, current = heapq.heappop(queue)
        if current == end:
            # Reconstruct the path
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                new_distance = distance + 1
                if new_distance < distances[nx][ny]:
                    distances[nx][ny] = new_distance
                    parent[(nx, ny)] = current
                    heapq.heappush(queue, (new_distance, (nx, ny)))
    
    # If end is not reachable
    return None

def visualize_maze(maze, start, end, path):

 #   Visualize the maze using guizero waffle widgets.

    app = App(title="Maze Runner!", bg = "#6c83ca")
    stop_button = PushButton
    waf_board = Waffle(app, dotty=False, dim=20, height=len(maze), width=len(maze[0])) 

    if path:
        for i in range(len(maze)):
            for j in range(len(maze[0])):     
                if maze[i][j] == 1:
                    waf_board[j, i].color = "black"
                elif (i, j) == start:
                    waf_board[j, i].color = "green"
                    app.update()
                    sleep(0.1)
                elif (i, j) == end:
                    waf_board[j, i].color = "red"
                    app.update()
                    sleep(0.1)
                elif (i, j) in path:
                    waf_board[j, i].color = "yellow"
                    app.update()
                    sleep(0.1)
                else:
                    waf_board[j, i].color = "white"
    else:
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 1:
                    waf_board[j, i].color == "black"
                elif (i, j) == start:
                    waf_board[j, i].color == "green"
                elif (i, j) == end:
                    waf_board[j, i].color == "red"
                else:
                    waf_board[j, i].color == "white"
                app.update()
                sleep(0.1)
                    
                   
def solve_maze():

 #   Solve the maze using Dijkstra's algorithm and display the shortest path.
    
    start_node = start_input.value
    end_node = end_input.value
    start = tuple(map(int, start_node.split(',')))
    end = tuple(map(int, end_node.split(',')))
    path = dijkstra(maze, start, end)
    
    if path is None:
        message.value = "End point is not reachable from the start point."
##        visualize_maze(maze, start, end, path)
    else:
        message.value = f"Shortest distance from start to end: {len(path)-1}"
        visualize_maze(maze, start, end, path)

    
def select_file():

#    Open file dialog to let the user select the Excel file containing the maze.

    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        global maze
        maze = load_maze(file_path)
        print("Maze loaded successfully!")
##        for row in maze:
##            print(row)
        start_input.show()
        end_input.show()
        select_button.disable()
        solve_button.enable()
                 
    
# Create GUI
app = App(title="Maze Runner!",bg = "#bee3ff")

start_input = TextBox(app, width=30, text="Enter start node (row, column):")
end_input = TextBox(app, width=30, text="Enter end node (row, column):")
start_input.hide()
end_input.hide()

select_button = PushButton(app, text="Select File", command=select_file)
select_button.width = 20

maze_box = Box(app, layout="grid")
message = Text(app, text="")

solve_button = PushButton(app, text="Solve Maze", command=solve_maze)
solve_button.width = 20
solve_button.disable()

app.display()

