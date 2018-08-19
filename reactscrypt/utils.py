# deep = True enhances JS {} [] as python dict and lists 
# might be expensive for large objects. Don't use this for things like
# chartdata, only for data we might want to use python members
# and looping constructs on
def enhance(object_or_array,deep=False):
    #TODO implement this iteratively
    def enhance_list(list_to_walk):
        enhanced = list(list_to_walk)
        for i in range(len(enhanced)):
            enhanced[i] = walk(enhanced[i])
        return enhanced

    def enhance_dict(dict_to_walk):
        enhanced = dict(dict_to_walk)
        for k in enhanced.keys():
            enhanced[k] = walk(enhanced[k])
        return enhanced

    def walk(js_obj):
        descrip = Object.prototype.toString.call(js_obj)

        if descrip == '[object Array]':
            enhanced = enhance_list(js_obj) if deep else list(js_obj)
        elif descrip == '[object Object]':
            enhanced = enhance_dict(js_obj) if deep else dict(js_obj)
        else:
            enhanced = js_obj

        return enhanced

    return walk(object_or_array) #if deep else parsed

#need to use __eq__ here for == with sets so the equality test works correctly
#enable operator overloading for this method
__pragma__('opov')
"""
#recursive
def deep_equal(item,other_item):

    def check_list():
        item_len = len(item)
        other_len = len(other_item)
        if item_len == other_len:
            for i in range(item_len):
                if not deep_equal(item[i],other_item[i]):
                    return False
            return True
        return False

    def check_dict():
        item_keys = set(item.keys())
        other_keys = set(other_item.keys())
        if item_keys == other_keys:
            for k in item_keys:
                if not deep_equal(item[k],other_item[k]):
                    return False
            return True
        return False

    item_type = type(item)
    if item_type is type(other_item):
        if item_type is list:
            return check_list()
        elif item_type is dict:
            return check_dict()
        else:
            return item == other_item

    return False
"""

#iterative
def deep_equal(item,other_item):
    stack = [(item,other_item)]
    is_equal = True

    def check_list(item,other_item):
        item_len = len(item)
        other_len = len(other_item)
        if item_len == other_len:
            for i in range(item_len):
                stack.append((item[i],other_item[i]))
            return True
        return False

    def check_dict(item,other_item):
        item_keys = set(item.keys())
        other_keys = set(other_item.keys())
        if item_keys == other_keys:
            for k in item_keys:
                stack.append((item[k],other_item[k]))
            return True
        return False

    while len(stack) and is_equal:
        node = stack.pop()
        item_type = type(node[0]) 
        if item_type is type(node[1]):
            if item_type is list:
                is_equal = check_list(node[0],node[1])
            elif item_type is dict:
                is_equal = check_dict(node[0],node[1])
            else:
                is_equal = (node[0] == node[1])
        else:
            is_equal = False
    return is_equal

__pragma__('noopov')

#javascript sorts strings lexographically, and Transcrypt seems to fall back on this behavior
#use this instead for sorting numbers as a convenience method
#this will sort in place
def numsort(iterable):
    return iterable.js_sort(lambda a,b: a-b )

def get_opt_attr(obj,attr,default_val=None):
    if hasattr(obj,attr):
        return getattr(obj,attr)
    return default_val

__pragma__ ('kwargs')
#TODO implement deep if needed
def immutable_append(to_this,*append_these,deep=False):
    # do this in native JS for efficiency
    return to_this.concat(append_these)

def immutable_remove_from_list(from_this,*delete_these,deep=False,key=lambda x:x):

    #if key is not None:
    #TODO can probably use set.difference or something here
    delete_these = set([key(x) for x in delete_these])
    result = [x for x in from_this if key(x) not in delete_these]
    return result

def immutable_remove_index_from_list(from_this,index_to_remove,deep=False):
    new_copy = shallow_copy(from_this)
    new_copy.pop(index_to_remove) 
    return new_copy

