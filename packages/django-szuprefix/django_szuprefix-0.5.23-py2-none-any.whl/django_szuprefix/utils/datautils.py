# -*- coding:utf-8 -*-
import re
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile
from datetime import date, datetime
from django.db.models import Model, QuerySet
from collections import OrderedDict


class JSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, (FieldFile,)):
            return o.name
        if isinstance(o, Model):
            return o.pk
        if isinstance(o, QuerySet):
            return [self.default(a) for a in o]
        return super(JSONEncoder, self).default(o)


def jsonSpecialFormat(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, Model):
        return v.pk
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, (FieldFile,)):
        return {'name:': v.name, 'url': v.url}
    return v


def model2dict(model, fields=[], exclude=[]):
    return dict([(attr, jsonSpecialFormat(getattr(model, attr)))
                 for attr in [f.name for f in model._meta.fields]
                 if not (fields and attr not in fields or exclude and attr in exclude)])


def queryset2dictlist(qset, fields=[], exclude=[]):
    return [model2dict(m, fields, exclude) for m in qset]


def queryset2dictdict(qset, fields=[], exclude=[]):
    return dict([(m.pk, model2dict(m, fields, exclude)) for m in qset])


def node2dict(node):
    children = node.getchildren()
    if not children:
        return node.text
    d = {}
    for n in children:
        d[n.tag] = node2dict(n)
    return d


def str2int(s):
    try:
        return int(s)
    except ValueError:
        try:
            return int(re.finditer(r'\d+', s).next().group())
        except:
            return None


def xml2dict(xml):
    from lxml import etree
    return node2dict(etree.fromstring(xml))


def dict2xml(d):
    ks = d.keys()
    ks.sort()
    return u"\n".join(["<%s><![CDATA[%s]]></%s>" % (k, d[k], k) for k in ks if d[k]])


def dictlist2arraylist(dict_data, field_names):
    return [[row[fn] for fn in field_names] for row in dict_data]


def node2model(node, model, timestamp_fields=[], name_format_func=None):
    if name_format_func == None:
        name_format_func = lambda x: x[0].lower() + x[1:]
    for cnode in node.getchildren():
        tg = name_format_func(cnode.tag)
        tx = cnode.text
        if tg in timestamp_fields:
            tx = datetime.fromtimestamp(int(tx))
        setattr(model, tg, tx)


def xml2model(xml, model):
    from lxml import etree
    return node2model(etree.fromstring(xml))


def re_group_split(r, s):
    g = []
    p = 0
    t = None
    for m in r.finditer(s):
        g.append((t, s[p:m.start()]))
        p = m.end()
        t = m.groups()
    g.append((t, s[p:]))
    return g


def count_group_by(data, groups):
    """

      dl = [
         {"f1":"a1","f2":"b1","f3":"c1"},
         {"f1":"a1","f2":"b2","f3":"c1"},
         {"f1":"a1","f2":"b2","f3":"c2"},
         {"f1":"a1","f2":"b2","f3":"c2"},
         {"f1":"a2","f2":"b1","f3":"c2"},
         {"f1":"a2","f2":"b1","f3":"c2"},
         {"f1":"a2","f2":"b1","f3":"c2"},
         {"f1":"a2","f2":"b2","f3":"c2"},
         {"f1":"a2","f2":"b2","f3":"c1"},
      ]

    >>> count_group_by(dl,["f2"])
    {('b1',): 4, ('b2',): 5}

    >>> count_group_by(dl,["f2","f3"])
    {('b1', 'c2'): 3, ('b1',): 4, ('b1', 'c1'): 1, ('b2',): 5, ('b2', 'c1'): 2, ('b2', 'c2'): 3}

    >>> count_group_by(dl,["f1","f2"])
    {('a1', 'b2'): 3, ('a1',): 4, ('a1', 'b1'): 1, ('a2', 'b2'): 2, ('a2',): 5, ('a2', 'b1'): 3}

    >>> count_group_by(dl,["f1","f2","f3"])
    {('a1', 'b2', 'c1'): 1, ('a2', 'b2', 'c1'): 1, ('a2', 'b1', 'c2'): 3, ('a2',): 5, ('a2', 'b2', 'c2'): 1, ('a1', 'b2', 'c2'): 2, ('a1', 'b2'): 3, ('a1',): 4, ('a1', 'b1'): 1, ('a2', 'b2'): 2, ('a1', 'b1', 'c1'): 1, ('a2', 'b1'): 3}


    >>> cr = count_group_by(dl,["f1","f2","f3"])
    >>> for k in sorted(cr.keys()):
    ...     print "\t"*len(k),k[-1], cr[k]
    ...
    """
    res = {}
    gc = len(groups)
    for d in data:
        for i in range(gc):
            k = tuple([d.get(g) for g in groups[:i + 1]])
            res.setdefault(k, 0)
            res[k] += 1
    return res


