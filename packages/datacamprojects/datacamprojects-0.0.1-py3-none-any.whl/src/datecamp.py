from datetime import datetime


def keep_digits(string):
    return ''.join(char for char in string if char.isdigit())


def parse_date(date_str, input_format: str = '%Y%m%d'):
    return datetime.strptime(keep_digits(date_str), input_format).date()


def get_range(start, end):
    return range(int((end - start).days) + 1)


def to_date(start, end):
    if any(type(x) in (str, int) for x in (start, end)):
        return map(parse_date, [str(start), str(end)])
    else:
        return start, end


def format_weekdays(weekdays):
    if type(weekdays) in (str, int):
        return [int(x) for x in list(keep_digits(str(weekdays)))]
    else:
        return weekdays


def get_start_end_range(start, end):
    start_date, end_date = to_date(start, end)
    return start_date, end_date, get_range(start_date, end_date)
