import requests
import json

pushshift_api_url = 'https://api.pushshift.io/reddit/search/'

# returns JSON


def get_data(sub_or_comment, subreddit, size):
    res = requests.get(pushshift_api_url +
                       f'{sub_or_comment}/?subreddit={subreddit}&size={size}')
    return res.json()['data']


def post_data(subreddit, size):
    return get_data('submission', subreddit, size)


def comment_data(subreddit, size):
    return get_data('comment', subreddit, size)


def filter_data(data, criteria=None):
    mydict = dict()
    counter = 0
    for item in data:
        if criteria in item['url']:
            if not 'shorts' in item['url']:
                mydict[counter] = {
                    'title': item['title'],
                    'url': item['url'],
                }
                counter += 1
        #     mydict[counter] = {
        #         'title': data[item]['title'],
        #         'url': data[item]['url'],
        #     }
        #     counter += 1
    return json.dumps(mydict, indent=4)

    # NEED TO MAKE LAYER ABOVE THIS FOR MULTIPLE KEYS
    # def filter(data, key, criteria=None):
    #     mydict = dict()
    #     '''
    #         mydict = item[key]s if item[key] contains criteria
    #     '''
    #     if type(criteria) is list:
    #         mydict = {i: {key: item[key] for item in data if any(
    #             c in item[key] for c in criteria) for i in range(0, len([item[key] for item in data if any(c in item[key] for c in criteria)]))}}
    #     elif type(criteria) is str:
    #         for i in range(0, len([item[key] for item in data if criteria in item[key]])):
    #             mylist = [item[key] for item in data if criteria in item[key]]
    #             mydict[i] = {key: mylist[i]}
    #         # mydict = {i: {key: item[key] for item in data if criteria in item[key]}
    #         #            for i in range(0, len([item[key] for item in data if criteria in item[key]]))}
    #     elif type(criteria) is None:
    #         mydict = {i: {item[key] for item in data}
    #                   for i in range(0, len([item[key] for item in data]))}
    #     return mydict

    # def filter_urls(data, criteria=None):
    #     return filter(data, 'url', criteria=criteria)
