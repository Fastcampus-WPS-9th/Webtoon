import os
import re

import requests
from bs4 import BeautifulSoup

from data import Episode, Webtoon, WebtoonNotExist


class Crawler:
    def __init__(self):
        self._webtoon_dict = {}

    def get_html(self):
        """
        전체 웹툰 목록의 HTML을 리턴한다.
        만약에 파일로 저장되어 있다면, 해당 내용을 읽어온다.

        파일로 저장되어 있지 않다면, requests를 사용해 웹에서 받아와 리턴해준다.
            파일위치는 ./saved_data/weekday.html를 사용
            경로 작성에는 os.path모듈을 사용

        -> 다 작성한 후에는 show_webtoon_list에서 이 메서드를 사용하도록 함
        :return: HTML데이터 문자열
        """
        # weekday.html파일의 경로
        root = os.path.dirname(os.path.abspath(__file__))
        dir_path = os.path.join(root, 'saved_data')
        file_path = os.path.join(dir_path, 'weekday.html')

        if os.path.exists(file_path):
            # 경로가 존재하면
            # 해당 경로의 파일을 읽기
            html = open(file_path, 'rt').read()
        else:
            # 경로가 존재하지 않으면
            # HTTP요청결과를 가져오고, 이후 다시 요청시 읽기위한 파일을 기록

            # 파일을 저장할 폴더를 생성. 이미 존재하는 경우 무시하기 위해 exist_ok인수 추가
            os.makedirs(dir_path, exist_ok=True)
            response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
            html = response.text
            open(file_path, 'wt').write(html)
        return html

    @property
    def webtoon_dict(self):
        if not self._webtoon_dict:
            html = self.get_html()
            soup = BeautifulSoup(html, 'lxml')
            col_list = soup.select_one('div.list_area.daily_all').select('.col')
            li_list = []
            for col in col_list:
                col_li_list = col.select('.col_inner ul > li')
                li_list.extend(col_li_list)

            for li in li_list:
                href = li.select_one('a.title')['href']
                m = re.search(r'titleId=(\d+)', href)
                webtoon_id = m.group(1)
                title = li.select_one('a.title').get_text(strip=True)
                url_thumbnail = li.select_one('.thumb > a > img')['src']

                if title not in self._webtoon_dict:
                    new_webtoon = Webtoon(webtoon_id, title, url_thumbnail)
                    self._webtoon_dict[title] = new_webtoon
        return self._webtoon_dict

    def get_webtoon(self, title):
        """
        title이 제목인 Webtoon객체를 가져옴

        :param title:
        :return:
        """
        try:
            self.webtoon_dict[title]
        except KeyError:
            raise WebtoonNotExist(title)

    def show_webtoon_list(self):
        for title, webtoon in self.webtoon_dict.items():
            print(title)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.show_webtoon_list()
