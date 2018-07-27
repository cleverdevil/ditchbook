from ditchbook import micropub

import os
import json
import re
import conf


MENTION_EXPR = re.compile("@\[\d+:\d+:(.*)]")


def replace_mentions(content):
    def f(match):
        name = match.groups()[0]
        return conf.MENTION_MAP.get(name, name)
    return re.sub(MENTION_EXPR, f, content)


def process_post(post):
    mf2 = post.copy()

    # skip videos for now
    if mf2['properties'].get('video'):
        return

    # upload photos, if any
    photos = []
    for photo in post['properties'].get('photo', []):
        photos.append(micropub.upload(photo))
    if len(photos):
        mf2['properties']['photo'] = photos

    # prepare content
    if len(mf2['properties'].get('content', [])):
        mf2['properties']['content'] = [
            {'html': replace_mentions(mf2['properties']['content'][0])}
        ]

    # publish it
    micropub.publish(mf2)
