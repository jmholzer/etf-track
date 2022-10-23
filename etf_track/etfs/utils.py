from collections import defaultdict
from datetime import datetime

from django.db.models.query import QuerySet
from pandas import DataFrame


def get_current_datetime(self) -> datetime:
    """A utility function for returning the current date and time in a
    datetime object

    Returns:
        A datetime object containing the date / time of measurement.

    """
    return datetime.now()


def convert_queryset_to_dataframe(
    queryset: QuerySet, *, exclude_id: bool = False
) -> DataFrame:
    """Convert a QuerySet to a pandas DataFrame

    Arguments:
        queryset: the QuerySet object to convert

    Returns:
        A DataFrame object containing the data of the QuerySet
    """
    result = defaultdict(list)

    for row in queryset:
        for field in vars(row):
            if field == "_state":
                continue
            if exclude_id and field == "id":
                continue
            result[field].append(getattr(row, field))
    return DataFrame.from_dict(result)
