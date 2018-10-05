import re
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

from . import Episode

__all__ = (
    'Webtoon',
    'WebtoonNotExist',
)


class Webtoon:
    TEST_WEBTOON_ID = 714834

    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self._episode_dict = OrderedDict()

    def __repr__(self):
        return self.title

    @property
    def url(self):
        return f'https://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'

    @property
    def episode_dict(self):
        """
        에피소드 목록을 파싱하는부분을 먼저 연습
            -> notebook에서

        자신의 _episode_dict가 있다면 그대로 리턴
        아니라면 채워준다
         주소는 (에피소드 리스트 URL)
          https://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}

        키는 Episode의 episode_id
            에피소드 상세 URL에서의 'no' GET parameter값에 해당
            https://comic.naver.com/webtoon/detail.nhn?titleId=651673&no=345&weekday=wed

        webtoon_dict를 채울때와 비슷하게, 새로운 Episode클래스 인스턴스를 만들어 할당

        page값을 1부터 늘려가면서 '다음'버튼이 안보일때까지 내용을 가져옴
        :return:
        """

        if not self._episode_dict:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'lxml')

            table = soup.select_one('table.viewList')
            tr_list = table.select('tr')[1:]
            for tr in tr_list:
                try:
                    td_list = tr.select('td')
                    href = td_list[0].select_one('a')['href']

                    no = re.search(r'no=(\d+)', href).group(1)
                    if no not in self._episode_dict:
                        url_thumbnail = td_list[0].select_one('img')['src']
                        title = td_list[1].select_one('a').get_text(strip=True)
                        rating = td_list[2].select_one('strong').get_text()
                        created_date = td_list[3].get_text(strip=True)

                        episode = Episode(
                            episode_id=no,
                            title=title,
                            url_thumbnail=url_thumbnail,
                            rating=rating,
                            created_date=created_date,
                        )
                        self._episode_dict[no] = episode
                except:
                    # 로그를 쌓으면 좋음
                    pass
        return self._episode_dict

    def get_episode(self, index):
        """
        index번에 해당하는 에피소드를 자신의 episode_dict프로퍼티를 사용해서 리턴
        :param index:
        :return:
        """


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'Webtoon(title: {self.title})을 찾을 수 없습니다'
