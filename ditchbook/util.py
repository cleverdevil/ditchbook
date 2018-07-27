import re
import conf


MENTION_EXPR = re.compile("@\[\d+:\d+:(.*)]")

def replace_mentions(content):
    def f(match):
        name = match.groups()[0]
        return conf.MENTION_MAP.get(name, name)
    return re.sub(MENTION_EXPR, f, content)


