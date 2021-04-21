import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_raw_data(city):
    """
        it aims to print the raw data about the city selected by the user upon request.
        Args:
            [ city ]variable that represents the city name to be used to print the necessary data.
        Returns:
            actually, it does not return any thing ;), XD, it prints the output instead on the console.
    """
    # this loads the pandas data frame about the city selected by the user.
    df = pd.read_csv(CITY_DATA[city])
    current_index = 0 # start point to continue printing from this point. In case of head raw data.
    next_index = None
    next_tail = 0     #  In case of tail raw data.
    current_tail = None
    _sec_case = False
    choice_user_1 = input('would you like to see raw data about {} | Enter y OR n? ->'.format(city)).lower()
    while True:
          choice_user_1 = input('would you like to see raw data about {} | Enter y OR n? ->'
                                    .format(city)).lower()
       
          if choice_user_1 == 'y' or choice_user_1 == 'yes':     
             choice_user_2 = input('would you like to see raw data from [ Head ] OR [ Tail ] | Enter h OR t?->').lower()                                         
             if choice_user_2 == 'h' or choice_user_2 == 'head':
                print('printing 5 records from raw data about {} from'.format(city), 'head\n')
                next_index = current_index + 5
                print(df[current_index:next_index])# 5 records.
                current_index = next_index
             
             elif choice_user_2 == 't' or choice_user_2 == 'tail':
                print('printing 5 records from raw data about {} from'.format(city), 'tail\n')
                current_tail = next_tail - 5
                if not _sec_case:
                   print(df.tail()) 
                else:   
                    print(df[current_tail : next_tail])# 5 records.
                next_tail = current_tail
                
             else:
                print('invalid choice.\n')
                continue
             _sec_case = True   
          
          else:
              if choice_user_1 == 'n' or 'no':
                 print('you selected {}.\n you do not want to see raw data about {}'.format(choice_user_1,                            city))  
                 break
            
              else:
                 print('invalid choice.\n select either yes[y] or no[n] only.')   
  
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\t\tHello! Let\'s explore some US bikeshare data!')
    
    # initially
    city, month, day = None, None, None  
    cities = ['chicago', 'washington', 'new york']
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days = ['all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nEnter a city:[ Chicago, Washington or New York ] OR Press e to exit: ').lower() # to ensure consistency of input.
    while True:
          if city == 'e': # it means that the user wants to exit the program.
             break
          elif city in cities:
               # to be consistent with the dictionary keys.
               if city == 'new york': 
                  city+=' city'     
               print('You selected to process data about: ', city + '\n')
               break 
          else:      
               city = input('\nInvalid City.\nEnter Only Chicago, Washigton, New York: ').lower()    
    
