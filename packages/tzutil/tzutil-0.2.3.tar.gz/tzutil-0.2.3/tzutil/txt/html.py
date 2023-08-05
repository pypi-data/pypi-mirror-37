import re
from tzutil.unescape import unescape
from html import escape


def txt2html(txt):
    if not txt:
        return ''

    r = []
    for i in txt.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if i.strip():
            r.append(escape(i))

    return "<p>" + "</p><p>".join(r) + "</p>"


def html2txt_brief(data):
    data = data.replace("</p>", "\n").replace("<br>",
                                              "\n").replace("</div>", "\n")
    p = re.compile(r'<.*?>')
    return unescape(p.sub('', data)).strip()


def cnenlen(s):
    return len(s.encode('gb18030', 'ignore')) // 2


def cnencut(s, length):
    s = s.encode('gb18030', 'ignore')[:length * 2].decode('gb18030', 'ignore')
    return s


def cnenoverflow(s, length):
    txt = cnencut(s, length)
    if txt != s:
        txt = '%s … …' % txt.rstrip()
        has_more = True
    else:
        has_more = False
    return txt, has_more


def txt_rstrip(txt):
    return '\n'.join(
        map(
            str.rstrip,
            txt.replace('\r\n', '\n')
            .replace('\r', '\n').rstrip('\n ')
            .split('\n')
        )
    )


RE_NUMBER_STR = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
RE_NUMBER = re.compile(
    RE_NUMBER_STR,
    re.VERBOSE
)


def remove_number(txt):
    return RE_NUMBER.sub('-', txt)


if __name__ == "__main__":
    print(remove_number('啊3'))
    txt = "；，（）。"
    print(txt)
    print(全角转半角(txt))
    # print(html2txt_brief(
    #     """<p>来源｜21金融圈 周末晚上在我百无聊赖时候，朋友安利了一部获得今年奥斯卡最佳剧本奖《大空头》给我。看完后发现它</p>来源 : 投资世界 · 新财富杂志 ( http://htm.space/184137 )"""))
