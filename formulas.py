import decimal as d


MONTHS_IN_YEAR = 12

def percentileToRate(percentile : str):
    return d.Decimal(percentile)/100

# https://www.youtube.com/watch?v=lkNJvsy0qU8
def montlyPaymentYears(principal :int, years: int, interestPercent: str):
    rate = d.Decimal(interestPercent) / 100

    top = principal * (rate / MONTHS_IN_YEAR)
    nt = MONTHS_IN_YEAR * years
    bot = 1 - ( 1 + rate / MONTHS_IN_YEAR)**-nt
    
    return float(round(top/bot,2)) # rounding to 

def montlyPaymentMonths(principal :d.Decimal, months: int, interestPercent: str):
    rate = d.Decimal(interestPercent) / 100

    # interest is defined per year. Each month you pay 1/12 of yearly interest.
    montlyInterest = rate / MONTHS_IN_YEAR
    top = principal * montlyInterest
    bot = 1 - ( 1 + montlyInterest )**-months
    
    return float(round(top/bot,2)) # rounding 2 decimals 

# https://money.stackexchange.com/questions/94140/what-is-the-math-used-to-calculate-the-impact-that-overpaying-a-mortgage-has-an 
def monthlyAmortizationTable(balanceRemaining :d.Decimal, interestPercent: str, moneyPayed :d.Decimal):
    rate = d.Decimal(interestPercent) / 100 

    interest =  round(d.Decimal(balanceRemaining * (rate / MONTHS_IN_YEAR)) ,2)
    principalContributed = round(moneyPayed - interest, 2)

    print (
            ("Remaining "        + str(balanceRemaining)).ljust(20) + " | " + 
            ("Towards interest " + str(interest)).ljust(20)         + " | " +
            ("Towards principal "+ str(principalContributed)).ljust(20) +  "|" 
    )

    return interest, principalContributed

# # # # # # # # # # # # #
# Simulations
# # # # # # # # # # # # #

def mixedMortgage():
    balance = d.Decimal(105000)

    # Importat. 
    # The monthly payment for the fixed part is calculated for the full loan duration (10 years in this case).
    # Basically "how much is your monthly if you were to pay 2.25 for the entire duration and when your fixed part ends we see".
    fixedPartInterest = "2.25"
    fixedDurationMonths = int(MONTHS_IN_YEAR * 5)
    fixedMonthlyPayment = montlyPaymentMonths(balance, 10 * MONTHS_IN_YEAR, fixedPartInterest)
       
    totalInterestLost = 0
    for _ in range(fixedDurationMonths):
        interestLost , principalContributed,  = monthlyAmortizationTable(balance, fixedPartInterest, d.Decimal(fixedMonthlyPayment))
        balance = d.Decimal(balance - principalContributed)
        totalInterestLost = totalInterestLost + interestLost
    fixedPartInterest = totalInterestLost;

    # Importat. 
    # The monthly payment for the var part is caclulated after the fixed part has ended based on `left to pay` and `remaining duration`
    # It's effectively acts as a re-mortgage.
    euribor = 4
    bankInterest = 1.8
    varPartInterest = str(euribor + bankInterest)
    varDurationMonths = int(MONTHS_IN_YEAR * 5)
    varMonthlyPayment = montlyPaymentMonths(balance, 5 * MONTHS_IN_YEAR, varPartInterest)
    

    for _ in range(varDurationMonths):
        interestLost , principalContributed,  = monthlyAmortizationTable(balance, varPartInterest, d.Decimal(varMonthlyPayment))
        balance = d.Decimal(balance - principalContributed)
        totalInterestLost = totalInterestLost + interestLost

    varPartInterest = totalInterestLost - fixedPartInterest

    
    print("Fix monthly " + str(fixedMonthlyPayment))
    print("Var monthly " + str(varMonthlyPayment))
    
    print("Fixed={} Var={} Total={} Balance={}".format(fixedPartInterest,varPartInterest, totalInterestLost, balance))
    return

if __name__ == '__main__':
    mixedMortgage()


