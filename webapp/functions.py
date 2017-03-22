import numpy as np

nat_as_integer = np.datetime64('NAT').view('i8')

def isnat(dt_obj):
    if "isnat" in dir(np):
        return np.isnat(dt_obj)
    dtype_string = str(dt_obj.dtype)
    if 'datetime64' in dtype_string or 'timedelta64' in dtype_string:
        return dt_obj.view('i8') == nat_as_integer
    return False  # it can't be a NaT if it's not a dateime

