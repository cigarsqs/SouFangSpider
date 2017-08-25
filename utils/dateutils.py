import datetime


def get_date_from_str(str_date):
    try:
        date = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    except ValueError:
        print "error happened!"
        return None
    return date

