import time
import pandas as pd
import numpy as np

# Dictionary contains city and its corresponding csv file name
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}
# Dictionary to map day names to their integer values
day_mapping = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}
RESPONSE_LIST = ['yes', 'no']

# Function to get user input for the city
def get_city():
    while True:
        city = input("Enter the name of the city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            return CITY_DATA[city]
        else:
            print("Invalid input. Please re-enter a valid city.")

# Function to get user input for the month
def get_month():
    while True:
        month = input("Enter the name of the month (January, February, ... June) or 'all' for no filter: ").strip().lower()
        if month in ["all", "january", "february", "march", "april", "may", "june"]:
            return month
        else:
            print("Invalid input. Please re-enter a valid month or 'all'.")

# Function to get user input for the day of the week
def get_day():
    while True:
        day = input("Enter the day of the week (Monday, Tuesday, ... Sunday) or 'all' for no filter: ").strip().lower()
        if day in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            return day
        else:
            print("Invalid input. Please re-enter a valid day or 'all' for no filter.")

# Function to load data from CSV file based on user input
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
    try:
        df = pd.read_csv(city)
    except FileNotFoundError:
        print(f"Error: The data file for {city} was not found.")
        return None

    # Extract month and day of the week from 'Start Time'
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Apply filters based on user input for month and day
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    print("Filtering by: ")
    print('City: ',city)
    print('Month: ',month)
    print('Day: ',day)
    print("\nLoading data...")
    print("-" * 40)
    return df

# Function to calculate and display time-related statistics
def time_stats(df):
    """Displays statistics on the most frequent times of travel.
       Args: df : the data frame
       Returns: Nothing
       """
       
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # computing the most common month, day, start time
    most_common_month = df['Month'].mode()[0]
    most_common_day = df['Day of Week'].mode()[0]
    most_common_hour = df['Start Time'].dt.hour.mode()[0]

    #Most common month using pandas mode() method
    print(f'Most common month: {most_common_month}')
    #Most common day using pandas mode() method
    print(f'Most common day: {most_common_day}')
    #Most common start Hour using pandas mode() method
    print(f'Most common start hour: {most_common_hour}h')

    print(f"\nThis took {time.time() - start_time:.3f} seconds.")
    print('-' * 40)

# Function to calculate and display station-related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip.
       Args: df : the data frame
       Returns: Nothing
       """
       
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # computing the most popular start & end station and combination of both using mode() method
    most_popular_start_station = df['Start Station'].mode()[0]
    most_popular_end_station = df['End Station'].mode()[0]
    most_popular_combination = (df['Start Station'] + " --> " + df['End Station']).mode()[0]

    print(f'Most commonly used start station: {most_popular_start_station}')
    print(f'Most commonly used end station: {most_popular_end_station}')
    print(f'Most frequent combination of start station and end station trip: {most_popular_combination}')

    print(f"\nThis took {time.time() - start_time:.3f} seconds.")
    print('-' * 40)

# Function to calculate and display trip duration statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
       Args: df : the data frame
       Returns: Nothing
       """
       
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # computing total, average, longest and shortest travel time using 
    total_travel_time_seconds = df['Trip Duration'].sum()
    total_travel_time = format_duration(total_travel_time_seconds)
    
    mean_travel_time_seconds = df['Trip Duration'].mean()
    mean_travel_time = format_duration(mean_travel_time_seconds)
    
    max_travel_time_seconds = df['Trip Duration'].max()
    max_travel_time = format_duration(max_travel_time_seconds)
    
    min_travel_time_seconds = df['Trip Duration'].min()
    min_travel_time = format_duration(min_travel_time_seconds)

    print(f'Total travel time: {total_travel_time}')
    print(f'Average travel time: {mean_travel_time}')
    print(f'Longest travel time: {max_travel_time}')
    print(f'Shortest travel time: {min_travel_time}')

    print(f"\nThis took {time.time() - start_time:.3f} seconds.")
    print('-' * 40)

# Function to format seconds into days, hours, minutes, and seconds
def format_duration(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


# Function to calculate and display user-related statistics
def user_stats(df):
    """Displays statistics on bikeshare users.
       Args: df : the data frame
       Returns: Nothing
       """
       
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df:
        user_types = df['User Type'].value_counts() # count of user types using value_counts() method
        print('\nCounts of user types:\n', user_types)
    else:
        print('\nUser Type information not available in the dataset.')

    if 'Gender' in df:
        genders = df['Gender'].value_counts() # count of user gender using value_counts() method
        print('\nCounts of gender:\n', genders)
    else:
        print('\nThis information is not available in the database.')

    if 'Birth Year' in df:
        oldest_birth_year = int(df['Birth Year'].min()) # age of oldest customer using min()
        youngest_birth_year = int(df['Birth Year'].max()) # age of youngest customer using max()
        most_common_birth_year = int(df['Birth Year'].mode()[0]) # most common birth year using mode()

        print(f'\nOldest Customer birth year: {oldest_birth_year}')
        print(f'Youngest Customer birth year: {youngest_birth_year}')
        print(f'Most common Customer birth year: {most_common_birth_year}')
    else:
        print('\nThis information is not available in the database.')

    print(f"\nThis took {time.time() - start_time:.3f} seconds.")
    print('-' * 40)

# Function to display raw data to the user upon request
def display_raw_data(df):
    """Show 5 records from the selected city.
    Asks user to type if he wants to show raw data or not

    Args:
        (df): the data frame of the selected city.
    Returns:
        Nothing.
    """
    i = 0
    while True:
        show_data = input('\nDo you want to see 5 lines of raw data? Enter "yes" or "no": ').strip().lower()
        if show_data not in RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")
            continue
        
        if show_data == 'yes':
            print(df.iloc[i:i+5]) # displaying 5 rows of raw data with df.iloc method
            i += 5
        
        elif show_data == 'no':
            break

# Main function to control the flow of the program
def main():

    while True:
        city_file = get_city()
        month = get_month()
        day = get_day()

        df = load_data(city_file, month, day)
        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

        restart = input('\nChoose "yes" to continue or "no" to exit: ').strip().lower()
        while restart not in RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")
            restart = input('\nChoose "yes" to continue or "no" to exit: ').strip().lower()

        if restart != 'yes':
            print('-' * 40)
            print("See you later!")
            break

if __name__ == "__main__":
    main()
