import json
import requests
import sys
import time


def prompt():
    prompt_config = {}

    print("Input the YouTube channel ID. This can be found in the URL when in YouTube Studio.")
    prompt_config['channelId'] = input("Channel ID: ")

    print("\nInput the :path Request Header. This can be found in developer tools as explained in the README.")
    prompt_config['path'] = input("Path Header: ")

    print("\nInput the authorization Request Header. This can be found in developer tools as explained in the README.")
    prompt_config['authorization'] = input("Authorization Header: ")

    print("\nInput the cookie Request Header. This can be found in developer tools as explained in the README.")
    prompt_config['cookie'] = input("Cookie Header: ")

    print("\nInput the Session Token. This can be found in developer tools as explained in the README.")
    prompt_config['token'] = input("Session Token: ")

    print("\nDo you wish to opt out of Remixes/Shorts for all videos, even those you have explicitly opted into?")
    print("By default, this program will only opt you out of videos in the default state (which should be most).")
    print("Input ALL for all videos or anything else/nothing for the default behaviour.")
    prompt_config['unmixWhich'] = input("Unmix which? (DEFAULT/ALL): ")

    print("\nAll required input received! Beginning operation.\n")

    return prompt_config


def prepare_config(_input_config):
    output_config = {
        'channelId': _input_config['channelId'],
        'origin': "https://studio.youtube.com",
        'path': _input_config['path'].strip().replace(':path: ', '').replace('"', ''),
        'authorization': _input_config['authorization'].strip().replace('authorization: ', '').replace('"', ''),
        'cookie': _input_config['cookie'].strip().replace('cookie: ', '').replace('"', ''),
        'token': _input_config['token'].strip().replace('"', '')
    }

    output_config['api_key'] = \
        output_config['path'][output_config['path'].index('key') + 4:]  # Gets the API key from the Path parameter

    unmix_which = _input_config['unmixWhich'].strip()
    if unmix_which == 'ALL':
        output_config['unmixWhich'] = 'ALL'
    else:
        output_config['unmixWhich'] = 'DEFAULT'

    return output_config


def list_videos(_config, _page_token=None):
    list_videos_url = 'https://studio.youtube.com/youtubei/v1/creator/list_creator_videos'
    list_videos_params = {
        'alt': 'json',
        'key': _config['api_key']
    }
    list_videos_data = {
        "filter": {
            "and": {
                "operands": [
                    {
                        "channelIdIs": {
                            "value": _config['channelId']
                        }
                    },
                    {
                        "videoOriginIs": {
                            "value": "VIDEO_ORIGIN_UPLOAD"
                        }
                    }
                ]
            }
        },
        "order": "VIDEO_ORDER_DISPLAY_TIME_DESC",
        "pageSize": 50,
        "context": {
            "client": {
                "clientName": 62,
                "clientVersion": "1.20210503.02.00",
                "hl": "en-GB",
                "gl": "CA",
                "experimentsToken": "",
                "utcOffsetMinutes": -240
            },
            "request": {
                "returnLogEntry": True,
                "internalExperimentFlags": []
            }
        }
    }
    if _page_token is not None:
        list_videos_data['pageToken'] = _page_token
    list_videos_headers = {
        "referer": "https://studio.youtube.com/",
        "content-type": "application/json",
        "authorization": _config['authorization'],
        "origin": _config['origin'],
        "cookie": _config['cookie']
    }

    list_videos_request = requests.post(
        url=list_videos_url, headers=list_videos_headers, params=list_videos_params, data=json.dumps(list_videos_data))

    list_videos_json = list_videos_request.json()
    if not list_videos_json.get('videos'):
        print(f'Error listing videos: {json.dumps(list_videos_json)}')
        sys.exit(1)
    else:
        videos = list_videos_json['videos']
    next_page_token = list_videos_json.get('nextPageToken')

    return videos, next_page_token


