import decimal as d


"""
None of this takes into account the compounding interest.
I assume it becomes important for large loans over many years.
"""

MONTHS_IN_YEAR = 12

def percentileToRate(percentile : str):
    return d.Decimal(percentile)/100

# https://www.youtube.com/watch?v=lkNJvsy0qU8
def montlyPaymentYears(principal :int, years: int, interestPercent: str):
    rate = d.Decimal(interestPercent) / 100

    top = principal * (rate / MONTHS_IN_YEAR)
    nt = MONTHS_IN_YEAR * years
    bot = 1 - ( 1 + rate / MONTHS_IN_YEAR)**-nt
    
    return d.Decimal(round(top/bot,2)) # rounding to 


# M= Co ((1+i/m)^(n*m)*(i/m))/((1+ i/m)^(n*m)-1)
# M: Mensualidad
# Co: Capital del préstamo
# n: Número de años
# i: Tipo nominal de interés anual en tanto por uno
# m: Número de cuotas en el año (12 si es mensual)
def montlyPaymentMonths(principal :d.Decimal, months: int, interestPercent: str):
    rate = d.Decimal(interestPercent) / 100

    # interest is defined per year. Each month you pay 1/12 of yearly interest.
    montlyInterest = rate / MONTHS_IN_YEAR
    top = principal * montlyInterest
    bot = 1 - ( 1 + montlyInterest )**-months
    
    return d.Decimal(round(top/bot,2)) # rounding 2 decimals 

# https://money.stackexchange.com/questions/94140/what-is-the-math-used-to-calculate-the-impact-that-overpaying-a-mortgage-has-an 
def monthlyAmortizationTable(balanceRemaining :d.Decimal, interestPercent :str, moneyPayed :d.Decimal):
    rate = d.Decimal(interestPercent) / 100 

    interest =  round(d.Decimal(balanceRemaining * (rate / MONTHS_IN_YEAR)) ,2)
    principalContributed = round(moneyPayed - interest, 2)

    print (
            ("Remaining "        + str(balanceRemaining)).ljust(20) + " | " + 
            ("Towards interest " + str(interest)).ljust(20)         + " | " +
            ("Towards principal "+ str(principalContributed)).ljust(20) +  "|" 
    )

    return interest, principalContributed


def silentMonthlyAmortizationTable(balanceRemaining :d.Decimal, interestPercent :str, moneyPayed :d.Decimal):
    rate = d.Decimal(interestPercent) / 100 
    interest =  round(d.Decimal(balanceRemaining * (rate / MONTHS_IN_YEAR)) ,2)
    principalContributed = round(moneyPayed - interest, 2)
    return interest, principalContributed


"""
Useful to see any hidden fees for maintaing the loan.
Plug in the fees that you know of, if the resulting APR (aka TAE) is lower than what the bank tells you
the contract might include some extra fee that you have missed.

https://www.wallstreetmojo.com/annual-percentage-rate-apr/
https://www.youtube.com/watch?v=GNihZ4lfYCA
"""
def monthlyApr(balanceRemaining :d.Decimal, interestPercent :str, loanDurationMonths :int, monthlyServiceChange :d.Decimal): 
    rate = d.Decimal(interestPercent) / 100 
    interest = balanceRemaining * (rate / MONTHS_IN_YEAR)
    aprRate = ((interest + monthlyServiceChange) / balanceRemaining) / loanDurationMonths * 100
    return (aprRate * 100)


