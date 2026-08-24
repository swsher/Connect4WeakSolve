from time import perf_counter, sleep

def init_game():
    """
    Returns a board representing a new game.
    
    Args:
    
    Returns:
        list[list[list[str]], bool]: Created game.
    """
    
    board = [["-" for i in range(0, 5)] for j in range(0, 5)]
    is_red_turn = True
    
    game_state = [board, is_red_turn]
    return game_state

def get_game_string(game_state=None):
    """
    Gets a string of the game to be printed.
    
    Args:
        game_state (list[list[list[str], bool]]): Game to be printed.
    
    Returns:
        str: Printable string representation of the board.
    """
    turn = "Yellow"
    if game_state[1]:
        turn = "Red"
    return_string = f"Current Turn: {turn}\n"
    
    for row in game_state[0]:
        for tile in row:
            return_string += f"{tile} "
        return_string += "\n"

    return return_string
    
def game_state_shallow_debug(parent_func=None, game_state=None):
    """
    Performs a shallow check on a list representing a connect 3 game state, raising an error if it is malformed.
    
    Args:
        game_state (list[list[list[str]], bool): Object to be checked.
        parent_func (str): Name of originating function.
    
    Returns:
        None
    """
    
    assert isinstance(parent_func, str), "Parent function not passed into debugging function"
    assert isinstance(game_state, list), f"Instead of a list representing the game state, {type(game_state)} passed into {parent_func}"
    
    assert isinstance(game_state[0], list), f"Instead of a list for the board, {type(game_state[0])} in game state passed into {parent_func}"
    assert isinstance(game_state[0][0], list), f"Instead of a 2d list for the board, a 1d list was in game state passed into {parent_func}"
    assert isinstance(game_state[0][0][0], str), f"Instead of a string for each tile, {type(game_state[0][0][0])} was in game state passed into {parent_func}"
    assert isinstance(game_state[1], bool), f"Instead of a bool for the turn, {type(game_state[1])} in game state passed into {parent_func}"
    
    assert len(game_state[0]) == 5, f"Invalid row count in game state passed into {parent_func}: {len(game_state[0])}"
    assert len(game_state[0][0]) == 5, f"Invalid column count in game state passed into {parent_func}: {len(game_state[0][0])}"

def game_state_deep_debug(parent_func=None, game_state=None):
    """
    Performs a deep check on a connect 3 game state, raising an error if it detects a state irregularity.
    
    Args:
        game_state (list[list[list[str]], bool): Object to be checked.
        parent_func (str): Name of originating function.
        
    Returns:
        None
    """
    
    game_state_shallow_debug(parent_func, game_state)
    
    board = game_state[0]
    is_red_turn = game_state[1]
    
    red_count = 0
    yellow_count = 0
    total_tiles = 0
    
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            assert tile == "-" or tile == "r" or tile == "y", f"Invalid tile at ({j}, {i}): {tile} in game state passed into {parent_func}"
            red_count += tile == "r"
            yellow_count += tile == "y"
            total_tiles += 1
            
    assert total_tiles == 25, f"Invalid tile count on board: {total_tiles}, in game state passed into {parent_func}"
    assert yellow_count <= red_count, f"Irregular game state: more yellow tiles than reds in game state passed into {parent_func}"
    assert is_red_turn or red_count > yellow_count, f"Irregular game state: same amount of red and yellow tiles on yellow turn in game state passed into {parent_func}"
    assert not is_red_turn or red_count == yellow_count, f"Irregular game state: more reds than yellows on red turn in game state passed into {parent_func}"
            

