import re
from .models import PostImage

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
        'close': ')',
    },
    {
        'raw': '(',
        're': '(?<!\()\({1}(?!\()',
        'name': 'A',
        'tag': 'a',
        'close': ']',
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
    },
    {
        'raw': '{{',
        're': '(?<!\{)\{{2}(?!\{)',
        'name': 'IMG',
        'tag': 'img',
        'close': '}}'
    },
]


HEADERS = ['######','#####','####','###','##','#',]
INLINES = ['**','__','*','_','```','`',]
LINKS = ['[', '(']
IMAGES = ['{{']
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
                    formatted = insertHeader(tag, i, formatted)
            if tag['raw'] in INLINES:
                for idx,i in enumerate(indices):
                    formatted = insertInlines(tag, i, formatted, idx)
            if tag['raw'] in LINKS:
                for i in indices:
                    end = formatted[i:].find(tag['close']) + i + 1 # include the closing bracket
                    formatted = insertLink(i, end, formatted)
            if tag['raw'] in IMAGES:
                for i in indices:
                    formatted = insertImage(i, formatted)

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
            i2 = text.find(blocktag[-3:], i+4) + 3
            end = splitHeaders(text[i2:])
            splits.extend(start + [text[i:i2]] + end)
            return splits
    return ['<p>{}</p>'.format(text)]


def insertLink(start, end, text):
    link = text[start+1:end-1]
    link_text = link[:link.find(']')]
    link_href = link[link.find('(')+1:]
    l = '<a href="{}" target="_blank" rel="noopener">{}</a>'
    l = l.format(link_href, link_text)
    return '{}{}{}'.format(text[:start], l, text[end:])


def insertHeader(tag, i, text):
    # insert the opening tag adjusting for the markdown style tag removal
    text = '{}<{}>{}'.format(text[:i], tag['tag'], text[i+len(tag['raw']):])
    end = text[i:].find('\r\n')
    if end > -1:
        end += i
        # insert closing tag adjusting to remove the carriage return/newline characters
        return '{}</{}>{}'.format(text[:end], tag['tag'], text[end+2:])
    return '{}</{}>'.format(text, tag['tag'])


def insertInlines(tag, i, text, idx):
    adj = idx * ((len(tag['tag']) + 2) - len(tag['raw']))
    if idx % 2 == 0:
        return '{}<{}>{}'.format(text[:i+adj], tag['tag'], text[i+adj+len(tag['raw']):])
    return '{}</{}>{}'.format(text[:i+adj], tag['tag'], text[i+adj+len(tag['raw']):])


def insertImage(i, formatted):
    end = formatted.find('}}', i)
    tag = formatted[i:end+2]
    print(tag)
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
