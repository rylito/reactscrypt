# this is a port of the demo at https://www.transcrypt.org/examples#react_demo
# it makes use of the reactscrypt bindings to provide a more Pythonic syntax
# derived from React's ES6 classes

from reactscrypt.react import ReactComponent, ReactElement as e

class Hello(ReactComponent):

    initial_state = {
        'counter': 0
    }

    def render(self):
        return e('div', {'class': 'maindiv'},
            e('h1', None, 'Hello ', self.props['name']),
            e('p', None, 'Lorem ipsum dolor sit ame.'),
            e('p', None, 'Counter: ', self.state['counter'])
        )

    def component_did_mount(self):
        setInterval(self.update_counter, 1000)

    def update_counter(self):
        # use the updater method form of set_state to avoid race conditions since the next state
        # of loading_info depends on the previous state.
        # see https://reactjs.org/docs/react-component.html#setstate 
        self.set_state(lambda prev_state, props : {'counter': prev_state['counter'] + 1})

Hello(None).render_to('container', {'name': 'React!'})

