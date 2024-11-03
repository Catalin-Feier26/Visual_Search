import sys
import pygame
import heapq
from collections import deque
# Define colors
WHITE = (255, 255, 255)             #for EMPTY
BLACK = (0, 0, 0)                   #for obstacle
BRAT = (137, 204, 4)                #for final path
PURPLE =(105,54,156)                #for STSART
PINKISH = (156,53,101)              #for the end
GRAY = (90,90,90)                   #for the search
PINK = (255,192,203)                #for the BORDER
MENU_COLOR = (135, 37, 91)  # for menu background
MENU_TEXT_COLOR = (195, 195, 230)  # for menu text
HIGHLIGHT_COLOR = (180,112,176)  # for highlighted text
# Define GRID values
BORDER = -1
EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
PATH = 4
SEARCH = 5
# Define window sizes
WIDTH = 1080
HEIGHT = 720
# Define The algorithm type:
DFS = 1
BFS = 2
UCS = 3
ASTAR = 4

#Define the movements
NORTH = [0, 1]
SOUTH = [0, -1]
WEST = [1, 0]
EAST = [-1, 0]

#Define the SONGS:

DRESS = 'Dress Up Theme from Dress To Impress.mp3'
COMP = 'Competition.mp3'
CHARL = '365.mp3'
RUN = 'Runway.mp3'
SUN = 'The Last Sun.mp3'

start_count=0
end_count=0
selected_algorithm = 0

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Dress Up Theme from Dress To Impress.mp3')
pygame.mixer.music.set_volume(0.11)
pygame.mixer.music.play(-1)

#Function to run a specific song!
def playSong(songName):
    pygame.mixer.music.load(songName)
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
#Heuristic for the ASTAR algorithm
def heuristic(node,end):
    return abs(node[0] - end[0]) + abs(node[1] - end[1])
#A* algorithm
def astar(window, grid, cell_number, start, end):
    priority_q = [(heuristic(start,end),start)]
    g_cost = {start: 0}
    path = {}
    visited=set()

    while priority_q:
        current_f, current = heapq.heappop(priority_q)
        x,y=current

        if current != start and current != end:
            grid[x][y] = SEARCH
        
        gridDrawing(window, grid, cell_number)
        pygame.display.update()
        pygame.time.delay(100)

        if current == end:
            final_path = []
            while current != start:
                final_path.append(current)
                current=path[current]
            final_path.reverse()
            return final_path

        if current in visited:
            continue

        visited.add(current)

        for direction in [NORTH, SOUTH, EAST, WEST]:
            next_cell = (x+ direction[0], y+direction[1])
            new_g_cost = g_cost[current] + 1
            if(grid[next_cell[0]][next_cell[1]] != BORDER and
                    grid[next_cell[0]][next_cell[1]] != OBSTACLE and
                    next_cell not in visited and
                    (grid[next_cell[0]][next_cell[1]] == EMPTY or next_cell == end)
                    ):
                if next_cell not in g_cost or new_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = new_g_cost
                    f_cost = new_g_cost + heuristic(next_cell, end)
                    heapq.heappush(priority_q, (f_cost, next_cell))
                    path[next_cell] = current
    
    return None
#Uniform Cost search algorithm
def ucs(window, grid, cell_number, start, end):
    priority_q = [(0,start)]
    visited = set()
    path ={}
    cost_so_far={start: 0}

    while priority_q:
        current_cost, current=heapq.heappop(priority_q)
        x,y = current

        if current != start and current != end:
            grid[x][y] = SEARCH
        
        gridDrawing(window,grid,cell_number)
        pygame.display.update()
        pygame.time.delay(100)

        if current == end:
            final_path=[]
            while current != start:
                final_path.append(current)
                current=path[current]
            final_path.reverse()
            return final_path

        if current in visited:
            continue

        visited.add(current)

        for direction, step_cost in zip([NORTH, SOUTH, EAST, WEST],[1,1,1,1]):
            next_cell=(x+direction[0], y+direction[1])
            new_cost = current_cost + step_cost

            if(grid[next_cell[0]][next_cell[1]] != BORDER and
                grid[next_cell[0]][next_cell[1]] != OBSTACLE and
                next_cell not in visited and
                (grid[next_cell[0]][next_cell[1]] == EMPTY or next_cell == end) and
                (next_cell not in cost_so_far or new_cost < cost_so_far[next_cell])):

                cost_so_far[next_cell] = new_cost
                heapq.heappush(priority_q,(new_cost,next_cell))
                path[next_cell]=current
        
    return None
#Breadth first search
def bfs(window, grid, cell_number, start, end):
    queue = deque([start])
    visited = set([start])
    path={}
    while queue:
        current = queue.popleft()
        x,y = current

        if current != start and current != end:
            grid[x][y]=SEARCH
        
        gridDrawing(window,grid,cell_number)
        pygame.display.update()
        pygame.time.delay(100)

        if current == end:
            final_path=[]
            while current != start:
                final_path.append(current)
                current=path[current]
            final_path.reverse()
            return final_path
        for direction in [NORTH,EAST,SOUTH,WEST]:
            next_cell = (x+ direction[0], y+direction[1])
            if( grid[next_cell[0]][next_cell[1]] != BORDER and
                grid[next_cell[0]][next_cell[1]] != OBSTACLE and
                next_cell not in visited and
                (grid[next_cell[0]][next_cell[1]] == EMPTY or next_cell == end)
               ):
                queue.append(next_cell)
                visited.add(next_cell)
                path[next_cell] = current
    return None          
