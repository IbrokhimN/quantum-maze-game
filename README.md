# Quantum Maze Game

**Quantum Maze Game** is an educational Python project demonstrating the principles of quantum randomness applied to a simple maze game. The player's movements are determined by quantum states, generated and simulated using [Qiskit](https://qiskit.org/). The project also provides Bloch sphere visualization of qubit states.

---

## Features
- Maze navigation where moves are dictated by quantum-generated outcomes.
- Integration with **Qiskit** for quantum state preparation and measurement.
- Visualization of qubit states on the **Bloch sphere**.
- Interactive text-based gameplay.

---
---

## Requirements

* Python 3.9+
* [Qiskit](https://qiskit.org/)
* Matplotlib

All requirements are listed in `requirements.txt`.

---

## Usage

Run the game:

```bash
python quantum_maze.py
```

Available modes:

1. **Play the maze** – Navigate to the exit, with moves chosen by qubits.
2. **Visualize qubits** – Display qubit states on the Bloch sphere.
3. **Exit** – Terminate the program.

---

## Example Gameplay

```
Choose a mode:
1. Play the maze
2. Visualize qubits
3. Exit
>>> 1

Welcome to the Quantum Maze!
Reach the exit 'E'. Your moves are determined by qubits.

P              
               
               
              E
Qubits choose: R
```

---

## Purpose

This project is designed as a **didactic tool** for introducing quantum computing concepts through interactive gameplay.
It illustrates:

* Randomness from quantum superposition.
* Statevector probabilities.
* Basic visualization of quantum states.

---

## License

This project is distributed under the **MIT License**. See `LICENSE` for details.
