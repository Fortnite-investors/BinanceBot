import decimal


class ParseError(Exception):
    pass


def parse_decimal(value: str, arg_name: str) -> decimal.Decimal:
    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation:
        raise ParseError(f'Не верный формат аргумента {arg_name}')


class CostArgs:
    goal_amount: decimal.Decimal
    goal_currency: str
    goal_bank: str
    base_currency: str
    base_bank: str

    def __init__(self, args):
        if len(args) < 5:
            raise ParseError(f'Не верное число аргументов')
        self.goal_amount = parse_decimal(args[0], 'goal_amount')
        self.goal_currency = args[1]
        self.goal_bank = args[2]
        self.base_currency = args[3]
        self.base_bank = args[4]

