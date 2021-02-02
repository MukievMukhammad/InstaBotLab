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


if __name__ == '__main__':
    abl_query = 'query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables=%7B%22shortcode%22%3A%22Bw2aCOJh4Ca%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFDUTRXZ0ZHRHBZa0ZZUnBkcnRaMlJvQm1WQkFsZ0VuZUczLXJkLW81Z2lEN1JIcVQ4dzRrWlludllfZmg0RHlULXZFYVhSaTNxTTNLTWhYS2NncWRhVw%3D%3D%22%7D'
    response = get_comments(
        'bc3296d1ce80a24b1b6e40b1e72903f5',
        'Bw2aCOJh4Ca',
        # 'QVFCU3pKUkJuRlRuNVFrX2x1cGFaalhuWEVzb2xiU0FtazQya3RGcUtMR2JLclp3WEk0bm9qd2dkY2pfZEFOMGEzXzJZaFlwYl9BZkdfZ2tfcENMQ2ltSQ==',
        # 12
    )
    print(response)
    pass
