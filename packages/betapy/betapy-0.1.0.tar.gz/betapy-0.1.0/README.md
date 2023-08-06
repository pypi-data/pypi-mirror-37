# betapy

Inferface object for bdata. Performs all calculations and moves all data fields to the top level. For a list of accessible data fields see object representation (call `repr(betapy_obj)` or simply call your object in the interpreter). 

betapy also calculates all asymmetry values and places the results in top level numpy arrays. To re-calculate asymmetries use `betapy.set_asym()` which takes as input the same as `bdata.asym()`. For a list of options print the docstring with `print(betapy.set_asym.__doc__)`