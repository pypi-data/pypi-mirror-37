from gladepaypython.errors import InvalidDataError


def validate_pay_amount(pay_amount):

    if not pay_amount:
        raise InvalidDataError("pay_Amount to be charged is required")

    if isinstance(pay_amount, int) or isinstance(pay_amount, float): #Perform some checks
        if pay_amount < 0:
            raise InvalidDataError("Negative pay_amount is not allowed")
        return pay_amount
    else:
        raise InvalidDataError("Amount should be a number")