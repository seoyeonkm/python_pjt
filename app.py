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
        # salespoint 높은 순으로 top10 정렬하는 코드에요
        df['salesPoint'] = pd.to_numeric(df['salesPoint'], errors='coerce').fillna(0)

        return df
    return None


def get_display_df(data):
    d = data[['title', 'genre', 'year']].copy()
    
    d.columns = ['제목', '장르', '발행년도']
    return d


def show_dataframe(df):
    st.dataframe(
        df,
        width='stretch', 
        hide_index=True,
        column_config={
            "제목": st.column_config.TextColumn("제목", width="large"),
            "장르": st.column_config.TextColumn("장르", width="small"),
            "발행년도": st.column_config.NumberColumn("발행년도", format="%d")
        }
    )


def get_unique_genres(df):
    genre_series = df['genre'].dropna().astype(str)
    split_genres = genre_series.str.split(',')
    return sorted({g.strip() for genres in split_genres for g in genres if g.strip()})


def has_genre(genre_text, selected_genre):
    genre_list = [g.strip() for g in str(genre_text).split(',') if g.strip()]
    return selected_genre in genre_list


def render_recommendation_tabs(df, content_key):
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([" 전체 TOP 10", " 장르별 정밀 추천", " 랜덤 발견"])

    with sub_tab1:
        show_dataframe(get_display_df(df.sort_values(by='salesPoint', ascending=False).head(10)))

    with sub_tab2:
        # if문에서는 영화는 genre 데이터 자체가 복수값이므로, 장르 선택 시 해당 장르가 포함된 영화들을 필터링
        if content_key == "movie":
            genre_options = get_unique_genres(df)
            genre = st.selectbox("장르 선택", genre_options, key=f"genre_{content_key}")
            filtered_df = df[df['genre'].apply(lambda x: has_genre(x, genre))].sort_values(by='salesPoint', ascending=False).head(10)
            show_dataframe(get_display_df(filtered_df))
        # else문에서는 book과 music은 genre가 단일값이므로 기존 방식으로 필터링
        else:
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
        st.error("영화 데이터를 찾을 수 없습니다.")

with main_tab3:
    df_music = load_and_process_data("music_data.csv")
    if df_music is not None:
        render_recommendation_tabs(df_music, "music")
    else:
        st.error("음악 데이터를 찾을 수 없습니다.")