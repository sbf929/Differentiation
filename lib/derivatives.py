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

def log_of_var(var:str, log_base = 'e'):
    "**d(log_a(x)) / dx = 1 / x \* (log_e(a))**"




