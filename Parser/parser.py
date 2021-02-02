import requests
import urllib.parse


def get_comments(query_hash, shortcode, pointer='', count=12):
    response = requests.get(
        'https://www.instagram.com/graphql/query/?query_hash={0}&variables=%7B%22shortcode%22%3A%22{1}%22%2C%22first%22%3A{2}%2C%22after%22%3A%22{3}%22%7D'
            .format(
            urllib.parse.quote(query_hash),
            urllib.parse.quote(shortcode),
            count,
            urllib.parse.quote(pointer)
        ),
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
        data = response.json()['data']['shortcode_media']['edge_media_to_parent_comment']
        print('Successful')
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


def get_commented_users():
    usernames = []
    has_next = True
    pointer = ''
    while has_next:
        response = get_comments(
            'bc3296d1ce80a24b1b6e40b1e72903f5',
            'Bw2aCOJh4Ca',
            pointer
            # 12
        )
        has_next = response['page_info']['has_next_page']
        if has_next:
            pointer = response['page_info']['end_cursor']
        comments = response['edges']
        usernames += [comment['node']['owner']['username'] for comment in comments]
    return usernames


if __name__ == '__main__':
    usernames = get_commented_users()
    for username in usernames:
        
