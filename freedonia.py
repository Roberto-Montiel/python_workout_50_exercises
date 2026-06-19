import sys

print(sys.path)
taxes = {"Chico": 50, "Groucho": 70, 
         "Harpo": 50, "Zeppo": 40}

class HourTooLowError(Exception): pass
class HourTooHighError(Exception): pass

def calculate_tax(price, country, hour) -> float:
    if hour < 0:
        raise HourTooLowError(f"Hour of {hour} is < 0")
    
    if hour >= 24:
        raise HourTooHighError(f"Hour of {hour} is >= 24")
    
    tax = taxes[country]

    return price + price * (tax/100 * hour/24)


    

def taxes_to_pay(income):
    if income < 0:
        return "Income must be positive"

    tax = 0

    if income > 1000:
        taxable = min(income - 1000, 10000)
        tax += taxable * 0.10

    if income > 11000:
        taxable = min(income - 11000, 10000)
        tax += taxable * 0.20

    if income > 21000:
        taxable = income - 21000
        tax += taxable * 0.50

    return f"Taxes to be paid: {tax:.2f}"
    
def digit_alpha_space(s: str) -> dict:
    funcs = {
        "isdigit": str.isdigit,
        "isalpha": str.isalpha,
        "isspace": str.isspace,
    }
    return {name: sum(func(char) for char in s)
            for name, func in funcs.items()}
    
def creating_dict_from_function(s: str, f):
    return {c: f(c) for c in s}