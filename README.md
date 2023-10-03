# DarkSide calendar sync tool

This is a single-use tool for calendar and training sessions synchronization. 

_I was just lazy after each training (un)registered to update my calendar._


## Installation
The tool uses `pdm` (**P**ython **d**ependency **m**anager), so install it first.

Then, just run:

```
pdm install
```

## Usage
Tool requires credentials both for CalDAV and your Gym account, see `pdm run sync --help`:

```
usage: -c [-h] [--start_date START_DATE] [--end_date END_DATE] --gym-url GYM_URL [--slow] [--gym-user GYM_USER] [--gym-password GYM_PASSWORD] --caldav-url CALDAV_URL [--calendar CALENDAR] [--caldav-user CALDAV_USER]
          [--caldav-password CALDAV_PASSWORD]

Gym Arguments

options:
  -h, --help            show this help message and exit
  --start_date START_DATE
                        Start date
  --end_date END_DATE   End date
  --gym-url GYM_URL     Gym base URL
  --slow                Sleep between requests
  --gym-user GYM_USER   User name
  --gym-password GYM_PASSWORD
                        Password
  --caldav-url CALDAV_URL
                        CalDAV URL
  --calendar CALENDAR   Calendar name
  --caldav-user CALDAV_USER
                        User name
  --caldav-password CALDAV_PASSWORD
                        Password
```

There is a support of passing secrects via environment, in that case, you can run the tool with:

```
GYM_USER="" GYM_PASSWORD="" CALDAV_USER="" CALDAV_PASSWORD="" pdm run sync --gym-url "" --caldav-url "" --calendar "CalendarName"
```


