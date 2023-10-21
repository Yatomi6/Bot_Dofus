def laby(liste_real_cases_mobs, liste_real_cases_wakable, liste_real_cases_perso):   
    import heapq
    import pygame

    class Node:
        def __init__(self, position, parent=None):
            self.position = position
            self.parent = parent
            self.g = 0
            self.h = 0

        def __lt__(self, other):
            return (self.g + self.h) < (other.g + other.h)

    def astar(maze, start, end):
        open_list = []
        closed_list = set()
        start_node = Node(start)
        end_node = Node(end)
        
        heapq.heappush(open_list, start_node)
        
        while open_list:
            current_node = heapq.heappop(open_list)
            
            if current_node.position == end_node.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]
            
            closed_list.add(current_node.position)
            
            neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in neighbors:
                new_position = (current_node.position[0] + dx, current_node.position[1] + dy)
                if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                    continue
                if maze[new_position[0]][new_position[1]] == 1:
                    continue
                if new_position in closed_list:
                    continue
                
                new_node = Node(new_position, current_node)
                new_node.g = current_node.g + 1
                new_node.h = abs(new_position[0] - end_node.position[0]) + abs(new_position[1] - end_node.position[1])
                
                heapq.heappush(open_list, new_node)
        
        return None

    def draw_maze_with_pygame(maze, path=None):
        pygame.init()

        TILE_SIZE = 20  # Modifiez cette valeur pour ajuster la taille des cases
        WIDTH = len(maze[0]) * TILE_SIZE
        HEIGHT = len(maze) * TILE_SIZE

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Labyrinthe Solver")

        clock = pygame.time.Clock()

        wall_color = (0, 0, 0)
        path_color = (0, 0, 255)
        start_color = (0, 255, 0)
        end_color = (255, 0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            screen.fill((255, 255, 255))

            # Dessiner les obstacles
            for y, row in enumerate(maze):
                for x, tile in enumerate(row):
                    if tile == 1:
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, wall_color, tile_rect)

            if path:
                # Dessiner le chemin
                for y, x in path:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, path_color, tile_rect)

            # Dessiner le point de départ et d'arrêt
            start_rect = pygame.Rect(start[1] * TILE_SIZE, start[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, start_color, start_rect)

            end_rect = pygame.Rect(end[1] * TILE_SIZE, end[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, end_color, end_rect)

            # Dessiner le quadrillage en dernier
            for y in range(len(maze)):
                for x in range(len(maze[0])):
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (0, 0, 0), tile_rect, 1)

            pygame.display.flip()
            clock.tick(30)

    file_name = "start.txt"
    with open(file_name, "r") as file:
        start = file.read()
    start = liste_real_cases_perso[0]

    end = liste_real_cases_mobs[0]

    obstacles = []
    cases_good = []

    for i in range (0, 32):
        for k in range (0, 33):
            obstacles.append((i, k))

    for i in liste_real_cases_wakable:
        cases_good.append(i)
    
    



    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # Placer les obstacles dans la grille du labyrinthe
    for obstacle in obstacles:
        maze[obstacle[0]][obstacle[1]] = 1

    for good in cases_good:
        maze[good[0]][good[1]] = 0

    for good in liste_real_cases_mobs:
            maze[good[0]][good[1]] = 0
    for good in liste_real_cases_wakable:
        maze[good[0]][good[1]] = 0

    path = astar(maze, start, end)
    if path:
        print("Chemin trouvé:", path)
        draw_maze_with_pygame(maze, path)
    else:
        draw_maze_with_pygame(maze, path)
        print("Aucun chemin trouvé")

liste_real_cases_wakable = [(17, 24), (18, 26), (14, 12), (21, 8), (3, 20), (10, 21), (6, 20), (21, 19), (11, 31), (25, 8), (18, 14), (8, 23), (10, 14), (11, 16), (23, 10), (10, 22), (11, 27), (9, 18), (0, 19), (26, 11), (19, 20), (12, 16), (16, 30), (23, 9), (27, 13), (24, 13), (17, 22), (13, 29), (21, 11), (11, 20), (1, 22), (2, 21), (25, 15), (28, 13), (22, 15), (15, 24), (4, 17), (19, 13), (6, 18), (12, 12), (8, 21), (26, 15), (20, 17), (16, 12), (5, 22), (12, 23), (24, 17), (8, 22), (23, 21), (8, 20), (27, 10), (21, 5), (20, 19), (20, 16), (18, 16), (10, 25), (10, 23), (28, 12), (25, 12), (19, 7), (12, 24), (10, 24), (17, 25), (10, 11), (3, 17), (11, 18), (11, 28), (26, 14), (21, 22), (8, 13), (25, 11), (18, 20), (4, 15), (4, 22), (24, 16), (7, 15), (19, 24), (12, 13), (3, 24), (2, 17), (11, 29), (4, 23), (27, 17), (17, 26), (10, 15), (8, 24), (19, 10), (21, 15), (20, 22), (6, 17), (9, 17), (25, 19), (8, 17), (0, 20), (11, 10), (4, 19), (6, 25), (4, 24), (9, 30), (21, 12), (23, 7), (10, 29), (20, 18), (12, 25), (17, 23), (19, 14), (11, 21), (2, 19), (21, 9), (22, 7), (12, 26), (19, 27), (24, 7), (28, 16), (19, 11), (20, 9), (14, 27), (10, 13), (22, 9), (6, 24), (26, 18), (4, 21), (18, 11), (6, 22), (14, 28), (9, 15), (8, 15), (11, 15), (12, 10), (10, 26), (7, 17), (21, 24), (18, 22), (0, 21), (6, 21), (19, 26), (18, 15), (20, 21), (8, 27), (5, 17), (11, 32), (23, 14), (9, 19), (15, 21), (13, 21), (12, 31), (18, 23), (19, 25), (21, 16), (14, 25), (2, 23), (13, 23), (3, 22), (27, 11), (7, 19), (22, 18), (26, 9), (25, 16), (19, 18), (12, 27), (24, 22), (12, 15), (14, 26), (20, 20), (24, 11), (23, 18), (20, 6), (29, 13), (9, 11), (10, 17), (21, 20), (9, 23), (10, 28), (27, 15), (20, 24), (25, 17), (12, 19), (12, 29), (28, 17), (23, 17), (12, 30), (5, 16), (15, 23), (26, 19), (20, 3), (16, 27), (3, 18), (5, 19), (24, 21), (11, 9), (6, 26), (2, 20), (9, 21), (14, 29), (7, 18), (16, 28), (22, 22), (5, 20), (21, 6), (7, 21), (22, 8), (11, 23), (19, 8), (20, 10), (11, 25), (24, 10), (23, 8), (17, 10), (10, 19), (2, 22), (18, 12), (27, 19), (22, 12), (14, 21), (3, 16), (12, 28), (21, 10), (15, 12), (6, 16), (20, 14), (19, 12), (12, 21), (22, 5), (10, 16), (19, 23), (5, 18), (8, 11), (8, 28), (20, 7), (8, 18), (4, 20), (12, 32), (25, 9), (15, 25), (6, 23), (9, 13), (12, 20), (13, 25), (28, 11), (16, 29), (26, 13), (21, 13), (8, 25), (15, 26), (26, 12), (25, 10), (18, 19), (8, 26), (15, 27), (1, 19), (13, 28), (24, 14), (14, 30), (23, 12), (16, 21), (8, 16), (28, 14), (22, 16), (1, 20), (22, 23), (21, 14), (14, 23), (4, 25), (10, 9), (19, 21), (11, 11), (5, 24), (21, 25), (26, 16), (7, 20), (20, 25), (19, 16), (10, 20), (15, 11), (10, 18), (24, 18), (16, 25), (6, 27), (12, 11), (27, 18), (17, 27), (7, 26), (14, 22), (12, 22), (9, 22), (25, 13), (13, 26), (28, 15), (21, 4), (23, 15), (23, 22), (10, 27), (17, 29), (13, 27), (18, 21), (13, 10), (8, 12), (1, 21), (21, 23), (16, 23), (13, 11), (16, 11), (9, 20), (3, 23), (16, 22), (8, 29), (20, 11), (7, 22), (9, 28), (10, 30), (24, 15), (14, 24), (19, 15), (11, 24), (18, 13), (11, 22), (3, 19), (15, 28), (22, 17), (19, 17), (18, 24), (4, 16), (10, 31), (9, 24), (10, 10), (11, 30), (6, 19), (16, 26), (9, 12), (24, 8), (15, 29), (5, 21), (20, 23), (7, 14), (7, 24), (22, 10), (27, 12), (21, 7), (17, 21), (29, 12), (18, 25), (11, 14), (20, 12), (25, 14), (19, 9), (27, 14), (7, 25), (9, 16), (23, 16), (17, 11), (13, 22), (5, 25), (20, 4), (22, 13), (21, 18), (26, 17), (21, 17), (20, 15), (13, 24), (9, 10), (7, 27), (5, 26), (22, 6), (19, 19), (20, 26), (18, 17), (11, 26), (7, 12), (16, 24), (10, 12), (3, 21), (22, 21), (20, 8), (18, 28), (17, 28), (11, 12), (7, 23), (18, 10), (13, 12), (21, 21), (15, 30), (9, 26), (24, 12), (9, 14), (5, 23), (9, 25), (22, 14), (27, 16), (20, 5), (7, 16), (2, 18), (24, 9), (9, 27), (25, 18), (12, 9), (15, 22), (22, 11), (18, 27), (1, 18), (7, 13), (8, 19), (19, 22), (20, 13), (4, 18), (9, 29), (11, 19), (14, 11), (23, 6), (11, 17), (7, 28)]
liste_real_cases_perso = [(26, 10)]
liste_real_cases_mobs = [(23, 11), (23, 13)]
laby(liste_real_cases_mobs, liste_real_cases_wakable, liste_real_cases_perso)