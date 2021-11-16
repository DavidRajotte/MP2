import time
import random

class Game:
    # Variables
    #   n: Size of the grid
    #   b: Number of blocs
    #   s: winning line up size
    #   d1: maximum search depth for player 1
    #   d2: maximum search depth for player 2
    #   t: maximum allowed search time
    #   a: which algorithm will be used

    n = 0
    b = 0
    s = 0
    d1 = 0
    d2 = 0
    t = 0
    a = False

    player_x = 'AI'
    player_o = 'AI'

    h1 = 'e1'
    h2 = 'e1'
    current_state = []
    bloc_positions = []

    win_x = ''
    win_o = ''

    player_turn = 'X'
    recommend = True

    MAX = 1
    MIN = 2

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    total_evaluation_time_e1 = 0
    total_evaluation_time_e2 = 0

    states_evaluated_e1 = 0
    states_evaluated_e2 = 0

    evaluation_time_e1 = 0
    evaluation_time_e2 = 0


    total_states_evaluated_e1 = 0

    total_states_evaluated_e2 = 0


    # Initialize the game
    def initialize_game(self, get_input=False, recommend=True, n=3, b=0, s=3, d1=4, d2=4, t=10, a=True, player_x='AI', player_o='AI', h1='e1', h2='e2'):
        self.player_turn = 'X'
        self.recommend = recommend

        self.evaluation_time = 0
        self.total_evaluation_time = 0

        # Get user input
        if get_input:
            # Set up game board
            self.n = self.get_board_size()
            self.current_state = [['.' for j in range(0, self.n)] for i in range(0, self.n)]

            # Set blocs on game board
            self.b = self.get_num_blocs()
            self.get_block_position()

            # Set winning line up size
            self.s = self.get_winning_line_up_size()

            # set maximum search depth for player 1 and player 2
            self.d1 = self.get_maximum_depth('X')
            self.d2 = self.get_maximum_depth('O')

            # Set maximum allowed search time
            self.t = self.get_maximum_time()

            # Set which algorithm will be used
            self.a = self.get_search_algorithm()

            # Set player mode for player 1 and player 2
            self.player_x = self.get_player_mode('X')
            self.player_o = self.get_player_mode('O')

            # Set which heuristic will be used for player 1 and player 2
            self.h1 = h1
            self.h2 = h2
        else:
            # Set up game board
            self.n = n
            self.current_state = [['.' for j in range(0, self.n)] for i in range(0, self.n)]

            # Set blocs on game board
            self.b = b
            for num in range(0, self.b):
                while True:
                    i = int(random.uniform(0, self.n))
                    j = int(random.uniform(0, self.n))
                    if self.is_valid_position(i, j):
                        self.bloc_positions.append([F"({j}, {i})"])
                        self.current_state[i][j] = '~'
                        break

            # Set winning line up size
            self.s = s

            # set maximum search depth for player 1 and player 2
            self.d1 = d1
            self.d2 = d2

            # Set maximum allowed search time
            self.t = t

            # Set which algorithm will be used
            self.a = a

            # Set player mode for player 1 and player 2
            self.player_x = player_x
            self.player_o = player_o

            # Set which heuristic will be used for player 1 and player 2
            self.h1 = h1
            self.h2 = h2

        # Define win condition
        self.win_x = ''.join(['X' for i in range(0, self.s)])
        self.win_o = ''.join(['O' for i in range(0, self.s)])

    # Get the game board
    def get_game_board(self):
        game_board = ""

        # Display Top row
        for i in range(-1, self.n):
            if i == -1:
                game_board += "\n| |"
            else:
                game_board += F'{self.alphabet[i]}|'

        # Display other rows
        for i in range(0, self.n):
            game_board += F"\n|{i}|"
            for j in range(0, self.n):
                game_board += F'{self.current_state[i][j]} '
        game_board += "\n"

        return game_board

    # ---------------------------------------------------------------
    # Check for win condition
    # evaluation function (needs to be quick)
    # ---------------------------------------------------------------
    def is_end_state(self):
        # Horizontal win
        for i in range(0, self.n):
            if self.win_x in ''.join(self.current_state[i]):
                return 'X'
            elif self.win_o in ''.join(self.current_state[i]):
                return 'O'

        # Vertical win
        for j in range(0, self.n):
            column = []
            for i in range(0, self.n):
                column.append(self.current_state[i][j])
            if self.win_x in ''.join(column):
                return 'X'
            elif self.win_o in ''.join(column):
                return 'O'

        # Get diagonals

        diag = [[self.current_state[i - j][j] for j in range(0, self.n) if 0 <= i - j < self.n] for i in range(0, 2 * self.n - 1)]

        for d in range(0, len(diag)):
            if self.win_x in ''.join(diag[d]):
                return 'X'
            elif self.win_o in ''.join(diag[d]):
                return 'O'

        # Is whole board Full
        for i in range(0, self.n):
            for j in range(0, self.n):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end_state()
        if self.result != None:
            return True, self.result
        else:
            return False, self.result

    # ---------------------------------------------------------------
    # Heuristics
    # ---------------------------------------------------------------
    def e1(self):
        value = 0

        start_time = time.time()

        # Just for analysis
        for i in range(0, 1000):
            a = 1

        for i in range(0, self.n):
            if 'O' in ''.join(self.current_state[i]):
                value = -25
            elif 'X' in ''.join(self.current_state[i]):
                value = 25

        end_time = time.time()

        evaluation_time = end_time - start_time

        self.evaluation_time_e1 += evaluation_time
        self.total_evaluation_time_e1 += evaluation_time

        self.states_evaluated_e1 += 1
        self.total_states_evaluated_e1 += 1

        return value

    def e2(self):
        value = 0

        start_time = time.time()

        # Just for analysis
        for i in range(0, 10000):
            a = 1

        for j in range(0, self.n):
            column = []
            for i in range(0, self.n):
                column.append(self.current_state[i][j])
            if 'X' in ''.join(column):
                value = -25
            elif 'O' in ''.join(column):
                value = 25

        end_time = time.time()

        evaluation_time = end_time - start_time

        self.evaluation_time_e2 += evaluation_time
        self.total_evaluation_time_e2 += evaluation_time

        self.states_evaluated_e2 += 1
        self.total_states_evaluated_e2 += 1

        return value


    # ---------------------------------------------------------------
    # Search Algorithms
    # ---------------------------------------------------------------
    # MiniMax
    def minimax(self, player=MIN, search_depth=0, max_search_depth=0, search_time=0, max_search_time=5, h='e1'):
        # Initialize value to 2 or -2 as worse than the worst case:
        if player == self.MAX:
            value = -100
        else: #player == self.MIN
            value = 100

        x = y = None

        # First check if search time is reached
        # Then check if max depth has been reached

        if search_time > max_search_time - 2:
            if h == 'e1':
                return self.e1(), x, y
            elif h == 'e2':
                return self.e2(), x, y
        elif search_depth == max_search_depth:
            if h == 'e1':
                return self.e1(), x, y
            elif h == 'e2':
                return self.e2(), x, y
            # run our heuristic and return

        result = self.is_end_state()
        if result == 'X':
            return -50, x, y
        elif result == 'O':
            return 50, x, y
        elif result == '.':
            return 0, x, y

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if player == self.MAX:
                        self.current_state[i][j] = 'O'
                        v, _, _ = self.minimax(self.MIN, search_depth=search_depth+1, max_search_depth=max_search_depth, h=h)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        v, _, _ = self.minimax(self.MAX, search_depth=search_depth+1, max_search_depth=max_search_depth, h=h)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return value, x, y

    # AlphaBeta
    def alphabeta(self, alpha=-2, beta=2, player=MIN, search_depth=0, max_search_depth=0, search_time=0, max_search_time=5, h='e1'):
        # Initialize value to 2 or -2 as worse than the worst case:
        if player == self.MAX:
            value = -100
        else:  # player == self.MIN
            value = 100

        x = y = None

        # First check if search time is reached
        # Then check if max depth has been reached

        if search_time > max_search_time-2:
            if h == 'e1':
                return self.e1(), x, y
            elif h == 'e2':
                return self.e2(), x, y
        elif search_depth == max_search_depth:
            if h == 'e1':
                return self.e1(), x, y
            elif h == 'e2':
                return self.e2(), x, y

        result = self.is_end_state()
        if result == 'X':
            return -50, x, y
        elif result == 'O':
            return 50, x, y
        elif result == '.':
            return 0, x, y

        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == '.':
                    if player == self.MAX:
                        self.current_state[i][j] = 'O'
                        v, _, _ = self.alphabeta(alpha, beta, player=self.MIN, search_depth=search_depth+1, max_search_depth=max_search_depth, h=h)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        v, _, _ = self.alphabeta(alpha, beta, player=self.MAX, search_depth=search_depth+1, max_search_depth=max_search_depth, h=h)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if player == self.MAX:
                        if value >= beta:
                            return value, x, y
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return value, x, y
                        if value < beta:
                            beta = value
        return value, x, y

    # ---------------------------------------------------------------
    # Game loop
    # ---------------------------------------------------------------
    def play_game_once(self):
        # Write to file
        file_name = F"gameTrace-{self.n}{self.b}{self.s}{self.t}.txt"
        f = open(file_name, "w")

        # Write the game parameters to the file
        f.write(F"n = {self.n} b = {self.b} s = {self.s} t = {self.t}")

        # Write the block positions to the file
        f.write(F"\nblocs = {self.bloc_positions}\n")

        # Write the parameters of each player to the file
        if self.player_x == 'AI':
            f.write(F"\nPlayer 1: AI, d = {self.d1} a = {self.a} {self.h1}")
        else:
            f.write(F"\nPlayer 1: H")
        if self.player_o == 'AI':
            f.write(F"\nPlayer 2: AI, d = {self.d2} a = {self.a} {self.h2}\n")
        else:
            f.write(F"\nPlayer 2: H\n")

        total_moves_x = 0
        total_moves_o = 0
        total_moves = 0

        evaluation_time = 0

        # Display/write the game board configuration
        print(self.get_game_board())
        f.write(self.get_game_board())

        self.total_evaluation_time_e1 = 0
        self.total_evaluation_time_e2 = 0

        # Main game loop
        while True:
            # Check if game is over
            end, result = self.check_end()
            if end:
                break

            # Display/Write which move is taking place
            total_moves += 1
            print(F'\nMove #{total_moves}\n')
            f.write(F'\nMove #{total_moves}\n')

            self.evaluation_time_e1 = 0
            self.evaluation_time_e2 = 0

            self.states_evaluated_e1 = 0
            self.states_evaluated_e2 = 0

            # Perform search
            # -------------------------------------------------------------------------------------
            start = time.time()

            if self.a:
                if self.player_turn == 'X':
                    m, i, j = self.alphabeta(player=self.MIN, max_search_depth=self.d1, h=self.h1)
                elif self.player_turn == 'O':
                    m, i, j = self.alphabeta(player=self.MAX, max_search_depth=self.d2, h=self.h2)
            else:
                if self.player_turn == 'X':
                    _, i, j = self.minimax(player=self.MIN, max_search_depth=self.d1, h=self.h1)
                elif self.player_turn == 'O':
                    _, i, j = self.minimax(player=self.MAX, max_search_depth=self.d2, h=self.h2)

            end = time.time()
            #-------------------------------------------------------------------------------------

            # If Human turn
            if (self.player_turn == 'X' and self.player_x == 'H') or (self.player_turn == 'O' and self.player_o == 'H'):
                # If reccomend
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 9)}s')
                    print(F'Recommended move: {self.alphabet[j]}{i}')

                # Get move from player
                i, j = self.get_move_position()

                # Write which move was taken
                f.write(F'\nPlayer {self.player_turn} under Human control plays: {self.alphabet[j]}{i}\n')

            # If AI turn
            if self.player_turn == 'X' and self.player_x == 'AI':
                print(F'Evaluation time: {round(end - start, 9)}s')
                print(F'Player {self.player_turn} under AI control plays: {self.alphabet[j]}{i}')

                # Write which move was taken
                f.write(F'\nPlayer {self.player_turn} under AI control plays: {self.alphabet[j]}{i}\n')

                if self.h1 == 'e1':
                    evaluation_time = self.evaluation_time_e1
                    states_evaluated = self.states_evaluated_e1
                elif self.h1 == 'e2':
                    evaluation_time = self.evaluation_time_e2
                    states_evaluated = self.states_evaluated_e2

                # Display heuristic statistics
                f.write(F"\ni   Evaluation time: {evaluation_time}")
                f.write(F"\nii  Heuristic evaluations: {states_evaluated}")
                f.write("\niii Evaluations by depth: ")
                f.write("\niv  Average evaluation depth: ")
                f.write("\nv   Average recursion depth \n")

            elif self.player_turn == 'O' and self.player_o == 'AI':
                print(F'Evaluation time: {round(end - start, 9)}s')
                print(F'Player {self.player_turn} under AI control plays: {self.alphabet[j]}{i}')

                # Write which move was taken
                f.write(F'\nPlayer {self.player_turn} under AI control plays: {self.alphabet[j]}{i}\n')

                if self.h2 == 'e1':
                    evaluation_time = self.evaluation_time_e1
                    states_evaluated = self.states_evaluated_e1
                elif self.h2 == 'e2':
                    evaluation_time = self.evaluation_time_e2
                    states_evaluated = self.states_evaluated_e2

                # Display heuristic statistics
                f.write(F"\ni   Evaluation time: {evaluation_time}")
                f.write(F"\nii  Heuristic evaluations: {states_evaluated}")
                f.write(F"\niii Evaluations by depth: ")
                f.write(F"\niv  Average evaluation depth: ")
                f.write(F"\nv   Average recursion depth \n")


            # Update the game board configuration
            self.current_state[i][j] = self.player_turn

            # Display/write the new game board configuration
            print(self.get_game_board())
            f.write(self.get_game_board())

            # Swap players
            if self.player_turn == 'X':
                self.player_turn = 'O'
            elif self.player_turn == 'O':
                self.player_turn = 'X'

        # Display/write the result of the game
        if result == '.':
            print('It\'s a tie')
            f.write('\nIt\'s a tie\n')
        elif result == 'X' or result == 'O':
            print(F'The winner is {result}!')
            f.write(F'\nThe winner is {result}!\n')

        # Write to file the results of the heuristic for player 1
        f.write(F"\nResults for heuristic e1\n")
        f.write(F"\ni   Average evaluation time: {self.total_evaluation_time_e1/self.total_states_evaluated_e1}")
        f.write(F"\nii  Total heuristic evaluations: {self.total_states_evaluated_e1}")
        f.write(F"\niii Evaluations by depth: ")
        f.write(F"\niv  Average evaluation depth: ")
        f.write(F"\nv   Average recursion depth ")
        f.write(F"\nvi  Total moves: {total_moves}\n")

        # Write to file the results of the heuristic for player 2
        f.write(F"\nResults for heuristic e2\n")
        f.write(F"\ni   Average evaluation time: {self.total_evaluation_time_e2/self.total_states_evaluated_e2}")
        f.write(F"\nii  Total heuristic evaluations: {self.total_states_evaluated_e2}")
        f.write(F"\niii Evaluations by depth: ")
        f.write(F"\niv  Average evaluation depth: ")
        f.write(F"\nv   Average recursion depth ")
        f.write(F"\nvi  Total moves: {total_moves}")

        f.close()

    def play_game_multiple(self, r=5):
        # Write to file
        file_name = F"scoreboard-{self.n}{self.b}{self.s}{self.t}.txt"
        f = open(file_name, "w")

        # Write the game parameters to the file
        f.write(F"n = {self.n} b = {self.b} s = {self.s} t = {self.t}")

        # Write the parameters of each player to the file
        if self.player_x == 'AI':
            f.write(F"\nPlayer 1: AI, d = {self.d1} a = {self.a}")
        else:
            f.write(F"\nPlayer 1: H")

        if self.player_o == 'AI':
            f.write(F"\nPlayer 2: AI, d = {self.d2} a = {self.a}\n")
        else:
            f.write(F"\nPlayer 2: H\n")

        total_e1_wins = 0
        total_e2_wins = 0
        total_ties = 0

        total_evaluation_time = 0
        moves = 0
        total_moves = 0


        f.write(F"\n{2*r} games\n")

        self.total_evaluation_time_e1 = 0
        self.total_evaluation_time_e2 = 0

        # Repeat 2 * r times
        for n in range(0, 2*r):
            # Main game loop
            while True:
                # Check if game is over
                end, result = self.check_end()
                if end:
                    break

                if n < r:
                    h1 = 'e1'
                    h2 = 'e2'
                else:
                    h1 = 'e2'
                    h2 = 'e1'

                moves += 1
                # Perform search
                # -------------------------------------------------------------------------------------
                start = time.time()

                if self.a:
                    if self.player_turn == 'X':
                        m, i, j = self.alphabeta(player=self.MIN, max_search_depth=self.d1, h=h1)
                    elif self.player_turn == 'O':
                        m, i, j = self.alphabeta(player=self.MAX, max_search_depth=self.d2, h=h2)
                else:
                    if self.player_turn == 'X':
                        _, i, j = self.minimax(player=self.MIN, max_search_depth=self.d1, h=h1)
                    elif self.player_turn == 'O':
                        _, i, j = self.minimax(player=self.MAX, max_search_depth=self.d2, h=h2)

                end = time.time()
                #-------------------------------------------------------------------------------------

                # Update the game board configuration
                self.current_state[i][j] = self.player_turn

                # Swap players
                if self.player_turn == 'X':
                    self.player_turn = 'O'
                elif self.player_turn == 'O':
                    self.player_turn = 'X'

            # Display/write the result of the game
            if result == '.':
                total_ties += 1
            elif result == 'X':
                if h1 == 'e1':
                    total_e1_wins += 1
                else:
                    total_e2_wins += 1
            elif result == 'O':
                if h2 == 'e1':
                    total_e1_wins += 1
                else:
                    total_e2_wins += 1

            total_moves += moves

        # Write the results of the games
        f.write(F'\nTotal wins for heuristic e1: {total_e1_wins}')
        f.write(F'\nTotal wins for heuristic e2: {total_e2_wins}')
        f.write(F'\nTies: {total_ties}\n')

        # Write to file the results of the heuristic for player 1
        f.write(F"\nResults for heuristic e1\n")
        f.write(F"\ni   Average evaluation time: {self.total_evaluation_time_e1/self.total_states_evaluated_e1}")
        f.write(F"\nii  Total heuristic evaluations: {self.total_states_evaluated_e1}")
        f.write(F"\niii Evaluations by depth: ")
        f.write(F"\niv  Average evaluation depth: ")
        f.write(F"\nv   Average recursion depth ")
        f.write(F"\nvi Average moves per game: {total_moves/(2*r)}")

        # Write to file the results of the heuristic for player 2
        f.write(F"\nResults for heuristic e2\n")
        f.write(F"\ni   Average evaluation time: {self.total_evaluation_time_e2/self.total_states_evaluated_e2}")
        f.write(F"\nii  Total heuristic evaluations: {self.total_states_evaluated_e2}")
        f.write(F"\niii Evaluations by depth: ")
        f.write(F"\niv  Average evaluation depth: ")
        f.write(F"\nv   Average recursion depth ")
        f.write(F"\nvi Average moves per game: {total_moves / (2 * r)}")

        f.close()

    # --------------------------------------------------------
    # Get user input
    #--------------------------------------------------------
    def get_board_size(self):
        while True:
            n = int(input('Enter the board size [3 - 10]: '))
            if 3 <= n <= 10:
                return n
            else:
                print('Board size must be in the range [3 - 10]! Try again.')

    def get_num_blocs(self):
        while True:
            b = int(input(F'Enter the number of blocs [0 - {self.n * 2}]: '))
            if 0 <= b <= self.n * 2:
                return b
            else:
                print(F'Bloc number must be in the range [0 - {self.n * 2}]! Try again.')

    def get_block_position(self):
        for num in range(0, self.b):
            print(self.get_game_board())
            while True:
                print(F'Enter position of block {num}:')
                j = self.get_column()
                i = self.get_row()
                if self.is_valid_position(i, j):
                    self.current_state[i][j] = '~'
                    self.bloc_positions.append([F"({j}, {i})"])
                    break
                else:
                    print(F'The bloc position must be in range [0 - {self.n}]! Try again.')

    def get_winning_line_up_size(self):
        while True:
            s = int(input(F'Enter the winning line up size [3 - {self.n}]: '))
            if 3 <= s <= self.n:
                return s
            else:
                print(F'Winning line up size must be in the range [3 - {self.n}]! Try again.')

    def get_maximum_depth(self, player):
        while True:
            d = int(input(F'Enter the maximum search depth for Player {player}: '))
            if 0 <= d:
                return d
            else:
                print('Maximum search depth must be greater than 0! Try again.')

    def get_maximum_time(self):
        while True:
            t = int(input('Enter the maximum allowed search time: '))
            if 0 <= t:
                return t
            else:
                print('Maximum search time must be greater than 0.')

    def get_search_algorithm(self):
        while True:
            a = input('Use alphabeta (T or F): ')
            if a == 'T' or a == 'F':
                if a == 'T':
                    return True
                elif a == 'F':
                    return False
            else:
                print('Input must be (T or F)! Try again.')

    def get_player_mode(self, player):
        while True:
            p = input(F'Enter the player mode for Player {player} (H or AI): ')
            if p == 'H' or p == 'AI':
                return p
            else:
                print(F'Input must be (H or AI)! Try again.')

    def get_move_position(self):
        while True:
            print(F'Player {self.player_turn}, enter your move: ')
            j = self.get_column()
            i = self.get_row()
            if self.is_valid_position(i, j):
                return i, j
            else:
                print(F'The position is not valid.')

    def get_column(self):
        while True:
            j = input('Enter the column: ')
            for n in range(0, self.n):
                if j == self.alphabet[n]:
                    return n
            print(F'The column must be in range [A - {self.alphabet[self.n]}]! Try again.')

    def get_row(self):
        while True:
            i = int(input('Enter the row: '))
            if 0 <= i < self.n:
                return i
            else:
                print(F'The row must be in range [0 - {self.n}]! Try again.')

    # --------------------------------------------------------
    # Check for valid position
    # --------------------------------------------------------
    def is_valid_position(self, i, j):
        if 0 <= i < self.n and 0 <= j < self.n:
            if self.current_state[i][j] == '.':
                return True
        return False


