# from __future__ import range_function
from copy import deepcopy
import logging
from pprint import pprint
from collections import namedtuple
import operator

mainResult = namedtuple('dict_search', [
    'found',
    'results'
])

searchResult = namedtuple('dict_branch', [
    'path',
    'value'
])


def set_value(dic, path, value, debug=False):
    """Sets a value in a nested dict using a key
    list (such those returned by 'get_value') to 
    locate the value to set.
    
    Arguments:
        dic {dict} -- Dict where set the value
        
        keys {list} -- List of strings or ints
        (such those returned with 'get_value()')
        to locate the value to set in the dict

        value {any} -- Value to set
    Returns:
        {bool} -- True if value has been successfully
        set
    """
    try:

        for n,key in enumerate(path[:-1]):
            try:

                dic = dic.__getitem__(key)
            except KeyError as e:
                logging.error ("Element '{}' at position {} of given path isn't among current level keys or indexes".format(key, n))
                return False
            # if isinstance(dic, dict):
            #     dic = dic.setdefault(key, {})
            # elif isinstance(dic, list):
            #     dic = dic[0]
        dic[path[-1]] = value
        return True
    except Exception as e:
        logging.error("Can't set '{}' value by '{}' path due to an error: {}".format(
            value, path, e))
        return False
    
