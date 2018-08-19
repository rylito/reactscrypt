from reactscrypt.react import ReactComponent, ReactElement as e
from components.board import Board

def calculate_winner(squares):
    lines = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    )

    for a,b,c in lines:
        if squares[a] and (squares[a] is squares[b]) and (squares[a] is squares[c]):
            return squares[a]
    return None

class Game(ReactComponent):

    initial_state = {
        'history': [{'squares': [None for _ in range(9)]}],
        'step_number': 0,
        'x_is_next': True
    }

    def handle_click(self, i):
        history = self.state['history'][0:self.state['step_number'] + 1]
        current = history[len(history) - 1]
        squares = current['squares'][:]

        # can also use javascript .slice() directly to copy
        #squares = current['squares'].slice()

        if calculate_winner(squares) or squares[i]:
            return

        squares[i] = 'X' if self.state['x_is_next'] else 'O'
        self.set_state({
            # use javascript concat directly
            # could also use utils.common.immutable_append
            'history': history.concat([{'squares': squares}]),
            'step_number': len(history),
            'x_is_next': not self.state['x_is_next']
        })

    def jump_to(self, step):
        self.set_state({
            'step_number': step,
            'x_is_next': (step % 2) == 0
        })

    def render(self):
        history = self.state['history']
        current = history[self.state['step_number']]
        winner = calculate_winner(current['squares'])

        def get_button(move):
            desc = 'Go to ' + ('move #' + move if move else 'game start')
            return e('li', {'key': move},
                e('button', {'onClick': lambda: self.jump_to(move)}, desc)
            )
        moves = [get_button(move) for move in range(len(history))]

        if winner:
            status = 'Winner: ' + winner
        else:
            status = 'Next player: ' + ('X' if self.state['x_is_next'] else 'O')

        return e('div', {'class': 'game'},
            e('div', {'class': 'game-board'},
                e(self.use('board', Board), {'squares': current['squares'], 'onClick': self.handle_click})
            ),
            e('div', {'class': 'game-info'},
                e('div', None, status),
                e('ol', None, moves)
            )
        )
