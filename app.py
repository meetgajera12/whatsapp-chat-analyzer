import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import emoji
import seaborn as sns
import preprocessor, helper
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Chat Analysis",
    page_icon="💬",
    layout="wide"
)

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue() 
    data = byte_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    # st.dataframe(df)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('show analysis wrt', user_list)

    if st.sidebar.button("show analysis"):

        num_messages, words, num_media_msg, num_links = helper.fetch_stat(selected_user,df)
        
        st.title(f"TOP STATISTICS for {selected_user}")
        st.divider()
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.text("Total Messages")
            st.header(num_messages)

        with col2:
            st.text("Total Words")
            st.header(words)

        with col3:
            st.text("Total Media Shared")
            st.header(num_media_msg)

        with col4:
            st.text("Total Links Shared")
            st.header(num_links)

        st.divider()


        #monthly_timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots(figsize=(8,3))
        ax.plot(timeline['time'], timeline['messages'], color='red')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.divider()
         

        #daily_timeline
        st.title("Daily Timeline")
        d_timeline = helper.daily_timline(selected_user, df)
        fig, ax = plt.subplots(figsize=(8,4))
        ax.plot(d_timeline['only_date'], d_timeline['messages'], color='green')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.divider()


        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2) 

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            colors = plt.cm.tab20(np.linspace(0,1,len(busy_day)))
            bars = ax.bar(busy_day.index, busy_day.values, color = colors)
            ax.bar_label(bars) 
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            colors = plt.cm.tab20(np.linspace(0,1,len(busy_month)))
            bars = ax.bar(busy_month.index, busy_month.values, color =colors)
            ax.bar_label(bars) 
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.divider()
        
        #heatmap
        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heat_map(selected_user,df)
        if user_heatmap.size == 0:
            st.write("No data available for heatmap")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)

        st.divider()

        # finding busiest user in group (at group level)
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_user(df)

            fig, ax = plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                colors = plt.cm.plasma(np.linspace(0,1,len(x)))
                bars = ax.bar(x.index, x.values, color=colors)
                ax.bar_label(bars) 
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

            st.divider()

        
        #wordcloud
        df_wc = helper.create_wordcloud(selected_user, df)
        st.title('WordCloud')
        fig, ax = plt.subplots()
        st.text("Disclaimer: Some Gujarati or Hindi words may be not visible in this plot")
        ax.axis("off")
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.divider()
        

        #most common words
        st.title("most common words")
        col1,col2 = st.columns(2)
        with col1:
            most_common_df = helper.most_common_words(selected_user, df)
            st.dataframe(most_common_df)

        with col2:
            fig, ax = plt.subplots()
            st.text("Disclaimer: Some Emojies and Gujarati or Hindi words may be not visible in this plot")
            font_path = "NotoSansGujarati-VariableFont_wdth,wght.ttf"
            prop = fm.FontProperties(fname=font_path)
            colors = plt.cm.viridis(np.linspace(0,1,len(most_common_df)))
            bars = ax.barh(most_common_df[0], most_common_df[1], color=colors)
            ax.bar_label(bars) 
            plt.yticks(fontproperties=prop)
            st.pyplot(fig)
            
        st.divider()


        #count of deleted msg
        deleted_msg = helper.count_deleted_msg(selected_user,df)

        if selected_user == 'Overall':
            st.title('Total No. of Deleted Messages')
            fig, ax = plt.subplots(figsize=(10,8))
            colors = plt.cm.cividis(np.linspace(0,1,len(deleted_msg)))
            bars = ax.barh(deleted_msg['user'], deleted_msg['total_deleted_msg'], color=colors)
            ax.bar_label(bars)
            ax.set_xlim(0, deleted_msg['total_deleted_msg'].max() + 5)
            st.pyplot(fig)
        else:
            st.title('Total Deleted Messages')
            dm = deleted_msg['total_deleted_msg'].iloc[0]
            st.header(f'by {selected_user}: {dm}')

        st.divider()


        #emoji counter
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            emoji_df.rename(columns={0:'emoji', 1:"count"}, inplace=True)
            st.dataframe(emoji_df)

        with col2:
            fig1 = px.pie(emoji_df.head(10), values='count', names='emoji', title='Top 10 emojis')
            st.plotly_chart(fig1)

        st.divider()
    
        # reply time
        st.title('User Average Reply Time')
        reply_time = helper.reply_time(df)
        reply_time['reply_minutes'] = reply_time['reply_minutes']
        fig, ax = plt.subplots(figsize=(10,8))
        colors = plt.cm.tab20(np.linspace(0,1,len(reply_time)))
        bars = ax.barh(reply_time['user'], reply_time['reply_minutes'], color=colors)
        ax.bar_label(bars,fmt='%.2f min')
        ax.set_xlim(0, reply_time['reply_minutes'].max() + 5)
        st.pyplot(fig)

        st.divider()