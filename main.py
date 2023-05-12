import random
from collections import deque

# generowanie planszy
A = random.randint(5, 10)
B = random.randint(5, 10)
board = [[0 for j in range(B)] for i in range(A)]

# losowanie startu i końca
start = (random.randint(1, A-2), random.randint(1, B-2))
end = (random.randint(1, A-2), random.randint(1, B-2))
while end == start or abs(end[0] - start[0]) <= 1 or abs(end[1] - start[1]) <= 1:
    end = (random.randint(1, A-2), random.randint(1, B-2))

# losowe przeszkody
num_obstacles = int(A * B * 0.2)
obstacles = set()
while len(obstacles) < num_obstacles:
    obstacle = (random.randint(0, A-1), random.randint(0, B-1))
    if obstacle != start and obstacle != end:
        obstacles.add(obstacle)

for obstacle in obstacles:
    board[obstacle[0]][obstacle[1]] = 1

# tworzenie kolejki
q = deque()
q.append(start)

# tworzenie słownika do przechowywania odwiedzonych wierzchołków
visited = {start: None}

# rozpoczynamy BFS
while q:
    current = q.popleft()
    if current == end:
        break
    row, col = current
    # sprawdzanie sąsiadów
    for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if r < 0 or c < 0 or r >= A or c >= B or board[r][c] == 1 or (r, c) in visited:
            continue
        q.append((r, c))
        visited[(r, c)] = current

# odtwarzanie ścieżki
path = []
current = end
while current != start:
    path.append(current)
    current = visited[current]
path.append(start)
path.reverse()

# wyświetlanie ścieżki
print("Ścieżka:")
for i in range(A):
    for j in range(B):
        if (i, j) == start:
            print("S", end=" ")
        elif (i, j) == end:
            print("E", end=" ")
        elif board[i][j] == 1:
            print("#", end=" ")
        elif (i, j) in path:
            print("*", end=" ")
        else:
            print(".", end=" ")
    print()