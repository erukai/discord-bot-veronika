from datetime import datetime, timezone

# Reference Earth start time: 1/1/10 AD, 00:00:00 UTC
earth_ref = datetime(10, 1, 1, tzinfo=timezone.utc)

# Reference World start time: 1/1/3235, 00:00:00 SST
orcus_ref = datetime(3235, 1, 1)
orcus_ref_year = orcus_ref.year

# Orcus time constants
HOURS_PER_DAY = 20

DAYS_REG_MONTH = 50
DAYS_FINAL_MONTH = 61
DAYS_FINAL_MONTH_LEAP = 62

MONTHS_PER_YEAR = 30
REG_MONTHS_PER_YEAR = 29

DAYS_PER_YEAR = 1511
DAYS_PER_YEAR_LEAP = 1512

LEAP_INTERVAL = 9
DAYS_IN_CYCLE = 13600 #total days in the 9-year leap cycle


#------------------------------------------------------------------


def running_time():

    # Get the current Earth time
    earth_now = datetime.now(timezone.utc)
    delta = earth_now - earth_ref
    elapsed_hours = delta.total_seconds() / 3600 #total of hours between the two earth dates


    # Convert the hours into days + hours in Orcus
    orcus_elapsed_days = int(elapsed_hours // HOURS_PER_DAY)
    orcus_hour = int(elapsed_hours % HOURS_PER_DAY)


    # 9-year leap cycles

    cycles = orcus_elapsed_days // DAYS_IN_CYCLE
    orcus_year = orcus_ref_year + cycles * LEAP_INTERVAL
    remaining_days = orcus_elapsed_days % DAYS_IN_CYCLE


    # Leftover years (years that hasn't completed a leap cycle yet)

    while True:
        days_in_year = DAYS_PER_YEAR_LEAP if (orcus_year % LEAP_INTERVAL == 0) else DAYS_PER_YEAR
        if remaining_days < days_in_year:
            break
        remaining_days -= days_in_year
        orcus_year += 1


    # Months

    #days_in_lastmonth = DAYS_FINAL_MONTH_LEAP if orcus_year % LEAP_INTERVAL == 0 else DAYS_FINAL_MONTH #kinda not necessary honestly
    #add leap day on final month if current year is leap year, else no leap day

    if remaining_days < REG_MONTHS_PER_YEAR * DAYS_REG_MONTH:
        orcus_month = remaining_days // DAYS_REG_MONTH + 1
        orcus_day = remaining_days % DAYS_REG_MONTH + 1

    else:
        remaining_days -= REG_MONTHS_PER_YEAR * DAYS_REG_MONTH
        orcus_month = MONTHS_PER_YEAR
        orcus_day = remaining_days + 1


    # Turn into date format
    orcus_time = f"{orcus_day:02}/{orcus_month:02}/{orcus_year} {orcus_hour:02}:{earth_now.minute:02}"

    return orcus_time