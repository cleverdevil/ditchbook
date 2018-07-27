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


photo_tmpl = '''<div class="album-photo">
    <a href="%(photo_uri)s"><img src="%(photo_uri)s" width="600" height="600"></a>
    %(caption)s
</div>'''

caption_tmpl = '''<p>%(caption)s</p>'''


def process_album(album):
    mf2 = album.copy()
    mf2['properties']['photo'] = []
    content_parts = []

    # add the album caption
    album_caption = mf2['properties'].get('content', [None])[0]
    if album_caption:
        album_caption = replace_mentions(album_caption)
        content_parts.append(caption_tmpl % {'caption': album_caption})

    # iterate through the children and populate the body
    for child in mf2.get('children', []):
        uploaded_photo = micropub.upload(child['properties']['photo'][0])

        ns = {'photo_uri': uploaded_photo, 'caption': ''}
        caption = child['properties'].get('content', [None])[0]
        if caption:
            caption = replace_mentions(caption)
            ns['caption'] = caption_tmpl % {'caption': caption}

        content_parts.append(
            photo_tmpl % ns
        )

    del mf2['children']

    mf2['properties']['content'] = [ {'html': ''.join(content_parts)} ]

    # publish it
    micropub.publish(mf2)