def win_check(game_state=None, debug_mode="None"):
    """
    Naive algorithm to check if a connect 3 game has been won or tied.
    
    Args:
        game_state (list[list[list[str]], bool]): Game to be checked.
        debug_mode (str): The level of debug mode to run in: "Deep", "Shallow", or "None".
    
    Returns:
        str: Status of the game, either: "Red Win", "Yellow Win", "Tie", or "Continue"
    """
    
    if debug_mode == "Shallow":
        game_state_shallow_debug("win_check", game_state)
    elif debug_mode == "Deep":
        game_state_deep_debug("win_check", game_state)
    
    board = game_state[0]
    last_turn_red = not game_state[1]
    
    target_tile = ""
    win_string = ""
    
    if last_turn_red:
        target_tile = "r"
        win_string = "Red Win"
    else:
        target_tile = "y"
        win_string = "Yellow Win"
    
    # horizontal win checks
    row = 0
    while row < 5:
        column = 0
        while column < 3:
            if board[row][column] == target_tile and board[row][column+1] == target_tile and board[row][column+2] == target_tile:
                return win_string
            column += 1
        row += 1
    
    # vertical win checks
    row = 0
    while row < 3:
        column = 0
        while column < 5:
            if board[row][column] == target_tile and board[row+1][column] == target_tile and board[row+2][column] == target_tile:
                return win_string
            column += 1
        row += 1
                
    # diagonal down right win checks
    row = 0
    while row < 3:
        column = 0
        while column < 3:
            if board[row][column] == target_tile and board[row+1][column+1] == target_tile and board[row+2][column+2] == target_tile:
                return win_string
            column += 1
        row += 1
        
    # diagonal down left win checks
    row = 2
    while row < 5:
        column = 0
        while column < 3:
            if board[row][column] == target_tile and board[row-1][column+1] == target_tile and board[row-2][column+2] == target_tile:
                return win_string
            column += 1
        row += 1
    
    for row in board:
        for tile in row:
            if tile == "-":
                return "Continue"
                
    return "Tie"
    
def get_all_moves(game_state=None, debug_mode="None"):
    """
    Gets an unsorted list of all possible moves from a given position.
    
    Args:
        game_state (list[list[list[str]], bool]): Game to be checked.
        debug_mode (str): The level of debug mode to run in: "Deep", "Shallow", or "None".
    
    Returns:
        list: Columns of all possible moves
    """
    
    if debug_mode == "Shallow":
        game_state_shallow_debug("get_all_moves", game_state)
    elif debug_mode == "Deep":
        game_state_deep_debug("get_all_moves", game_state)
    
    possible_moves = []
    top_row = game_state[0][0]
    
    for column, tile in enumerate(top_row):
        if tile == "-":
            possible_moves.append(column)
    
    return possible_moves
    
def copy_game_state(game_state=None, debug_mode="None"):
    """
    Returns a deep copy of the game state passed in.
    
    Args:
        game_state (list[list[list[str]], bool]): Game state to be copied.
        debug_mode (str): The level of debug mode to run in: "Deep", "Shallow", or "None".
    
    Returns:
        list[list[list[str]], bool]: Copy of the original game state.
    """
    
    if debug_mode == "Shallow":
        game_state_shallow_debug("copy_game_state", game_state)
    elif debug_mode == "Deep":
        game_state_deep_debug("copy_game_state", game_state)
        
    new_board = [["-" for i in range(0, 5)] for j in range(0, 5)]
    for i in range(0, 5):
        for j in range(0, 5):
            new_board[i][j] = game_state[0][i][j]
    new_is_red_turn = game_state[1]
    
    new_game_state = [new_board, new_is_red_turn]
    return new_game_state
    

def play_move(game_state=None, column=67, debug_mode="None"):
    """
    Returns a new game state after a piece has been placed.
    
    Args:
        game_state (list[list[list[str]], bool]): Original game state.
        column (int): Column in which a piece has been placed.
        debug_mode (str): The level of debug mode to run in: "Deep", "Shallow", or "None".
    
    Returns:
        list[list[list[str]], bool]: New game state after the move has occurred.
    """
    
    new_game_state = copy_game_state(game_state, debug_mode)
    
    if debug_mode == "Shallow":
        game_state_shallow_debug("play_move", new_game_state)
    elif debug_mode == "Deep":
        game_state_deep_debug("play_move", new_game_state)
    
    turn = "y"
    if new_game_state[1]:
        turn = "r"
    new_game_state[1] = not new_game_state[1]
    
    row = 4
    while row > -1:
        if new_game_state[0][row][column] == "-":
            new_game_state[0][row][column] = turn
            return new_game_state
        row -= 1
    
    return new_game_state

def get_next_open(stack, current):
    for i in range(current, len(stack)):
        if stack[i] is None:
            return i
    for i in range(0, current):
        if stack[i] is None:
            return i
    return -1

def get_next_unsolved(stack, index_queue=None):
    if index_queue is None or not index_queue:
        index_queue = [0]
    
    while index_queue:
        current_index = index_queue[0]
        del index_queue[0]
        if stack[current_index] is None:
            continue
        
        for index in reversed(stack[current_index][3]):
            index_queue.insert(0, index)
        
        if not stack[current_index][2]:
            return current_index, index_queue

    return None, index_queue

