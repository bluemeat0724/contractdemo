from datetime import datetime


def validate_date_expire(date: datetime):
    if date < datetime.now():
        return "合同结束日期早于当前日期 请检查"
    return ''


def check_contract_amount(float_amount, chinese_amount):
    if float_amount != chinese_amount:
        return f"合同金额不匹配 请检查\n 数字金额: {float_amount}\n 中文金额: {chinese_amount}"
    return ''
