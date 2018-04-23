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
        're': '(?<!#)#{2}(?!#)',
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
BLOCKTAGS = ['<h1>','<h2>','<h3>','<h4>','<h5>','<h6>']

def parseText(text):
    #split = text.split()
    #new_text = []
    formatted = text
    #matches = {}
    for tag in TAGS:
        indices = [m.start() for m in re.finditer(tag['re'], formatted)]
        if len(indices) > 0:
            #matches[tag['raw']] = tag
            #matches[tag['raw']]['indices'] = indices
            if tag['raw'] in HEADERS:
                for i in indices:
                    formatted = '{}<{}>{}'.format(formatted[:i], tag['tag'], formatted[i+len(tag['raw']):])
                    end = formatted[i:].find('\r\n')
                    if end > -1:
                        end += i
                        formatted = '{}</{}>{}'.format(formatted[:end], tag['tag'], formatted[end+2:])
                    else:
                        end
                        formatted = '{}</{}>'.format(formatted, tag['tag'])
            if tag['raw'] in WRAPPERS:
                for idx,i in enumerate(indices):
                    adj = idx * ((len(tag['tag']) + 2) - len(tag['raw']))
                    if idx % 2 == 0:
                        formatted = '{}<{}>{}'.format(
                            formatted[:i+adj], tag['tag'], formatted[i+adj+len(tag['raw']):]
                        )
                    else:
                        formatted = '{}</{}>{}'.format(
                            formatted[:i+adj], tag['tag'], formatted[i+adj+len(tag['raw']):]
                        )
    doublespace = formatted.split('\r\n\r\n')
    temp = []
    for paragraph in doublespace:
        splits = splitHeaders(paragraph)
        if len(splits) == 0:
            temp.append('<p>{}</p>'.format(paragraph))
        else:
            temp.extend(splits)
    formatted = ''.join(temp)
    return formatted


def splitHeaders(text):
    splits = []
    if len(text) == 0:
        return splits
    # the text is too short to contain proper open/close header tags.
    if len(text) < 9:
        return ['<p>{}</p>'.format(text)]
    for blocktag in BLOCKTAGS:
        # the text value passed was the header tag line only.
        if text[:4] == blocktag and text[-3:] == blocktag[-3:]:
            return [text]
        #wrap = wrap and (blocktag not in paragraph)
        if blocktag in text:
            i = text.find(blocktag)
            start = splitHeaders(text[:i])
            end = splitHeaders(text[i:])
            splits.extend(start)
            splits.extend(end)
            return splits
    return ['<p>{}</p>'.format(text)]


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
