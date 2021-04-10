import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './BikeShare_Project/chicago.csv',
              'new york': './BikeShare_Project/new_york_city.csv',
              'washington': './BikeShare_Project/washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    
    # Asks user to specify a city, month, and day to analyze.

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input('Which city would you like to analyze, Chicago, New York or Washington?: ').lower()
        if city in CITY_DATA: 
            break
        else:
            print('Please choose from the following cities:\nChicago\nNew York\nWashington')

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Please enter the month you would like to analyze between January and June! If all, enter 'all': ").lower()
        if (month in months) or (month == 'all'):
            break
        else:
            print('Please enter a month from the following list or enter \'all\': ')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("Please enter the day of the week you would like to analyze! If all, enter 'all': ").lower()
        if (day in days) or (day == 'all'):
            break
        else:
            print('Please enter a valid day of the week or enter \'all\': ') 

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    
    # Loads data for the specified city and filters by month and day if applicable.
    # Returns: df - Pandas DataFrame containing city data filtered by month and day
    
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day and create new columns
    # range limit for dt.month = 1 to 12
    df['month'] = df['Start Time'].dt.month 
    # range limit for dt.day_of_week = 0 to 6
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    # range limit for dt.hour = 0 to 23
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # Since the month parameter is given as the name of the month we'll need to 
        # first convert this to the corresponding month number by adding one to the index
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    elif day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df, month, day):
    # Displays statistics on the most frequent times of travel.

    print('\nCalculating The Most Frequent Times of Travel...\n')
    try:
    # display the most common month
        if month == 'all':
            month_ = df['month'].mode()[0]
            # - 1 used in the following line as we have corresponding month number
            # but require the index number of months list to display the proper month name
            popular_month = months[month_ - 1].capitalize()
            print('Most Frequent Start Month:', popular_month, '\n')

    # display the most common day of week
        if day == 'all':
            day_ = df['day_of_week'].mode()[0]
            popular_day = days[day_].capitalize() 
            print('Most Frequent Start Day of Week:', popular_day, '\n')

    # display the most common start hour
        popular_hour = df['hour'].mode()[0] 
        print('Most Frequent Start Hour in military time:', popular_hour, '\n')
    except Exception as e:
        print('Couldn\'t calculate the most frequent times of travel, as the following error occurred: {}'.format(e))
    print('-'*40)


def station_stats(df):
    # Displays statistics on the most popular stations and trip.

    print('\nCalculating The Most Popular Stations and Trip...\n')
    try:
        # display most commonly used start station
        print('Most Common Start Station:', df['Start Station'].mode()[0], '\n')
     
        # display most commonly used end station
        print('Most Common End Station:', df['End Station'].mode()[0], '\n')

        # display most frequent combination of start station and end station trip
        df['combination'] = df['Start Station'] + " and " + df['End Station'] 
        print('Most Frequent Start and End Stations:', df['combination'].mode()[0], '\n')
    except Exception as e:
        print('Couldn\'t calculate the most popular station, as the following Error occurred: {}'.format(e))

    print('-'*40)


def trip_duration_stats(df):
    # Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    try:
        print('The Total Travel Time is:', int(df['Trip Duration'].sum()/86400), 'days \n')
    except Exception as e:
        print('Couldn\'t calculate the total travel time, as the following Error occurred: {}'.format(e))
    
    # display mean travel time
    try:
        print('The Average Travel Time is:', int(df['Trip Duration'].mean())/60, 'minutes \n')
    except Exception as e:
        print('Couldn\'t calculate the average travel time, as the following Error occurred: {}'.format(e))
    
    print('-'*40)


def user_stats(df):
    # Displays statistics on bikeshare users.

    print('\nCalculating User Stats...\n')
    df.dropna(axis = 0, inplace = True)

    # Display counts of user types
    try:
        user_type_counts = df['User Type'].value_counts()
        print(user_type_counts, "\n")
    except Exception as e:
        print('Couldn\'t print user types, as the following Error occurred: {}'.format(e))

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    except:
        print('There are no gender details in this file.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode())
        print('\nThe Earliest Year of Birth is:', earliest_year, "\n")
        print('The Most Recent Year of Birth is:', most_recent_year, "\n")
        print('The Most Common Year of Birth is:', most_common_year, "\n")
    except:
        print("There are no birth year details in this file.")

    print('-'*40)


def display_data(city):

    # loading the chosen city dataframe to have the unmanipulated version of the data
    df = pd.read_csv(CITY_DATA[city])
    
    # while loop requesting to display raw data and displaying
    # the  next 5 rows of raw data everytime 'yes' is inputted
    raw_data = input('Would you like to display 100 lines of raw data? Enter yes or no.\n')
    x = 0
    y = 100
    while True:
        if raw_data.lower() != 'yes':
            break
        else:
            print(df[x:y]) 
            raw_data = input('\nWould you like to display the next 100 lines of raw data? Enter yes or no.\n')
            x += 100
            y += 100



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
