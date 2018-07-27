from ditchbook import micropub
from ditchbook.util import replace_mentions


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
