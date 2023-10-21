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
        closed_set = set()
        start_node = Node(start)
        end_node = Node(end)
        
        open_list.append(start_node)
        
        while open_list:
            current_node = min(open_list, key=lambda node: node.g + node.h)
            open_list.remove(current_node)
            
            if current_node.position == end_node.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]
            
            closed_set.add(current_node.position)
            
            neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in neighbors:
                new_position = (current_node.position[0] + dx, current_node.position[1] + dy)
                
                if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                    continue
                if maze[new_position[0]][new_position[1]] == 1:
                    continue
                if new_position in closed_set:
                    continue
                
                new_node = Node(new_position, current_node)
                new_node.g = current_node.g + 1
                new_node.h = abs(new_position[0] - end_node.position[0]) + abs(new_position[1] - end_node.position[1])
                
                existing_open_node = next((node for node in open_list if node.position == new_node.position), None)
                if existing_open_node:
                    if new_node.g < existing_open_node.g:
                        existing_open_node.g = new_node.g
                        existing_open_node.parent = new_node.parent
                else:
                    open_list.append(new_node)
        
        return None


    def draw_maze_with_pygame(maze, path=None, other_ends=None):
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
        other_ends_color = (255, 0, 0)  # Couleur pour les autres ends

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

            # Dessiner les autres ends en carrés rouges
            if other_ends:
                for end_position in other_ends:
                    tile_rect = pygame.Rect(end_position[1] * TILE_SIZE, end_position[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, other_ends_color, tile_rect)

            # Dessiner le quadrillage en dernier
            for y in range(len(maze)):
                for x in range(len(maze[0])):
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (0, 0, 0), tile_rect, 1)

            pygame.display.flip()
            clock.tick(30)

    # Définir les coordonnées du départ, de l'arrivée et des obstacles
    start = liste_real_cases_perso[0]
    ends = liste_real_cases_mobs

    obstacles = []
    cases_good = []

    for i in range (0, 32):
        for k in range (0, 33):
            obstacles.append((i, k))

    for i in liste_real_cases_wakable:
        cases_good.append(i)

    # Trouver le chemin vers la destination la plus proche
    shortest_path = None
    shortest_distance = float('inf') 

    for end in ends:
 
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

        # Placer les obstacles et les cases traversables dans la grille du labyrinthe
        for obstacle in obstacles:
            if 0 <= obstacle[0] < len(maze) and 0 <= obstacle[1] < len(maze[0]):
                maze[obstacle[0]][obstacle[1]] = 1

        for good in cases_good:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0

        for good in liste_real_cases_mobs:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0
        for good in liste_real_cases_wakable:
            if 0 <= good[0] < len(maze) and 0 <= good[1] < len(maze[0]):
                maze[good[0]][good[1]] = 0
  

        # Trouver le chemin vers la destination actuelle
        path = astar(maze, start, end)

        if path and len(path) < shortest_distance:
            shortest_distance = len(path)
            shortest_path = path

    # Afficher le chemin le plus court trouvé dans la fenêtre pygame
    if shortest_path:
        #supprimer la case de départ de la liste
        del shortest_path[0]

        print("Chemin le plus court trouvé:", shortest_path)
        other_ends = [end_position for end_position in ends if end_position != shortest_path[-1]]
        other_ends.append(shortest_path[-1])  # Ajouter la fin la plus courte à la liste des autres ends
        #draw_maze_with_pygame(maze, shortest_path, other_ends)
        return(shortest_path)
    else:
        print("Aucun chemin trouvé")
        draw_maze_with_pygame(maze, ends, ends)
