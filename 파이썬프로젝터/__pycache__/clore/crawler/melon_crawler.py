import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
def crawl_melon_chart():
    print("멜론 TOP 100 차트 크롤링을 시작합니다...")
    url = 'https://www.melon.com/chart/index.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"오류: 웹 페이지를 가져오는 데 실패했습니다 - {e}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    song_list = soup.select('tr.lst50, tr.lst100')
    if not song_list:
        print("오류: 차트 정보를 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
        return None
    chart_data = []
    for song in song_list:
        try:
            rank = song.select_one('span.rank').get_text(strip=True)
            title = song.select_one('div.ellipsis.rank01 a').get_text(strip=True)
            artists = ' & '.join([a.get_text(strip=True) for a in song.select('div.ellipsis.rank02 a')])
            album = song.select_one('div.ellipsis.rank03 a').get_text(strip=True)
            
            chart_data.append({
                'Rank': int(rank),
                'Title': title,
                'Artist': artists,
                'Album': album
            })
        except AttributeError:
            continue
    df = pd.DataFrame(chart_data)
    if not df.empty:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"melon_top100_{today}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n크롤링 완료! '{filename}' 파일로 저장되었습니다.")
    else:
        print("데이터를 추출하지 못했습니다.")
    return df
if __name__ == "__main__":
    melon_df = crawl_melon_chart()
    if melon_df is not None:
        print("\n--- 멜론 TOP 100 차트 ---")
        print(melon_df.to_string(index=False))
        print("------------------------")

