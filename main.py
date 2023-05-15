import random
import pytest

from collections import deque

def main():
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
# Klasa testowa
class TestBFS:
    @classmethod
    def setup_class(cls):
        print("Przygotowanie klasy testowej")

    @classmethod
    def teardown_class(cls):
        print("Sprzątanie po klasie testowej")

    def setup_method(self, method):
        print(f"Przygotowanie metody testowej: {method.__name__}")

    def teardown_method(self, method):
        print(f"Sprzątanie po metodzie testowej: {method.__name__}")
        
# Funkcja sprawdzająca, czy dany punkt znajduje się na planszy
@pytest.mark.skipif(pytest.raises(AssertionError), reason="Skip is_valid_point if start and end positions are correct.")
def is_valid_point(point, A, B):
    row, col = point
    return row >= 0 and col >= 0 and row < A and col < B

# Test sprawdzający, czy start i end są poprawnie wylosowane na planszy
@pytest.mark.parametrize("start, end", [
    ((1, 1), (8, 8)),
    ((0, 0), (9, 9))
])
def test_start_end_positions(start, end):
    A = 10
    B = 10
    assert is_valid_point(start, A, B)
    assert is_valid_point(end, A, B)
    assert start != end
    assert abs(end[0] - start[0]) > 1 or abs(end[1] - start[1]) > 1

# Test sprawdzający, czy algorytm nie wychodzi poza granice planszy
@pytest.mark.parametrize("start, end", [
    ((1, 1), (8, 8)),
    ((0, 0), (9, 9))
])
def test_boundary_check(start, end):
    A = 10
    B = 10
    board = [[0 for j in range(B)] for i in range(A)]

    q = deque()
    q.append(start)
    visited = {start: None}

    while q:
        current = q.popleft()
        row, col = current
        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if not is_valid_point((r, c), A, B) or board[r][c] == 1 or (r, c) in visited:
                continue
            q.append((r, c))
            visited[(r, c)] = current

    # Sprawdzanie, czy wszystkie odwiedzone punkty są na planszy

    for point in visited:
        assert is_valid_point(point, A, B)

# Test sprawdzający, czy algorytm omija przeszkody na planszy
@pytest.mark.parametrize("start, end", [
    ((1, 1), (8, 8)),
    ((0, 0), (9, 9))
])
def test_obstacle_avoidance(start, end):
    A = 10
    B = 10
    board = [[0 for j in range(B)] for i in range(A)]

    q = deque()
    q.append(start)
    visited = {start: None}

    while q:
        current = q.popleft()
        row, col = current
        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if not _point_point((r, c), A, B) or board[r][c] == 1 or (r, c) in visited:
                continue
            q.append((r, c))
            visited[(r, c)] = current
            
# Funkcja sprawdzająca, czy dany punkt znajduje się na planszy
def is_valid_point(point, A, B):
    row, col = point
    return row >= 0 and col >= 0 and row < A and col < B

# Test sprawdzający, czy żadne odwiedzone pole nie jest przeszkodą
@pytest.mark.parametrize("start, end", [
    ((1, 1), (8, 8)),
    ((0, 0), (9, 9))
])
@pytest.mark.xfail(reason="Visited points may include obstacles.")
def test_obstacle_avoidance(start, end):
    A = 10
    B = 10
    board = [[0 for j in range(B)] for i in range(A)]

    q = deque()
    q.append(start)
    visited = {start: None}

    while q:
        current = q.popleft()
        row, col = current
        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if not is_valid_point((r, c), A, B) or board[r][c] == 1 or (r, c) in visited:
                continue
            q.append((r, c))
            visited[(r, c)] = current

    # Sprawdzanie, czy żadne odwiedzone pole nie jest przeszkodą
    for point in visited:
        assert board[point[0]][point[1]] != 1              
