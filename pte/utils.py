import datetime


def get_date(s: str) -> datetime.date:
    """
    Helper function to convert string to datetime.date instance
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d').date()
