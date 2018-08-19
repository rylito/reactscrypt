	(function () {
		var __name__ = '__main__';
		var Game = __init__ (__world__.components.game).Game;
		Game (null).render_to ('root');
		__pragma__ ('<use>' +
			'components.game' +
		'</use>')
		__pragma__ ('<all>')
			__all__.Game = Game;
			__all__.__name__ = __name__;
		__pragma__ ('</all>')
	}) ();
