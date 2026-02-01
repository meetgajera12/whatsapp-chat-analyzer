import re
import pandas as pd

def preprocess(data):

    pattern = (
    r'(?:\d{2}/\d{2}/\d{2}),\s'
    r'(?:\d{1,2}:\d{2})[\s\u202f]?'
    r'(?:[ap]m)\s-\s'
)
    
    messages = re.split(pattern,data)[1:]
    messages = [msg.strip() for msg in messages]

    dates = re.findall(pattern, data)
    

    df = pd.DataFrame({'user_msg':messages, 'msg_date':dates})

    #convert message_date type
    df['msg_date'] = pd.to_datetime(
        df['msg_date'],
        format='%d/%m/%y, %I:%M %p - '
    )
    df.rename(columns={"msg_date": 'date'}, inplace=True)


    #separate usera and messages
    user = []
    messages = []

    for msg in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]: #user name
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('group_notification')
            messages.append(entry[0])


    df['user'] = user
    df['messages'] = messages
    df.drop(columns=['user_msg'], inplace=True)


    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period=[]
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df 
