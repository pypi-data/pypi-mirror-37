from lxml import etree
from collections import OrderedDict

def parseDict(obj, root, current_field=''):

    if type(root) == str:
        data = etree.Element(root)
    elif isinstance(root, etree._Element):
        data = root

    if type(obj) == OrderedDict:
        for k, el in obj.items():

            if type(el) == list:
                for el2 in el: 
                    dict_raw_data = parseDict(el2, k)
                    data.append(dict_raw_data)
            else:
                dict_raw_data = parseDict(el, k)

                if isinstance(dict_raw_data, etree._Element):
                    data.append(dict_raw_data)

        return data
    elif hasattr(obj, '__dict__'):
        for k, el in obj.__dict__.iteritems():
            if (not el.startswith('__') and not callable(el)):
                dict_raw_data = parseDict(el, k)
                data.append(dict_raw_data)
        return data    
    else:
        result = etree.Element(root)

        if type(obj) == str:
            result.text = etree.CDATA(unicode(obj))
        else:
            result.text = unicode(obj)
        return result
