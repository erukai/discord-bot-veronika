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

def earth_to_orcus(day, month, year, hour):

    # Get total hours
    earth_input = datetime(year, month, day, hour, tzinfo=timezone.utc)
    delta = earth_input - earth_ref
    elapsed_hours = delta.total_seconds() / 3600 #total of hours between the two earth dates


    # Convert the hours into days + hours in Orcus
    orcus_elapsed_days = int(elapsed_hours // HOURS_PER_DAY)
    'Apparently  using int() is wrong? int() ignores whatever decimal points it has, so i guess it can create misalignment...?'
    orcus_hour = int(elapsed_hours % HOURS_PER_DAY)
    'Same issue. Honestlly, it probably does not matter.'


    # 9-year leap cycles

    cycles = orcus_elapsed_days // DAYS_IN_CYCLE
    orcus_year = orcus_ref_year + cycles * LEAP_INTERVAL #current year. Compared to current day and month, the year is easy to get, huh?
    remaining_days = orcus_elapsed_days % DAYS_IN_CYCLE


    # Leftover years (years that hasn't completed a leap cycle yet, i.e. current cycle)

    while True:
        days_in_year = DAYS_PER_YEAR_LEAP if (orcus_year % LEAP_INTERVAL == 0) else DAYS_PER_YEAR
        #days_in_year = 1512 if current year is divisible by 9, which is a leap year. If not, then not leap year

        if remaining_days < days_in_year:
            break

        remaining_days -= days_in_year
        orcus_year += 1


    # Months

    #if orcus_year % LEAP_INTERVAL == 0: #if current year is leap year, add leap day
        #days_in_lastmonth = DAYS_FINAL_MONTH_LEAP
    #else:
        #days_in_lastmonth = DAYS_FINAL_MONTH #if current year not leap year, no leap day

    if remaining_days < (REG_MONTHS_PER_YEAR) * DAYS_REG_MONTH: #if current month not 30th
        orcus_month = remaining_days // DAYS_REG_MONTH + 1
        orcus_day = remaining_days % DAYS_REG_MONTH + 1
    else:
        remaining_days -= (REG_MONTHS_PER_YEAR) * DAYS_REG_MONTH #else, current month is 30th
        orcus_month = MONTHS_PER_YEAR
        orcus_day = remaining_days + 1


    # Turn into date format
    earth_time = f"{day:02}/{month:02}/{year} {hour:02}:00:00"
    orcus_time = f"{orcus_day:02}/{orcus_month:02}/{orcus_year} {orcus_hour:02}:00:00"

    return earth_time, orcus_time