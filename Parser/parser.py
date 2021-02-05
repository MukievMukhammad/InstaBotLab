import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import json
import requests
import time
import urllib.parse

from selenium import webdriver


def get_comments(query_hash, shortcode, pointer='', count=12):
    # url = 'https://www.instagram.com/graphql/query/?query_hash={0}&variables=%7B%22shortcode%22%3A%22{1}%22%2C%22first%22%3A{2}%2C%22after%22%3A%22{3}%22%7D'\
    #     .format(
    #         urllib.parse.quote(query_hash),
    #         urllib.parse.quote(shortcode),
    #         count,
    #         urllib.parse.quote(pointer)
    #     )
    # response = requests.get(
    #     url,
    #     params={
    #         'accept': '*/*',
    #         'accept-encoding': 'gzip, deflate, br',
    #         'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    #         'cookie': 'ig_did=396C024E-E9B0-4156-A7C6-74883545AC1F; mid=X8yyRQAEAAFXZ17UTf5PFimVzm5o; ig_nrcb=1; shbid=2224; shbts=1612248235.9215565; rur=ATN; csrftoken=yclATnvQYVonM00FL341ekcTyJxBuqtz',
    #         'referer': 'https://www.instagram.com/p/{0}/'.format(shortcode),
    #         'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    #         'sec-ch-ua-mobile': '?0',
    #         'sec-fetch-dest': 'empty',
    #         'sec-fetch-mode': 'cors',
    #         'sec-fetch-site': 'same-origin',
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    #         'x-csrftoken': 'yclATnvQYVonM00FL341ekcTyJxBuqtz',
    #         'x-ig-app-id': '936619743392459',
    #         'x-ig-www-claim': 'hmac.AR1gwKfXH30fF1j7_mFkvNGMH168psFEy1WDEr78lqj_UfCF',
    #         'x-requested-with': 'XMLHttpRequest'
    #     },
    # )
    # if response.status_code == 200:
    #     data = response.json()['data']['shortcode_media']['edge_media_to_parent_comment']
    #     print('Success')
    # elif response.status_code == 404:
    #     print('Not Found.')
    #     return
    # else:
    #     print('Something goes wrong')
    #     print()
    #     print(response.reason)
    #     print()
    #     print(response.text)
    #     return
    with open('json/{0}.json'.format(shortcode)) as f:
        data = json.load(f)['data']['shortcode_media']['edge_media_to_parent_comment']

    return data


def get_user_info(username):
    response = requests.get(
        'https://www.instagram.com/{0}/?__a=1'.format(username),
        params={
            'Accept': '*/*',
            'Referer': 'https://www.instagram.com/{0}/'.format(username),
            'Host': 'www.instagram.com',
            'Accept-Language': 'ru',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.43',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': 'hmac.AR2peVxsS4zycPenoL3XbojrZGQDOXIWwn71QytID2YACgHa',
            'X-Requested-With': 'XMLHttpRequest'
        },
    )
    if response.status_code == 200:
        data = response.json()['graphql']['user']
        print('Success')
    elif response.status_code == 404:
        print('Not Found.')
        return
    else:
        print('Something goes wrong')
        print()
        print(response.reason)
        print()
        print(response.text)
        return

    result = [
        '"' + data['biography'] + '"',
        str(data['edge_followed_by']['count']),
        str(data['edge_follow']['count']),
        '"' + data['full_name'] + '"',
        str(data['highlight_reel_count']),
        str(data['is_business_account']),
        str(data['business_category_name']),
        str(data['overall_category_name']),
        str(data['category_name']),
        str(data['is_private']),
        str(data['is_verified']),
        '"' + data['username'] + '"',
        '"' + str(data['connected_fb_page']) + '"',
        str(data['edge_owner_to_timeline_media']['count'])
    ]
    return result


def get_user_info_by_selenium(username, driver):
    driver.get("https://www.instagram.com/{0}/?__a=1".format(username))
    data = json.loads(driver.find_element(By.CSS_SELECTOR, "pre").text)['graphql']['user']
    # time.sleep(1)

    result = [
        str(data['biography']),
        str(data['edge_followed_by']['count']),
        str(data['edge_follow']['count']),
        str(data['full_name']),
        str(data['highlight_reel_count']),
        str(data['is_business_account']),
        str(data['business_category_name']),
        str(data['overall_category_name']),
        str(data['category_name']),
        str(data['is_private']),
        str(data['is_verified']),
        str(data['username']),
        str(data['connected_fb_page']),
        str(data['edge_owner_to_timeline_media']['count'])
    ]
    return result


def init_selenium():
    driver = webdriver.Chrome('/Users/user/Downloads/chromedriver')
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").click()
    driver.find_element(By.NAME, "username").send_keys("mansion_style")
    driver.find_element(By.NAME, "password").click()
    driver.find_element(By.NAME, "password").send_keys("A12QweR45")
    driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
    time.sleep(4)
    return driver


def get_commented_users(post_code):
    usernames = []
    has_next = True
    pointer = ''
    while has_next:
        response = get_comments(
            'bc3296d1ce80a24b1b6e40b1e72903f5',
            post_code,
            pointer
            # 12
        )
        has_next = response['page_info']['has_next_page']
        if has_next:
            pointer = response['page_info']['end_cursor']
        comments = response['edges']
        usernames += [comment['node']['owner']['username'] for comment in comments]
    return usernames


def get_liked_users_selenium(_driver, shortcode, pointer=""):
    url = "https://www.instagram.com/graphql/query/?" \
          "query_hash=d5d763b1e2acf209d62d22d184488e57&" \
          "variables=%7B%22" \
          "shortcode%22%3A%22{0}%22%2C%22" \
          "include_reel%22%3Atrue%2C%22" \
          "first%22%3A100%2C%22" \
          "after%22%3A%22{1}%22%7D".format(shortcode, pointer)
    _driver.get(url)
    data = json.loads(_driver.find_element(By.CSS_SELECTOR, "pre").text)['data']['shortcode_media']['edge_liked_by']
    _next = data['page_info']
    _users = [user['node']['username'] for user in data['edges']]
    return _users, _next


def insert_users_to_csv(_users, _driver):
    for username in _users:
        user_info = get_user_info_by_selenium(username, _driver)
        with open('bots.csv', "r") as infile:
            reader = list(csv.reader(infile))
            reader.insert(1, user_info)

        with open('bots.csv', "w") as outfile:
            writer = csv.writer(outfile)
            for line in reader:
                writer.writerow(line)


if __name__ == '__main__':
    driver = init_selenium()
    users = []
    pointer = ''
    has_next = True
    while has_next:
        urs, _next = get_liked_users_selenium(driver, 'Bw2aCOJh4Ca', pointer)
        users += urs
        has_next = _next['has_next_page']
        if has_next:
            pointer = _next['end_cursor']
    insert_users_to_csv(users, driver)
    print()
