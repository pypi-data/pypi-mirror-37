'''
Created on 28Apr.,2017

@author: cac009
'''
import os
import yaml


def check_for_keys(idict, key_check_list):
    """
    Check dict to see if all keys specfied in key_check_list are present
    
    :param idict: input dictionary 
    :type idict: dict
    :param key_check_list: list of key names that should be present in idict
    :type key_check_list: list of string
    :raises ValueError if key not present in dictionary
    """

    keys = list(idict.keys())  # required in py3
    nkeys = len(keys)
    a = key_check_list
    b = [False]*len(key_check_list)
    check = dict(zip(a, b))
    for ix in range(nkeys):
        if (keys[ix] in key_check_list):
            check[keys[ix]] = True
        else:
            # key not in list
            raise ValueError("invalid field - %s" % (keys[ix]))

    if (all(list(check.values())) == False):
        missing_keys = [k for k, v in check.items() if v is False]
        raise ValueError("missing fields - %s" % ', '.join(missing_keys))

    return


def load_config_file(arg, key_check_list):
    """
    Load yaml file and check that all necessary keys are present
    
    :param arg: yaml file to load
    :type arg: string
    :param key_check_list: list of key names
    :type key_check_list: list of strings
    :return key value pairs
    :rtype dict of key value pairs
    :raises ValueError if key not present in dictionary
    """
    
    if (os.path.isfile(arg) == False):
        raise IOError("specified file %s does not exist" % arg)

    with open(arg, 'r') as fid:
        dict_config = yaml.safe_load(fid)

    try:
        check_for_keys(dict_config, key_check_list)
    except ValueError as e:
        raise ValueError('specified file %s has an error %s\n' % (arg, str(e)))

    return dict_config
