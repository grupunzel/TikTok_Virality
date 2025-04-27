import pandas as pd
import streamlit as st
from collections import Counter
import io

def database_loader(path):
    return pd.read_csv(path)

def linear_graphic(df, param1, param2):
    st.subheader(f'Dependency of {param2} on {param1}:')
    st.line_chart(df, x=param1, y=param2, color="#d36df8")

def upload_dataset(data):
    st.subheader("Upload your own dataset")
    data_file = st.file_uploader("Upload CSV:", type=["csv"])
    if data_file is not None:
        df = pd.read_csv(data_file)
        st.success('Your CSV file has been successfully uploaded!')
        return df
    else:
        return data

def main():
    st.set_page_config(page_title='Statistics of the TikTok virality', layout='wide')
    st.title('Statistics of the TikTok Virality')
    st.markdown('Interactive dashboard for statistics of the TikTok virality of the song based on the average number of streams the song receives per day.')

    df = database_loader('music_dataset.csv')

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f6eafb; 
            }
            .stSidebar {
                background-color: #ecd5f6;
            }
        </style>
        """,
        unsafe_allow_html=True
    )   

    with st.sidebar:
        st.write('Use filters for your own research.')
        st.subheader('Search filters:')

        genres = st.multiselect("Song genres: ", ['Pop', 'Rock', 'Jazz', 'Electronic', 'Hip-Hop', 'Country', 'K-Pop'])
        st.write("You selected", len(genres), 'genres.')

        if len(genres) == 0:
            genres = ['Pop', 'Rock', 'Jazz', 'Electronic', 'Hip-Hop', 'Country', 'K-Pop']


        min_year = df['Release Year'].min()
        max_year = df['Release Year'].max()
        year = st.slider("Select the year of song release: ", min_year, max_year)

        daily_streams = st.radio("Daily Streams: ", ('<1.5M', '<3M', '<5M'))
        if daily_streams == '<1.5M':
            daily = [df['Daily Streams'].min(), 1500000]
        elif daily_streams == '<3M':
            daily = [df['Daily Streams'].min(), 3000000]
        else:
            daily = [df['Daily Streams'].min(), df['Daily Streams'].max()]

        st.write('Lyrics sentiment: ')
        lyrics_sent = st.checkbox("Sentimental")
        lyrics_unsent = st.checkbox("Unsentimental")

        if lyrics_sent == lyrics_unsent:
            sentiment = [-1, 1]
        elif lyrics_sent:
            sentiment = [0, 1]
        else:
            sentiment = [-1, 0]

        weeks_min, weeks_max = st.slider('Weeks on chart: ', df['Weeks on Chart'].min(), df['Weeks on Chart'].max(), (df['Weeks on Chart'].min(), df['Weeks on Chart'].max()))
        low_chart, high_chart = st.slider('Peak position: ', df['Peak Position'].min(), df['Peak Position'].max(), (df['Peak Position'].min(), df['Peak Position'].max()))

        filtered_df = df[
            (df['Song']).notna()
            & (df['Artist']).notna() 
            & (df['Streams']).notna() 
            & (df['Daily Streams'].between(daily[0], daily[1])) 
            & (df['Genre'].isin(genres)) 
            & (df['Release Year'] == year)        
            & (df['Peak Position'].between(low_chart, high_chart)) 
            & (df['Weeks on Chart'].between(weeks_min, weeks_max)) 
            & (df['Lyrics Sentiment'].between(sentiment[0], sentiment[1])) 
            & (df['TikTok Virality']).notna()
        ]

    upload_dataset(df)
    st.write('\n')
    
    col1, col2, col3 = st.columns(3)
    col1.metric('Amount of all streams', '{0:,}'.format(sum(filtered_df['Streams'].tolist())).replace(',', ' '))
    col1.metric('Average of all streams', '{0:,}'.format(sum(filtered_df['Streams'].tolist()) // len(filtered_df['Streams'].tolist())).replace(',', ' '))

    col2.metric('Average peak position', sum(filtered_df['Peak Position'].tolist()) // len(filtered_df['Peak Position'].tolist()))
    col2.metric('Average number of weeks on chart', sum(filtered_df['Weeks on Chart'].tolist()) // len(filtered_df['Weeks on Chart'].tolist()))

    sent_average = round(sum(filtered_df['Lyrics Sentiment'].tolist()) / len(filtered_df['Lyrics Sentiment'].tolist()), 3)
    sent = lambda x: 'sentimental' if 0 <=x<= 1 else 'unsentimental'
    col3.metric('Average of lyrics sentiment', f"{sent_average} - {sent(sent_average)}")
    most_common_artist = Counter(filtered_df['Artist'].tolist()).most_common(1)[0][0]
    col3.metric('Most popular artist', most_common_artist)

    with st.expander('Linear graphic'):
        linear_graphic(filtered_df, 'Streams', 'TikTok Virality')

    with st.expander('Table'):
        st.subheader('Filtered table:')
        st.dataframe(filtered_df)

        col1, col2 = st.columns([0.15, 1])

        with col1:
            csv_download = st.download_button(
                label="Download as CSV",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='df.csv',
                mime='text/csv'
            )

        with col2:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

                download2 = st.download_button(
                    label="Download as xlsx",
                    data=buffer,
                    file_name='df.xlsx',
                    mime='application/vnd.ms-excel'
                )

main()