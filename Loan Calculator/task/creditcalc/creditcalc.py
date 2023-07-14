import math
import argparse
from collections import Counter


def get_payment(principal: float, month: int) -> float:
    payment: float = (principal / month)
    return payment


def get_annuity_payment(principal: float, annual_interest_rate: float = 0.12, number_of_payments: int = 1) -> float:
    i = annual_interest_rate / 12  # monthly interest rate
    term1 = pow(1 + i, number_of_payments)
    annuity_payment = principal * i * term1 / (term1 - 1)
    return annuity_payment


def get_loan_principal(annuity_payment: float, annual_interest_rate: float = 0.12,
                       number_of_payments: int = 1) -> float:
    i = annual_interest_rate / 12  # monthly interest rate
    term1 = pow(1 + i, number_of_payments)
    loan_principal = annuity_payment / (i * term1 / (term1 - 1))
    return loan_principal


def get_number_of_payments(annuity_payment: float, annual_interest_rate: float = 0.12,
                           principal: float = 1000.0) -> int:
    i = annual_interest_rate / 12  # monthly interest rate
    number_of_payments = math.ceil(math.log(annuity_payment / (annuity_payment - i * principal), 1 + i))
    return number_of_payments


# def get_number_of_months(principal: float, payments: float) -> int:
#    number_of_months = principal / payments
#    return number_of_months


def get_last_payment(principal: float, periods: int, monthly_payment: float) -> float:
    last_payment = principal - (periods - 1) * monthly_payment
    return last_payment


def ask_what_to_calc() -> str:
    print("What do you want to calculate?")
    print('type "n" for number of monthly payments,')
    print('type "a" for annuity monthly payment amount,')
    print('type "p" for loan principal:')
    return input()


def convert_months_to_years_and_months(num_months: int) -> (int, int):
    rest_months = num_months % 12
    year = num_months // 12
    return year, rest_months


def get_differentiated_payments_months(principal: float,
                                       annual_interest_rate: float = 0.12,
                                       number_of_payments: int = 1,
                                       current_month: int = 1) -> float:
    i = annual_interest_rate / 12  # monthly interest rate

    differentiated_payments_months = math.ceil(
        (principal/number_of_payments)
        + i
        * (principal -
           (principal *
            (current_month - 1)
            / (number_of_payments))))

    print(f"Month {current_month + 1}: payment is {differentiated_payments_months}")

    return differentiated_payments_months


def get_differentiated_payments(principal: float,
                                annual_interest_rate: float = 0.12,
                                number_of_payments: int = 1) -> float:
    sum_of_differentiated_payments = 0
    for current_month in range(number_of_payments):
        sum_of_differentiated_payments += get_differentiated_payments_months(principal,
                                                                             annual_interest_rate,
                                                                             number_of_payments,
                                                                             current_month + 1)
    return sum_of_differentiated_payments


def args_checker(args_set):
    if Counter(args_set.values())[None] > 1:
        print("Incorrect parameters")
        exit()
    elif args_set.get("type") not in ["annuity", "diff"]:
        print("Incorrect parameters")
        exit()
    elif args_set.get("principal"):
        if args_set.get("principal") < 0:
            print("Incorrect parameters")
            exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program is a loan calculator.")
    parser.add_argument("--principal", type=float, help="set principal as float")
    parser.add_argument("--payment", type=float, help="set payment as float")
    parser.add_argument("--type", choices=["annuity", "diff"], help="select one of the choices")
    parser.add_argument("--periods", type=int, help="set periods as int")
    parser.add_argument("--interest", type=float, help="set interest rate as float")
    args, unparsed = parser.parse_known_args()
    args_set = vars(parser.parse_args())
    args_checker(args_set)

    if args.type == "annuity" and args_set.get("principal") is None:
        annuity_payment = args_set.get("payment")
        number_of_payments = args_set.get("periods")
        annual_interest_rate = args_set.get("interest") / 100
        loan_principal = math.floor(get_loan_principal(annuity_payment, annual_interest_rate, number_of_payments))
        overpayment = math.ceil(-1 * (loan_principal - annuity_payment * number_of_payments))
        print(f"Your loan principal = {loan_principal}!")
        print(f"Overpayment = {overpayment}")

    elif args.type == "annuity" and args_set.get("payment") is None:
        loan_principal: float = args_set.get("principal")
        number_of_payments: int = args_set.get("periods")
        annual_interest_rate: float = args_set.get("interest") / 100
        annuity_payment: float = math.ceil(get_annuity_payment(loan_principal, annual_interest_rate, number_of_payments))
        print(f"Your monthly payment = {annuity_payment}!")

    elif args.type == "annuity" and args_set.get("periods") is None:
        loan_principal: float = args_set.get("principal")
        annual_interest_rate: float = args_set.get("interest") / 100
        annuity_payment: float = args_set.get("payment")
        number_of_payments = get_number_of_payments(annuity_payment, annual_interest_rate, loan_principal)
        years, rest_months = convert_months_to_years_and_months(number_of_payments)
        print(f"It will take "
              f"{years} year{'' if years == 1 else 's'} "
              f"and "
              f"{rest_months} month{'' if rest_months == 1 else 's'} "
              f"to repay this loan!")
        overpayment = math.ceil(-1 * (loan_principal - annuity_payment * number_of_payments))
        print(f"Overpayment = {overpayment}")

    elif args.type == "diff":
        loan_principal: float = args_set.get("principal")
        number_of_payments: int = args_set.get("periods")
        annual_interest_rate: float = args_set.get("interest") / 100
        sum_of_differentiated = get_differentiated_payments(principal=loan_principal,
                                                            annual_interest_rate=annual_interest_rate,
                                                            number_of_payments=number_of_payments)
        overpayment = math.ceil(sum_of_differentiated-loan_principal)
        print(f"Overpayment = {overpayment}")

    # what_to_calc: str = ask_what_to_calc()
    what_to_calc = ""
    if what_to_calc == "a":
        loan_principal: float = float(input("Enter the loan principal:\n"))
        number_of_payments: int = int(input("Enter the number of periods:\n"))
        annual_interest_rate: float = float(input("Enter the loan interest:\n")) / 100
        annuity_payment: float = get_annuity_payment(loan_principal, annual_interest_rate, number_of_payments)
        print(f"Your monthly payment = {math.ceil(annuity_payment)}!")
    elif what_to_calc == "n":
        loan_principal: float = float(input("Enter the loan principal:\n"))
        annuity_payment = int(input("Enter the monthly payment:\n"))
        annual_interest_rate: float = float(input("Enter the loan interest:\n")) / 100
        num_months_to_pay = get_number_of_payments(annuity_payment, annual_interest_rate, loan_principal)
        years, rest_months = convert_months_to_years_and_months(num_months_to_pay)
        print(f"It will take "
              f"{years} year{'' if years == 1 else 's'} "
              f"and "
              f"{rest_months} month{'' if rest_months == 1 else 's'} "
              f"to repay this loan!")
    elif what_to_calc == "p":
        annuity_payment = float(input("Enter the monthly payment:\n"))
        number_of_payments: int = int(input("Enter the number of periods:\n"))
        annual_interest_rate: float = float(input("Enter the loan interest:\n")) / 100
        loan_principal = get_loan_principal(annuity_payment, annual_interest_rate, number_of_payments)
        print(f"Your loan principal = {math.floor(loan_principal)}!")