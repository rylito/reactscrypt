	(function () {
		var __name__ = '__main__';
		var ReactComponent = __init__ (__world__.reactscrypt.react).ReactComponent;
		var e = __init__ (__world__.reactscrypt.react).ReactElement;
		var Hello = __class__ ('Hello', [ReactComponent], {
			__module__: __name__,
			initial_state: dict ({'counter': 0}),
			get render () {return __get__ (this, function (self) {
				return e ('div', dict ({'class': 'maindiv'}), e ('h1', null, 'Hello ', self.props ['name']), e ('p', null, 'Lorem ipsum dolor sit ame.'), e ('p', null, 'Counter: ', self.state ['counter']));
			});},
			get component_did_mount () {return __get__ (this, function (self) {
				setInterval (self.update_counter, 1000);
			});},
			get update_counter () {return __get__ (this, function (self) {
				self.set_state ((function __lambda__ (prev_state, props) {
					return dict ({'counter': prev_state ['counter'] + 1});
				}));
			});}
		});
		Hello (null).render_to ('container', dict ({'name': 'React!'}));
		__pragma__ ('<use>' +
			'reactscrypt.react' +
		'</use>')
		__pragma__ ('<all>')
			__all__.Hello = Hello;
			__all__.ReactComponent = ReactComponent;
			__all__.__name__ = __name__;
			__all__.e = e;
		__pragma__ ('</all>')
	}) ();
