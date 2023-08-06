# -*- coding: utf-8 -*-
"""
OMXWare Utils
"""
import string
import random

import pprint
import pandas as pd
import json

"""
Generate a random string 

Returns:
    A random string with Uppercase alphabets and numbers.
"""
def rand(size=36, chars=string.ascii_uppercase + string.digits):
    N = 36
    return ''.join(random.choice(chars) for _ in range(size))

def toJson(resList):
    result = []
    for res in resList:
        res = res._jobj
        try:
            del res['GENE_SEQUENCE']
        except KeyError:
            pass

        try:
            del res['PROTEIN_SEQUENCE']
        except KeyError:
            pass

        try:
            del res['DOMAIN_SEQUENCE']
        except KeyError:
            pass

        result.append(res)

    return result

def toString(obj):
    if isinstance(obj, str):
        return repr(obj)
    try:
        if(len(obj)>25):
            obj = obj[0:25]
        return "----------------------------------------------------------------------------------------------------------------------\n" + "\n".join(str(x) for x in obj) + "\n----------------------------------------------------------------------------------------------------------------------\n"
    except TypeError:  # catch when for loop fails
        return str(obj)  # not a sequence so just return repr

def processOutput(output_type, output_obj):

    if (output_type == 'dict'):
        return output_obj
    elif (output_type == 'dataframe'):
        df = pd.DataFrame(toJson(output_obj))
        return df
    elif (output_type == 'json'):
        return toJson(output_obj)
    elif (output_type == 'stdout'):
        print(toString(output_obj))