#Depth first search
def dfs(window,grid, cell_number, start, end):
    stack = [start]
    visited = set()
    path = {}

    while stack:
        current = stack.pop()
        x, y = current

        if current != start and current != end:
            grid[x][y]= SEARCH

        gridDrawing(window, grid, cell_number)
        pygame.display.update()
        pygame.time.delay(100)

        if current == end:
            final_path = []
            while current != start:
                final_path.append(current)
                current =path[current]
            final_path.reverse()
            return final_path
        
        visited.add(current)
        for direction in [EAST, SOUTH, NORTH, WEST]:
            next_cell = (x + direction[1], y + direction[0])
            if( grid[next_cell[0]][next_cell[1]] != BORDER and
                grid[next_cell[0]][next_cell[1]] != OBSTACLE and
                next_cell not in visited and
                (grid[next_cell[0]][next_cell[1]] == EMPTY or next_cell == end)
               ):
                stack.append(next_cell)
                path[next_cell] = current
    return None
#Controller function for the algorithms
def executeAlgorithm(window, cell_number,grid, selected_algorithm, start_x, start_y, end_x, end_y):

    start = (start_x,start_y)
    end = (end_x, end_y)
    if selected_algorithm == DFS:
        playSong(SUN)
        path = dfs(window,grid, cell_number, start, end)
    elif selected_algorithm == BFS:
        playSong(CHARL)
        path = bfs (window,grid,cell_number,start,end)
    elif selected_algorithm == UCS:
        playSong(COMP)
        path = ucs (window, grid, cell_number, start, end)
    else:
        playSong(RUN)
        path = astar(window, grid, cell_number, start, end)
    
    if path:
        length=1
        print("PATH")
        print("Start:")
        print("\t({}, {})".format(start_x, start_y))
        for (x,y) in path:
            length+=1
            if (x,y) != end:
                print("\t({}, {})".format(x, y))
                grid[x][y] = PATH
                gridDrawing(window,grid,cell_number)
                pygame.display.update()
                pygame.time.delay(100)
            else:
                print("\t({}, {})".format(x, y))
                print("Goal\nLength: ",length)

#Functions to get the start and endpoints from the GRID    
def getStart(grid, cell_number):
    for row in range(cell_number):
        for col in range(cell_number):
            if grid[row][col]==START:
                return (row,col)
    return None
def getEnd(grid, cell_number):
    for row in range(cell_number):
        for col in range(cell_number):
            if grid[row][col]==END:
                return (row,col)
    return None

#Reading arguments from the command line
def readArguments():
    if len(sys.argv) > 1:
        cell_number = int(sys.argv[1])
        if cell_number < 2 or cell_number > 40:
            print("Please provide a cell number between 3 and 40")
            sys.exit(1)
        return cell_number
    else:
        print("Please provide the number of cells as an argument.")
        sys.exit(1)
# Grid Creation
def createGrid(cell_number):
    return [[0 for _ in range(cell_number)] for _ in range(cell_number)]
#Reset function for the APP
def resetGrid(grid, cell_number):
    global selected_algorithm, start_count, end_count
    selected_algorithm = 0
    start_count=0
    end_count=0
    for row in range(cell_number):
        for col in range(cell_number):
            if row == 0 or row == cell_number - 1 or col == 0 or col == cell_number - 1:
                grid[row][col] = BORDER
            else:
                grid[row][col] = EMPTY
#The clicking mechanism
def toggleCell(grid, row, col):
    global start_count, end_count

    if grid[row][col] == EMPTY:
        grid[row][col] = OBSTACLE
    elif grid[row][col] == OBSTACLE:
        grid[row][col] = START
        start_count +=1
    elif grid[row][col] == START:
        grid[row][col] = END
        end_count+=1
        start_count-=1
    elif grid[row][col] == END:
        end_count-=1
        grid[row][col] = EMPTY
