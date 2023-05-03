import re
import pandas as pd
from datetime import datetime




def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s*[ap]m'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # create a list of tuples containing only the message and date pairs
    message_dates = [(message, date) for message, date in zip(messages, dates) if date]

    # unpack the tuples into separate lists
    messages, dates = zip(*message_dates)

    # convert the dates to datetime objects
    dates = [datetime.strptime(date, '%d/%m/%y, %I:%M\u202f%p') for date in dates]

    # create a DataFrame from the messages and dates
    df = pd.DataFrame({'date': dates, 'user_message': messages})

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])  # username is extracted from the first part of the split
            messages.append(" ".join(entry[2:])) #the message body is extracted from the rest of the split, which is entry[2:].
        else: #If a username is found in the message (i.e., entry[1:] is not an empty list), it is appended to the users list
            users.append('group_notification')#If a username is not found in the message (i.e., entry[1:] is an empty list), the username is set to 'group_notification', and the entire message is added to the messages list.
            messages.append(entry[0])# the message body is appended to the messages list after being joined into a single string with spaces.

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period
    return df
