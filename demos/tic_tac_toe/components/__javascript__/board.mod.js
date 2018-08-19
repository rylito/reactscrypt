	__nest__ (
		__all__,
		'components.board', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'components.board';
					var ReactComponent = __init__ (__world__.reactscrypt.react).ReactComponent;
					var e = __init__ (__world__.reactscrypt.react).ReactElement;
					var Board = __class__ ('Board', [ReactComponent], {
						__module__: __name__,
						get render () {return __get__ (this, function (self) {
							var render_square = function (i) {
								var value = self.props ['squares'] [i];
								return e ('button', dict ({'class': 'square', 'onClick': (function __lambda__ () {
									return self.props ['onClick'] (i);
								})}), value);
							};
							var board = e ('div');
							for (var row = 0; row < 3; row++) {
								var board_row = e ('div', dict ({'class': 'board-row'}));
								for (var col = 0; col < 3; col++) {
									var index = row * 3 + col;
									board_row.append (render_square (index));
								}
								board.append (board_row);
							}
							return board;
						});}
					});
					__pragma__ ('<use>' +
						'reactscrypt.react' +
					'</use>')
					__pragma__ ('<all>')
						__all__.Board = Board;
						__all__.ReactComponent = ReactComponent;
						__all__.__name__ = __name__;
						__all__.e = e;
					__pragma__ ('</all>')
				}
			}
		}
	);
