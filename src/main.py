#!/usr/bin/env python3
"""
main.py - The main module for processing data and creating visual summaries
for this study.
"""
# =========================================================================== #
# METADATA
# =========================================================================== #

__author__ = 'Robert (Bob) L. Jones'
__credits__ = ['Robert (Bob) L. Jones']

__created_date__ = 'Sep 16, 2020'
__modified_date__ = 'Sep 16, 2020'


# =========================================================================== #
# EXPORTS
# =========================================================================== #


# Define the module's API -- the list of exportable objects (classes,
# functions, etc.) -- when performing a "wild import" (`from field import *`).
__all__ = [
    'DEBUG',
]


# =========================================================================== #
# IMPORTS
# =========================================================================== #

# -- Python Standard Library -- #

import os

# -- 3rd Party -- #

import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# =========================================================================== #
# CONSTANTS
# =========================================================================== #

# -- Data -- #

DAILY = 'daily'
WEEKLY = 'weekly'

COLUMNS = {
    'positive': 'pos',
    'negative': 'neg',
    'negativeIncrease': 'negIncrease',
    'positiveIncrease': 'posIncrease',
}

DOW = [
    'Sunday', 'Monday', 'Tuesday', 'Wednesday',
    'Thursday', 'Friday', 'Saturday',
]

# -- Debugging -- #

DEBUG = True

# -- Filesytem -- #

ROOT_DIR = os.path.join(os.getcwd(), '..')

DATA_DIR = '../data'
RESULTS_DIR = '../results'

# -- URLs -- #

SOURCE_URL = 'https://covidtracking.com/api/v1/us/daily.csv'


# =========================================================================== #
# FUNCTIONS
# =========================================================================== #

# -- Data Analytics -- #

def plot_series(df: pd.DataFrame):
    fig = plt.figure()

    ax = plt.subplot(111)

    ax.xaxis.set_major_formatter(
        mpl_dates.DateFormatter('%m-%d-%Y'),
    )

    sns.lineplot(
        data=df,
        x='date',
        y='posIncrease',
        marker='o',
    )

    ax.set_title('COVID-19 | Year 2020 | USA | Daily New Positive Cases')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count of Cases')
    ax.xaxis_date()
    # plt.show()

    # Debug data frame.
    DEBUG and preview(df, plot_series.__name__)

    fig.savefig(f'{RESULTS_DIR}/plot_series.png')


def set_figure_defaults():
    # Use seaborn style defaults.  Set the default figure size.
    sns.set(
        style='darkgrid',
        rc={'figure.figsize': (16, 9)},
    )


def summarize_by_dow(df: pd.DataFrame):
    fig = plt.figure()

    ax = plt.subplot(111)

    sns.boxplot(
        data=df,
        x='dow',
        y='posIncrease',
        order=DOW,
    )

    ax.set_title('COVID-19 | Year 2020 | USA | Daily New Positive Cases')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Count of Cases')

    # Debug data frame.
    DEBUG and preview(df, summarize_by_dow.__name__)

    # plt.show()
    fig.savefig(f'{RESULTS_DIR}/summarize_dow.png')


def summarize_by_dow_percent(df: pd.DataFrame):
    fig = plt.figure()

    ax = plt.subplot(111)

    sns.boxplot(
        data=df,
        x='dow',
        y='pctWeeklyPosIncrease',
        order=DOW,
    )

    ax.set_title('COVID-19 | Year 2020 | USA | Daily New Positive Cases')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Percent of Weekly Count of Cases')

    # Debug data frame.
    DEBUG and preview(df, summarize_by_dow_percent.__name__)

    # plt.show()
    fig.savefig(f'{RESULTS_DIR}/summarize_dow_percent.png')


def summarize_by_dow_zscore(df: pd.DataFrame):
    fig = plt.figure()

    ax = plt.subplot(111)

    sns.boxplot(
        data=df,
        x='dow',
        y='zscoreWeeklyPosIncrease',
        order=DOW,
    )

    ax.set_title('COVID-19 | Year 2020 | USA | Daily New Positive Cases')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Z-Score of Weekly Count of Cases')

    # Debug data frame.
    DEBUG and preview(df, summarize_by_dow_zscore.__name__)

    # plt.show()
    fig.savefig(f'{RESULTS_DIR}/summarize_dow_zscore.png')


