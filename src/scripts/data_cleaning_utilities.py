import pandas as pd
from typing import List, Union
import datetime
from dateutil import parser



def change_date_type(dates: Union[pd.DataFrame, pd.Series]) -> List:
    """
    Formats string column into datetime object
    """
    column = []
    
    for date in dates:
        column.append(parser.parse(date).strftime("%d-%m-%Y %H:%M:%S"))
    
    series = pd.Series(column)
    return pd.to_datetime(series)


def str_to_list(row):
    """convert a string List into a List"""
    row = str(row).strip("[]").replace("'","")
    return row


def parsed_email_processing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic email formatting and cleaning
    """
    
    df['Date'] = change_date_type(df['Date'])
    
    df['body'] = df['body'].str.replace('\n','').str.replace('\t','')
    
    df['To'] = df['To'].astype('str')\
        .str.replace('b','')\
        .apply(str_to_list)
        
    df['From'] = df['From'].astype('str')\
        .str.replace('b','')\
        .apply(str_to_list)
    
    return df

    
    