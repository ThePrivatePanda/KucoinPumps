investment = float(input("Invested: "))
peak = float(input("Peak: "))
dip = float(input("Dip: "))

profit =  ((investment/dip)*peak) - investment
print(f"\nProfit: {profit}\nReturn: {profit+investment}\n")
