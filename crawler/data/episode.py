class Episode:
    def __init__(self, episode_id, title, url_thumbnail, rating, created_date):
        self.episode_id = episode_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self.rating = rating
        self.created_date = created_date

    def __repr__(self):
        return self.title
