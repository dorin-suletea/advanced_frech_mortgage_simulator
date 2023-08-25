import main as m
import decimal as d
import unittest

class TestSum(unittest.TestCase):

    def test_montly_payment(self):
        montly = m.montlyPaymentYears(300000,30, '6.0')
        self.assertEqual(montly,1798.65)


    def test_using_months(self):
        usingYears = m.montlyPaymentYears(300000, 30 , '6.0')
        usingMonths = m.montlyPaymentMonths(d.Decimal(300000), 30 * 12, '6.0')
        self.assertEqual(usingYears, usingMonths)


    # idealista simulator has lower accuracy than this script because rounds up to 0dp.
    # https://www.loanamortizationschedule.org/schedule/105000/225/?down=0&years=15&by=monthly
    # https://www.idealista.com/hipotecas/simulador-hipotecas/
    def test_compare_to_online_calcs(self):
        years = 15
        principal = 105000
        interest = '2.25'

        montlyPaymet = m.montlyPaymentMonths(d.Decimal(principal), years * 12, interest)
        totalCost = round(montlyPaymet * 15 * 12, 2)
        loanInterest = round(totalCost - principal, 2)

        self.assertEqual(687.84,montlyPaymet)
        self.assertEqual(18811.2, loanInterest)
        self.assertEqual(123811.2, totalCost)

    def test_amortization_table(self):
        balance = d.Decimal(105000)
        interest = '2.25'

        interestLost , principalContributed,  = m.monthlyAmortizationTable(balance, interest, d.Decimal(687.84))
        self.assertEqual(196.88, float(interestLost))
        self.assertEqual(490.96, float(principalContributed))
        
        totalInterestLost = 0
        for _ in range(12 * 15):
            interestLost , principalContributed,  = m.monthlyAmortizationTable(balance, interest, d.Decimal(687.84))
            balance = d.Decimal(balance - principalContributed)
            totalInterestLost = totalInterestLost + interestLost

        self.assertEqual(18810.94, float(totalInterestLost))
        self.assertEqual(-0.26, float(balance)) # should be 0 but we lost some accuracy with 2dp rounding

if __name__ == '__main__':
    unittest.main()
