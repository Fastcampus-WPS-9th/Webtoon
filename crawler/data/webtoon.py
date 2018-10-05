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
            # 비어있는 경우
            # self.url (목록페이지 URL)에 HTTP요청 후, 받은 결과를 파싱 시작
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'lxml')

            # 에피소드 목록이 table.viewList의 각 'tr'요소 하나씩에 해당함
            table = soup.select_one('table.viewList')
            tr_list = table.select('tr')[1:]
            for tr in tr_list:
                # 이 루프 내부의 'tr'하나당 에피소드 하나를 만들어야 함
                try:
                    # 데이터 파싱
                    td_list = tr.select('td')
                    href = td_list[0].select_one('a')['href']
                    no = re.search(r'no=(\d+)', href).group(1)
                    url_thumbnail = td_list[0].select_one('img')['src']
                    title = td_list[1].select_one('a').get_text(strip=True)
                    rating = td_list[2].select_one('strong').get_text()
                    created_date = td_list[3].get_text(strip=True)
                    # 파싱한 데이터로 새 Episode인스턴스 생성
                    episode = Episode(
                        episode_id=no,
                        title=title,
                        url_thumbnail=url_thumbnail,
                        rating=rating,
                        created_date=created_date,
                    )
                    # 인스턴스의 _episode_dict사전에 episode_id (파싱데이터에서는 'no'변수)키로 인스턴스 할당
                    self._episode_dict[no] = episode
                except:
                    # 위 파싱에 실패하는 경우에는 무시 (tr이 의도와 다르게 생겼을때 실패함)
                    # 기왕이면 실패 로그를 쌓으면 좋음 (어떤 웹툰의 몇 번째 페이지 몇 번째 row시도중 실패했다를 텍스트 파일에)
                    pass
        return self._episode_dict

    def get_episode(self, index):
        """
        index번에 해당하는 에피소드를 자신의 episode_dict프로퍼티를 사용해서 리턴
        :param index:
        :return:
        """
        pass


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'Webtoon(title: {self.title})을 찾을 수 없습니다'
