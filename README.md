# 🧩 Eight Puzzle Solver

This project implements three classic search algorithms to solve the Eight Puzzle problem:
- *Uniform Cost Search (UCS)*
- **A* Search with Misplaced Tile heuristic*
- **A* Search with Manhattan Distance heuristic*

Developed as part of **CS205: Introduction to Artificial Intelligence** under Dr. Eamonn Keogh at the University of California, Riverside (Spring 2025).

---

## 📌 Problem Description

The **Eight Puzzle** is a sliding tile game consisting of a 3x3 grid with eight numbered tiles and one blank space. The objective is to reach a **goal state** (typically tiles in ascending order with the blank in the bottom-right) from a given initial configuration by sliding tiles into the blank space.

---

## 🚀 Features

- Accepts custom or default goal states
  
- Allows user-defined initial states
  
- Supports three search strategies:
  - UCS (uninformed)
  - A* with Misplaced Tile heuristic
  - A* with Manhattan Distance heuristic
    
- Tracks performance metrics:
  - Execution time
  - Memory usage
  - Nodes expanded
  - Solution depth

---

## 📊 Results Summary

Performance was evaluated on puzzles of varying depths. Key observations:

- At lower depths, all algorithms perform similarly.
- As depth increases, **UCS becomes significantly less efficient** in both time and memory.
- **A* with Manhattan Distance** consistently performs best due to its more accurate heuristic.
- All metrics were **manually tested and verified**.

Detailed results and analysis are available in the full report:  
📄 [Eight Puzzle Performance Report](https://docs.google.com/document/d/1o_r-64GTqWpBjQn3xDb5xHT1XkNp0AIdkMyxVF0ujRs/edit?usp=sharing)

---

## 🧠 Algorithms

| Algorithm                | Heuristic Used             | Optimal? | Complexity (Time & Space) |
|--------------------------|----------------------------|----------|----------------------------|
| Uniform Cost Search (UCS)| h(n) = 0                   | ✅        | O(b^d)                     |
| A* (Misplaced Tile)      | Number of misplaced tiles  | ✅        | O(b^d)                     |
| A* (Manhattan Distance)  | Sum of tile distances      | ✅        | O(b^d), but more efficient |

---

## 🛠 How to Run

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/8-Puzzle.git
    cd 8-Puzzle
    ```

2. Run the script:
    ```bash
    python3 solver.py
    ```

3. Follow the interactive prompts to choose:
    - Puzzle size
    - Initial and goal states
    - Search algorithm

---

## 📁 Files

| File                     | Description                                  |
|--------------------------|----------------------------------------------|
| `puzzle_solver.py`       | Main script with UCS and A* implementations |
| `stats.json`             | UCS performance data                        |
| `stats1.json`            | A* (Misplaced Tile) performance data        |
| `stats2.json`            | A* (Manhattan) performance data             |
| [`Eight Puzzle Report`](https://docs.google.com/document/d/1o_r-64GTqWpBjQn3xDb5xHT1XkNp0AIdkMyxVF0ujRs/edit?usp=sharing) | Full performance analysis and tables |



## 🙋‍♂️ Author

**Aryan Ramachandra**  
Graduate Student, Computational Data Science  
University of California, Riverside  
