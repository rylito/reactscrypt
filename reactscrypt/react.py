from reactscrypt.utils import get_opt_attr, deep_fetch

# Since react was designed with JSX in mind, they had to change many normal
# HTML and CSS attributes so they wouldn't clash with Javascript keywords (I guess)
# (i.e. class -> className). This is annoying now that we don't care about
# JSX and ES6 syntax silliness, so just use the 'real' name of attributes and
# remap them automatically before handing them off to React so React doesn't complain

# actual_name : react_name
react_attr_name_mappings = {
    'class' : 'className',
    'margin-left' : 'marginLeft',
    'background-color' : 'backgroundColor',
    'onclick' : 'onClick',
    'onchange' : 'onChange',
    'cellspacing' : 'cellSpacing',
    'colspan' : 'colSpan',
    'rowspan' : 'rowSpan',
}

#TODO this is only shallow
def _js_only_obj(py_dict,do_remap=False):
    if py_dict is None:
        return None

    # if py_dict is not an enhanced object, no need to process it further 
    if not py_dict.hasOwnProperty('__class__'):
        return py_dict 

    __pragma__('jsiter')
    js_only = {}
    __pragma__('nojsiter')
    if do_remap:
        for k,v in py_dict.items():
            if k == 'style':
                # just do this in place
                for style_key in v.keys():
                    remapped_key = react_attr_name_mappings.get(style_key,None)
                    if remapped_key is not None:
                        style_val = v[style_key]
                        del v[style_key]
                        v[remapped_key] = style_val
                use_key = k
            else:
                use_key = react_attr_name_mappings.get(k,k)

            js_only[use_key] = v 
    # put this in own block for slight performance gain
    # so we're not hitting the do_remap check for every item if not
    # needed
    else:
        for k,v in py_dict.items():
            js_only[k] = v

    return js_only

class ReactElement:
    def __init__(self,elm_type,props=None,*args):
        self.elm_type = elm_type
        self.props = props or {}
        self.children = args or []

    def get_react_element(self):

        def walk(node):
            if not node:
                return None

            if type(node) in (str,float,int):
                return node

            if type(node) is list:
                return [walk(_) for _ in node]

            use_elem = node.elm_type
            if isinstance(node.elm_type,ReactComponent):
                use_elem = node.elm_type._get_react_class()
                if not node.elm_type.is_root(): 
                    for k in node.elm_type._root_component._initial_global_state.keys():
                        node.props[k] = node.elm_type._root_component.state[k]

            react_children = [walk(_) for _ in node.children]

            return React.createElement(use_elem, _js_only_obj(node.props,True), *react_children)

        return walk(self)

    def append(self, child):
        self.children.append(child)

class ReactComponent:

    REMAP_LIFECYCLE_NAMES = {
        'component_did_mount': 'componentDidMount', 
        'component_will_mount': 'componentWillMount', 
        'component_will_unmount': 'componentWillUnmount', 
        'render': 'render',
        'should_component_update': 'shouldComponentUpdate',
        'component_will_receive_props': 'componentWillReceiveProps',
        'component_will_update': 'componentWillUpdate',
        'component_did_update': 'componentDidUpdate'
    }

    def __init__(self,root_component,initial_global_state = {}):
        self._instance_cache = {}
        self._root_component = root_component or self # this is the root component if root_component is None
        self._initial_global_state = initial_global_state

        prop_change_events = get_opt_attr(self,'prop_change_events')
        if prop_change_events is not None:
            self._prop_change_events = prop_change_events()
        else:
            self._prop_change_events = []

        self._updates_queue = []
        self._is_ready = False

    #cache these
    react_class = None

    #helper methods for set_state immutability
    def set_state(self,update,callback):
        # this can take either an object (dict), or an updater function

        #TODO would it be better to use python-style check:
        # type(update) is dict
        if typeof(update) == 'object': # JS-style check
            #TODO is js_only necessary here (prob. not)
            self.obj.setState(_js_only_obj(update),callback)
        else:
            self.obj.setState(update,callback)

    def set_global_state(self,update):
        self._root_component.set_state(update)

    def is_root(self):
        return self._root_component is self

    def force_update(self):
        self.obj.forceUpdate()

    #use this in the render method to easily fetch cached instances of python React objects
    #so they aren't re-instantiated on every call to render
    def use(self,key,cls):
        use_instance = self._instance_cache.get(key,None)
        if use_instance is None:
            use_instance = self._instance_cache.setdefault(key,cls(self._root_component))
        return use_instance

    def _get_react_class(self):

        if self.react_class is not None:
            return self.react_class

        members = _js_only_obj({})
        members['displayName'] = self.__class__.__name__

        def wrap(func):
            def inner(*args):
                self.obj = this
                self.state = this.state
                self.props = this.props
                return func(*args)
            return inner

        def render_wrap(func):
            def inner():
                self.obj = this
                self.state = this.state
                self.props = this.props
                elements = func()

                def set_container_element(elem):
                    self.container_element = elem

                elements.props['ref'] = set_container_element
                react_element = elements.get_react_element()
                return react_element
            return inner 

        initial_state = get_opt_attr(self,'initial_state')
        if initial_state is not None:
            # add in global state. This should be {} unless this is the root_component
            # initial_state should override _initial_global_state in cases of duplicate keys 
            self._initial_global_state.update(initial_state)
            initial_state = self._initial_global_state
        elif len(self._initial_global_state):
            initial_state = self._initial_global_state

        if initial_state is not None:
            cleaned_obj = _js_only_obj(initial_state)
            members['getInitialState'] = lambda : cleaned_obj

        for py_name,react_name in self.REMAP_LIFECYCLE_NAMES.items():
            ref = get_opt_attr(self,py_name)
            if ref is not None:
                if py_name == 'render':
                    members[react_name] = render_wrap(ref)
                else:
                    members[react_name] = wrap(ref)

        self.react_class = React.createClass(members)
        return self.react_class

    def render_to(self,destination_id,props=None,callback=lambda: None):

        react_element = ReactElement(self, props).get_react_element()
        container = document.getElementById(destination_id)
        ReactDOM.render(react_element, container, callback)

    # methods for prop change events. Provides a way to map
    # prop changes to actions/method calls to be triggered when the prop changes

    def ready(self):
        self._is_ready = True
        while len(self._updates_queue) > 0:
            self._updates_queue.pop(0)()

    def component_did_update(self,prev_props, prev_state):

        def call_if_changed(key_list,func,deferred):
            # convert plain strings to list of single item so they work
            # as lists, and so string keys can be used for convienence if
            # nested lookup not needed
            if type(key_list) is not list:
                key_list = [key_list]

            use_state_or_props = (prev_state,self.state) if self.is_root() else (prev_props,self.props)
            prev = deep_fetch(use_state_or_props[0],key_list)
            curr = deep_fetch(use_state_or_props[1],key_list)

            if prev is not curr:
                if deferred and not self._is_ready:
                    self._updates_queue.append(lambda: func(prev_props))
                else:
                    func(prev_props)

        for key_list,func,deferred in self._prop_change_events:
            call_if_changed(key_list,func,deferred)