# THe menu PANEL when prpessing ESC
def showMenu(window, selected_index):
    font = pygame.font.Font(None,36)
    menu_items = ["DFS", "BFS", "UCS", "A*","START"]
    menu_surface = pygame.Surface((300,200))
    menu_surface.fill(MENU_COLOR)

    for index, item in enumerate(menu_items):
        text_color = HIGHLIGHT_COLOR if index == selected_index else MENU_TEXT_COLOR
        text = font.render(item, True, text_color)
        menu_surface.blit(text,(50, 40+index*40))

    window.blit(menu_surface,(WIDTH // 2 - 150, HEIGHT // 2 -100))
#Drawing the grid
def gridDrawing(window, grid, cell_number):
    cell_width = WIDTH // cell_number
    cell_height = HEIGHT // cell_number

    for row in range(cell_number):
        for col in range(cell_number):
            rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            
            if grid[row][col] == EMPTY :
                pygame.draw.rect(window, WHITE, rect)  
            if grid[row][col] == OBSTACLE :
                pygame.draw.rect(window,BLACK,rect)
            if grid[row][col] == START :
                pygame.draw.rect(window,PURPLE,rect)
            if grid[row][col] == END :
                pygame.draw.rect(window,PINKISH,rect)
            if grid[row][col] == PATH :
                pygame.draw.rect(window,BRAT,rect)
            if grid[row][col] == SEARCH:
                pygame.draw.rect(window,GRAY,rect)
            if grid[row][col] == BORDER:
                pygame.draw.rect(window, PINK, rect)
            
            pygame.draw.rect(window, BLACK, rect, 1)  # Draw border
# The start window
def startWindow(window):
    WINDOW_WIDTH, WINDOW_HEIGHT = window.get_size()

    start_window_width = 600
    start_window_height = 500
    start_window_x = (WINDOW_WIDTH - start_window_width) // 2
    start_window_y = (WINDOW_HEIGHT - start_window_height) // 2

    button_width = 150
    button_height = 50
    button_x = start_window_x + (start_window_width - button_width) //2
    button_y = start_window_y + (start_window_height - button_height) - 20

    font = pygame.font.Font(None, 32)

    start_text_lines = [
        "WELCOME!",
        "READ THE RULES:",
        "1. Click on a cell to change its state.",
        "2. Have one start and one end.",
        "3. Press ESC and choose an algorithm.",
        "4. Press S to start!"
    ]

    while True:
        pygame.draw.rect(window,BRAT,(start_window_x,start_window_y,start_window_width,start_window_height))

        line_height = 40  # Space between lines
        for i, line in enumerate(start_text_lines):
            rendered_line = font.render(line, True, BLACK)
            line_y = start_window_y + 50 + i * line_height
            window.blit(rendered_line, (start_window_x + 20, line_y))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hover = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
        button_color = HIGHLIGHT_COLOR if button_hover else PINK
        pygame.draw.rect(window,button_color, (button_x, button_y, button_width, button_height))

        button_text = font.render("Understood", True, BLACK)
        button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        window.blit(button_text, button_text_rect)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_hover:
                    return 
# The error window
def showError(window, errorMessage):
    # Window dimensions
    WINDOW_WIDTH, WINDOW_HEIGHT = window.get_size()
    
    error_window_width = 400
    error_window_height = 200
    error_window_x = (WINDOW_WIDTH - error_window_width) // 2
    error_window_y = (WINDOW_HEIGHT - error_window_height) // 2
    
    button_width = 150
    button_height = 50
    button_x = error_window_x + (error_window_width - button_width) // 2
    button_y = error_window_y + error_window_height - button_height - 20
    
    font = pygame.font.Font(None, 32)

    while True:
        pygame.draw.rect(window, BRAT, (error_window_x, error_window_y, error_window_width, error_window_height))
        
        error_text = font.render(errorMessage, True, BLACK)
        error_text_rect = error_text.get_rect(center=(error_window_x + error_window_width // 2, error_window_y + 60))
        window.blit(error_text, error_text_rect)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
        button_color = HIGHLIGHT_COLOR if button_hovered else PINKISH
        pygame.draw.rect(window, button_color, (button_x, button_y, button_width, button_height))
        
        button_text = font.render("Understood", True, BLACK)
        button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        window.blit(button_text, button_text_rect)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_hovered:
                    return 
# The main function
def main():
    global selected_algorithm, start_count, end_count
    cell_number = readArguments()
    print(cell_number)
    selected_algorithm = 0

    pygame.init()
    window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
    startWindow(window)
    grid = createGrid(cell_number=cell_number)
    resetGrid(grid, cell_number)
    #I initialize the grid with 0 and the BORDER here.

    show_menu = False
    sel = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    col = x // (WIDTH // cell_number)
                    row = y // (HEIGHT // cell_number)

                    toggleCell(grid,row,col)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu=True
                if show_menu:
                    if event.key == pygame.K_UP:
                        sel = (sel-1) % 4
                    elif event.key == pygame.K_DOWN:
                        sel = (sel+1) % 4
                    elif event.key == pygame.K_RETURN:
                        selected_algorithm = [DFS, BFS, UCS, ASTAR][sel]
                        show_menu=False
                        print(selected_algorithm)
                if event.key == pygame.K_s:
                    if selected_algorithm != 0:
                        if start_count == 1 and end_count == 1:
                            sx,sy=getStart(grid,cell_number)
                            ex,ey=getEnd(grid,cell_number)
                            executeAlgorithm(window, cell_number,grid,selected_algorithm, sx, sy, ex, ey)
                        else:
                            showError(window,"Select a valid start and end points")
                    else:
                        showError(window,"SELECT AN ALGORITHM FIRST")
                if event.key == pygame.K_r:
                    playSong(DRESS)
                    resetGrid(grid, cell_number)
        window.fill(BRAT)
        gridDrawing(window, grid, cell_number)
        if show_menu:
            showMenu(window,sel)
        pygame.display.update()
# Init
if __name__ == "__main__":
    main()
