import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
month_index = {1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june"}
day_index = {"saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = str(input("would you like to see data from chicago, new york city, or washington? ")).lower()
    while city not in CITY_DATA.keys():
        print("Invalid inputs!. please type one of (chicago, new york city or washington).")
        city = str(input()).lower()

    filter_by_user = str(input("would you like to filter data by (month, day, both, or not at all(none))?")).lower()
    while filter_by_user not in {"month", "day", "both", "none"}:
        print("Invalid input!. please type one of(month, day, both, none).")
        filter_by_user = str(input()).lower()

    # get user input for month (all, january, february, ... , june)

    month = "all"
    day = "all"

    if filter_by_user in {"month", "both"}:
        month = str(input("which month (January,february,march,april,may or june?) ")).lower()
        while month not in month_index.values():
            print("Invalid inputs !. please type one of (january, february, march, april, may, june).")
            month = str(input()).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    if filter_by_user in {"day", "both"}:
        day = str(input("which week day (saturday,sunday,monday,tuesday,wednesday,thursday or friday)?")).lower()
        while day not in day_index:
            print("Invalid input !. please type one of (saturday,sunday,monday,tuesday,wednesday,thursday or friday?)")
            day = str(input()).lower()
    """
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('-' * 40)
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

    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()
    df["hours"] = df["Start Time"].dt.strftime("%H")
    df["start end combination"] = df["Start Station"] + " , " + df["End Station"]

    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df["month"] == month]

    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    most_common_month = df["month"].mode()[0]
    most_common_month_name = month_index[most_common_month]
    print("most common month : {}".format(most_common_month_name))

    # display the most common day of week

    most_common_day_of_week = df["day_of_week"].mode()[0]
    print("most common day of week : {}".format(most_common_day_of_week))

    # display the most common start hour

    most_common_start_hour = df["hours"].mode()[0]
    print("most common start hour : {}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df["Start Station"].mode()[0]
    print("most start station : {}".format(most_start_station))

    # display most commonly used end station
    most_end_station = df["End Station"].mode()[0]
    print("most end station : {}".format(most_end_station))

    # display most frequent combination of start station and end station trip

    most_frequent_combination = df["start end combination"].mode()[0]
    print("most common trip : {}".format(most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("total travel time : {} seconds.".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("mean travel time : {} seconds.".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_user = df["User Type"].value_counts().to_string()
    print("count of user count :\n {}".format(count_of_user))

    # Display counts of gender

    while "Gender" in df.columns:
        count_of_gender = df["Gender"].value_counts().to_string()
        print("count of gender : \n {}".format(count_of_gender))
        break

    # Display earliest, most recent, and most common year of birth

    while "Birth Year" in df.columns:
        earliest_year_of_birth = df["Birth Year"].max()
        most_recent_year_of_year = df["Birth Year"].min()
        most_common_year_of_year = df["Birth Year"].mode().to_string()
        print("earliest year of birth : {}".format(earliest_year_of_birth))
        print("most recent year of birth : {}".format(most_recent_year_of_year))
        print("most common year of birth : {}".format(most_common_year_of_year))
        break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    num_of_row = 0

    """ Display 5 rows of data at time """

    while True:
        respond = str(input("would you like to see raw data? please type (yes or no)? ")).lower()

        while respond not in {"yes", "no"}:
            respond = str(input("Invalid Input!. please type(yes or no). ")).lower()

        if respond == "yes":

            for i in range(num_of_row, num_of_row + 5):
                print(df.iloc[i].to_string())
        num_of_row += 5
        if respond == "no":
            break
    return


def main():
    while True:
        try:
            city, month, day = get_filters()
        except (KeyboardInterrupt, ValueError):
            break

        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = str(input('\nWould you like to restart? Enter yes or no.\n')).lower()
        while restart not in {"yes", "no"}:
            restart = str(input("Invalid input, please type 'yes' or 'no'.")).lower()
        if restart == 'no':
            break
        elif restart == "yes":
            continue

if __name__ == "__main__":
    main()
