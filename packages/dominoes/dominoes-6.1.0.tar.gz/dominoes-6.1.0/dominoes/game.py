import copy
import dominoes
import itertools
import random

def _randomized_hands():
    '''
    :return: 4 hands, obtained by shuffling the 28 dominoes used in
             this variation of the game, and distributing them evenly
    '''
    all_dominoes = [dominoes.Domino(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(all_dominoes)
    return [dominoes.Hand(all_dominoes[0:7]), dominoes.Hand(all_dominoes[7:14]),
            dominoes.Hand(all_dominoes[14:21]), dominoes.Hand(all_dominoes[21:28])]

def _validate_player(player):
    '''
    Checks that a player is a valid player. Valid players are: 0, 1, 2, and 3.

    :param int player: player to be validated
    :return: None
    :raises NoSuchPlayerException: if the player is invalid
    '''
    valid_players = range(4)
    if player not in valid_players:
        valid_players = ', '.join(str(p) for p in valid_players)
        raise dominoes.NoSuchPlayerException('{} is not a valid player. Valid players'
                                             ' are: {}'.format(player, valid_players))

def _domino_hand(d, hands):
    '''
    :param Domino d: domino to find within the hands
    :param list hands: hands to find domino in
    :return: index of the hand that contains the specified domino
    :raises NoSuchDominoException: if no hand contains the specified domino
    '''
    for i, hand in enumerate(hands):
        if d in hand:
            return i

    raise dominoes.NoSuchDominoException('{} is not in any hand!'.format(d))

def _remaining_points(hands):
    '''
    :param list hands: hands for which to compute the remaining points
    :return: a list indicating the amount of points
             remaining in each of the input hands
    '''
    points = []
    for hand in hands:
        points.append(sum(d.first + d.second for d in hand))

    return points

def _validate_hands(hands, missing):
    '''
    Validates hands, based on values that
    are supposed to be missing from them.

    :param list hands: list of Hand objects to validate
    :param list missing: list of sets that indicate the values
                         that are supposed to be missing from
                         the respective Hand objects
    :return: True if no Hand objects contain values that they
             are supposed to be missing; False otherwise
    '''
    for h, m in zip(hands, missing):
        for value in m:
            if dominoes.hand.contains_value(h, value):
                return False

    return True

def _all_possible_partitionings(elements, sizes):
    '''
    Helper function for Game.all_possible_hands(). Given a set of elements
    and the sizes of partitions, yields all possible partitionings of the
    elements into partitions of the provided sizes.

    :param set elements: a set of elements to partition.
    :param list sizes: a list of sizes for the partitions. The sum of the
                       sizes should equal the length of the set of elements.
    :yields: a tuple of tuples, each inner tuple corresponding to a partition.
    '''
    try:
        # get the size of the current partition
        size = sizes[0]
    except IndexError:
        # base case: no more sizes left
        yield ()
        return

    # don't include the current size in the recursive calls
    sizes = sizes[1:]

    # iterate over all possible partitions of the current size
    for partition in itertools.combinations(elements, size):
        # recursive case: pass down the remaining elements and the remaining sizes
        for other_partitions in _all_possible_partitionings(elements.difference(partition), sizes):
            # put results together and yield up
            yield (partition,) + other_partitions

def next_player(player):
    '''
    Returns the player that plays after the specified player.

    :param int player: player for which to calculate the
                       next player. Must be 0, 1, 2, or 3.
    :return: the next player
    '''
    return (player + 1) % 4

class Game:
    '''
    Python class for objects that represent a dominoes game.

    This variation of the dominoes game is played
    using 28 dominoes, which use values from 0 to 6:

    .. code-block:: none

        [0|0][0|1][0|2][0|3][0|4][0|5][0|6]
        [1|1][1|2][1|3][1|4][1|5][1|6]
        [2|2][2|3][2|4][2|5][2|6]
        [3|3][3|4][3|5][3|6]
        [4|4][4|5][4|6]
        [5|5][5|6]
        [6|6]

    These dominoes are shuffled, and distributed evenly among
    4 players. These players then sit on the edges of a square.
    Players sitting opposite of each other are on the same team,
    and the center of the square is the game board. Throughout
    the game, each player will only be able to see their hand,
    the game board, and the amount of dominoes left in the hands
    of the other players. Note that no player can see the values
    on the dominoes in the hands of the other players.

    The 4 players will then take turns placing dominoes from their
    hands onto the game board. The game board consists of a chain
    of dominoes placed end to end such that the values on connected
    ends always match.

    Prior to distributing the dominoes, the 4 players will agree on
    which player will play first, either by designating a specific
    player or a specific domino that must be played first (often [6|6]).
    After the game starts, play proceeds clockwise.

    If a player is able to place a domino on the board, he/she must.
    Only if they have no possible moves, can the pass on their turn.

    The game ends either when a player runs out of dominoes or when no
    player can play a domino (in which case we say the game is stuck).

    If a player runs out of dominoes, his/her team will earn a number
    of points computed by adding all the values of all the dominoes
    remaining in the hands of the 3 other players.

    If the game is stuck, each team will add up all the values of
    all the dominoes remaining in their hands. The team with the
    lower score wins, and earns a number of points computed by
    adding both teams' scores. If both teams have the same score,
    the game is declared a tie, and neither team earns any points.

    :var board: the game board
    :var hands: a list containing each player's hand
    :var moves: a list of the moves that have been played. Moves are
                represented by a tuple of Domino and bool. The domino
                indicates the domino that was played, and the bool
                indicates on what end of the board the domino was
                played (True for left, False for right). If the player
                passed, the move is None.
    :var turn: the player whose turn it is
    :var valid_moves: a tuple of valid moves for the player whose turn it is.
                      Moves are represented in the same way as in the moves list.
    :var starting_player: first player to make a move
    :var result: None if the game is in progress; otherwise a
                 Result object indicating the outcome of the game

    .. code-block:: python

        >>> import dominoes
        >>> d = dominoes.Domino(6, 6)
        >>> g = dominoes.Game.new(starting_domino=d)
        >>> g
        Board: [6|6]
        Player 0's hand: [2|4][5|5][2|3][1|3][1|6][1|2]
        Player 1's hand: [1|1][3|4][0|5][0|6][2|5][1|5][2|6]
        Player 2's hand: [0|4][0|3][4|4][3|6][0|2][4|5][1|4]
        Player 3's hand: [5|6][3|5][3|3][0|0][0|1][2|2][4|6]
        Player 1's turn
        >>> g.board
        [6|6]
        >>> g.hands
        [[2|4][5|5][2|3][1|3][1|6][1|2], [1|1][3|4][0|5][0|6][2|5][1|5][2|6], [0|4][0|3][4|4][3|6][0|2][4|5][1|4], [5|6][3|5][3|3][0|0][0|1][2|2][4|6]]
        >>> g.turn
        1
        >>> g.result
        >>> g.valid_moves # True is for the left of the board, False is for the right
        [([0|6], True), ([2|6], True)]
        >>> g.make_move(*g.valid_moves[0])
        >>> g.moves
        [([6|6], True), ([0|6], True)]
        >>> g
        Board: [0|6][6|6]
        Player 0's hand: [2|4][5|5][2|3][1|3][1|6][1|2]
        Player 1's hand: [1|1][3|4][0|5][2|5][1|5][2|6]
        Player 2's hand: [0|4][0|3][4|4][3|6][0|2][4|5][1|4]
        Player 3's hand: [5|6][3|5][3|3][0|0][0|1][2|2][4|6]
        Player 2's turn
        >>> g.make_move(*g.valid_moves[0])
        ...
        >>> g.make_move(*g.valid_moves[0])
        Result(player=1, won=True, points=-32)
        >>> g.result
        Result(player=1, won=True, points=-32)
        >>> g
        Board: [2|6][6|3][3|4][4|1][1|1][1|6][6|4][4|5][5|2][2|4][4|0][0|6][6|6][6|5][5|0][0|3][3|5][5|5][5|1][1|0]
        Player 0's hand: [2|3][1|3][1|2]
        Player 1's hand:
        Player 2's hand: [4|4][0|2]
        Player 3's hand: [3|3][0|0][2|2]
        Player 1 won and scored 32 points!
    '''
    def __init__(self, board, hands, moves, turn,
                 valid_moves, starting_player, result):
        self.board = board
        self.hands = hands
        self.moves = moves
        self.turn = turn
        self.valid_moves = valid_moves
        self.starting_player = starting_player
        self.result = result

    @classmethod
    def new(cls, starting_domino=None, starting_player=0):
        '''
        :param Domino starting_domino: the domino that should be played
                                       to start the game. The player
                                       with this domino in their hand
                                       will play first.
        :param int starting_player: the player that should play first.
                                    This value is ignored if a starting
                                    domino is provided. Players are
                                    referred to by their indexes: 0, 1,
                                    2, and 3. 0 and 2 are on one team,
                                    and 1 and 3 are on another team.
        :return: a new game, initialized according to
                 starting_domino and starting_player
        :raises NoSuchDominoException: if starting_domino is invalid
        :raises NoSuchPlayerException: if starting_player is invalid
        '''
        board = dominoes.Board()

        hands = _randomized_hands()

        moves = []

        result = None

        if starting_domino is None:
            _validate_player(starting_player)
            valid_moves = tuple((d, True) for d in hands[starting_player])
            game = cls(board, hands, moves, starting_player,
                       valid_moves, starting_player, result)
        else:
            starting_player = _domino_hand(starting_domino, hands)
            valid_moves = ((starting_domino, True),)
            game = cls(board, hands, moves, starting_player,
                       valid_moves, starting_player, result)
            game.make_move(*valid_moves[0])

        return game

    def skinny_board(self):
        '''
        Converts the board representation used by this game from a regular
        Board to a less descriptive but more memory efficient SkinnyBoard.

        :return: None
        '''
        self.board = dominoes.SkinnyBoard.from_board(self.board)

    def _update_valid_moves(self):
        '''
        Updates self.valid_moves according to the latest game state.
        Assumes that the board and all hands are non-empty.
        '''
        left_end = self.board.left_end()
        right_end = self.board.right_end()

        moves = []
        for d in self.hands[self.turn]:
            if left_end in d:
                moves.append((d, True))
            # do not double count moves if both of the board's ends have
            # the same value, and a domino can be placed on both of them
            if right_end in d and left_end != right_end:
                moves.append((d, False))

        self.valid_moves = tuple(moves)

    def make_move(self, d, left):
        '''
        Plays a domino from the hand of the player whose turn it is onto one
        end of the game board. If the game does not end, the turn is advanced
        to the next player who has a valid move.

        Making a move is transactional - if the operation fails at any point,
        the game will return to its state before the operation began.

        :param Domino d: domino to be played
        :param bool left: end of the board on which to play the
                          domino (True for left, False for right)
        :return: a Result object if the game ends; None otherwise
        :raises GameOverException: if the game has already ended
        :raises NoSuchDominoException: if the domino to be played is not in
                                       the hand of the player whose turn it is
        :raises EndsMismatchException: if the domino cannot be placed on
                                       the specified position in the board
        '''
        if self.result is not None:
            raise dominoes.GameOverException('Cannot make a move - the game is over!')

        i = self.hands[self.turn].play(d)

        try:
            self.board.add(d, left)
        except dominoes.EndsMismatchException as error:
            # return the domino to the hand if it cannot be placed on the board
            self.hands[self.turn].draw(d, i)

            raise error

        # record the move
        self.moves.append((d, left))

        # check if the game ended due to a player running out of dominoes
        if not self.hands[self.turn]:
            self.valid_moves = ()
            self.result = dominoes.Result(
                self.turn, True, pow(-1, self.turn) * sum(_remaining_points(self.hands))
            )
            return self.result

        # advance the turn to the next player with a valid move.
        # if no player has a valid move, the game is stuck. also,
        # record all the passes.
        passes = []
        stuck = True
        for _ in self.hands:
            self.turn = next_player(self.turn)
            self._update_valid_moves()
            if self.valid_moves:
                self.moves.extend(passes)
                stuck = False
                break
            else:
                passes.append(None)

        if stuck:
            player_points = _remaining_points(self.hands)
            team_points = [player_points[0] + player_points[2],
                           player_points[1] + player_points[3]]

            if team_points[0] < team_points[1]:
                self.result = dominoes.Result(self.turn, False, sum(team_points))
            elif team_points[0] == team_points[1]:
                self.result = dominoes.Result(self.turn, False, 0)
            else:
                self.result = dominoes.Result(self.turn, False, -sum(team_points))

            return self.result

    def missing_values(self):
        '''
        Computes the values that must be missing from each
        player's hand, based on when they have passed.

        :return: a list of sets, each one containing the
                 values that must be missing from the
                 corresponding player's hand
        '''
        missing = [set() for _ in self.hands]

        # replay the game from the beginning
        board = dominoes.SkinnyBoard()
        player = self.starting_player
        for move in self.moves:
            if move is None:
                # pass - update the missing values
                missing[player].update([board.left_end(), board.right_end()])
            else:
                # not a pass - update the board
                board.add(*move)

            # move on to the next player
            player = next_player(player)

        return missing

    def random_possible_hands(self):
        '''
        Returns random possible hands for all players, given the information
        known by the player whose turn it is. This information includes the
        current player's hand, the sizes of the other players' hands, and the
        moves played by every player, including the passes.

        :return: a list of possible Hand objects, corresponding to each player
        '''
        # compute values that must be missing from
        # each hand, to rule out impossible hands
        missing = self.missing_values()

        # get the dominoes that are in all of the other hands. note that, even
        # though we are 'looking' at the other hands to get these dominoes, we
        # are not 'cheating' because these dominoes could also be computed by
        # subtracting the dominoes that have been played (which are public
        # knowledge) and the dominoes in the current player's hand from the
        # initial set of dominoes
        other_dominoes = [d for p, h in enumerate(self.hands) for d in h if p != self.turn]

        while True:
            # generator for a shuffled shallow copy of other_dominoes
            shuffled_dominoes = (d for d in random.sample(other_dominoes, len(other_dominoes)))

            # generate random hands by partitioning the shuffled dominoes according
            # to how many dominoes need to be in each of the other hands. since we
            # know the current player's hand, we just use a shallow copy of it
            hands = []
            for player, hand in enumerate(self.hands):
                if player != self.turn:
                    hand = [next(shuffled_dominoes) for _ in hand]
                hands.append(dominoes.Hand(hand))

            # only return the hands if they are possible, according to the values we
            # know to be missing from each hand. if the hands are not possible, try
            # generating random hands again
            if _validate_hands(hands, missing):
                return hands

    def all_possible_hands(self):
        '''
        Yields all possible hands for all players, given the information
        known by the player whose turn it is. This information includes the
        current player's hand, the sizes of the other players' hands, and the
        moves played by every player, including the passes.

        :yields: a list of possible Hand objects, corresponding to each player
        '''
        # compute values that must be missing from
        # each hand, to rule out impossible hands
        missing = self.missing_values()

        # get the dominoes that are in all of the other hands. note that, even
        # though we are 'looking' at the other hands to get these dominoes, we
        # are not 'cheating' because these dominoes could also be computed by
        # subtracting the dominoes that have been played (which are public
        # knowledge) and the dominoes in the current player's hand from the
        # initial set of dominoes
        other_dominoes = {d for p, h in enumerate(self.hands) for d in h if p != self.turn}

        # get the lengths of all the other hands, so
        # that we know how many dominoes to place in each
        other_hand_lengths = [len(h) for p, h in enumerate(self.hands) if p != self.turn]

        # iterate over all possible hands that the other players might have
        for possible_hands in _all_possible_partitionings(other_dominoes, other_hand_lengths):
            # given possible hands for all players, this is a generator for
            # tuples containing the dominoes that are in the other players' hands
            possible_hands = (h for h in possible_hands)

            # build a list containing possible hands for all players. since we
            # know the current player's hand, we just use a shallow copy of it
            hands = []
            for player, hand in enumerate(self.hands):
                if player != self.turn:
                    hand = next(possible_hands)
                hands.append(dominoes.Hand(hand))

            # only yield the hands if they are possible, according
            # to the values we know to be missing from each hand
            if _validate_hands(hands, missing):
                yield hands

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __deepcopy__(self, _):
        if isinstance(self.board, dominoes.SkinnyBoard):
            if self.board:
                # SkinnyBoard attributes are ints; no need to deepcopy
                board = dominoes.SkinnyBoard(self.board.left_end(),
                                             self.board.right_end(),
                                             len(self.board))
            else:
                # board is empty
                board = dominoes.SkinnyBoard()
        else:
            # TODO: optimize for Board class
            board = copy.deepcopy(self.board)

        # only need to copy the Hand, because the Domino objects are
        # immutable. note that using copy.copy does not work because
        # the container of the Domino objects within the Hand also
        # needs to be copied, which the Hand initializer takes care of.
        hands = [dominoes.Hand(hand) for hand in self.hands]

        # list of tuples of Domino and bool; shallow copy is sufficient
        moves = list(self.moves)

        # tuple of immutable Domino objects; no need to deepcopy
        valid_moves = self.valid_moves

        # None or namedtuple of ints and bools; no need to deepcopy
        result = self.result

        # just an int; no need to deepcopy
        turn = self.turn

        # just an int; no need to deepcopy
        starting_player = self.starting_player

        return type(self)(board, hands, moves, turn,
                          valid_moves, starting_player, result)

    def __str__(self):
        string_list = ['Board: {}'.format(self.board)]

        for i, hand in enumerate(self.hands):
            string_list.append("Player {}'s hand: {}".format(i, hand))

        if self.result is None:
            string_list.append("Player {}'s turn".format(self.turn))
        else:
            if self.result.won:
                string_list.append(
                    'Player {} won and scored {} points!'.format(self.result.player,
                                                                 abs(self.result.points))
                )
            else:
                if not self.result.points:
                    string_list.append(
                        'Player {} stuck the game and tied (0 points)!'.format(self.result.player)
                    )
                elif pow(-1, self.result.player) * self.result.points > 0:
                    string_list.append(
                        'Player {} stuck the game and scored {} points!'.format(self.result.player,
                                                                                abs(self.result.points))
                    )
                else:
                    string_list.append(
                        'Player {} stuck the game and scored'
                        ' {} points for the opposing team!'.format(self.result.player,
                                                                   abs(self.result.points))
                    )

        return '\n'.join(string_list)

    def __repr__(self):
        return str(self)