# -----------------------------End of city selection-----------------------------------------------#
    
    # continue the program logic only if the user wants to do so. otherwise, skip.
    if city != 'e':
        
       # TO DO: get user input for month (all, january, february, ... , june)
       month = input('\nWhich month to filter data with?: \nJanuary\nFebruary\nMarch\nApril\nMay\nJune Or\
                    \n[ all ] if not to filter data by month at all: ').lower()
                  
       while month not in months:
             month = input('\nInvalid month.\nEnter a month from January to .. June only or [ all ]\
                         \nto cancel filtering data by month:').lower()
       if month == 'all':
          print('You selected not to do any filtering for data by month.\n')
       else:
          print('You selected to filter data by: ', month + '\n')       
    
    # ----------------------------End of month selection------------------------------------------------#
    
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
       day = input('\nWhich day of the week to filter data with?:\nSaturday\nSunday\nMonday\nTuesday\
                  \nWednesday\nThursday\nFriday Or\n[ all ] if not to filter data by day at all: ').lower()
       while day not in days:
             day = input('\nInvalid week day.\nEnter a day from Saturday to .. Friday only or [ all ] to cancel\nfiltering data by day of the week: ').lower()
                      
       if day == 'all':
          print('You selected not to do any filtering for data by day.\n')
       else:
          print('You selected to filter data by: ', day + '\n\n') 
    
    # ------------------------End of day selection----------------------------------------------------# 
 
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
        df - Pandas DataFrame containing city data filtered by month and day if requested to do filtering.
    """
    # initially we index our global dictionary to load the correct .csv file to load needed data.
    
    df = pd.read_csv(CITY_DATA[city])
    
    # we convert the 'Start Time' column into type of date_time object to allow extracting the day.
    # re-assigning the start time column again in the data frame.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extracting the month number from the start time column by the dt(date_time) accessor
    # creating new column in the data frame df called Month.
    df['Month'] = df['Start Time'].dt.month
    # creating new column in the data frame df called Day_Week
    df['Day_Week'] = df['Start Time'].dt.weekday_name
    
    month_selected = None
    # the value of the month selected = the index of the item in the list as it's orderd in the same sequence.
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    if month != 'all':
       month_selected = months.index(month) + 1 
       # filter the data frame df by month selected then re-assigning it again.
       df = df[df['Month'] == month_selected]
    if day != 'all':
       # filter the data frame df by day of week selected then re-assigning it again.
       #print(day) 
       df = df[df['Day_Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
       Args: df pandas dataframe object obtained after filtering data based on the user request.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mode_month = df['Month'].mode()[0]
    print('The most common month: ', mode_month, '\n')


    # TO DO: display the most common day of week
    mode_day_week = df['Day_Week'].mode()[0]
    print('The most common day of week: ', mode_day_week, '\n')


    # TO DO: display the most common start hour
    df['Start_Hour'] = df['Start Time'].dt.hour
    mode_start_hour = df['Start_Hour'].mode()[0]
    
    print('The most common start hour: ', mode_start_hour, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
      Args: df pandas dataframe object obtained after filtering data based on the user request.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mode_start_station = df['Start Station'].mode()[0]
    print('The most common start station: ', mode_start_station, '\n')

    # TO DO: display most commonly used end station
    mode_end_station = df['End Station'].mode()[0]
    print('The most common end station: ', mode_end_station, '\n')
    # TO DO: display most frequent combination of start station and end station trip
    
    # concatenating the two data frame columns together to get a combined version of the two stations.
    df['Combined_Stations'] = df['Start Station'].str.cat(df['End Station'], sep = ' || ')  
    mode_combined_stations = df['Combined_Stations'].mode()[0]
    print('The most common combined stations[ start || end ]: ', mode_combined_stations, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
      Args: df pandas dataframe object obtained after filtering data based on the user request.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # 1hr = 60Min,, 1Min = 60Sec,, 
    total_time_sec = round(df['Trip Duration'].sum(), 2)
    total_time_min = total_time_sec / 60
    total_time_hr =  total_time_min / 60 
    print('total time of travel:')
    print('\nin hours unit: {} \nin minutes unit: {} \nin seconds unit: {}'.format(total_time_hr,
           total_time_min, total_time_sec))                                                
          
    print('\n')
    # TO DO: display mean travel time
    mean_time_sec = round(df['Trip Duration'].mean(), 2)
    mean_time_min = mean_time_sec / 60
    mean_time_hr =  mean_time_min / 60 
    
    print('mean time of travel:\
          \nin hours unit: {} \nin minutes unit: {} \nin seconds unit: {}'.format(mean_time_hr,
          mean_time_min, mean_time_sec))     

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    
      Args: df pandas dataframe object obtained after filtering data based on the user request.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # here we extract the column of the user type as a pandas.series
    # .index[each_type] gives an access to the index labels in the series.
    # .values[each_type] gives an access to the values of each label in the series.
    user_count = df['User Type'].value_counts()
    
    print('Available User Types and their counts: \n')
    for each_type in range(len(user_count)):
        print(user_count.index[each_type], ':', user_count.values[each_type])
    
    try:
       # TO DO: Display counts of gender and birth year data in case only of Chicago and New York City.
       user_gender = df['Gender'].value_counts()
       print('\nUser Gender and their counts: \n')
       for each_gender in range(len(user_gender)):
           print(user_gender.index[each_gender], ':', user_gender.values[each_gender])
       print('\n')
       
       # TO DO: Display earliest, most recent, and most common year of birth
       # in order to sort based on the birth year, I used the group by() function for ordering.
       # ascendingly ordered.  i.e from earliest --> to most recent birth years.
       birth_years = df.groupby('Birth Year')['Start_Hour'].count()
        
       print('the earliest birth year: ', birth_years.index[0], '\n')
       print('the most recent birth year: ', birth_years.index[len(birth_years) - 1], '\n')
       print('the most common birth year: ', df['Birth Year'].mode()[0])
       print("\nThis took %s seconds." % (time.time() - start_time))
       print('-'*40)
    except KeyError as e: # unavailable key Gender and Birth Year within washington .csv file
       print('\n{} and Birth Year Data are unavailable for washington !'.format(e)) 


def main():
    while True:
        city, month, day = get_filters()
        if city =='e':
            print('Program is exiting ...')
            break # no need for else as it will go away from the while loop over all.
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
           break

    print('\nHope to see you again ;).. \nThanks for your time :)')

if __name__ == "__main__":
	main()