def get_value(dct, path, fail=False, debug=False):
    """Returns one or more values found in a nested dict
    according to specified path.

    Arguments:
        
        dct {dict or list of dict} -- Object to inspect
        
        path {iterable} -- List or tuple with elements
        specifing the route in the dict to get the value
        
    
    Keyword Arguments:
        
        fail {bool} -- If True when a value in the list
        doesn't produce any match raises an error 
        (default: {False})

        debug {int} -- If 0 no output will be printed.
        If 1 a small output wll be printed. If 2 or
        greater a verbose output will be printed
        (default: 0)
    
    Returns:
        
        'dict_search' object 
        
        [0] .found {int} - Number of match for the path
        
        [1] .results {list} -- List containing a number
        of 'dict_branch' objects equal to 'found'.

        Each 'dict_branch' object has the following structure:
        
        [0] .path {list} -- List of strings or ints to access
        directly the value in the dict (to be used with
        'set_value()')
        
        [1] .value {any} -- Value stored in the dict at given
        path

    Example:
    d = {
        'foo': [ 
            {
                'name':'bar', 
                'home':'rome', 
                'data':[0,1,2]
            },
            {
                'name':'bar', 
                'home':'london',
                'data':[3,4,5]
            },
            {
                'name':'baz', 
                'home':'london',
                'data':[6,7,8]
            }
              ]
    }

    get_value(d, ['foo', {'name':'baz'}, 'data', 0])

    returns following object:

        dict_search(
            found=1, 
            results=[
                dict_branch(
                    path=['foo', 2, 'data', 0], 
                    value=6
                    )
                ]
            )
    
    get_value(d, ['foo', {'name':'bar'}, 'data', 2])
    
    returns following object:
        dict_search(
            found=2, 
            results=[
                dict_branch(
                    path=['foo', 0, 'data', 2], 
                    value=2
                    ),
                dict_branch(
                    path=['foo', 1, 'data', 2], 
                    value=5
                    )
                ]
            )
    

    
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    # Current level to analize
    # Starts from given dict
    currLev = [dct]

    # Counter fo current level (just for screen msg)
    levCounter = 0
    ret_path = [[]]


    # Wrong type for 'path' argument
    if not isinstance(path, list) and not isinstance(path, tuple):
        msg = "Argument [1] ('path') must be iterable. '{tp}' given ('{pt}').".format(
            tp=type(path).__name__, pt=path
        )
        if fail:
            raise TypeError(msg)
        else:
            logging.error (msg)
            return None
    
    # Cicles over the given path elements
    for path_item in path:
        
        _path_elements, _nextLev, _excluded = _get_dict_value_for_item(
            currLev, path_item, fail, debug)
        if debug:
            logging.debug( "Current Level ({lv}) Results".format(lv=levCounter))
            logging.debug( "--------------------------------")
            logging.debug( "_path_elements: ")
            logging.debug((sorted(_path_elements)))
            logging.debug( "")
            logging.debug( "_excluded: ")
            logging.debug( _excluded)
            logging.debug( "")
            logging.debug( "_nextLev:")
            logging.debug((sorted(_nextLev)))
            logging.debug( "--------------------------------\n")

        # Returnd at least a result
        if _nextLev != []:
            # _nextLev now becomes currLev
            currLev = _nextLev

            # Makes a copy of the list of path to return, excluding elements
            # with indexes eventuallt contained in the _excluded list
            _ret_path = list(
                ret_path[x] for x in range(len(ret_path)) if x not in _excluded
                )
            if debug:
                logging.debug("ret_path pre-processing (Exclusions applied)")
                logging.debug((sorted(_ret_path)))
            
            # Cicles over elements number of currLev (aka _nextLev)
            for n in range(len(currLev)):
                # If n value is greater or equal to lenght of current ret
                # path (new branchs added from multiple results)
                if n >= len(ret_path):
                    # Appends to the copyied list a copy of the previous
                    # item present in it, withouth the last element (creates 
                    # a new path branch)
                    _ret_path.insert(n, deepcopy(_ret_path[n-1][:-1]))
                # Updates path branch at index n with value at index n
                # of _path_elements
                _ret_path[n].append(_path_elements[n])
            
            if debug: 
                logging.debug("ret_path post-processing")
                logging.debug((sorted(_ret_path)))
                logging.debug("")
            # Reverses the copied (updated) path list in the main one
            ret_path = deepcopy(_ret_path)
            # Updates level counter
            levCounter += 1
            
        else:
            logging.info("Item {} of search path didnt produce any results at level {}".format(
                path_item, levCounter))

            return mainResult(0, None)
    # Number of results (matches)
    resultsN = len(ret_path)

    return mainResult(
        found=resultsN, 
        results=list(searchResult(
            path=ret_path[n], 
            value=currLev[n]
            ) for n in range(resultsN))

        )
    



def _get_dict_value_for_item(currLev, item, fail=False, debug=False):
    """Returns deeper level of the dict (one or many)
    and the key to be used for accessing it.
    
    Arguments:
        currLev {dict, list} -- Current level of the
        dict where the key passed as item must be used 
        to retrieve the deeper level.

        item {vary} -- A string (dict key), integer
        (list index), a dict (pair key:value to be
        match in a list of dicts) or a list (of dicts
        as previous for multiple params query) to 
        identify one or more branches in the dict's
        current level, where search must continue
        with next items.
    
    Keyword Arguments:
        fail {bool} -- When True, if the given item 
        doesn't produce any match, raises a ValueError.
        Otherwise the function returns a tuple of empty 
        lists.
        (default: {False})
        
        debug {int} -- If 0 no output will be printed.
        If 1 a small output wll be printed. If 2 or
        greater a verbose output will be printed
        (default: 0)
    
    
    Returns:
        Tuple -- Two lists. 
        
        The former contains the key or keys required
        to access the deeper level of the dict (if the
        item is a string or an int will return it; if
        is a dict or a list of dicts will contain the 
        index(es) matching those pairs).
        
        The latter will contain one or more deeper level 
        of the 'currLev': only one, accessed via the item 
        (if int or str); possibly many if the deeper level
        has been identified through one or more key:value
        pairs (ie. item is dict or list of dicts). 
    """
    # Empy list to be filled to produce deeper level(s)
    _nextLev = []
    # Empty list to be filled with key(s) (int or str) used
    # to access the deeper level(s)
    _retPath = []

    # List to be filled with indexes of currLev list in case
    # of multiple match
    _excluded = []
    # currLev is always a list, even if has only 1 element
    # so its is cycled for single branchs
    for n, branch in enumerate(currLev):
        if debug:
            logging.debug( "Current Branch ({}) of current Level".format(n))
            logging.debug( "----------------------------------")
            logging.debug((branch))
            logging.debug( "----------------------------------\n")
        
        # current branch is iterable (list or tuple)
        if isinstance(branch, list) or isinstance(branch, tuple):

            keys, values = _get_value_from_list(branch, item, fail, debug)

            # item can be applied on one or more element in the list
            # so one or more sub-branches are returned
            if values != []:
                # Appends to next level list the values (sub-branches) 
                # returned
                for v in values:
                    _nextLev.append(v)
                # Appends to paths elements list the keys (path 
                # elements) returned
                for k in keys:
                    _retPath.append(k)
            # Item can't be applied to any element in the list
            else:
                # Appends current branch index to those to exclude from
                # main path elements results (so this path branch will
                # be deleted)
                _excluded.append(n)

            
        # Current branch is a dict
        elif isinstance(branch, dict):
            # Item is a string (appropriate value for a dict)
            if isinstance(item, str):
                
                keys, values = _get_value_by_key(branch, item, fail, debug)

                # item applied to dict in current branch returns one
                # or more ('*') values (sub branches)
                if values != []:
                    # Appends values to next level list
                    for value in values: 
                        _nextLev.append(value)
                    # Appends keys (path elements) to returned path list
                    for key in keys:
                        _retPath.append(key)
                    
                else:
                    # Appends current branch index to those to exclude from
                    # main path elements results (so this path branch will
                    # be deleted)
                    _excluded.append(n)
            # Item is not a string
            else:
                msg = "Current item ({it}) is inappropriate for current Branch {br} of current level".format(
                    it=item, br=n
                )
                # If function must fail error is raised
                if fail:
                    raise TypeError(msg)
                # Function can't fail, so this branch is simply
                # excluded from results
                else:
                    logging.debug(msg)
                    logging.debug("This branch will be removed from results")
                    _excluded.append(n)

    return _retPath, _nextLev, _excluded

def _get_value_from_list(currBranch_list, item, fail=False, debug=False):
    """Returns deeper level of the dict when current
    branch level is a list.
    
    Arguments:
        currBranch_list {list} -- List where the 'item'
        *arg must be applied to retrieve deeper level
        
        item {vary} -- A string (dict key), integer
        (list index), a dict (pair key:value to be
        found in a list of dicts) or a list (of dicts
        as previous for multiple params query) to 
        identify one or more branches in the dict's
        current level, where search must continue
        with next items.
    
    Keyword Arguments:
        fail {bool} -- When True, if the given item 
        doesn't produce any match, raises a ValueError.
        Otherwise the function returns a tuple of empty 
        lists.
        (default: {False})
        
        debug {int} -- If 0 no output will be printed.
        If 1 a small output wll be printed. If 2 or
        greater a verbose output will be printed
        (default: 0)
    
    Returns:
        Tuple -- Two lists ([keys], [values]). 
        
        The former contains the key or keys required
        to access the deeper level of the dict (if the
        item is a string or an int will return it; if
        is a dict or a list of dicts will contain the 
        index(es) matching those pairs).
        
        The latter will contain one or more deeper level 
        of the 'currLev': only one, accessed via the item 
        (if int or str); possibly many if the deeper level
        has been identified through one or more key:value
        pairs (ie. item is dict or list of dicts).

        If no match is found will return two empty lists.
    """
    
    # Item arg is int (index) and is valid (less than lenght
    # of currLev LIST)
    
    # arg 'item' is an int
    if isinstance(item, int):
        if debug: logging.debug("Retrieving value from list by int ({})".format(item))
        
        # Item is smaller than lenght of list (valid index)
        if item < len(currBranch_list):
            # Returns list element at given index
            return [item], [currBranch_list[item]]
        # Item is inappropriate as index (greater or equal to lenght)
        else:
            msg = "Given index ({id}) is greater than current list lenght ({ln}) (_get_value_from_list)".format(
                id=item, ln=len(currBranch_list)
            )
    else:
        # arg 'item' is a list (of dicts containing each one k:v pair)
        if isinstance(item, list):

            if debug:
                logging.debug("Looking for a match by list of dicts ({})".format(item))
                
            # First element of current branch is a dict (we suppose others
            # are the same)
            if isinstance(currBranch_list[0], dict):
                return _find_match_from_list_of_dicts(currBranch_list, item, debug)
            
            else:
                msg = "Type of elements in current branch is not 'dict' but '{tp}'. Given incorrect path item '{it}', usable only for lists of dicts".format(
                    tp=type(currBranch_list[0]).__name__, it=item
                )
        # arg 'item' is a dict (with a single k:v pair)
        elif isinstance(item, dict):
            if debug:
                logging.debug("Looking for a match by dict ({})".format(item))
            
            # First element of current branch is a dict (we suppose others
            # are the same)
            if isinstance(currBranch_list[0], dict):
                return _find_match_from_list_of_dicts(currBranch_list, [item], debug)
            
            else:
                msg = "Type of elements in current branch is not 'dict' but '{tp}'. Given incorrect path item '{it}', usable only for lists of dicts".format(
                    tp=type(currBranch_list[0]).__name__, it=item
                )

        # arg 'item' is a string
        elif isinstance(item, str):
            # The string contains '*': all elements of this branch will be returned
            if item=='*':
                if debug: 
                    logging.debug("Current item is '*': returning all elements in this branch")
                return (
                    # List of all element's indexes of currBranch_list
                    list(x for x in range(len(currBranch_list))),
                    currBranch_list
                    )
            else:    
                
                if len(currBranch_list) > 0:
                    
                    if isinstance(currBranch_list[0], dict):
                        if debug: 
                            logging.debug("Looking for a match by string ({}) among keys of dicts in current level list)".format(item))

                        # return _get_value_by_key(curr)
                        return _find_match_from_key_string(currBranch_list, item, debug)
                    elif str in [type(x) for x in currBranch_list]:
                        if debug: 
                            logging.debug("Looking for indexes of string '{}' among elements of current level list)".format(item))

                        return _find_match_by_value_type(currBranch_list, item, debug)
                    
                    
                    else:
                        msg = "Type of elements in current branch is not 'dict' but '{tp}'. Given incorrect path item '{it}', usable only for lists of dicts".format(
                            tp=type(currBranch_list[0]).__name__ if len(currBranch_list)>0 else 'XX', it=item
                        )
                else: 
                    msg = 'Empty list at current level skipped'

        elif type(item) in [type(x) for x in currBranch_list]:
            if debug: 
                logging.debug("Looking for indexes of item '{}' among elements of current level list)".format(item))

            return _find_match_by_value_type(currBranch_list, item, debug)
        else:
            msg = "Current 'item' arg type is not valid. Allowed only int, str, dict, or lists. (Given '{tp}': '{gv}')".format(
                tp=type(item).__name__, gv=item
            )

    if fail:
        raise ValueError(msg)
    else:
        logging.error(msg)
        return [],[]

def _find_match_by_value_type(currBranch_list, item, debug=False):
    """Returns a tuple of lists containig indexes of
    currentBranch_list arg where item arg is found and
    item itself repeated many times as indexes found
    
    Arguments:
        currBranch_list {list} -- List to inspect
        item {any} -- Item to be found in the list
    
    Keyword Arguments:
        debug {int} -- Level of debug (default: {0})
    """
    match = []
    path_element = []
    for n, currBranch_item in enumerate(currBranch_list):
        if type(currBranch_item) == type(item) and currBranch_item==item:
            if debug:
                logging.debug("Found item '{}' at index {}".format(item, n))
            path_element.append(n)
            match.append(item)
    return path_element, match

def _find_match_from_key_string(currBranch_list, key, debug=False):
    
    match = []
    path_element = []
    # print currBranch_list
    for currBranch_item in currBranch_list:
        if key in currBranch_item:
            
            if debug: 
                currBrDescr = "\n{}".format(currBranch_item)
                logging.debug("MATCH: {} in keys of '{}'".format(key, currBrDescr))
            
            match.append(currBranch_item[key])
            path_element.append(key)
    
    if debug:
        logging.debug("Returning: \n{}\n{}".format(path_element,match))
    return (path_element, match)

def _find_match_from_list_of_dicts(currBranch_list, match_list, debug=False):
    # print "_Look for dict match in a list of dicts"
    match = []
    path_element = []
    for n, currBranch_item in enumerate(currBranch_list):
        found = False
        for match_item in match_list:
            if debug: 
                logging.debug("Current values to find: {}".format(match_item))
            key = list(match_item.keys())[0]
            if (key in currBranch_item 
            and currBranch_item[key]==list(match_item.values())[0]):
                
                found = True
            else:
                found = False
                if debug:
                    logging.debug("Key and value of current match dict ({d}) aren't present in current branch item".format(d=match_item))
                break
        if found:
            if debug: 
                logging.debug("Found a match")
            match.append(currBranch_item)
            path_element.append(n)
    if debug:
        logging.debug("Returning: \n{}\n{}".format(path_element,match))
        
    return path_element, match

def _get_value_by_key(currLev, key, fail=False, debug=False):
    
    # arg key is '*': all items of currLev dict will be returned
    if key=='*':
        if debug:
            logging.debug("Using '*' key for current level dict: all items will be returned")
        keys = []
        _nextLev = []

        for k in currLev.keys():
            keys.append(k)
            _nextLev.append(currLev[k])
        return keys, _nextLev
    # The string must be found among dict keys
    else:

        # print "Given key: ", key
        if key in currLev:
            if debug: 
                logging.debug("Found KEY '{k}' in current dict: returning associated value".format(k=key))
            return (
                [key], # key for composing path to return
                [currLev[key]] # Value
            )
        else:
            if debug: 
                logging.debug("Dict at current level hasn't key '{}' (availables: {})".format(key, ','.join(currLev.keys())))
            c
            return ([], [])


