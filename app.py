import streamlit as st
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="콘텐츠 통합 추천 플랫폼", layout="wide")


@st.cache_data
def load_and_process_data(file_name):
    file_path = BASE_DIR / file_name
    if file_path.exists():
        df = pd.read_csv(file_path)
 
        df['salesPoint'] = pd.to_numeric(df['salesPoint'], errors='coerce').fillna(0)

        return df
    return None


def get_display_df(data):
    d = data[['title', 'artist', 'genre', 'year']].copy()
    
  
    d['title'] = d['title'].apply(lambda x: str(x)[:30] + '...' if len(str(x)) > 30 else x)
    
    d.columns = ['제목', '크리에이터', '장르', '발행년도']
    return d


def show_dataframe(df):
    st.dataframe(
        df,
        width='stretch', 
        hide_index=True,
        column_config={
            "제목": st.column_config.TextColumn("제목", width="large"),
            "크리에이터": st.column_config.TextColumn("크리에이터", width="medium"),
            "장르": st.column_config.TextColumn("장르", width="small"),
            "발행년도": st.column_config.NumberColumn("발행년도", format="%d")
        }
    )


def render_recommendation_tabs(df, content_key):
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([" 전체 TOP 10", " 장르별 정밀 추천", " 랜덤 추천"])

    with sub_tab1:
        show_dataframe(get_display_df(df.sort_values(by='salesPoint', ascending=False).head(10)))

    with sub_tab2:
        genre = st.selectbox("장르 선택", df['genre'].dropna().unique(), key=f"genre_{content_key}")
        filtered_df = df[df['genre'] == genre].sort_values(by='salesPoint', ascending=False).head(10)
        show_dataframe(get_display_df(filtered_df))

    with sub_tab3:
        if st.button("추천 받기", key=f"random_{content_key}"):
            show_dataframe(get_display_df(df.sample(min(10, len(df)))))


st.title("콘텐츠 통합 추천 플랫폼")

main_tab1, main_tab2, main_tab3 = st.tabs([" 도서", " 영화", " 음악"])


with main_tab1:
    df_book = load_and_process_data("book_data.csv")
    if df_book is not None:
        render_recommendation_tabs(df_book, "book")
    else:
        st.error("도서 데이터를 찾을 수 없습니다.")


with main_tab2:
    df_movie = load_and_process_data("movie_data.csv")
    if df_movie is not None:
        render_recommendation_tabs(df_movie, "movie")
    else:
        st.info("영화 데이터가 없습니다. kofic.py를 먼저 실행해 movie_data.csv를 생성하세요.")

with main_tab3:
    df_music = load_and_process_data("music_data.csv")
    if df_music is not None:
        render_recommendation_tabs(df_music, "music")
    else:
        st.info("음악 데이터가 없습니다. itunes.py를 먼저 실행해 music_data.csv를 생성하세요.")