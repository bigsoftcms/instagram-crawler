from .browser import Browser
from .utils import instagram_int
from time import sleep


class InsCrawler:
    URL = 'https://www.instagram.com'
    RETRY_LIMIT = 10

    def __init__(self):
        self.browser = Browser()
        self.page_height = 0

    def get_user_profile(self, username):
        browser = self.browser
        url = '%s/%s/' % (InsCrawler.URL, username)
        browser.get(url)
        name = browser.find_one('._kc4z2')
        desc = browser.find_one('._tb97a span')
        photo = browser.find_one('._9bt3u ')
        statistics = [ele.text for ele in browser.find('._fd86t')]
        post_num, follower_num, following_num = statistics

        return {
            'name': name.text,
            'desc': desc.text if desc else None,
            'photo_url': photo.get_attribute('src'),
            'post_num': post_num,
            'follower_num': follower_num,
            'following_num': following_num
        }

    def _get_posts(self, num):
        '''
            To get posts, we have to click on the load more
            button and make the browser call post api.
        '''
        browser = self.browser
        dict_posts = {}
        pre_post_num = 0

        while len(dict_posts) < num:
            browser.scroll_down()
            ele_posts = browser.find('._havey ._mck9w a')
            for ele in ele_posts:
                key = ele.get_attribute('href')
                if key not in dict_posts:
                    ele_img = browser.find_one('._2di5p', ele)
                    content = ele_img.get_attribute('alt')
                    img_url = ele_img.get_attribute('src')
                    dict_posts[key] = {
                        'content': content,
                        'img_url': img_url
                    }
            if pre_post_num == len(dict_posts):
                print('sleep: 2 mins')
                sleep(120)
                browser.scroll_up()
            pre_post_num = len(dict_posts)

        return list(dict_posts.values())

    def get_user_posts(self, username, number=None):
        user_profile = self.get_user_profile(username)
        if not number:
            number = instagram_int(user_profile['post_num'])
        return self._get_posts(number)

    def get_latest_posts_by_tag(self, tag, num):
        url = '%s/explore/tags/%s/' % (InsCrawler.URL, tag)
        self.browser.get(url)
        return self._get_posts(num)