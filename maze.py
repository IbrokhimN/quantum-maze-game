import random
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import time
import os

class QuantumEngine:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.qc = QuantumCircuit(n_qubits)

    def reset(self):
        self.qc = QuantumCircuit(self.n_qubits)

    def apply_hadamard(self, qubit):
        self.qc.h(qubit)

    def apply_x(self, qubit):
        self.qc.x(qubit)

    def apply_z(self, qubit):
        self.qc.z(qubit)

    def apply_cx(self, control, target):
        self.qc.cx(control, target)

    def get_random_bits(self):
        sv = Statevector.from_instruction(self.qc)
        probs = sv.probabilities_dict()
        outcomes = list(probs.keys())
        weights = list(probs.values())
        choice = random.choices(outcomes, weights=weights, k=1)[0]
        return choice

    def visualize_bloch(self):
        sv = Statevector.from_instruction(self.qc)
        plot_bloch_multivector(sv)
        plt.show()

class Maze:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[' ']*size for _ in range(size)]
        self.player = [0,0]
        self.exit = [size-1, size-1]
        self.grid[self.exit[0]][self.exit[1]] = 'E'

    def display(self):
        os.system('cls' if os.name=='nt' else 'clear')
        for i in range(self.size):
            row = ''
            for j in range(self.size):
                if [i,j] == self.player:
                    row += 'P '
                else:
                    row += f"{self.grid[i][j]} "
            print(row)
        print()

    def move(self, direction):
        x, y = self.player
        if direction == 'U' and x > 0:
            self.player[0] -= 1
        elif direction == 'D' and x < self.size-1:
            self.player[0] += 1
        elif direction == 'L' and y > 0:
            self.player[1] -= 1
        elif direction == 'R' and y < self.size-1:
            self.player[1] += 1

    def is_exit(self):
        return self.player == self.exit

class QuantumMazeGame:
    def __init__(self, maze_size=4, n_qubits=2):
        self.maze = Maze(maze_size)
        self.qengine = QuantumEngine(n_qubits)
        self.n_qubits = n_qubits

    def random_direction(self):
        self.qengine.reset()
        for q in range(self.n_qubits):
            self.qengine.apply_hadamard(q)
        bits = self.qengine.get_random_bits()
        num = int(bits, 2)
        directions = ['U','D','L','R']
        return directions[num % 4]

    def play(self):
        print("Welcome to the Quantum Maze!")
        print("Reach the exit 'E'. Your moves are determined by qubits.")
        time.sleep(2)
        while not self.maze.is_exit():
            self.maze.display()
            move = self.random_direction()
            print(f"Qubits choose: {move}")
            self.maze.move(move)
            time.sleep(1)
        print("Congratulations! You reached the exit.")

    def visualize_qubits(self):
        self.qengine.reset()
        for q in range(self.n_qubits):
            self.qengine.apply_hadamard(q)
        self.qengine.visualize_bloch()

if __name__ == "__main__":
    game = QuantumMazeGame(maze_size=4, n_qubits=2)
    while True:
        print("Choose a mode:")
        print("1. Play the maze")
        print("2. Visualize qubits")
        print("3. Exit")
        choice = input(">>> ")
        if choice == '1':
            game.play()
            input("Press Enter to return to menu...")
        elif choice == '2':
            game.visualize_qubits()
            input("Press Enter to return to menu...")
        elif choice == '3':
            break
        else:
            print("Invalid choice")
