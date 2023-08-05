import logging
from collections import namedtuple
from .dictPaths import get_value
from copy import deepcopy

diffResult = namedtuple('diff_result', [
    'compared',
    'updated',
    'added',
    'removed'
])

updData = namedtuple('updated_item', [
    'path',
    'old_value',
    'old_type',
    'new_value',
    'new_type'

])

delData = namedtuple('removed_item', [
    'path',
    'path_repr'
])

addData = namedtuple('added_item', [
    'path',
    'path_repr'
])

def diff(dct1, dct2, fail=False, startPath=None):
    """Performs a comparison between two nested dicts
    (or lists of dicts) and returns an object reporting
    the elements added (found in dct2 but not in dct1),
    those removed (found in dct1 but not in dct2),
    and those updated (found in both but with different
    values)
    
    Arguments:
        
        dct1 {dict or list} -- Dict to be used as reference.
        
        dct2 {dict or list} -- Dict, or list of dict, originated
        from the first one, where the user wants to find values
        changed, added or updated compared to the original
    
    Keyword Arguments:
        
        fail {bool} -- If True, when the function isn't able
        to perform the comparison for any reason, it will raise
        and error. Otherwise will log (level: error) a message
        describing the reason that determined the failure,
        returning the results object anyway, but with the
        'compared' attribute set to False (default: {False})
        
        startPath {list} -- List of int or strings
        corresponding to the keys or indexes to be used to 
        access to specific sublayers of the dict to compare.
        If not passed the entire dicts will be compared.
        (default: {None})
    
    Raises:
        TypeError -- If 'dct1' and 'dtc2' args are of different
        types or if they aren't lists or dicts
        
        
    Returns:
        'diff_result' namedtuple, structured as follows:

        [0] .compared {bool} -- True if the comparison has been
        performed, even with no results. False if (with 'fail'
        set to False) something went wrong.
        
        [1] .updated {list} -- List of 'updated_item' namedtuple
        structured as follows:
            
            [0] .path {list} -- Path to updated value.
            [1] .old_value {any} -- Old value of the element.
            [2] .old_type {type} -- Type element's old value.
            [3] .new_value {any} -- New value for the element.
            [4] .new_type (type) -- Type for element's new value.
        
        [2] .added {list} -- List of paths for elements found only
        in dct2.

        [3] .removed {list} -- List of paths for elements found
        only in dct1.
    """
    compared = False
    updated = []
    added = []
    removed = []
    # Different type for args containing dicts to compare    
    if type(dct1) != type(dct2):

        msg = "Different type for initial comparison layer ({tp1} vs{tp2}). Comparison for difference not possible.".format(
            tp1=type(dct1).__name__, tp2=type(dct2).__name__
        )
        if fail:
            raise TypeError(msg)
        else:
            logging.error(msg)
            return diffResult(compared,updated, added, removed)
    
    if type(dct1) not in [list, dict]:
        msg = "Diff() works only for dicts or lists of dicts. Passed '{tp1}'".format(
            tp1=type(dct1).__name__
        )
        if fail:
            raise TypeError(msg)
        else:
            logging.error(msg)
            return diffResult(compared,updated, added, removed)
    
    if startPath == None:
        currentPath = []
        currLev1 = dct1
        currLev2 = dct2
    else:
        try:
            found1, results1 = get_value(dct1, startPath)
            found2, results2 = get_value(dct2, startPath)

            if found1==1 and found2==1:
                currLev1 = results1[0].value
                currLev1 = results2[0].value
                currentPath = results1[0].path
            else:
                msg = "Given path ({2}) produced multiple or no match in dct1 ({0} match(es) and/or dct2 ({1} match(es))".format(
                    found1, found2, startPath
                )
                if fail:
                    raise RuntimeError(msg)
                else:
                    logging.error(msg)
                    return diffResult(compared,updated, added, removed)
    
        except Exception as e:
            msg = "Error occurred while retrieving value by given path ({}): {}".format(
                startPath, e
            )
            if fail:
                raise RuntimeError(msg)
            else:
                logging.error(msg)
                return diffResult(compared,updated, added, removed)
    try:
        # logging.debug("Launching compare function")
        updated, added, removed = _compare_levels(currLev1, currLev2, debugLevel, currentPath)
        compared = True
    except Exception as e:
        msg = "Unexpected error occurrend while performing comparison: {}".format(e)
        if fail:
            raise RuntimeError(msg)
        else:
            logging.error(msg)
    finally:
        return diffResult(compared, updated, added, removed)
    # Current level of comparison is on lists
    # if isinstance(currLev1, list):
def _compare_levels(lev1, lev2, debugLevel=0, currentPath=None):
    
    updated = []
    added = []
    removed = []

    # Both level are dicts
    if isinstance(lev1, dict) and isinstance(lev2, dict):
        # logging.debug("Comparing dicts")
        # Set for keys in lev1 but not in lev2
        _delKeys = set(lev1.keys()) - set(lev2.keys())
        # Set for keys in lev2 but not in lev1
        _addKeys = set(lev2.keys()) - set(lev1.keys())
        # Set for common keys
        _comKeys = set(lev1.keys()) & set(lev2.keys())

        # For every added key makes a copy of 'currentPath' list,
        # appends the added key to it, and appends the resulting
        # path to 'added' list
        for k in _addKeys:
            _cp = deepcopy(currentPath)
            _cp.append(k)
            added.append(_cp)
        # For every removed key makes a copy of 'currentPath' list,
        # appends the removed key to it, and appends the resulting
        # path to 'removed' list
        for k in _delKeys:
            _cp = deepcopy(currentPath)
            _cp.append(k)
            removed.append(_cp)
        # logging.debug("Now updated is: {}".format(added))
        # logging.debug("Now added is: {}".format(added))
        # logging.debug("Now removed is: {}".format(removed))
    # Both levels are lists
    elif isinstance(lev1, list) and isinstance(lev2, list):
        # If are different for lenght current level is to consider
        # updated
        if len(lev1) != len(lev2):
            updated.append(currentPath)
            return updated, added, removed
        _comKeys = range(len(lev1))
    
    
    for key in _comKeys:
        # logging.debug("Comparing common keys")
        _cp = deepcopy(currentPath)
        _cp.append(key)

        if all([x not in [dict,list] for x in [type(lev1[key]),type(lev2[key])]]):
            # logging.debug("Comparing non-dicts or non-lists values")
            if type(lev1[key]) != type(lev2[key]) or lev1[key] != lev2[key]:
                # logging.debug("Key {} changed".format(key))
                updated.append(
                    updData(
                        path=_cp,
                        old_value=lev1[key],
                        old_type=type(lev1[key]),
                        new_value=lev2[key],
                        new_type=type(lev2[key])

                    )
                )
        else:
            if type(lev1[key]) == type(lev2[key]) and type(lev1[key]) in [dict, list]:
                _upd, _add, _rem = _compare_levels(lev1[key], lev2[key], debugLevel, _cp)
                updated.extend(_upd)
                added.extend(_add)
                removed.extend(_rem)

            else:
                updated.append(
                    updData(
                        path=_cp,
                        old_value=lev1[key],
                        old_type=type(lev1[key]),
                        new_value=lev2[key],
                        new_type=type(lev2[key])

                    )
                )
    return updated, added, removed
            

        


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("DEBUG ON")
    