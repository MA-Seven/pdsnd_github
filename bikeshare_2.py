#import the needed libraries/packages
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # months and days short names are included
    months = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'jun','all']
    days = ['Monday','Mon' ,'Tuesday','Tue' ,'Wednesday','Wed' ,'Thursday','Thu' ,'Friday','Fri' ,'Sunday','Sun' ,'All']

    print('\n\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    i = True
    city = input('\nPlease enter the city (full name or 1st letter) you would like to analys, the options are:\n\nChicago (C), New york city (N), Washington (W).. ').lower()
    while i == True:
        if city in CITY_DATA.keys():
            i = False
        else:
            city = input('\nNOT correct value\nPlease enter one of the following options: Chicago (C), New york city (N), Washington (W).. ').lower()

    # get user input for month (all, january, february, ... , june)
    i = True
    month = input('\nPlease enter the month you would like to see or type all to show all the data.. ').lower()
    while i == True:
        if month in months:
            i = False
        else:
            month = input('\nNOT correct value\nPlease enter the CORRECT name such as January or Jan, otherwise type all to show all the data.. ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    i = True
    day = input('\nPlease enter the day you would like to see or type all to show all the data.. ').title()
    while i == True:
        if day in days:
            i = False
#         elif 0 <= int(day) <= 7:
#             i = False
        else:
            day = input('\nNOT correct value\nPlease enter the CORRECT name such as Monday or Mon, otherwise type all to show all the data.. ').title()

    xx = 7
    print('\n','-*'*xx,'- Based on your choises of filters, see below stats -','*-'*xx,'\n')
#     print('-'*40)
    return city, month, day


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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

        # depending on your Pandas version, new = keep the 1st line, old > commint 1st line and uncomment 2nd line:
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            month = months.index(month)+1
        else:
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
            month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Sunday']
        if day in days:
            # filter by day of week to create the new dataframe
            df = df.loc[df['day_of_week'] == day]
        else:
            adjust = ['Mon','Tue','Wed','Thu','Fri','Sun']
            for i, j in enumerate(adjust):
                if j == day:
                    day = days[i]
            df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    com_month = df['Start Time'].dt.month_name().mode()[0]
#     xadfe = pd.Series()
#     xadfe['dd'] = df['Start Time'].dt.month_name()
#     com_month = xadfe['dd'].mode()[0]

    # display the most common day of week
    com_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    com_hour = df['Start Time'].dt.hour.mode()[0]

    print('\n    Month is:  {}\n    Day is:  {}\n    Hour is:  {}'.format(com_month,com_day,com_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    com_ss = df['Start Station'].mode()[0]

    # display most commonly used end station
    com_es = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Path'] = df['Start Station']+'  _  '+df['End Station']
    com_path = df['Path'].mode()[0]

    print('\n    Start Station is:  {}\n    End Station is:  {}\n    Trip is:  {}'.format(com_ss,com_es,com_path))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    tota_t = np.sum(df['Trip Duration'])/60

    # display mean travel time
    mean_t = np.mean(df['Trip Duration'])/60

    print('\n    The Total Travel Time is:  {} min\n    The Average Travel Tiem is:  {} min'.format(tota_t,mean_t))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type:\n')
    i = 0
    user_type = df['User Type'].value_counts()
    while i < (user_type.size):
        print('    {}: {}'.format(user_type.index[i],user_type[i]))
        i += 1

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df.dropna()['Gender'].value_counts()
        print('\nGender:\n')
        i = 0
        while i < (gender.size):
            print('    {}: {}'.format(gender.index[i],gender[i]))
            i += 1

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        ear_year = int(df['Birth Year'].min())
        com_year = int(df['Birth Year'].mode())
        las_year = int(df['Birth Year'].max())
        print('\nThe Year of Birth analysis are as folow:\n')
        print('    The earliest is:  {}\n    The most recent is:  {}\n    And the most common is:  {}'.format(ear_year,las_year,com_year))
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

        complete_data = input('\nWould you like to see the 1st 5 rows of data? Enter yes or no.. ')
        i = 0
        while i < df.shape[0]:
            if complete_data.lower() == 'yes' or complete_data.lower() == 'y':
                print(df[i:i+5])
                complete_data = input('\nWould you like to see the next 5 rows of data? Enter yes or no.. ')
                i += 5
            else:
                i = df.shape[0]

        restart = input('\nWould you like to restart? Enter yes or no.. ')
        if restart.lower() == 'yes' or restart.lower() == 'y':
            continue
        else:
            break


if __name__ == "__main__":
	main()