# works
def red_turn_red_win(stack, index, forward_index=None):
    if index is not None:
        print(stack[index][3])
    print(forward_index)
    if stack[index][3] != [forward_index]:
        for del_index in stack[index][3]:
            if del_index != forward_index:
                stack[index][3].remove(del_index)
                recursive_delete(stack, del_index)
    back_index = stack[index][0]
    return yellow_turn_red_win(stack, back_index, index)

# erroneous
def yellow_turn_red_win(stack, index, forward_index=None):
    if index is not None:
        print(stack[index][3])
    print(forward_index)
    if index is None:
        return True
    if stack[index][3][-1] == forward_index: # forced move for yellow
        back_index = stack[index][0]
        return red_turn_red_win(stack, back_index, index)
    else:
        return False
 
# works       
def red_turn_red_loss(stack, index, forward_index=None):
    if stack[index][3] == [forward_index]: # forced loss for red
        back_index = stack[index][0]
        return yellow_turn_red_loss(stack, back_index, index)
    else:
        stack[index][3].remove(forward_index)
        recursive_delete(stack, forward_index)
        return False
        
# works        
def yellow_turn_red_loss(stack, index, forward_index=None):
    back_index = stack[index][0]
    return red_turn_red_loss(stack, back_index, index)
    
def recursive_delete(stack, index):
    for new_index in stack[index][3]:
        recursive_delete(stack, new_index)
    stack[index] = None

def left_stack_traversal(stack):
    current_index = 0
    while stack[current_index][3]:
        current_index = stack[current_index][3][-1]

def full_stack_traversal(stack, current=0, printing=False):
    total = 1
    if stack[current] is None:
        return 0
    if(printing):
        sleep(0.1)
        print(get_game_string(stack[current][1]))
    for branch in stack[current][3]:
        total += full_stack_traversal(stack, branch, printing)
    return total

def stack_iteration(stack):
    for game in stack:
        if game is not None:
            print(get_game_string(game[1]))
            pass
        else:
            print("\nNone")

def solve(size=1000, debug_mode="None"):
    """
    Solves connect 3.
    
    Args:
        debug_mode (str): The level of debug mode to run in: "Deep", "Shallow", or "None".
        
    Returns:
        float: Time taken for the solution in seconds.
    """
    
    start_time = perf_counter()
    total_nodes_evaluated = 0
    current = 1
    # oop vs high dimensional lists
    # high dimensional lists no-diff :troll:
    game_stack = [None for i in range(0, size)]
    game_stack[0] = [None, init_game(), False, []] 
    # back_link, game_state, already_searched, forward_links
    test_time = 0
    index_queue = []
    
    while (get_next_open(game_stack, current) != -1):
        total_nodes_evaluated += 1
        if total_nodes_evaluated % 10000 == 0:
            print(f"Nodes evaluated: {total_nodes_evaluated}, Size: {full_stack_traversal(game_stack)}")
        if total_nodes_evaluated > 1000000:
            break
        
        s_t = perf_counter()
        current_index, index_queue = get_next_unsolved(game_stack, index_queue)
        test_time += perf_counter() - s_t
        
        current_game = game_stack[current_index] 
        current_game[2] = True
        
        game_status = win_check(current_game[1], debug_mode)
        
        if game_status == "Red Win":
            if red_turn_red_win(game_stack, current_game[0], current_index):
                continue
            continue
        elif game_status == "Yellow Win" or game_status == "Tie":
            if current_game[1][1]:
                if yellow_turn_red_loss(game_stack, current_game[0], current_index):
                    continue
            else:
                if red_turn_red_loss(game_stack, current_game[0], current_index):
                    break
            continue
        
        possible_moves = get_all_moves(current_game[1], debug_mode)

        for move in possible_moves:
            index = get_next_open(game_stack, current)
            if index == -1:
                break
            current = index + 1
            current_game[3].append(index)
            game_stack[index] = [current_index, play_move(current_game[1], move, debug_mode), False, []]
        
    
    full_stack_traversal(game_stack, printing=True)
    print(total_nodes_evaluated)
    #print(test_time)
    end_time = perf_counter()
    return end_time - start_time

DEBUG_MODE = "None"
duration = solve(10000, DEBUG_MODE) # 4.5 kN/s at 250k
print(duration)


