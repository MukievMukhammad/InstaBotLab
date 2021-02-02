import requests
import urllib.parse


def get_comments(query_hash, shortcode, pointer='', count=12):
    url = 'https://www.instagram.com/graphql/query/?query_hash={0}&variables=%7B%22shortcode%22%3A%22{1}%22%2C%22first%22%3A{2}%2C%22after%22%3A%22{3}%22%7D'\
        .format(
            urllib.parse.quote(query_hash),
            urllib.parse.quote(shortcode),
            count,
            urllib.parse.quote(pointer)
        )
    response = requests.get(
        url,
        params={
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'ig_did=396C024E-E9B0-4156-A7C6-74883545AC1F; mid=X8yyRQAEAAFXZ17UTf5PFimVzm5o; ig_nrcb=1; shbid=2224; shbts=1612248235.9215565; rur=ATN; csrftoken=yclATnvQYVonM00FL341ekcTyJxBuqtz',
            'referer': 'https://www.instagram.com/p/{0}/'.format(shortcode),
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'x-csrftoken': 'yclATnvQYVonM00FL341ekcTyJxBuqtz',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR1gwKfXH30fF1j7_mFkvNGMH168psFEy1WDEr78lqj_UfCF',
            'x-requested-with': 'XMLHttpRequest'
        },
    )
    if response.status_code == 200:
        data = response.json()['data']['shortcode_media']['edge_media_to_parent_comment']
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

    return data


def get_user_info(username):
    response = requests.get(
        'https://www.instagram.com/{0}/?__a=1'.format(username),
        params={
            'accept': '* / *',
            'accept - encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': 'https://www.instagram.com/p/Bw2aCOJh4Ca/',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'x-csrftoken': 'CBRgqVOwpXGDXXdFc7rcgJ4mI3xJOtdA',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR2peVxsS4zycPenoL3XbojrZGQDOXIWwn71QytID2YACrAc',
            'x-requested-with': 'XMLHttpRequest'
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


def get_commented_users():
    usernames = []
    has_next = True
    pointer = ''
    while has_next:
        response = get_comments(
            'bc3296d1ce80a24b1b6e40b1e72903f5',
            'BurVe2sF5RZ',
            pointer
            # 12
        )
        has_next = response['page_info']['has_next_page']
        if has_next:
            pointer = response['page_info']['end_cursor']
        comments = response['edges']
        usernames += [comment['node']['owner']['username'] for comment in comments]
    return usernames


def insert_users_to_csv(users):
    for username in users:
        user_info = get_user_info(username)
        f = open('bots.csv', 'w')
        f.write('{0}\n'.format(','.join(user_info)))
        f.close()


if __name__ == '__main__':
    # user_info = get_user_info('mukiev_maga')
    users = get_commented_users()
    insert_users_to_csv(users)