def immutable_update(update_this,deep=False,**with_these):
    new_shallow_dict_copy = update_this.copy()
    new_shallow_dict_copy.update(**with_these)
    return new_shallow_dict_copy

__pragma__ ('nokwargs')

# determines difference between 2 lists and calls the given 'add' and 'remove'
# function for added and removed items passing the callbacks the item
# Note: this uses sets, so old_set and new_set must be unique lists or sets
def call_for_difference(old_set,new_set,func_add,func_remove):
    # make sure these are sets
    old_set = set(old_set)
    new_set = set(new_set)

    # find the things that were removed:
    for item in old_set.difference(new_set):
        func_remove(item)

    # find the things that were added:
    for item in new_set.difference(old_set):
        func_add(item)

# searches a data structure using a given template that specifies the locations that should be searched
# in each top-level array item for a value that matches find_value. If one is found in nested arrays,
# then return the position of the first top-level index the value was found in, otherwise -1.
# If find_all = True, return an array of all the top level indexes containing the value, or an empty array []
# if none are found
# 
# Note: the intent of this is to make it easier to re-map data. For example, if we want to find all of indexes
# where 'a' contains 2, this can be done with:

#   regions = [{'a':[1,2]},{'a':[2,3]}]
#   deep_index(regions,[['a'],[]],2,True) -> [0,1]
#   Note that the empty array in the template is necessary to denote that the array is 'plain' (contains no objects)
#
# Another example:
#
# data = [{'a':{'b':[{'c':{'d':[{'e':'value'},...]}},...]}},...]
# deep_index(data,[['a','b'],['c','d'],['e']],'value',True) -> [0] or 0 if find_all=False
def deep_fetch(item,path):
    for x in path:
        item = item[x]
        if item is None or item is js_undefined:
            break
    return item

def deep_index(initial_list_data,template,find_value,find_all=False):
    #TODO implement this iteratively

    def walk(list_data,path):
        found = []
        for i,list_item in enumerate(list_data): 
            fetch_result = deep_fetch(list_item,path[0])
            next_path = path[1:]
            if len(next_path):
                result = walk(fetch_result,next_path)

                if len(result):
                    found.append(i)
                    if not find_all:
                        break

            elif fetch_result == find_value:
                found.append(i)

        return found

    walk_return = walk(initial_list_data,template)

    if find_all:
        return_val = walk_return
    else:
        return_val = walk_return[0] if len(walk_return) else -1

    return return_val

# sometimes, it's useful to be able to pass de-referenced variables to
# event handlers, especially in the 'render' method. For example, we
# often want to pass the current value of loop iteration variables to
# event handlers, not references to these variables since they will change
# on subsequent iterations prior to the event being called. This accomplishes
# this in a standardized way so it's clear why we're using the nested lambda function

# This uses currying to accept arguments at creation time, and combine them with
# any args passed in at call time
def event_factory(func,*args):
    def inner(*inner_args):
        # use .__add__ here to force python behavior rather than
        # enabling __pragma__(ovop)
        all_args = args.__add__(inner_args)
        func(*all_args)
    return inner

# negative slicing a[-1] doesn't work in transcrypt
# (falls back to JS behavior which returns undefined
# slicing in transcrypt works as expected though, so use [-1:][0] instead of [-1]
# or this convenience method
def last(list_instance):
    # this raw JS implementation is prob. slightly faster than
    # using python-style slicing or len() since these requires
    # addl. method calls
    return list_instance[list_instance.length-1]
    # alternate python implementations
    # return list_instance[-1:][0]
    # return list_instance[len(list_instance)-1]

# numerical validation is annoying, especially when combining
# JS weirdness with Python. Use these methods to help

#TODO use regex here once I figure out how
def is_float(val):
    testval = val * 1
    if val != '' and testval.toString() != 'NaN':
        return True
    return False

def format_date(date_str):
    return __new__(Date(Date.parse(date_str))).toDateString() 

def format_datetime(date_str):
    return __new__(Date(Date.parse(date_str))).toGMTString() 
