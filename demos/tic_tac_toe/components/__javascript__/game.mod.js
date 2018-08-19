	__nest__ (
		__all__,
		'components.game', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'components.game';
					var ReactComponent = __init__ (__world__.reactscrypt.react).ReactComponent;
					var e = __init__ (__world__.reactscrypt.react).ReactElement;
					var Board = __init__ (__world__.components.board).Board;
					var calculate_winner = function (squares) {
						var lines = tuple ([tuple ([0, 1, 2]), tuple ([3, 4, 5]), tuple ([6, 7, 8]), tuple ([0, 3, 6]), tuple ([1, 4, 7]), tuple ([2, 5, 8]), tuple ([0, 4, 8]), tuple ([2, 4, 6])]);
						var __iterable0__ = lines;
						for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
							var __left0__ = __iterable0__ [__index0__];
							var a = __left0__ [0];
							var b = __left0__ [1];
							var c = __left0__ [2];
							if (squares [a] && squares [a] === squares [b] && squares [a] === squares [c]) {
								return squares [a];
							}
						}
						return null;
					};
					var Game = __class__ ('Game', [ReactComponent], {
						__module__: __name__,
						initial_state: dict ({'history': list ([dict ({'squares': (function () {
							var __accu0__ = [];
							for (var _ = 0; _ < 9; _++) {
								__accu0__.append (null);
							}
							return __accu0__;
						}) ()})]), 'step_number': 0, 'x_is_next': true}),
						get handle_click () {return __get__ (this, function (self, i) {
							var history = self.state ['history'].__getslice__ (0, self.state ['step_number'] + 1, 1);
							var current = history [len (history) - 1];
							var squares = current ['squares'].__getslice__ (0, null, 1);
							if (calculate_winner (squares) || squares [i]) {
								return ;
							}
							squares [i] = (self.state ['x_is_next'] ? 'X' : 'O');
							self.set_state (dict ({'history': history.concat (list ([dict ({'squares': squares})])), 'step_number': len (history), 'x_is_next': !(self.state ['x_is_next'])}));
						});},
						get jump_to () {return __get__ (this, function (self, step) {
							self.set_state (dict ({'step_number': step, 'x_is_next': __mod__ (step, 2) == 0}));
						});},
						get render () {return __get__ (this, function (self) {
							var history = self.state ['history'];
							var current = history [self.state ['step_number']];
							var winner = calculate_winner (current ['squares']);
							var get_button = function (move) {
								var desc = 'Go to ' + (move ? 'move #' + move : 'game start');
								return e ('li', dict ({'key': move}), e ('button', dict ({'onClick': (function __lambda__ () {
									return self.jump_to (move);
								})}), desc));
							};
							var moves = (function () {
								var __accu0__ = [];
								for (var move = 0; move < len (history); move++) {
									__accu0__.append (get_button (move));
								}
								return __accu0__;
							}) ();
							if (winner) {
								var status = 'Winner: ' + winner;
							}
							else {
								var status = 'Next player: ' + (self.state ['x_is_next'] ? 'X' : 'O');
							}
							return e ('div', dict ({'class': 'game'}), e ('div', dict ({'class': 'game-board'}), e (self.use ('board', Board), dict ({'squares': current ['squares'], 'onClick': self.handle_click}))), e ('div', dict ({'class': 'game-info'}), e ('div', null, status), e ('ol', null, moves)));
						});}
					});
					__pragma__ ('<use>' +
						'components.board' +
						'reactscrypt.react' +
					'</use>')
					__pragma__ ('<all>')
						__all__.Board = Board;
						__all__.Game = Game;
						__all__.ReactComponent = ReactComponent;
						__all__.__name__ = __name__;
						__all__.calculate_winner = calculate_winner;
						__all__.e = e;
					__pragma__ ('</all>')
				}
			}
		}
	);
