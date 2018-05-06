# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver
Student:  Kahlil Khan

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twin strategy ensures that no other box in the same unit shares digits with naked twins.  It is essentially an advanced elimination technique.  Once a naked twin pair is found, the function iterates through the rest of the shared units to remove the twin's two digits from the peers.   Although this may not solve the peer's value, it often reduces its number of possibilities, increasing the efficiency of the other strategies and the recursive depth-first search function.

# Question 2 (Diagonal Sudoku)
Q: By adding the two major diagonals as units to the unitlist and peers dictionaries, these units become constraints to the existing solution functions (eliminate, only choice, naked twins, reduce, and search) that rely on those dictionaries to identify peers.  For example, the "eliminate" function now factors in the diagonal units when reviewing a box's peers, and if that box falls on either of the major diagonals, there are additional peers to iterate through for possible value elimination.  Adding constraints, such as diagonal units, appears to restrict the number of possibilities remaining for unsolved boxes, making the puzzle easier to solve.

### Install

This project requires Python 3.  Pygame for visualization is optional.

### Code

* `solutions.py` - Sukodu grid encoding and strategy functions (eliminate, only choice, naked twins, search)
* `solution_test.py` - Unit test cases; run `python solution_test.py`.
* `PySudoku.py` - Code for visualizing your solution.
* `visualize.py` - Code for visualizing your solution.

### Data

The data consists of a text file of diagonal sudokus.