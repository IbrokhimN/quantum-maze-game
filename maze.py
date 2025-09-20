import os
import time
import random
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector


class QuantumEngine:
    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
        self.qc = QuantumCircuit(n_qubits)

    def reset(self):
        self.qc = QuantumCircuit(self.n_qubits)

    def apply_hadamard(self, qubit: int):
        self.qc.h(qubit)

    def get_random_bits(self) -> str:
        sv = Statevector.from_instruction(self.qc)
        probs = sv.probabilities_dict()
        outcomes = list(probs.keys())
        weights = list(probs.values())
        return random.choices(outcomes, weights=weights, k=1)[0]

    def visualize_bloch(self):
        sv = Statevector.from_instruction(self.qc)
        plot_bloch_multivector(sv)
        plt.show()


class Maze:
    EMPTY = " "
    PLAYER = "P"
    EXIT = "E"
    WALL = "■"
    PATH = "."

    def __init__(self, size: int = 6, wall_density: float = 0.2):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.player = [0, 0]
        self.exit = [size - 1, size - 1]

        # place walls randomly
        for i in range(size):
            for j in range(size):
                if random.random() < wall_density and [i, j] not in ([0, 0], self.exit):
                    self.grid[i][j] = self.WALL

        self.grid[self.exit[0]][self.exit[1]] = self.EXIT
        self.steps = 0
        self.max_steps = size * size * 2  # limit moves

    def display(self):
        os.system("cls" if os.name == "nt" else "clear")
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if [i, j] == self.player:
                    row += f"{self.PLAYER} "
                else:
                    row += f"{self.grid[i][j]} "
            print(row)
        print(f"\nSteps: {self.steps}/{self.max_steps}\n")

    def move(self, direction: str):
        x, y = self.player
        new_x, new_y = x, y

        if direction == "U" and x > 0:
            new_x -= 1
        elif direction == "D" and x < self.size - 1:
            new_x += 1
        elif direction == "L" and y > 0:
            new_y -= 1
        elif direction == "R" and y < self.size - 1:
            new_y += 1

        # block by walls
        if self.grid[new_x][new_y] != self.WALL:
            self.player = [new_x, new_y]
            if self.grid[x][y] == self.EMPTY:
                self.grid[x][y] = self.PATH
            self.steps += 1

    def is_exit(self) -> bool:
        return self.player == self.exit

    def is_game_over(self) -> bool:
        return self.steps >= self.max_steps


class QuantumMazeGame:
    DIRECTIONS = ["U", "D", "L", "R"]

    def __init__(self, maze_size=6, n_qubits=2, wall_density=0.2):
        self.maze = Maze(maze_size, wall_density)
        self.qengine = QuantumEngine(n_qubits)
        self.n_qubits = n_qubits

    def random_direction(self) -> str:
        self.qengine.reset()
        for q in range(self.n_qubits):
            self.qengine.apply_hadamard(q)
        bits = self.qengine.get_random_bits()
        num = int(bits, 2)
        return self.DIRECTIONS[num % len(self.DIRECTIONS)]

    def play(self):
        print("Welcome to the Quantum Maze!")
        print("Reach the exit 'E'. Your moves are determined by qubits!\n")
        time.sleep(2)

        while not self.maze.is_exit() and not self.maze.is_game_over():
            self.maze.display()
            move = self.random_direction()
            print(f"Qubits choose: {move}")
            self.maze.move(move)
            time.sleep(0.7)

        if self.maze.is_exit():
            print("🎉 Congratulations! You reached the exit!")
            self.save_score(self.maze.steps)
        else:
            print("❌ Game Over! You ran out of steps.")

    def visualize_qubits(self):
        self.qengine.reset()
        for q in range(self.n_qubits):
            self.qengine.apply_hadamard(q)
        self.qengine.visualize_bloch()

    def save_score(self, steps: int):
        try:
            with open("scores.txt", "a") as f:
                f.write(f"Finished maze in {steps} steps\n")
        except Exception:
            pass


if __name__ == "__main__":
    while True:
        print("Choose mode:")
        print("1. Play the maze")
        print("2. Visualize qubits")
        print("3. Exit")
        choice = input(">>> ").strip()
        if choice == "1":
            game = QuantumMazeGame(maze_size=6, n_qubits=2, wall_density=0.25)
            game.play()
            input("Press Enter to return to menu...")
        elif choice == "2":
            game = QuantumMazeGame()
            game.visualize_qubits()
            input("Press Enter to return to menu...")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
