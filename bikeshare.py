import time
import pandas as pd
from tabulate import tabulate # Pretty-print tabular data in Python, a library and a command-line utility.
#import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city and time filter to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    i = 0 # variable to limit number of wrong data entry if user is not serious
    city = "" # name of the city to analyze
    month = "" # name of the month to filter by, or "all" to apply no month filter
    day = "" # name of the day of week to filter by, or "all" to apply no day filter
    city_dict = {'chic.':'chicago', 'ny':'new york', 'wa':'washington' }
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Whould you like to see data from Chicago, Washington or New York?")
    while (city not in city_dict.keys()) and (city not in city_dict.values()):
        # To have a case agnost input, convert the input to lower case regardless of the casing input by user
        city = input("Enter city name exactly as above. If you are lazy enter the abbr. as Chic., NY, WA respectively.\n").lower()
        i += 1
        # limit the number of wrong data entry to 10 and warrning in between
        if i == 5:
            print("Are you serious? Please enter city name correctly")
        elif i == 10:
            print("Man up!! YOU ARE NOT SERIOUS..If you still interested, you have to restart")
            break
    #Check point when the user exceed the number of data entry limit.
    if city not in city_dict.values():
        try: 
            city = city_dict[city]
        except KeyError: 
            city = ""

    # get user input to which time filter he wants to apply on data
    filter_list = ['month', 'day', 'both', 'none']  # a list of all time filter options that can be selected by user
    user_filter = "" # a str get user choice for the time filter
    i = 0
    while (user_filter not in filter_list) and (city != ""): #don't continue as long as no vaild city entered from user
        # To have a case agnost input, convert the input to lower case regardless of the casing input by user
        user_filter = input('Whould you like to filter the data by month, day, both or not at all? Type "none" for no time filter\n').lower()
        i += 1
        # limit the number of wrong data entry to 10 and warrning in between
        if i == 5:
            print("Are you serious? Please enter the filter correctly")
        elif i == 10:
            print("Man up!! YOU ARE NOT SERIOUS..If you still interested, you have to restart")
            break
    if user_filter == "none":
        month = "all"
        day = "all"
    elif user_filter == "month":
        month = get_month_filter()
        day = "all"
    elif user_filter == "day":
        month = "all"
        day = get_day_filter()
    elif user_filter == "both":
        month = get_month_filter()
        if month != "": #Check point when the user exceed the number of data entry limit.
            day = get_day_filter()
     
    
    print('-'*40)
    return city, month, day

def get_month_filter():
    """
    Asks user to specify a month to analyze.
    Returns:
        (str) user_filter - name of the month to filter by
    """
    # get user input for month (january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june'] # A lit of months to be selected for filtering
    i = 0 # variable to limit number of wrong data entry if user is not serious
    user_filter = "" # a str get user choice for month filter
    while user_filter not in months:
        # To have a case agnost input, convert the input to lower case regardless of the casing input by user
        user_filter = input("Which month? January, February, March, April, May, or June?\n").lower()
        i += 1
        # limit the number of wrong data entry to 10 and warrning in between
        if i == 5:
            print("Are you serious? Please enter the month correctly")
        elif i == 10:
            print("Man up!! YOU ARE NOT SERIOUS..If you still interested, you have to restart")
            user_filter = ""
            break
    return user_filter.lower()

