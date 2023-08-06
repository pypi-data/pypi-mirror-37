"""DateTime class file."""

import sys
import pytz
import dateutil.parser

class DateTime(object):
    """DateTime class."""

    def __init__(self, verbose=False):
        """Initiator method."""
        pass

    def convert_iso8601(self, iso8601_datetime):
        """Converts a datetime string in ISO 8601 format to a python datetime object
        Args:
          iso8601_datetime (str): A datetime str in ISO 8601 format e.g. 2018-09-25T03:00:12.834Z
        """

        # Convert datetime string in ISO 8601 format to python datetime object
        try:
            py_datetime = dateutil.parser.parse(iso8601_datetime)
        # Check if any exceptions
        except Exception as e:
            print 'Convert ISO8601 string to python datetime object failed. ERROR: %s ' % (e)
            return False

        return py_datetime

    def convert_tz(self, py_datetime, tz_set):
        """Converts a datetime python object to a specified timezone
        Args:
          py_datetime (obj): A datetime python object e.g. 2018-09-25 03:00:12.834000+00:00
          tz_set (str): A timezone string e.g. 'US/Eastern'
        """

        # Convert python object to a set timezone
        try:
            tz_datetime = py_datetime.astimezone(pytz.timezone(tz_set))
        # Check if timezone string is valid
        except pytz.UnknownTimeZoneError as e:
            print 'Timezone string %s is not valid. ERROR: %s ' % (tz_set, e)
            return False
        # Check if any exceptions
        except Exception as e:
            print 'Convert timezone failed. ERROR: %s ' % (e)
            return False

        return tz_datetime