def summarize_maxima(df: pd.DataFrame):
    fig = plt.figure()

    ax = plt.subplot(111)

    sns.countplot(
        data=df,
        x='dow',
        order=DOW,
    )

    ax.set_title('COVID-19 | Year 2020 | USA | Daily New Positive Cases')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Count of Local Maxima of Cases')

    # Debug data frame.
    DEBUG and preview(df, summarize_maxima.__name__)

    # plt.show()
    fig.savefig(f'{RESULTS_DIR}/summarize_maxima.png')


def visualize_data(df: pd.DataFrame):
    set_figure_defaults()
    plot_series(df.sort_values('date'))
    summarize_by_dow(df)
    summarize_by_dow_percent(df)
    summarize_by_dow_zscore(df)
    summarize_maxima(df[df['localMaximum'].eq(True)])

    # Debug data frame.
    DEBUG and preview(df, visualize_data.__name__)

    # Return data frame for reuse.
    return df

# -- Data Processing: Extract -- #


def extract_data() -> pd.DataFrame:

    # Download source data as CSV from an API.
    df = pd.read_csv(SOURCE_URL)

    # Save a copy of the extracted data.
    df.to_csv(
        f'{DATA_DIR}/01_raw/{DAILY}_extract_data.csv',
        index=False,
    )

    # Debug data frame.
    DEBUG and preview(df, extract_data.__name__)

    # Return data frame for reuse.
    return df

# -- Data Processing: Transform -- #


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = rename_columns(df)
    df = add_columns(df)

    # Debug data frame.
    DEBUG and preview(df, transform_data.__name__)

    # Return data frame for reuse.
    return df


def add_columns(df: pd.DataFrame):

    # Format date.
    df.date = pd.to_datetime(df.date, format='%Y%m%d')

    # Set the date as the DataFrame's index.
    df = df.set_index('date')

    # Add date-derived columns.
    df['date'] = df.index.date
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['week'] = df.index.week
    df['dow'] = df.index.day_name()
    df['dowIndex'] = df.index.dayofweek

    # Add group-summarization columns.
    df_weekly = df.groupby('week', as_index=False)['posIncrease'].agg(
        {
            'weeklyPosIncrease': 'sum',
            'meanWeeklyPosIncrease': 'mean',
            'stdWeeklyPosIncrease': 'std',
        },
    )
    df = pd.merge(
        df, df_weekly,
        how='left', on='week',
    )
    df['pctWeeklyPosIncrease'] = percent(df.posIncrease, df.weeklyPosIncrease)
    df['zscoreWeeklyPosIncrease'] = zScore(
        df.posIncrease,
        df.meanWeeklyPosIncrease,
        df.stdWeeklyPosIncrease,
    )

    # Add delta columns.
    df['day1LagDelta'] = lag_delta(df.posIncrease, 1)
    df['day1LeadDelta'] = lead_delta(df.posIncrease, 1)

    # Add local extrema columns.
    df['localMaximum'] = df.apply(local_max, axis=1)
    df['localMinimum'] = df.apply(local_min, axis=1)

    # Save a copy of the processed data.
    df.to_csv(
        f'{DATA_DIR}/02_intermediate/{DAILY}_add_columns.csv',
        index=True,
    )

    # Debug data frame.
    DEBUG and preview(df, add_columns.__name__)

    # Return data frame for reuse.
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:

    # Rename columns.
    df.rename(columns=COLUMNS, inplace=True)

    # Save a copy of the processed data.
    df.to_csv(
        f'{DATA_DIR}/02_intermediate/{DAILY}_rename_columns.csv',
        index=True,
    )

    # Debug data frame.
    DEBUG and preview(df, rename_columns.__name__)

    # Return data frame for reuse.
    return df

# -- Data Processing: Load -- #

# -- Utilities -- #


def lag_delta(series, period):
    return series - series.shift(period)


def lead_delta(series, period):
    return series.shift(-period) - series


def local_max(row):
    if row['day1LagDelta'] > 0 and row['day1LeadDelta'] < 0:
        return True
    else:
        return False


def local_min(row):
    if row['day1LagDelta'] < 0 and row['day1LeadDelta'] > 0:
        return True
    else:
        return False


def percent(num, denom):
    return 100 * num / denom


def preview(df: pd.DataFrame, func_name: str):
    print(f'INSIDE {func_name}(): type =', type(df).__name__)
    print(df.head(5))


def zScore(x, mean, std):
    return (x - mean) / std

# -- Main Program -- #


def main():
    df = extract_data()
    df = transform_data(df)
    visualize_data(df)


# =========================================================================== #
# MAIN EXECUTION
# =========================================================================== #

# -- Main Program -- #

# If this module is in the main module, call the main() function.
if __name__ == '__main__':
    main()
