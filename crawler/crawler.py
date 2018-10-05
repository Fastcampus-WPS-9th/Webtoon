class Crawler:
    def show_webtoon_list(self):
        """
        전체 웹툰 제목을 출력해줌

        1. requests를 사용해서 웹툰 목록 URL의 내용을 가져옴
        2. BeautifulSoup을 사용해서 가져온 HTML데이터를 파싱
        3. 파싱한 결과를 사용해서 Webtoon클래스 인스턴스들을 생성
        4. 생성한 인스턴스 목록을 dict에 제목을 key를 사용해서 할당
        5. dict를 순회하며 제목들을 출력

        crawler = Crawler()
        crawler.show_webtoon_list()
        :return:
        """
        print('')


class Webtoon:
    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail

    def __repr__(self):
        return self.title


class Episode:
    def __init__(self, episode_id, title, url_thumbnail, rating, created_date):
        self.episode_id = episode_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self.rating = rating
        self.created_date = created_date

    def __repr__(self):
        return self.title
