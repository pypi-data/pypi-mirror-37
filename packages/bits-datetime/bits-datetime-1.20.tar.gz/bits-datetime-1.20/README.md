# bits-datetime

A set of reusable utilities to handle various datetime formats for conversion and display

```
from bits.datetime import DateTime as bits_datetime
  
bdt = bits_datetime()

# Convert a string in ISO8601 format to a Python datetime object
converted_date = bdt.convert_iso('2018-09-25T03:00:12.834Z')
print(converted_date)

# Change the timezone to US/Eastern
converted_date_tz = bdt.convert_tz(converted_date, 'US/Eastern')
print(converted_date_tz)
```