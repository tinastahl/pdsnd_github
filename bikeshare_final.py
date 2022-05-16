import time
import pandas as pd
import numpy as np

CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday', 'All']

def readable_time(secs):
    """
    This function splits seconds into days, hours, minutes and seconds 
    Args:
        secs - seconds 
    Returns:
        (int) days_r - days
        (int) hours_r - hours
        (int) mins_r - minutes
        (int) secs_r - seconds
    """
    days_r = int(secs // (24*60*60))
    hours_r = int((secs - days_r*24*60*60) // (60*60))
    mins_r = int((secs - days_r*24*60*60 - hours_r*60*60) // 60)
    secs_r = int(secs % 60)

    return days_r, hours_r, mins_r, secs_r

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\nWhich city is of interest? Chicago (c), New York City (n) or Washington (w)? \nNote: more detailed customer data available for Chicago and New York City')
      
    while True:
        try:
            city = input('\n  Filter city: ').lower()
            city_valid = CITY_DATA[city]
            break
        except KeyError:
            print('That was no valid input. Please try again...')

    # TO DO: get user input for month (all, january, february, ... , june)
    month = 0
    print('\nOkidoki. Do you want to filter this dataset by month? \nNote: January, February, March, April, May and June are available. \nIf you want to see all the data, please type: all.')
    month = input('\n  Filter month: ').title()
    while month not in MONTHS:
        print('That was no valid input. Please try again...')
        month = input('\nFilter month: ').title()
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nOk, thanks. Last question for now: Do you want to filter by the day of the week? \nPlease type: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? If you don\'t want to filter, please type: all.')
    day = input('\n  Filter day: ').title()
    while day not in days:
        print('That was no valid input. Please try again...')
        day = input('\nFilter day: ').title()
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day and sorted by index
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
   
    # filter by month if applicable
    if month != 'All':
        # use the index of the MONTHS list to get the corresponding int
        month = MONTHS.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    df = df.sort_index()
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month: ', MONTHS[most_common_month - 1])

    # TO DO: display the most common day of week
    print('Most common day of week: ', df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    print('Most common start hour: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' -> ' + df['End Station']
    print('Most commonly used combination of start and end station trip: ', df['Station Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time in seconds and in a more readable way
    total_travel_time = int(df['Trip Duration'].sum() )
    days_r, hours_r, mins_r, secs_r = readable_time(total_travel_time) 
    print('Total travel time [s]:', total_travel_time)
    print('Or: {} day(s), {} hour(s), {} minute(s) and {} second(s).'.format(days_r, hours_r, mins_r, secs_r))

    # TO DO: display mean travel time in seconds and in a more readable way
    mean_travel_time = int(df['Trip Duration'].mean())
    days_r, hours_r, mins_r, secs_r = readable_time(mean_travel_time) 
    print('\nMean travel time [s]: ', mean_travel_time)
    print('Or: {} day(s), {} hour(s), {} minute(s) and {} second(s).'.format(days_r, hours_r, mins_r, secs_r))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of different USER TYPES:') 
    print(user_types.to_string())
    user_type_is_null = df['User Type'].isnull().sum()
    df_length = len(df)
    print('{}/{} events without user type information.'.format(user_type_is_null, df_length))
    
    if 'Gender' in df:
        # TO DO: Display counts of gender
        gender_types = df['Gender'].value_counts()
        gender_is_null = df['Gender'].isnull().sum()
        print('\nCounts of GENDER:')
        print(gender_types.to_string())
        print('{}/{} events without gender information.'.format(gender_is_null, df_length))
    if 'Birth Year' in df:
        # TO DO: Display earliest, most recent, and most common year of birth
        birth_year_is_null = df['Birth Year'].isnull().sum()
        print('\nAGE statistics:')
        print('Earliest year of birth: ', int(df['Birth Year'].min()))
        print('Most recent year of birth: ', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mean(skipna=True)))
        print('{}/{} events without \'year of birth\' information.'.format(birth_year_is_null, df_length))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
             
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
                
        df_length = len(df)
        print('\nFor your information: There are {} rows in the raw data'.format(df_length))
        raw_data = input('\nDo you want to display some raw data? (y/n) ').lower()
        i=0
        while raw_data != 'n':
            if raw_data == 'y': 
                if i <= (df_length-5):
                    print(df[i:i+5].to_string())
                    i += 5
                    raw_data = input('\nDo you want to display more raw data? (y/n)').lower()
                elif i > (df_length-5) and i < df_length: 
                    print(df[i:df_length+1].to_string())
                    i = df_length
                elif i == df_length:
                    print('\nThat was it. There is no more raw data.')
                    break
            else: 
                raw_data = input('\nThat was no valid input. Please try again: Do you want to display some raw data? (y/n)').lower()
                               
        print('-'*40)    
        restart = input('\nWould you like to restart? y/n \n')
        if restart.lower() != 'y':
            break        
             

if __name__ == "__main__":
	main()
