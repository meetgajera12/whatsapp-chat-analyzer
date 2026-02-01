from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

def fetch_stat(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #no. of msg
    num_msg = df.shape[0]
    #no. of words
    words=[]
    for msg in df['messages']:
        words.extend(msg.split())

    #no. of media
    num_media_msg = df[df['messages'] == '<Media omitted>'].shape[0]

    #no. of urls
    extract = URLExtract()
    links=[]
    for msg in df['messages']:
        links.extend(extract.find_urls(msg))

    return num_msg, len(words), num_media_msg, len(links)



    # if selected_user == 'Overall':
    #     #no. of msg
    #     num_msg = df.shape[0]
    #     #no. of words
    #     words=[]
    #     for msg in df['messages']:
    #         words.extend(msg.split())

    #     return num_msg, len(words)
    
    # else:
    #     new_df = df[df['user'] == selected_user]

    #     #no. of msg
    #     num_msg = df[df['user'] == selected_user].shape[0]

    #     #no. of words
    #     words=[]
    #     for msg in new_df['messages']:
    #         words.extend(msg.split())

    #     return num_msg,len(words)


def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'user':'name', 'count':'Percent'})
    return x, df


def create_wordcloud(selected_user, df):
    
    f = open('stop_words.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    def remove_stop_words(msg):
        y=[]
        for word in msg.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500,min_font_size=10, background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=' '))

    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_words.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    words=[]
    for msg in temp['messages']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['messages']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    d_timeline = df.groupby(['only_date']).count()['messages'].reset_index()

    return d_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap