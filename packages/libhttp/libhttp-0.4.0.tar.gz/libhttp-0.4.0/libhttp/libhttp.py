#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:04:08 2018

@author: Antony Holmes
"""

import re

ID_STRING_REGEX = re.compile(r'^[a-zA-Z0-9\-\:\,]+$')

def parse_arg(x, name, param_spec):
    """
    Parse a string argument and attempt to turn numbers into actual
    number types.
    
    Parameters
    ----------
    x : str
        A string arg.
    
    Returns
    -------
    str, float, or int
        x type converted.
    """
    
    if isinstance(param_spec, tuple):
        default_value = tuple[0]
        param_type = tuple[1]
    else:
        default_value = param_spec
        param_type = type(default_value)

    if x.replace('.', '').isdigit():
        if x.isdigit():
            x = int(x)
        else:
            x = float(x)
    
    # if the param type does not match its spec, use the default
    if (param_type == 'id' and not ID_STRING_REGEX.match(x)) or type(x) != param_type:
        x = default_value
                
    return x


def parse_params(request, params, id_map=None):
    """
    Parse ids out of the request object and convert to ints and add
    as a named list to the id_map.
    
    Parameters
    ----------
    request : request
        URL request
    *args
        List of strings of id names to parse
    **kwargs
        If a map parameter named 'id_map' is passed through kwargs,
        it will have the ids loaded into it. In this way existing
        maps can be used/reused with this method rather than creating
        a new map each time.
        
    Returns
    -------
    dict
        dictionary of named ids where each entry is a list of numerical
        ids. This is to allow for multiple parameters with the same
        name.
    """
    
    if id_map is None:
        id_map = {}
    
    for name, param_spec in params.items():
        if name in request.GET:
            # if the sample id is present, pass it along
            values = [parse_arg(x, name, param_spec) for x in request.GET.getlist(name)]
            
            if len(values) > 0:
                # Only add non empty lists to dict
                id_map[name] = values
        else:
            # If arg does not exist, supply a default
            
            if isinstance(param_spec, tuple):
                id_map[name] = [param_spec[0]]
            else:
                id_map[name] = [param_spec]
            
            
    return id_map
