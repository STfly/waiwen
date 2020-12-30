import requests
import execjs
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url = 'https://translate.googleapis.com/translate_a/t'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Referer': 'https://www.sciencemag.org/'
}
ctx = execjs.compile("""
    function TL(a) {
    var k = "";
    var b = 406644;
    var b1 = 3293161072;

    var jd = ".";
    var $b = "+-a^+6";
    var Zb = "+-3^+b+-f";

    for (var e = [], f = 0, g = 0; g < a.length; g++) {
        var m = a.charCodeAt(g);
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
        e[f++] = m >> 18 | 240,
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
        e[f++] = m >> 6 & 63 | 128),
        e[f++] = m & 63 | 128)
    }
    a = b;
    for (f = 0; f < e.length; f++) a += e[f],
    a = RL(a, $b);
    a = RL(a, Zb);
    a ^= b1 || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return a.toString() + jd + (a ^ b)
};

function RL(a, b) {
    var t = "a";
    var Yb = "+";
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2),
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
    }
    return a
}
""")
def translate(word):

    body = {'q': word}
    tk = ctx.call("TL", body['q'])
    form = {
        'anno':	'3',
        'client': 'te_lib',
        'format': 'html',
        'v': '1.0',
        'key':	'AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw',
        'logld': 'vTE_20201130_00',
        'sl': 'en',
        'tl': 'zh-CN',
        'tc': '6',
        'sr': '1',
        'tk':	tk,
        'mode':	'1'
    }
    try:
        response = requests.post(url=url, headers=headers, params=form, data=body, verify=False)
        if response.status_code == 200:
            # print(response.json())
            # 整段话翻译内容在<b></b>之间
            # 一句话直接获得

            content = re.findall('<b>(.*?)</b>', response.json())
            if content == []:
                return response.json()
            else:
                return ''.join(content)
    except:
        print('翻译失败')
        return ''
# word = ' Plan to map oil in Alaska’s Arctic refuge ignores environmental risks, critics say'
# data = translate(word)
# print(data)

