
def date_to_datetime(d):
    from datetime import datetime, date

    if isinstance(d, date):
        return datetime.combine(d, datetime.min.time())
    else:
        raise Exception("'d' is not a datetime.date object.")
