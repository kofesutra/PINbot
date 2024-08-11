from yoomoney import Authorize, Quickpay
from yoomoney import Client

from Config.config import YOOWALLET, YOOTOKEN, YOOCLIENTID, YOOREDIRECTURI


async def yoo_receive_pay_link(pay_description, amount, label):  # Наименование платежа и метка string, amount int
    quickpay = Quickpay(
        receiver=YOOWALLET,  # Номер кошелька в юмани
        quickpay_form="shop",
        targets=pay_description,  # Описание (название) платежа
        paymentType="SB",
        sum=amount,  # Сумма в рублях
        label=label  # Метка платежа Допустимо использовать значения длиной до 64 символов. Значение метки чувствительно к регистру символов.
    )
    # print(quickpay.base_url)  # Бессрочная ссылка
    # print(quickpay.redirected_url)  # Со сроком давности, берём эту в работу
    return quickpay.redirected_url


async def yoo_check_payment(label):  # return status (success, refused, in_progress), datetime, amount
    token = YOOTOKEN
    client = Client(token)
    status = 'none'
    datetime = '2000-01-01 01:01:01'
    amount = 0
    try:
        history = client.operation_history(label=label)
        ll = len(history.operations)  # При неудаче выдаёт 0 иначе 1
        if ll != 0:
            for operation in history.operations:
                status = operation.status
                datetime = operation.datetime
                amount = operation.amount
            return status, datetime, amount
        else:
            return status, datetime, amount
    except Exception as ex:
        return status, datetime, amount
