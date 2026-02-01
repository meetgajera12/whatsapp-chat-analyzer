import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue() 
    data = byte_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('show analysis wrt', user_list)

    if st.sidebar.button("show analysis"):

        num_messages, words, num_media_msg, num_links = helper.fetch_stat(selected_user,df)
        
        st.title("TOP STATISTICS")
        
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


        #monthly_timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily_timeline
        st.title("Daily Timeline")
        d_timeline = helper.daily_timline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(d_timeline['only_date'], d_timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2) 

        with col1:
            st.text("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.text("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728','#9467bd', '#8c564b', '#e377c2', '#7f7f7f','#bcbd22', '#17becf', '#aec7e8', '#ffbb78'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heat_map(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        #finding busiest user in group (at group level)
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_user(df)

            fig, ax = plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        
        #wordcloud
        df_wc = helper.create_wordcloud(selected_user, df)
        st.title('WordCloud')
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color=['#8c564b'])
        plt.xticks(rotation='vertical')

        st.title("most common words")
        st.pyplot(fig)

        #emoji counter
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            emoji_df.rename(columns={0:'emoji', 1:"count"}, inplace=True)
            st.dataframe(emoji_df)

        with col2:
            from matplotlib import rcParams
            rcParams['font.family'] = 'Segoe UI Emoji'

            fig, ax = plt.subplots()
            st.text('Top 10 emojis')
            ax.pie(emoji_df.head(10)['count'], labels=emoji_df.head(10)['emoji'], autopct="%0.2f")
            st.pyplot(fig)