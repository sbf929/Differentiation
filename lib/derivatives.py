# Basic:
def const():
    """**dc / dx = 0** 
    """
    return "0"

def power_of_var(var:str, n:str):
    "**d(x^n) / dx = n\*x ^ (n - 1)**"
    return f"{n} * ({var} ^ ({n} - 1))" 

def var():
    "**d(x)/dx = 1**"
    return "1"

# Exponential and Logarithmic:
def e_of_var(var:str):
    "**d(e^x) / dx = e^x**"
    return f"e ^ {var}"

def const_power_var(const, var:str):
    "**d(c^x) / dx = (c^x)\*log_e(c)**"
    return f"({str(const)}^{var}) * log_e({str(const)})"

def log_of_var(var:str, arg: str, base = 'e'):
    "**d(log_a(x)) / dx = 1 / x \* (log_e(a)). Uses change of log base formulae if `base != 'e'`.**"
    if arg != var: # Case: log_...(const)
        return const() # Returns 0

    if base == 'e': # Case: log_e(...)
        return f"1 / ({arg})"
    
    return f"1 / ({arg} * log_e({base}))" # Case: log_...(...)

def trignometric(fn: str, arg:str):
    if fn == 'sin':
        return f"cos({arg})"

    elif fn == 'cos':
        return f"-sin({arg})"

    elif fn == 'tan':
        return f"(sec({arg})) ^ 2"

    elif fn == 'cosec':
        return f"-cosec({arg}) * cot({arg})"

    elif fn == 'sec':
        return f"sec({arg}) * tan({arg})"

    elif fn == 'cot':
        return f"(-cosec({arg})) ^ 2"

    else:
        print('ERR. INVALID TRIG FUNCTION.')




