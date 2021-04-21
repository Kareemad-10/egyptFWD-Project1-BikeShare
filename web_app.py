import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time

caption_str = 'Divvy is a bicycle sharing system in the City of Chicago and two adjacent suburbs'

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def render_main(): # to show the main screen of the application.
    st.write('# Explore US Bikeshare Application')
    st.subheader('For basic data analysis tasks')
    image = Image.open('divvy.jpg')
    st.image(image, caption=caption_str,
                use_column_width=True)
    

def get_city_input(): # a function for basic sidebar input data by user.
    st.sidebar.title('User Inputs: ')
    st.sidebar.write('Which city to show data about?')
    city_selected = st.sidebar.selectbox('', ("none", "Chicago", "New York City", "Washington")) 
    if city_selected == 'none':
       st.write('### Please, select a city from the list.')
    else:
       st.write('### You selected to show data about: ', city_selected)
       
    return city_selected    
   
def render_data_filter_input(city):
    cities = ['chicago', 'washington', 'new york']
    months = ['..','all','january', 'february', 'march', 'april', 'may', 'june']
    days = ['..','all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    st.sidebar.write('### Filter data by month: ')
    month = st.sidebar.selectbox('', months)
    st.sidebar.write('### Filter data by day: ')
    day = st.sidebar.selectbox('', days)
    st.write('### Select the type of data filtering if required from the list.\n **all** means to include all *months* or *days* data in the analysis\n ... ')
    if month == 'all':
       st.write('### You selected to include ALL months.\n')
    elif month != '..':
       st.write('### You selected to do filtering by: ', '**' ,month, '**' ,'\n')
       
    if day == 'all':
       st.write('### You selected to include ALL days.\n')
    elif day != '..':
       st.write('### You selected to do filtering by: ', '**' ,day, '**' ,'\n')
           
    if month != '..' and day != '..':
       time.sleep(1) 
       st.write('\n ***Computing..***')
       time.sleep(1) 
       return month, day
    else:
       return 0, 0 # in case the user didn't select any choice.
     
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    
    # we convert the 'Start Time' column into type of date_time object to allow extracting the day.
    # re-assigning the start time column again in the data frame.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extracting the month number from the start time column by the dt(date_time) accessor
    # creating new column in the data frame df called Month.
    df['Month'] = df['Start Time'].dt.month
    # creating new column in the data frame df called Day_Week
    df['Day_Week'] = df['Start Time'].dt.day_name()
    
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
    st.write('\n '+ '-'*40)
    data = [] 
    st.write('\nCalculating **The Most Frequent Times of Travel** ...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mode_month = df['Month'].mode()[0]
    data.append(mode_month)
    print('The most common month: ', mode_month, '\n')


    # TO DO: display the most common day of week
    mode_day_week = df['Day_Week'].mode()[0]
    data.append(mode_day_week)
    print('The most common day of week: ', mode_day_week, '\n')


    # TO DO: display the most common start hour
    df['Start_Hour'] = df['Start Time'].dt.hour
    mode_start_hour = df['Start_Hour'].mode()[0]
    data.append(mode_start_hour)
    
    print('The most common start hour: ', mode_start_hour, '\n')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    pd_ser_dict = {'Statistics Computed:': pd.Series(data, ['The most common month:', 'The most common day of week', 'The most common start hour:'])}
    pd_df = pd.DataFrame(pd_ser_dict)
    st.table(pd_df)

def station_stats(df):
    data = []
    st.write('\nCalculating **The Most Popular Stations and Trip**...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mode_start_station = df['Start Station'].mode()[0]
    data.append(mode_start_station)
    print('The most common start station: ', mode_start_station, '\n')

    # TO DO: display most commonly used end station
    mode_end_station = df['End Station'].mode()[0]
    data.append(mode_end_station)
    print('The most common end station: ', mode_end_station, '\n')
    # TO DO: display most frequent combination of start station and end station trip
    
    # concatenating the two data frame columns together to get a combined version of the two stations.
    df['Combined_Stations'] = df['Start Station'].str.cat(df['End Station'], sep = '|')  
    mode_combined_stations = df['Combined_Stations'].mode()[0]
    data.append(mode_combined_stations)
    print('The most common combined stations[ start || end ]: ', mode_combined_stations, '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    pd_ser_dict = {'Statistics Computed:': pd.Series(data, ['The most common start station:', 'The most common end station:', 'The most common combined stations start|end:'])}
    pd_df = pd.DataFrame(pd_ser_dict)
    st.table(pd_df)

def trip_duration_stats(df):
    data = []
    st.write('\nCalculating **Trip Duration**...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # 1hr = 60Min,, 1Min = 60Sec,, 
    total_time_sec = round(df['Trip Duration'].sum(), 2)
    total_time_min = total_time_sec / 60
    total_time_hr =  total_time_min / 60 
    print('total time of travel:')
    
    data.append(total_time_sec)
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
             
    data.append(mean_time_sec)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    pd_ser_dict = {'Statistics Computed:': pd.Series(data, ['The total time of travel in seconds:', 'The mean time of travel in seconds:'])}
    pd_df = pd.DataFrame(pd_ser_dict)
    st.table(pd_df)

def user_stats(df):
    data = []
    st.write('\nCalculating **User Stats**...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # here we extract the column of the user type as a pandas.series
    # .index[each_type] gives an access to the index labels in the series.
    # .values[each_type] gives an access to the values of each label in the series.
    user_count = df['User Type'].value_counts()
    
    print('Available User Types and their counts: \n')
    for each_type in range(len(user_count)):
        print(user_count.index[each_type], ':', user_count.values[each_type])
    pd_ser_dict = {'No. of each user type:': user_count}
    pd_df = pd.DataFrame(pd_ser_dict)
    st.table(pd_df)

    try:
       # TO DO: Display counts of gender and birth year data in case only of Chicago and New York City.
       user_gender = df['Gender'].value_counts()
       print('\nUser Gender and their counts: \n')
       for each_gender in range(len(user_gender)):
           print(user_gender.index[each_gender], ':', user_gender.values[each_gender])
       st.write('\n\n')
       pd_ser_dict = {'Gender Counts:': user_gender}
       pd_df = pd.DataFrame(pd_ser_dict)
       st.table(pd_df)
       # TO DO: Display earliest, most recent, and most common year of birth
       # in order to sort based on the birth year, I used the group by() function for ordering.
       # ascendingly ordered.  i.e from earliest --> to most recent birth years.
       birth_years = df.groupby('Birth Year')['Start_Hour'].count()
        
       print('the earliest birth year: ', birth_years.index[0], '\n')
       data.append(birth_years.index[0])
       print('the most recent birth year: ', birth_years.index[len(birth_years) - 1], '\n')
       data.append(birth_years.index[len(birth_years) - 1])
       print('the most common birth year: ', df['Birth Year'].mode()[0])
       data.append(df['Birth Year'].mode()[0])
       print("\nThis took %s seconds." % (time.time() - start_time))
       print('-'*40)
       pd_ser_dict = {'Statistics Computed:': pd.Series(data, ['The earliest birth year:','The most recent birth year: ','The most common birth year: '])}
       pd_df = pd.DataFrame(pd_ser_dict)
       st.table(pd_df)
    except KeyError as e: # unavailable key Gender and Birth Year within washington .csv file
       st.write('\n**{}** and **Birth Year** raw data are unavailable for *washington* !'.format(e)) 


def render_raw_data(city_selected):
     df = pd.read_csv(CITY_DATA[city])
     st.write('### Do you want to print a sample of raw data about {} ***Without Any Filter***?'.format(str(city_selected)))
     choice_raw_data = st.radio('',('No', 'Yes'))
     if choice_raw_data == 'Yes':
        st.write('### Do you want to see raw data from head OR tail?') 
        choice_head_tail = st.radio('',('Head', 'Tail')) 
        st.write('### select a number of records to be printed: ')
        no_records = st.slider('', 1, 50, 5) # assume we can print 1 till 50 records of the raw data.
        if choice_head_tail == 'Head':
           st.dataframe(df.head(no_records))
        else:
           st.dataframe(df.tail(no_records))     
           
       

 #---------------------Main Section-------------------------------   

render_main()
city = get_city_input()
if city != 'none':
   month, day = render_data_filter_input(city)
   #----------------------------------------------
   if month != 0 and day != 0:
      df = load_data(city, month, day)
      time_stats(df)
      station_stats(df)
      trip_duration_stats(df)
      user_stats(df) 
      render_raw_data(city)
      
      
      