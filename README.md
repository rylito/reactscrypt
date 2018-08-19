# Reactscrypt

Reactscrypt is a Transcrypt module that allows you to write [React](https://reactjs.org/) code in a syntax similar in structure to JavaScript ES6 classes, but in Python. Rather than using [Babel](https://babeljs.io) as the transpiler, it leverages the [Transcrypt](https://www.transcrypt.org) transpiler to convert Python syntax to JavaScript that browsers can run.

This module includes wrappers for React.createClass and React.createElement along with some added utils and functionality.

## Example

The following code shows how to use React in Transcrypt. It is a basic use case that uses **React.createClass** and **React.createElement** directly:

```python
# Helper functions
    def h(elm_type, props='', *args):
        return React.createElement(elm_type, props, *args)

    def render(react_element, destination_id, callback=lambda: None):
        container = document.getElementById(destination_id)
        ReactDOM.render(react_element, container, callback)

    # Create a component
    Hello = React.createClass({
        'displayName': 'Hello',

        'getInitialState': lambda: {'counter': 0},

        'updateCounter': lambda: (this.setState({'counter': this.state['counter']+1})),

        'componentDidMount': lambda: (setInterval(this.updateCounter, 1000)),

        'render': lambda: h('div', {'className': 'maindiv'},
                              h('h1', None, 'Hello ', this.props['name']),
                              h('p', None, 'Lorem ipsum dolor sit ame.'),
                              h('p', None, 'Counter: ', this.state['counter'])
                            )
    })

    # Render the component in a 'container' div
    element = React.createElement(Hello, {'name': 'React!'})
    render(element, 'container')
```

Note: This example is from <https://www.transcrypt.org/examples#react_demo>

With Reactscrypt, this becomes:

```python
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
        self.set_state(lambda prev_state, props : {'counter': prev_state['counter'] + 1})

Hello(None).render_to('container', {'name': 'React!'})
```

This example and its compiled JavaScript source is included in **demos/counter**.

**demos/tic_tac_toe** contains another example. This is the React [example project](https://codepen.io/gaearon/pen/gWWZgR) ported to Python using Reactscrypt. It also demonstrates how Python imports can be used to organize your code into Python modules.

## Installation

To include the Reactscrypt module in your Transcrypt project, you can either drop the Reactscript module directory in your project, or make it available globally by placing it in **transcrypt/modules** directory of your Transcrypt installation.

## Other Notes

### Building the Demos
The demos contained in this repo already include the transpiled JavaScript, but if you'd like to play around with them and re-build, here's how to do that:
1. Ensure you have Transcrypt installed. Transcrypt requires Python 3.5 or 3.6. I recommend installing it in a virtual environment. Transcrypt installation instructions are here: <https://www.transcrypt.org/docs/html/installation_use.html#installation>
2. Make sure the Reactscrypt module is available to the demo projects. Either copy the **reactscrypt** directory into one of the demo folder OR make it available globally in Transcrypt by placing it in the **transcrypt/modules** directory of your Transcrypt installation
3. Vavigate to the demo you want to re-build and, build it with: **transcrypt -bmn [filename].py**. Note that this creates an un-minified build. There are several other options available in Transcrypt. Consult the [Transcrypt Docs](https://www.transcrypt.org/docs/html/index.html) for more info.

### About JSX

This module does not support JSX, as that would require an additional layer of complexity in the form of a pre-transpile step or perhaps modification/extension of Transcrypt itself since JSX is its own syntax and not Python or JavaScript. However, the React community seems to be pretty divided on JSX anyways. This module just provides a wrapper for **React.createElement** to build tags directly, and this approach is similar [HyperScript](https://github.com/mlmorg/react-hyperscript) which many in the JavaScript community seem to prefer over JSX anyways.

If you are interested in using JSX with React and Transcrypt, check out [PyReact](https://github.com/doconix/pyreact/blob/master/src/scripts/pyreact.py). It offers similar functionality to this module, but also allows you to specify JSX (currently as a string) for external processing by an Node.