def get_videos(_config, _video_ids):
    get_videos_url = 'https://studio.youtube.com/youtubei/v1/creator/get_creator_videos'
    get_videos_params = {
        'alt': 'json',
        'key': _config['api_key']
    }
    get_videos_data = {
        "context": {  # Required nonsense
            "client": {
                "clientName": 62,
                "clientVersion": "1.20210503.02.00",
                "hl": "en-GB",
                "gl": "CA",
                "experimentsToken": "",
                "utcOffsetMinutes": -240
            },
            "request": {
                "returnLogEntry": True,
                "internalExperimentFlags": []
            }
        },
        "failOnError": True,  # Sound like a good thing to do
        "videoIds": _video_ids,  # Video IDs to request details about
        "mask": {
            "title": True,  # Requests the title in the videos response
            "remix": {
                "all": True  # Requests the remixes/shorts setting in the videos response
            }
        }
    }

    get_videos_headers = {
        "referer": "https://studio.youtube.com/",
        "content-type": "application/json",
        "authorization": _config['authorization'],
        "origin": _config['origin'],
        "cookie": _config['cookie']
    }

    get_videos_request = requests.post(
        url=get_videos_url, headers=get_videos_headers, params=get_videos_params, data=json.dumps(get_videos_data))

    get_videos_json = get_videos_request.json()
    if not get_videos_json.get('videos'):
        print(f'Error getting videos: {json.dumps(get_videos_json)}')
        sys.exit(1)
    else:
        videos = get_videos_json['videos']

    return videos


def update_video(_config, _video_id):
    update_video_url = 'https://studio.youtube.com/youtubei/v1/video_manager/metadata_update'
    update_video_params = {
        'alt': 'json',
        'key': _config['api_key']
    }
    update_video_data = {
        "encryptedVideoId": _video_id,
        "remix": {
            "operation": "MDE_REMIX_UPDATE_OPERATION_SET",
            "newRemixSourceOption": "MDE_REMIX_SOURCE_OPTION_OPT_OUT_AND_MUTE_DERIVATIVES"
        },
        "context": {
            "client": {
                "clientName": 62,
                "clientVersion": "1.20210503.02.00",
                "hl": "en-GB",
                "gl": "CA",
                "experimentsToken": "",
                "utcOffsetMinutes": -240
            },
            "request": {
                "returnLogEntry": True,
                "internalExperimentFlags": [],
                "sessionInfo": {
                    "token": _config['token']
                }
            }
        }
    }
    update_video_headers = {
        "referer": "https://studio.youtube.com/",
        "content-type": "application/json",
        "authorization": _config['authorization'],
        "origin": _config['origin'],
        "cookie": _config['cookie']
    }

    update_video_request = requests.post(url=update_video_url, headers=update_video_headers, params=update_video_params,
                                         data=json.dumps(update_video_data))

    result = update_video_request.json()['remix']['success']

    if not result:
        print(f'Error opting out of remixes/shorts for video ID: {_video_id}. Please try again or process manually.')
    else:
        print(f'Successfully opted out of remixes/shorts for video ID: {_video_id}!')


def main(_config):
    next_page_token = None
    while True:
        listed_videos, next_page_token = list_videos(_config, next_page_token)
        listed_video_ids = []
        for video in listed_videos:
            listed_video_ids.append(video["videoId"])

        got_videos = get_videos(_config, listed_video_ids)

        video_ids_to_fix = []
        for video in got_videos:
            if video['remix'].get('remixSourceOption') is None:
                remix_status = 'DEFAULT'
                video_ids_to_fix.append(video["videoId"])
            elif video['remix']['remixSourceOption'] == 'REMIX_SOURCE_OPTION_OPT_IN':
                remix_status = 'OPT_IN'
                if _config['unmixWhich'] == 'ALL':  # Only opt out videos that were explicitly opted-in if desired
                    video_ids_to_fix.append(video["videoId"])
            elif video['remix']['remixSourceOption'] == 'REMIX_SOURCE_OPTION_OPT_OUT_AND_MUTE_DERIVATIVES':
                remix_status = 'OPT_OUT'
            else:
                remix_status = 'UNKNOWN'
            print(f'Found video with ID {video["videoId"]} and Title {video["title"]} - Remix status: {remix_status}')

        for video_id in video_ids_to_fix:
            update_video(_config, video_id)
            time.sleep(1)  # Don't hammer the YouTube update API too hard...

        if not next_page_token:
            break
        else:
            time.sleep(3)  # Don't hammer the YouTube list API too hard...

    input('All done! Press Enter to continue...')


if __name__ == "__main__":
    input_config = prompt()
    prepared_config = prepare_config(input_config)
    main(prepared_config)