def str2dict(s, line_spliter='\n', key_spliter=':'):
    d = OrderedDict()
    s = s.strip()
    if not s:
        return d
    for a in s.split(line_spliter):
        a = a.strip()
        if not a:
            continue
        p = a.find(key_spliter)
        if p == -1:
            d[a] = ""
        else:
            d[a[:p].strip()] = a[p + 1:].strip()
    return d


def dict2str(d, line_spliter='\n', key_spliter=':'):
    return line_spliter.join(["%s%s%s" % (k, key_spliter, v) for k, v in d.iteritems()])


def not_float(d):
    if isinstance(d, (float,)):
        return int(d)
    return d


def phonemask(value):
    if not value:
        return value
    l = list(value.replace(" ", ""))
    l[3:7] = "****"
    return "".join(l)


def strQ2B(ustring):
    """全角转半角"""
    if not ustring:
        return ustring
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288 or inside_code == 8197:  # 全角空格直接转换
            inside_code = 32
        if inside_code == 12290:  # 。 -> .
            inside_code = 46
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring


def strB2Q(ustring):
    """半角转全角"""
    if not ustring:
        return ustring
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring


def list2csv(data, line_spliter=u"\n", field_spliter=u"\t"):
    s = []
    for line in data:
        s.append(field_spliter.join([unicode(v) for v in line]))
    return line_spliter.join(s)


def exclude_dict_keys(d, *args):
    return dict([(k, v) for k, v in d.items() if k not in args])


def choices_map_reverse(choices):
    return dict([(v, k) for k, v in choices])


def clear_dict_keys(d, *args):
    for a in args:
        if a in d:
            d.pop(a)


common_used_numerals = {u'零': 0, u'一': 1, u'二': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9,
                        u'十': 10, u'百': 100, u'千': 1000, u'万': 10000, u'亿': 100000000}


def cn2digits(uchars_cn):
    s = uchars_cn
    if not s:
        return 0
    for i in [u'亿', u'万', u'千', u'百', u'十']:
        if i in s:
            ps = s.split(i)
            lp = cn2digits(ps[0])
            if lp == 0:
                lp = 1
            rp = cn2digits(ps[1])
            # print i,s,lp,rp
            return lp * common_used_numerals.get(i, 0) + rp
    return common_used_numerals.get(s[-1], 0)


def auto_code(n):
    from unidecode import unidecode
    import re
    add_space = lambda s: re.sub(r"([\s\w])([^\s\w])", r"\1 \2", s)
    return "".join([a[0] for a in unidecode(add_space(n)).split(" ") if a]).upper()


def try_numeric_dict(d):
    for k, v in d.items():
        try:
            d[k] = int(v)
        except ValueError:
            try:
                d[k] = float(v)
            except ValueError:
                pass
    return d


def split_test_case(s):
    cs = []
    rs = []
    for l in s.split("\n"):
        ps = l.split("=>")
        a = try_numeric_dict(str2dict(ps[0], line_spliter=" "))
        b = len(ps) > 1 and try_numeric_dict(str2dict(ps[1], line_spliter=" ")) or {}
        rs.append(a)
        cs.append(b)
    return rs, cs


RE_SPACES = re.compile(r"\s+")


def space_split(s):
    ss = RE_SPACES.split(s)
    if ss[0] == '':
        del ss[0]
    if len(ss) > 0 and ss[-1] == '':
        del ss[-1]
    return ss


def ischildof(obj, cls):
    try:
        for i in obj.__bases__:
            if i is cls or isinstance(i, cls):
                return True
        for i in obj.__bases__:
            if ischildof(i, cls):
                return True
    except AttributeError:
        return ischildof(obj.__class__, cls)
    return False


def filter_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, unicode(desstr))

