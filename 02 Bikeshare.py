import time
import csv
import itertools
import pandas as pd
import numpy as np

chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

## Removed get_filters() too difficult to debug code with such large chunks!!
## Define each specific fucntion before moving on to another. 

##get_filters():
"""
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
def get_city():
    city = input('Hi There! Let\'s rock some US bikeshare data!'
                 'Pick one of these three Chicago, New York, or Washington?\n')
    city = city.strip().lower()

    valid_cities = ['chicago','new york', 'washington']

    while city not in valid_cities:
        city = input('\nDoes not compute. Try Chicago, New york, or Washinton.\n')

    if city == 'chicago':
        return chicago
    elif city == 'new york':
        return new_york_city
    elif city == 'washington':
        return washington

## need time period after selecting city so the loop is less complicated 

def get_time_period():
    time_period = input('\nDo you want to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
    time_period = time_period.strip().lower()
    
    valid_time_periods = ['month','day','none']

    while time_period not in  valid_time_periods:
        time_period = input('\nDoes not compute.'
                            '\nTry month, Day, or None.\n')

    return time_period

## define nmonth after user selects month for time period observed 
# TO DO: get user input for month (all, january, february, ... , june) 
def get_month():
    month = input('\nWhich month in this list? January, February, March, April, May, or June?\n')
    month = month.strip().lower()

    valid_months = ['january','february','march','april','may','june']

    while month not in valid_months:
        month = input('\nMonth filter does not compute.'
                      'Which month? January, February, March, April, May, or June?\n')

    return month

# TO DO: get user input for day of week (all, monday, tuesday, ... sunday) 
def get_day(month):
    while True:
        try:
            day = int(input('\nAny specific day? Please type your response as a whole number.\n'))
        except ValueError:
            print('\nDoes not compute. Try a whole number.')
            continue 
        if day < 1:
            print("Does not exist.")
            continue
        elif month == 'february' and day > 28:
            print("Tis this a leap year? Try again.")
            continue
        elif (month == 'april' or month == 'june') and day > 30:
            print("Does not exist.")
            continue
        elif day > 31:
            print("Does not exist.")
            continue
        else: 
            break

    return day

    print('-'*40)

def load_data(city, month, day):
    
    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['date'] = df['Start Time'].dt.day

# index months to integer
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1

        df = df = df[df['month'] == month]
#index day to integer
    if day != 'all':
        df = df[df['date'] == day]

    return df

"""Displays statistics on the most frequent times of travel."""
    
# TO DO: display the most common month - Need to define in smaller chunks
def popular_month(df):
    print('Calculating The Most Frequent Times of Travel...')
    start_time = time.time()
    print("This took %s seconds.\n" % (time.time() - start_time))
    
    popular_month = df['month'].mode()[0]

    if popular_month == 1:
        return 'January'
    if popular_month == 2:
        return 'February'
    if popular_month == 3:
        return 'March'
    if popular_month == 4:
        return 'April'
    if popular_month == 5:
        return 'May'
    if popular_month == 6:
        return 'June'

# TO DO: display the most common day of week
def popular_day(df):
    
    popular_day = df['day_of_week'].mode()[0]

    return popular_day

# TO DO: display the most common start hour
def popular_hour(df):
    
    popular_hour = df['hour'].mode()[0]

    if popular_hour == 0:
        return '12 a.m.'
    elif popular_hour == 12:
        return '12 p.m.'
    elif popular_hour <= 11:
        return '{} a.m.'.format(popular_hour)
    elif popular_hour > 12:
        popular_hour -= 12
        return '{} p.m.'.format(popular_hour)
    
    print('-'*40)

    ## next section on start stop values
def trip_duration(df):
    ## Trip Duration needed to calc average

    total_duration = df['Trip Duration'].sum()
    avg_duration = df['Trip Duration'].mean()

    total_hours = total_duration / 3600.00
    avg_hours = avg_duration / 60.00

    return (total_hours, avg_hours)

def popular_stations(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()
    print("This took %s seconds.\n" % (time.time() - start_time))

# TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    
# TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    
    return(popular_start, popular_end)
# TO DO: display most frequent combination of start station and end station trip

# TO DO: display total travel time
def popular_trip(df):
    """Displays statistics on the total and average trip duration."""
    print('-'*80)
    print('Calculating Trip Duration...')
    start_time = time.time()
    print("This took %s seconds.\n" % (time.time() - start_time))
    
    popular_trip = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().idxmax()
    
    return popular_trip

# TO DO: Display counts of user types
def users(df):
    print('Calculating User Stats...')
    start_time = time.time()
    print("This took %s seconds.\n" % (time.time() - start_time))
    
    user_types_count = pd.value_counts(df['User Type']).values

    return user_types_count

# TO DO: Display counts of gender
def gender(df):
    genders = pd.value_counts(df['Gender']).values

    return genders

# TO DO: Display earliest, most recent, and most common year of birth
def birth_years(df):
 
    most_common_year = str(int(df['Birth Year'].mode()[0]))
    youngest = str(int(df['Birth Year'].max()))
    oldest = str(int(df['Birth Year'].min()))

    return (most_common_year, oldest, youngest)
   
## To Do: Display city data 5 lines of sequence
def display_data(city):
    
    display = input('\nDo you want to see individual trip data? '
                    'Type \'yes\' or \'no\'.\n')

    valid_input = ['yes','no']

    while display not in valid_input:
        print("I don't understand that.")
        display = input('\nDo you want to see individual trip data? '
                    'Type \'yes\' or \'no\'.\n')

    start = 1
    end = 6    
    while display == 'yes':
        with open(city, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in itertools.islice(reader, start, end):
                print(row)
                start +=5
                end +=5
        display = input('\nDo you want to keep going on individual trip data? '
                    'Type \'yes\' or \'no\'.\n')
        while display not in valid_input:
            print("does not compute.")
            display = input('\nKeep going? '
                    'Type \'yes\' or \'no\'.\n')

def main():
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    if time_period == 'month':
        month = get_month()
    else:
        month = 'all'

    if time_period == 'day':
        month = get_month()
        day = get_day(month)
    else:
        day = 'all'

    df = load_data(city, month, day)
    
    print('-'*80)
    print('Computing stats...')
    print('-'*80)

    # Print popular month
    if time_period == 'none':
        
        print(popular_month(df) + " is the most popular month.\n")

    # Print popular day of week
    if time_period == 'none' or time_period == 'month':
        
        print(popular_day(df) + " is the favorite day.\n")        

    # Print popular hour
    print(popular_hour(df) + " is the busiest hour of the day.\n")
    
    print('-'*80)

    # Print popular stations 
    stations = popular_stations(df)
    print("The most popular start station is {}.\n".format(stations[0],stations[1]))
    print("The most popular end station is {}.\n".format(stations[0],stations[1]))
    
    # print popular trips
    trip = popular_trip(df)
    print("The most popular trip is {} to {}.\n".format(trip[0],trip[1]))
    
    # print popular trip duration
    durations = trip_duration(df)
    print("The total duration is {} hours.\nThe average duration is {} minutes.\n".format(durations[0],durations[1]))
    
    print('-'*80)
    
# TO DO: Display counts of user types
    types = users(df)
    print("There are {} users and {} customers.\n".format(types[0],types[1]))

# TO DO: Display counts of gender
    if city != washington:
        genders = gender(df)
        print("There are {} males and {} females.\n".format(genders[0],genders[1]))

# TO DO: Display earliest, most recent, and most common year of birth
    if city != washington:
        years = birth_years(df)
        print("The most frequent birth year is {}.\n".format(years[0]))
        print("The oldest rider was born in {}.\n".format(years[1]))
        print("The youngest rider was born in {}.\n".format(years[2]))

    print('-'*80)
    
# To Do Display data sequence
    display_data(city)
    
    print('-'*80)
    
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
  main()
