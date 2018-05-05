assignments = []

def assign_value(values, box, value):
    """
    Assigns an updated value, and if it is the final value for the box, 
        stores a copy of the sudoku board for pygame visualization
    Args:
        values(dict): The sudoku in dictionary form
        box(string): The box to be changed
        value(number):  The new value for the box
    Returns:
        Nothing
    """
    #print("\t", box, ": \t", values[box], "\t --> ", value)   #debugging
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Algorithm: 
        Identify naked twins, and iterate thru thier peers to remove digits 
        they share with the naked twin
    Args:
        values(dict): he sudoku in dictionary form
    Returns:
        The values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins,
    # First, find all boxes with 2 numbers
    doubles = [box for box in boxes if len(values[box]) == 2]   
    # Then, iterate thru doubles and its peers to find naked twins
    # Store in array as pairs, e.g. [['A3', 'C3'], ['H5', 'H8']]
    twins = [[a,b] for a in doubles for b in peers[a] if (a < b) and (values[a] == values[b])]

    # Eliminate the naked twins as possibilities for their peers
    for twin in twins:
        # find peers common between both twins
        common_peers = set.intersection(*[set(peers[twin[0]]), set(peers[twin[1]])])
        # iterate thru peers to remove digits shared with naked twin
        for peer in common_peers:
            for digit in values[twin[0]]:
                if digit in values[peer]:
                    values = assign_value(values, peer, values[peer].replace(digit,''))
    
    return values

def cross(A, B):
    """
    Cross product of elements in A and elements in B.".
    Args:
        cross(string, string) - grid row and column markers in string form.
    Returns:
        An listing of boxes in array, e.g., ['A1','A2','A3','B1','B2'...]
    """
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # check if grid has right number of entries
    if len(grid) != 81:
        return False

    # create array of box values from grid string, replace '.' with '123456789'
    digits = '123456789'
    values = []
    for i in grid:
        if i == '.':
            values.append(digits)
        elif i in digits:
            values.append(i)
        else:
            print("Input error:  Non-numerical value in input string")

    # create dict of grid with keys and values
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values: 
        # copied from 'utils.py' code in lecture notes
        width = 1+max(len(values[s]) for s in boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                          for c in cols))
            if r in 'CF': print(line)
    else:
        print("Sorry, I could not find a solution to this sudoku.")

    return

def eliminate(values):
    """
    Applies one run of the sudoku 'elimination' strategy: If a box has a value
        assigned, then none of the peers of this box can have this value.
    Algorithm: 
        Go through all the boxes, and whenever there is a box with a single
        value, eliminate this value from the set of values of all its peers.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): Resulting Sudoku in dictionary form after eliminating value
    """
    # find boxes with a single value
    solved_boxes = [box for box in values if len(values[box]) == 1]

    # iterate thru solved boxes to eliminate its value in peers
    for box in solved_boxes:
            #print("Elim ", box, values[box])
            my_peers = peers[box] # gets peer array from peer dictionary
            for peer in my_peers:
                new_value = values[peer].replace(values[box],'')
                if new_value != values[peer]:  # if diff, assign new value
                    values = assign_value(values, peer, new_value)
    return values

def only_choice(values):
    """
    Applies one run of the sudoku 'only choice' strategy: If there is only
        one box in a unit which would allow a certain digit, then that box
        must be assigned that digit.
    Algorithm: 
        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): Resulting Sudoku in dictionary form after eliminating value
    """
    for unit in unitlist:
        for digit in '123456789':
            # create array for boxes contain current digit iteration 
            possible_choices = [box for box in unit if digit in values[box]]
            if len(possible_choices) == 1:                 #  then there is only one choice
                if digit != values[possible_choices[0]]:   #  if diff, assign new value
                    values = assign_value(values, possible_choices[0], digit)
    return values

def reduce_puzzle(values):
    """
    Apply reduction strategies until puzzle is solved or no more improvement
        can be made 
    Algorithm: 
        Iterating consective 'eliminate' and 'only_choice' strategies until 
        puzzle is solved or no more improvement can be made 
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): Resulting Sudoku in dictionary form after eliminating value
    """

    # modified from 'Constraint Propogation' lecture notes
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Pick a box with a minimal number of possible values. Try to solve each of 
        the puzzles obtained by choosing each of these values, recursively.
    Algorithm: 
        Using depth-first search and propagation, create a search tree and 
        solve the sudoku.
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): Resulting Sudoku in dictionary form after eliminating value
    """

    # First, reduce the puzzle
    values = reduce_puzzle(values)
    
    # Test recursive cases
    if values is False:
        return False    # failed
    if all(len(values[i]) == 1 for i in boxes):
        return values   # solved
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,unsolved_box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Select a digit from a unsolved box, use this value for that box, and start
    # recursion with the updated grid
    for digit in values[unsolved_box]:
        grid_copy = values.copy()
        grid_copy[unsolved_box] = digit
        attempt = search(grid_copy)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

# global variables specific for sudoku
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'], ['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    display(solve(diag_sudoku_grid))
    
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