def get_day_filter():
    """
    Asks user to specify a day of week to analyze.
    Returns:
        (str) user_filter - name of the day to filter by
    """
    # get user input for day of week (monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] # A lit of days to be selected for filtering
    i = 0 # variable to limit number of wrong data entry if user is not serious
    user_filter = "" # a str get user choice for day filter
    while user_filter not in days:
        # To have a case agnost input, convert the input to lower case regardless of the casing input by user
        user_filter = input("Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday?\n").lower()
        i += 1
        # limit the number of wrong data entry to 10 and warrning in between
        if i == 5:
            print("Are you serious? Please enter the day correctly")
        elif i == 10:
            print("Man up!! YOU ARE NOT SERIOUS..If you still interested, you have to restart")
            user_filter = ""
            break
    return user_filter.lower()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time & End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]
    # extract hour from the Start Time column to create an hour column 
    df['hour'] = df['Start Time'].dt.hour
    
    # Create a trip column from start station to end station
    df['trip'] = df['Start Station'] + "_" + df['End Station']
    
    
    return df


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.
   
    Args:
        (Pandas DataFrame) df - Data set the function will apply the stats on
        (str) month - name of the month the user used as filter or 'all'
        (str) day - name of the day the user used as filter or 'all'    
    """

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()
    print('_'*60, '\n')
    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("The most common month is:\n{}".format(months[popular_month-1].title()))
    # If the user filtered on month, print notification that common month stats is irrelevant
    if month != 'all':
        print("You filtered on that month so above stat is irrelevant")
    print('*'*60)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print("The most common day is:\n{}".format(days[popular_day].title()))
    # If the user filtered on day, print notification that common month stats is irrelevant
    if day != 'all':
        print("You filtered on that day so above stat is irrelevant")    
    print('*'*60)
    # display the most common start hour
    
    popular_hour = df['hour'].mode()[0]
    print("The most common hour of the day is:\n", popular_hour )
    print('*'*60)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (Pandas DataFrame) df - Data set the function will apply the stats on
    
    """

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()
    print('_'*60, '\n')
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popluar start station is:\n    ", popular_start_station.title())
    print('*'*60)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popluar end station is:\n    ", popular_end_station.title())
    print('*'*60)
    # display most frequent combination of start station and end station trip
    popular_trip = df['trip'].mode()[0]
    popular_trip_st_a = popular_trip.split("_")[0]
    popular_trip_st_b = popular_trip.split("_")[1]    
    print("The most popular trip is:")
    print("    Start Station:", popular_trip_st_a)
    print("    End Station:", popular_trip_st_b)
    print('*'*60)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (Pandas DataFrame) df - Data set the function will apply the stats on
    
    """

    print('\nCalculating Trip Duration...')
    start_time = time.time()
    print('_'*60, '\n')
    # Calculate trip time from start & end time columns and create a trip_time column
    df['trip_time'] = df['End Time'] - df['Start Time']
    
    # display total travel time calculated
    total_travel_time_calc = df['trip_time'].sum()
    print("The total traveling time done for 2017 through June (calculated):\n", total_travel_time_calc)
    print('*'*60)

    # display mean travel time calculated
    average_travel_time_calc = df['trip_time'].mean()
    print("The average time spent for each trip (calculated):\n", average_travel_time_calc)
    print('*'*60)
    
    # display total travel time from Trip Duration column
    total_travel_time = df['Trip Duration'].sum()
    print("The total traveling time done for 2017 through June (Dataset):\n", total_travel_time)
    print('*'*60)
    
    # display total travel time from Trip Duration column
    average_travel_time = df['Trip Duration'].mean()
    print("The average time spent for each trip (Dataset):\n", average_travel_time)
    print('*'*60) 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (Pandas DataFrame) df - Data set the function will apply the stats on
    
    """

    print('\nCalculating User Stats...')
    start_time = time.time()
    print('_'*60, '\n')
    # Display counts of user types
    # This has been excluded for longer execution time
    # user_types = df.groupby(['User Type'])['User Type'].count()
    user_types = df['User Type'].value_counts()
    print("The counts of user types are:")
    
    #use reset_index & to_string to suppress Name & dtype from the output
    print((user_types.reset_index()).to_string(header=None, index=None))
    print('*'*60)
    
    # Use try-except clause to skip Gender/Birth year stats in case of Washington
    try:
        # Display counts of gender
        user_gender = df['Gender'].value_counts()
        print("The counts of each gender are:")
        #use reset_index & to_string to suppress Name & dtype from the output
        print((user_gender.reset_index()).to_string(header=None, index=None))
        print('*'*60)
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("The earlies Birth Year is:", earliest_birth_year)
        print('#'*40)
        print("The most recent Birth Year is:", most_recent_birth_year)
        print('#'*40)
        print("The most common Birth Year is:", most_common_birth_year)
        print('*'*60)
    except KeyError:
        print('No gender/year of birth data to share for Washington')
        print('*'*60)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        #Check point when the user exceed the number of data entry limit, he need to restart if he still interested
        try:
            df = load_data(city, month, day)
        except KeyError:
            break
        except ValueError:
            break
        # Check which stats the user is interested in and display stats one by one upon his needs
        if input("'\nWould you like to see time stats? Enter yes or press any key if no.\n").lower() == 'yes':         
            time_stats(df, month, day)
        if input("'\nWould you like to see station stats? Enter yes or press any key if no.\n").lower() == 'yes':
            station_stats(df)
        if input("'\nWould you like to see trip stats? Enter yes or press any key if no.\n").lower() == 'yes':
            trip_duration_stats(df)
        if input("'\nWould you like to see user stats? Enter yes or press any key if no.\n").lower() == 'yes': 
            user_stats(df)
   
        # cleaning up Data Frame by deleting all added columns and keep the original ones to be displayed to user upon request
        df.drop(columns = ['month', 'day_of_week', 'hour', 'trip', 'trip_time'], errors = 'ignore', inplace = True)
                
        # Displaying individual trips in groups of 5 rows untill the user says no

        print("We came to the end of stats show. We hope you liked it!")
        display_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or press any key if no\n').lower()
        pointer_loc = 0 # A variable used as a pointer to the row/s need to be diplayed 
        while display_data == 'yes':
            pd.set_option("display.max_columns", None) # the maximum number of columns to display to unlimited. (Hint. this can be used for rows as well)
            print(tabulate(df.iloc[pointer_loc : pointer_loc + 5], headers='keys', tablefmt='pretty', showindex = False)) # use tabulate to diplay rows in a pretty table
            display_data = input('\nWould you like to continue? Enter yes or press any key if no\n').lower()
            pointer_loc += 5
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
