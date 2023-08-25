import decimal as d
import formulas as m


# # # # # # # # # # # # #
# Simulations
# # # # # # # # # # # # #

"""
Runs good ol' boring mixed simulation without any overpayment. 
The code calculates the mothly payment, it should be very similar to what the bank tells you it's going to be.

Example : for a mixed loan for 105k for 15 years, 5 years fixed at 2.25, and remaining 10 years variable at 5.8 
run the following :  mixedMortgage(d.Decimal(105000),"2.25", 5, "5.8", 10)

Note: variableRate is usually EURIBOR (or a similar metric in your reguion) + what the bank wants on top.
EURIBOR is not constant but fluctuates from month to month.
Take your best guess for what an avg EURIBOR looks like for the duration of your loan. 
"""
def mixedMortgage(loan: d.Decimal, fixedInterest: str, fixedTermYears: int, varInterest: str, varTermYears: int):
    balance = loan
    totalLoanDuration = fixedTermYears + varTermYears

    # Importat. 
    # The monthly payment for the fixed part is calculated for the full loan duration (10 years for example).
    # Basically "how much is your monthly if you were to pay 2.25 for the entire duration and when your fixed part ends we shall recalculate".
    fixedDurationMonths = int(m.MONTHS_IN_YEAR * fixedTermYears)
    fixedMonthlyPayment = m.montlyPaymentMonths(balance, totalLoanDuration * m.MONTHS_IN_YEAR, fixedInterest)       
    interestForFixed = 0
    for _ in range(fixedDurationMonths):
        interestLost , principalContributed,  = m.monthlyAmortizationTable(balance, fixedInterest, d.Decimal(fixedMonthlyPayment))
        balance = d.Decimal(balance - principalContributed)
        interestForFixed += interestLost


    # Importat. 
    # The monthly payment for the var part is caclulated after the fixed part has ended based on `left to pay` and `remaining duration`
    # It's effectively acts as a re-mortgage.
    varDurationMonths = int(m.MONTHS_IN_YEAR * varTermYears)
    varMonthlyPayment = m.montlyPaymentMonths(balance, varDurationMonths, varInterest)
    interestForVar = 0
    for _ in range(varDurationMonths):
        interestLost , principalContributed,  = m.monthlyAmortizationTable(balance, varInterest, d.Decimal(varMonthlyPayment))
        balance = d.Decimal(balance - principalContributed)
        interestForVar += interestLost


    print("Fix monthly payment" + str(fixedMonthlyPayment))
    print("Var monthly payment" + str(varMonthlyPayment))
    print("Fixed={} Var={} Total={} Balance={}".format(interestForFixed, interestForVar, interestForFixed + interestForVar, balance))
    return

"""
You overpay each month by a fixed ammount in addition to what the bank wants you to pay.

Note : AFAIK Loans are issued in "years & montly payment" for convenience.
The bank calculates what's the mininimum montly payment for you to be done with it in x years.
The loan is finished when the balance you owe becomes zero. 
This code breaks when you owe 0 money. The loan should go for the full duration only if you overpay 0 each month.

Amortization table cross-checkked with : https://www.halifax.co.uk/mortgages/mortgage-calculator/overpayment-calculator.html
"""

def mixedMortgageWithOverPayment(loan: d.Decimal, fixedInterest: str, fixedTermYears: int, varInterest: str, varTermYears: int, overPayment: d.Decimal):
    balance = loan
    totalLoanDuration = fixedTermYears + varTermYears

    # fix
    fixedDurationMonths = int(m.MONTHS_IN_YEAR * fixedTermYears)
    fixedMonthlyPayment = m.montlyPaymentMonths(balance, totalLoanDuration * m.MONTHS_IN_YEAR, fixedInterest)       
    interestForFixed = 0
    for _ in range(fixedDurationMonths):
        if balance <= 0:
            break
        interestLost , principalContributed = m.monthlyAmortizationTable(balance, fixedInterest, d.Decimal(fixedMonthlyPayment) + overPayment)
        balance = d.Decimal(balance - principalContributed)
        interestForFixed += interestLost

    # var
    varDurationMonths = int(m.MONTHS_IN_YEAR * varTermYears)
    varMonthlyPayment = m.montlyPaymentMonths(balance, varDurationMonths, varInterest)
    interestForVar = 0
    for _ in range(varDurationMonths):
        if balance <= 0:
            break
        interestLost , principalContributed,  = m.monthlyAmortizationTable(balance, varInterest, d.Decimal(varMonthlyPayment) + overPayment)
        balance = d.Decimal(balance - principalContributed)
        interestForVar += interestLost


    print("Fix monthly payment = {} + {}".format(fixedMonthlyPayment, overPayment))
    print("Var monthly payment = {} + {}".format(varMonthlyPayment, overPayment))
    print("FixedInterest={} | VarInterest={} | TotalInterest={} | Balance={}".format(interestForFixed, interestForVar, interestForFixed + interestForVar, balance))
    return

 
 
"""
Utility method similar to mixedMortgageWithOverPayment. 

Instead of overpaying by X each month in addition to what the bank wants, you decide to pay a flat sum each month 
(can't be lower than the min monthly bank requires)
"""
def mixedMortgageWithSelfInposedPayment(loan: d.Decimal, fixedInterest: str, fixedTermYears: int, varInterest: str, varTermYears: int, selfImposedPayment: d.Decimal):
    balance = loan

    # fix
    fixedDurationMonths = int(m.MONTHS_IN_YEAR * fixedTermYears)
    interestForFixed = 0
    for _ in range(fixedDurationMonths):
        if balance <= 0:
            break
        interestLost , principalContributed = m.monthlyAmortizationTable(balance, fixedInterest, selfImposedPayment)
        balance = d.Decimal(balance - principalContributed)
        interestForFixed += interestLost

    # var
    varDurationMonths = int(m.MONTHS_IN_YEAR * varTermYears)
    interestForVar = 0
    for _ in range(varDurationMonths):
        if balance <= 0:
            break
        interestLost , principalContributed,  = m.monthlyAmortizationTable(balance, varInterest, selfImposedPayment)
        balance = d.Decimal(balance - principalContributed)
        interestForVar += interestLost


    print("Fix monthly payment = {}".format(selfImposedPayment))
    print("Var monthly payment = {}".format(selfImposedPayment))
    print("FixedInterest={} | VarInterest={} | TotalInterest={} | Balance={}".format(interestForFixed, interestForVar, interestForFixed + interestForVar, balance))
    return
 

if __name__ == '__main__':
    # mixedMortgage(d.Decimal(105000),"2.25", 5, "5.8", 10)

    # mixedMortgageWithOverPayment(d.Decimal(105000),"2.25", 5, "5.8", 5, d.Decimal(1000))
     mixedMortgageWithOverPayment(d.Decimal(105000),"2.25", 5, "5.8", 10, d.Decimal(1500))

    #mixedMortgageWithSelfInposedPayment(d.Decimal(105000),"2.25", 5, "5.8", 5, d.Decimal(2000))
    #mixedMortgageWithSelfInposedPayment(d.Decimal(105000),"2.25", 5, "5.8", 10, d.Decimal(2000))






    
