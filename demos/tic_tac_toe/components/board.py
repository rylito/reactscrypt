from reactscrypt.react import ReactComponent, ReactElement as e

class Board(ReactComponent):

    def render(self):

        def render_square(i):
            value = self.props['squares'][i]
            return e('button', {'class': 'square', 'onClick': lambda: self.props['onClick'](i)}, value)

        board = e('div')

        for row in range(3):
            board_row = e('div', {'class': 'board-row'})
            for col in range(3):
                index = (row * 3) + col
                board_row.append(render_square(index))
            board.append(board_row)

        return board
