import argparse


class LoanAmortizationCalculator(object):
    import math

    def __init__(self, principle: float, interest_rate: float, loan_term: int, monthly_pay: float = None):
        self.principle = principle
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        if monthly_pay is None:
            self.monthly_payment = self.calculate_monthly_payment()
        else:
            self.monthly_payment = monthly_pay
        self.loan_list = [] * loan_term

    def calculate_monthly_payment(self):
        j = self.interest_rate / 100 / 12
        return self.principle * (j / (1 - self.math.pow((1 + j), -self.loan_term)))

    # def monthly_interest(self, principle, interest_rate, loan_term, ):

    def amortize(self, counter: int):
        if counter >= self.loan_term:
            return self.loan_list

        month_interest = self.principle * self.interest_rate / 100 / 12
        self.loan_list.append({
            counter: {
                'interest': self.principle * month_interest,
                'principle_payment': self.monthly_payment - (self.principle * month_interest),
                'remaining_balance': self.principle - (self.monthly_payment - (self.principle * month_interest))
            }
        })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--principle')
    parser.add_argument('-r', '--interest-rate')
    parser.add_argument('-n', '--loan-term')
    parser.add_argument('-m', '--monthly-payment', default='None')

    args = parser.parse_args()
    loan = LoanAmortizationCalculator(args.principle, args.interest_rate, args.loan_term,
                                      None if args.monthly_payment == 'None' else args.monthly_payment)

    amor = loan.amortize(args.loan_term)
    print(amor)