def main():
    # Create game object
    game = Game()

    # Initialize and play
    game.initialize_game(n=4, b=4, s=3, t=5, d1=6, d2=6, a=False)
    game.play_game_once()

    game.initialize_game(n=4, b=4, s=3, t=1, d1=6, d2=6, a=True)
    game.play_game_once()

    game.initialize_game(n=5, b=4, s=4, t=1, d1=6, d2=6, a=True)
    game.play_game_once()

    game.initialize_game(n=5, b=4, s=4, t=5, d1=6, d2=6, a=True)
    game.play_game_once()

    game.initialize_game(n=8, b=5, s=5, t=1, d1=6, d2=6, a=True)
    game.play_game_once()

    game.initialize_game(n=8, b=5, s=5, t=5, d1=6, d2=6, a=True)
    game.play_game_once()

    game.initialize_game(n=8, b=6, s=5, t=1, d1=6, d2=6, a=True)
    game.play_game_once()

    game.initialize_game(n=8, b=6, s=5, t=5, d1=6, d2=6, a=True)
    game.play_game_once()



    # Initialize and play multiple
    game.initialize_game(n=4, b=4, s=3, t=5, d1=6, d2=6, a=False)
    game.play_game_multiple()

    game.initialize_game(n=4, b=4, s=3, t=1, d1=6, d2=6, a=True)
    game.play_game_multiple()

    game.initialize_game(n=5, b=4, s=4, t=1, d1=6, d2=6, a=True)
    game.play_game_multiple()

    game.initialize_game(n=5, b=4, s=4, t=5, d1=6, d2=6, a=True)
    game.play_game_multiple()

    game.initialize_game(n=8, b=5, s=5, t=1, d1=6, d2=6, a=True)
    game.play_game_multiple()

    game.initialize_game(n=8, b=5, s=5, t=5, d1=6, d2=6, a=True)
    game.play_game_multiple()

    game.initialize_game(n=8, b=6, s=5, t=1, d1=6, d2=6, a=True)
    game.play_game_multiple()

    game.initialize_game(n=8, b=6, s=5, t=5, d1=6, d2=6, a=True)
    game.play_game_multiple()

if __name__ == "__main__":
    main()
