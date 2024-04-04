from datetime import datetime


def convert_date(str_date):
    str_date = str(str_date).strip()
    str_date = str_date.replace(' ', '')

    # 根据字符串特征选择合适的日期格式
    if '-' in str_date:
        if ':' in str_date:
            date_format = "%Y-%m-%d %H:%M:%S"
        else:
            date_format = "%Y-%m-%d"
    elif '年' in str_date:
        if '秒' in str_date:
            if ' ' in str_date:
                date_format = "%Y年%m月%d日 %H时%M分%S秒"
            else:
                date_format = "%Y年%m月%d日%H时%M分%S秒"
        elif '时' in str_date:
            if ' ' in str_date:
                date_format = "%Y年%m月%d日 %H时%M分"
            else:
                date_format = "%Y年%m月%d日%H时%M分"
        else:
            date_format = "%Y年%m月%d日"
    else:
        date_format = "%Y%m%d"

    # 尝试解析日期，避免了多次异常处理
    try:
        return datetime.strptime(str_date, date_format)
    except ValueError:
        raise ValueError(f'日期无法解析: {str_date}')


def pares_json(json_data: dict, date_keys: list):
    for key in date_keys:
        if key in json_data:
            json_data[key] = convert_date(json_data[key])
    return json_data
