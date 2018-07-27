from ditchbook import micropub

from datetime import datetime
from pytz import timezone, utc

import json
import re
import os
import conf


FILTERS = [
    re.compile(".* wrote on .*'s timeline."),
    re.compile(".* shared .*'s .*."),
    re.compile(".* shared (a|an) (group|quote|memory|event|link|post|Page)."),
    re.compile(".* shared (his|her) (post|video|album)."),
    re.compile(".* posted in .*."),
    re.compile(".* was (in|at) .*."),
    re.compile(".* was live in."),
    re.compile(".* updated the (group|event) photo in .*."),
    re.compile(".* was looking for recommendations.")
]

NOTE_EXPR = re.compile(".* published a note.")
PHOTO_EXPR = re.compile(".* (added|posted) .* (photo|photos).")
VIDEO_EXPR = re.compile(".* added .* new (video|videos).")


def apply_timezone(dt, default=utc):
    for start, stop, zone in conf.TIMEZONES:
        if start <= dt <= stop:
            return zone.localize(dt).astimezone(utc)

    return default.localize(dt).astimezone(utc)


def process_post(post):
    for expr in FILTERS:
        if expr.match(post.get('title', '')):
            return

    # get localized datetime and then convert to UTC
    dt = datetime.fromtimestamp(post['timestamp'])
    dt = apply_timezone(dt)

    # create MF2 container
    mf2 = {
        'type': ['h-entry'],
        'properties': {
            'published': [dt.isoformat(sep=' ')]
        }
    }

    # check to see if this is a "note"
    if NOTE_EXPR.match(post['title']):
        note = post['attachments'][0]['data'][0]['note']
        mf2['properties']['content'] = [note['text']]
        mf2['properties']['name'] = [note['title']]

    # handle photos
    elif PHOTO_EXPR.match(post['title']):
        if 'data' in post:
            mf2['properties']['content'] = [post['data'][0]['post']]

        mf2['properties']['photo'] = []
        for attachment in post['attachments']:
            for media in attachment['data']:
                mf2['properties']['photo'].append(
                    'export/%s' % media['media']['uri']
                )

    # handle videos
    elif VIDEO_EXPR.match(post['title']):
        if 'data' in post:
            mf2['properties']['content'] = [post['data'][0]['post']]

        if 'attachments' not in post:
            return

        mf2['properties']['video'] = []
        for attachment in post['attachments']:
            for media in attachment['data']:
                mf2['properties']['video'].append(
                    'export/%s' % media['media']['uri']
                )

    # handle standard status updates
    elif 'data' in post:
        mf2['properties']['content'] = [post['data'][0]['post']]

    else:
        return

    return mf2


def process_album(album):
    # get localized datetime and then convert to UTC
    dt = datetime.fromtimestamp(album['last_modified_timestamp'])
    dt = apply_timezone(dt)

    # create basic MF2 JSON structure
    mf2 = {
        'type': ['h-entry'],
        'properties': {
            'name': [album['name']],
            'published': [dt.isoformat(sep=' ')]
        }
    }

    # add "featured" photo, if present
    if 'cover_photo' in album:
        mf2['properties']['featured'] = [
            'export/' + album['cover_photo']['uri']
        ]

    # if the album has a caption, set it
    if 'description' in album:
        mf2['properties']['content'] = [
            album['description']
        ]

    # append the children to parent
    mf2['children'] = []
    for photo in album['photos']:
        child = {
            'type': ['h-entry'],
            'properties': {
                'photo': [
                    'export/' + photo['uri']
                ]
            }
        }

        # add photo caption, if available
        if 'description' in photo:
            child['properties']['content'] = [photo['description']]

        mf2['children'].append(child)

    return mf2
