from datetime import datetime


def get_current_datetime(self) -> datetime:
    """
    A utility function for returning the current date and time in a
    datetime object
    
    Returns:
        A datetime object containing the date / time of measurement.

    """
    return datetime.now()
