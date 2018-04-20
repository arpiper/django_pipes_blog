import re

TAGS = [
    {
        'raw': '######',
        're': '(?<!#)#{6}(?!#)',
        'name': 'H6',
        'tag': 'h6',
    },
    {
        'raw': '#####',
        're': '(?<!#)#{5}(?!#)',
        'name': 'H5',
        'tag': 'h5',
    },
    {
        'raw': '####',
        're': '(?<!#)#{4}(?!#)',
        'name': 'H4',
        'tag': 'h4',
    },
    {
        'raw': '###',
        're': '(?<!#)#{3}(?!#)',
        'name': 'H3',
        'tag': 'h3',
    },
    {
        'raw': '##',
        're': r'(?<!#)#{2}(?!#)',
        'name': 'H2',
        'tag': 'h2',
    },
    {
        'raw': '#',
        're': '(?<!#)#{1}(?!#)',
        'name': 'H1',
        'tag': 'h1',
    },
    {
        'raw': '**',
        're': '(?<!\*)\*{2}(?!\*)',
        'name': 'B',
        'tag': 'b',
    },
    {
        'raw': '*',
        're': '(?<!\*)\*{1}(?!\*)',
        'name': 'I',
        'tag': 'i',
    },
    {
        'raw': '__',
        're': '(?<!_)_{2}(?!_)',
        'name': 'B',
        'tag': 'b',
    },
    {
        'raw': '_',
        're': '(?<!_)_{1}(?!_)',
        'name': 'I',
        'tag': 'i',
    },
    {
        'raw': '[',
        're': '(?<!\[)\[{1}(?!\[)',
        'name': 'A',
        'tag': 'a',
    },
    {
        'raw': '(',
        're': '(?<!\()\({1}(?!\()',
        'name': 'A',
        'tag': 'a',
    },
    {
        'raw': '```',
        're': '(?<!`)`{3}(?!`)',
        'name': 'CODE',
        'tag': 'code',
    },
    {
        'raw': '`',
        're': '(?<!`)`{1}(?!`)',
        'name': 'CODE',
        'tag': 'code',
    }
]
HEADERS = ['######','#####','####','###','##','#',]
WRAPPERS = ['**','__','*','_','[','(','```','`',]

def parseText(text):
    split = text.split()
    new_text = []
    formatted = text
    matches = {}
    for tag in TAGS:
        #formatted = re.sub(pattern=tag['re'], repl=tag['tag'], string=formatted)
        indices = [m.start() for m in re.finditer(tag['re'], formatted)]
        if len(indices) > 0:
            matches[tag['raw']] = tag
            matches[tag['raw']]['indices'] = indices
            if tag['raw'] in HEADERS:
                for i in indices:
                    formatted = '{}<{}>{}'.format(formatted[:i], tag['tag'], formatted[i+len(tag['raw']):])
                    end = formatted[i:].find('\r\n')
                    formatted = '{}</{}>{}'.format(formatted[:end+1], tag['tag'], formatted[end:])
            if tag['raw'] in WRAPPERS:
                for idx,i in enumerate(indices):
                    adj = idx * ((len(tag['tag']) + 2) - len(tag['raw']))
                    if idx % 2 == 1:
                        formatted = '{}<{}>{}'.format(
                            formatted[:i+adj], tag['tag'], formatted[i+adj+len(tag['raw']):]
                        )
                    else:
                        formatted = '{}</{}>{}'.format(
                            formatted[:i+adj+1], tag['tag'], formatted[i+adj:]
                        )


    return formatted


##
# return dictionary with the post date in form {year,month,day}
##
def getPostDates(post):
    return {
        'year': post.date_published.year,
        'month': post.date_published.strftime('%m'),
        'day': post.date_published.strftime('%d'),
    }


##
# Prep post list for for simpler consumption in the templates 
##
def preparePostList(post_list):
    posts = []
    for p in post_list:
        post = {
            'title': p.title,
            'date_published': p.date_published,
            'textblock_set': p.textblock_set.all(),
            'slug': p.slug,
            'tags': p.tags.split(' '),
            'text': p.text,
            'images': p.postimage_set.all(),
        }
        post.update(getPostDates(p))
        posts.append(post)
    return posts
