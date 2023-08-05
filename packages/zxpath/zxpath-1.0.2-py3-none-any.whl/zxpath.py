# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zxpath.py
   Author :       Zhang Fan
   date：         18/10/12
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from lxml import etree


class _base_library:
    @staticmethod
    def get_once(result, default=None):
        if result:
            return result[0]
        return default

    # region xpath原始查询代码
    @staticmethod
    def xpath_once(node, code, default=None):
        return _base_library.get_once(node.xpath('{}[1]'.format(code)), default=default)

    @staticmethod
    def xpath_all(node, code):
        return node.xpath(code)

    # endregion

    # region 比较判断
    @staticmethod
    def is_element(obj):
        return isinstance(obj, etree._Element) or \
               isinstance(obj, etree._ElementUnicodeResult) or \
               isinstance(obj, etree._Comment)

    @staticmethod
    def is_node_element(obj):
        # 判断对象是否为元素节点
        return isinstance(obj, etree._Element)

    @staticmethod
    def is_text_element(obj):
        # 判断对象是否为文本节点
        return isinstance(obj, etree._ElementUnicodeResult)

    @staticmethod
    def is_comment(obj):
        return isinstance(obj, etree._Comment)

    # endregion

    # region 转换获取
    @staticmethod
    def to_etree(text):
        return etree.HTML(text)

    @staticmethod
    def to_string(node, default=None, del_none=True):
        if isinstance(node, list):
            result = []
            for s in node:
                s = _base_library.to_string(s, default)
                if s or not del_none:
                    result.append(s)
            return result
        else:
            return node.xpath('string(.)')

    @staticmethod
    def get_text(node, default=None, del_none=True):
        if isinstance(node, list):
            result = []
            for s in node:
                s = _base_library.get_text(s, default)
                if s or not del_none:
                    result.append(s)
            return result
        else:
            return _base_library.get_once(node.xpath('./text()'), default)

    @staticmethod
    def get_attr(node, attr, default=None):
        return _base_library.get_once(node.xpath('./@' + attr), default)

    @staticmethod
    def get_html(node, encoding=None):
        bhtml = etree.tostring(node, encoding=encoding)
        if encoding:
            return bhtml.decode(encoding)
        return bhtml.decode()

    # endregion

    # region 高级查询
    @staticmethod
    def _parser_attr(**attrs):
        if len(attrs) == 0:
            return ''

        fmt = '[{}]'
        attr_fmt_all = '@{}'
        attr_fmt = '@{}="{}"'
        not_fmt = 'not({})'
        text_fmt = 'text()="{}"'

        search_attrs = []  # 查询属性
        not_attrs = []  # 排除属性

        for key, value in attrs.items():
            if value is None:  # 排除无效属性值
                continue

            # 判断是否为排除属性
            _not = False
            if value is False:
                _not = True
            # 去除前端下划线,并标记为排除
            if key[0] == '_':
                _not = True
                key = key[1:]

            # 去除class_尾部下划线
            if key == 'class_':
                key = 'class'

            # 将key:value转换为xpath查询格式
            if value is True or value is False:
                attr_text = 'text()' if key == 'text' else attr_fmt_all.format(key)
            else:
                attr_text = text_fmt.format(value) if key == 'text' else attr_fmt.format(key, value)

            search_attrs.append(attr_text) if not _not else not_attrs.append(attr_text)

        # 检查排除属性
        if not_attrs:
            not_attrs = ' or '.join(not_attrs)
            not_attrs = not_fmt.format(not_attrs)
            search_attrs.append(not_attrs)

        # 连接属性
        search_attrs = ' and '.join(search_attrs)

        if search_attrs:
            return fmt.format(search_attrs)
        return ''

    @staticmethod
    def find(node, name=None, class_=None, text=None, sun_node=True, **attrs):
        '''
        查询节点
        :param node: 原始节点
        :param name: 元素名, 如果不是str类型则查找所有元素
        :param class_: class属性
        :param text: 文本值
        :param sun_node: 递归查询孙节点
        :param attrs: 属性名前加下划线_会排除这个属性, 如_id=True在xpath中表现为 not(@id)
                            属性值为True, 表示这个属性匹配任意值
        :return: 成功返回etree._Element节点, 失败返回None
        '''
        result = _base_library._find(node, once=True, name=name, class_=class_, text=text, sun_node=sun_node, **attrs)
        return _base_library.get_once(result)

    @staticmethod
    def find_all(node, name=None, class_=None, text=None, sun_node=True, **attrs):
        '''查询多个节点,使用方法同find,返回一个列表,查询失败返回空列表'''
        return _base_library._find(node, once=False, name=name, class_=class_, text=text, sun_node=sun_node, **attrs)

    @staticmethod
    def _find(node, once=False, name=None, class_=None, text=None, sun_node=True, **attrs):
        fmt = '{sun_node}{name}{attr_text}'
        sun_node = './/' if sun_node else './'
        name = name if isinstance(name, str) else '*'
        attr_text = _base_library._parser_attr(class_=class_, text=text, **attrs)
        code = fmt.format(sun_node=sun_node, name=name, attr_text=attr_text)
        if once:
            code = '{}[1]'.format(code)
        return node.xpath(code)

    # endregion

    # region 节点树
    @staticmethod
    def find_pre(node):
        # 返回当前节点前面的所有同级元素节点
        return node.xpath('preceding-sibling::*')

    @staticmethod
    def find_pre_text(node):
        # 返回当前节点前面的所有同级文本节点
        return node.xpath('preceding-sibling::text()')

    @staticmethod
    def find_pre_all(node):
        # 返回当前节点前面的所有同级节点
        return node.xpath('preceding-sibling::node()')

    @staticmethod
    def find_pre_one(node):
        return _base_library.get_once(node.xpath('preceding-sibling::node()[1]'))

    @staticmethod
    def find_next(node):
        # 返回当前节点后面的所有同级元素节点
        return node.xpath('following-sibling::*')

    @staticmethod
    def find_next_text(node):
        # 返回当前节点后面的所有同级文本节点
        return node.xpath('following-sibling::text()')

    @staticmethod
    def find_next_all(node):
        # 返回当前节点后面的所有同级节点
        return node.xpath('following-sibling::node()')

    @staticmethod
    def find_next_one(node):
        return _base_library.get_once(node.xpath('following-sibling::node()[1]'))

    @staticmethod
    def find_child(node):
        # 返回当前节点的所有子元素节点
        return node.xpath('child::*')

    @staticmethod
    def find_child_text(node):
        # 返回当前节点的所有子文本节点
        return node.xpath('child::text()')

    @staticmethod
    def find_child_all(node):
        # 返回当前节点的所有子节点
        return node.xpath('child::node()')

    @staticmethod
    def find_parent(node):
        return _base_library.get_once(node.xpath('parent::*'))

    @staticmethod
    def find_ancestor(node):
        return node.xpath('ancestor::*')
    # endregion


class _Element_List(list):

    @property
    def empty(self):
        return len(self) == 0

    def is_empty(self):
        return len(self) == 0

    @property
    def string(self):
        return self.get_string()

    @property
    def text(self):
        return self.get_text()

    @property
    def string_list(self):
        return self.get_string()

    @property
    def text_list(self):
        return self.get_text()

    def get_string(self, join_str='\t', strip=True):
        return join_str.join(self.get_string_list(strip))

    def get_text(self, join_str='\t', strip=True):
        return join_str.join(self.get_text_list(strip))

    def get_string_list(self, strip=True):
        if not strip:
            return [node.string for node in self if node.string]

        values = []
        for node in self:
            text = node.string.strip()
            if text:
                values.append(text)
        return values

    def get_text_list(self, strip=True):
        if not strip:
            return [node.text for node in self if node.text]

        values = []
        for node in self:
            text = node.text.strip()
            if text:
                values.append(text)
        return values


class _Element():
    def __init__(self, src):
        self.name = 'comment' if _base_library.is_comment(src) else src.tag.lower()
        self.base = src

        self._string = None
        self._text = None
        self._attrs = None

    # region 原始xpath代码查询
    def xpath_once(self, code):
        result = _base_library.xpath_once(self.base, code=code)
        return self._build_Element(result)

    def xpath_all(self, code):
        result = _base_library.xpath_all(self.base, code=code)
        return self._build_Element(result)

    # endregion

    # region 查询函数
    def find(self, name=None, class_=None, text=None, sun_node=True, **attrs):
        result = _base_library.find(self.base, name=name, class_=class_, text=text, sun_node=sun_node,
                                    **attrs)
        return self._build_Element(result)

    def find_all(self, name=None, class_=None, text=None, sun_node=True, **attrs):
        result = _base_library.find_all(self.base, name=name, class_=class_, text=text, sun_node=sun_node,
                                        **attrs)
        return self._build_Element(result)

    # endregion

    # region 判断
    @property
    def is_element(self):
        return True

    @property
    def is_node_element(self):
        return True

    @property
    def is_text_element(self):
        return False

    @property
    def is_comment(self):
        return _base_library.is_comment(self.base)

    # endregion

    # region 转换-获取函数
    @property
    def string(self):
        # 返回此节点下所有的文本的组合
        return self.get_string()

    @property
    def text(self):
        # 返回此节点下文本
        return self.get_text()

    @property
    def html(self):
        return self.get_html()

    def get_string(self):
        if self._string is None:
            result = _base_library.to_string(self.base)
            self._string = self._build_Element(result)
        return self._string

    def get_text(self):
        if self._text is None:
            result = _base_library.get_text(self.base, '')
            self._text = self._build_Element(result)
        return self._text

    def get_html(self, encoding='utf8'):
        return _base_library.get_html(self.base, encoding)

    def get_attr(self, attr, default=None):
        # result = simple_xpath.get_attr(self.base, attr, default)
        # return self._build_Element(result)
        return self.attrs.get(attr, default)

    @property
    def attrs(self):
        if self._attrs is None:
            self._attrs = dict(self.base.attrib)
        return self._attrs

    # endregion

    def remove_self(self):
        _base_library.find_parent(self.base).remove(self.base)

    def remove(self, element):
        assert isinstance(element, _Element), '只能删除sharp_xpath._Element对象'
        self.base.remove(element.base)

    # region 节点树
    @property
    def previous_siblings(self):
        result = _base_library.find_pre(self.base)
        return self._build_Element(result)

    @property
    def previous_siblings_all(self):
        result = _base_library.find_pre_all(self.base)
        return self._build_Element(result)

    @property
    def previous_siblings_text(self):
        result = _base_library.find_pre_text(self.base)
        return self._build_Element(result)

    @property
    def previous_siblings_one(self):
        result = _base_library.find_pre_one(self.base)
        return self._build_Element(result)

    @property
    def next_siblings(self):
        result = _base_library.find_next(self.base)
        return self._build_Element(result)

    @property
    def next_siblings_all(self):
        result = _base_library.find_next_all(self.base)
        return self._build_Element(result)

    @property
    def next_siblings_text(self):
        result = _base_library.find_next_text(self.base)
        return self._build_Element(result)

    @property
    def next_siblings_one(self):
        result = _base_library.find_next_one(self.base)
        return self._build_Element(result)

    @property
    def childs(self):
        result = _base_library.find_child(self.base)
        return self._build_Element(result)

    @property
    def childs_all(self):
        result = _base_library.find_child_all(self.base)
        return self._build_Element(result)

    @property
    def childs_text(self):
        result = _base_library.find_child_text(self.base)
        return self._build_Element(result)

    @property
    def parent(self):
        result = _base_library.find_parent(self.base)
        return self._build_Element(result)

    @property
    def ancestor(self):
        result = _base_library.find_ancestor(self.base)
        return self._build_Element(result)

    # endregion

    def __call__(self, *args, **kwargs):
        return self.find_all(*args, **kwargs)

    def _build_Element(self, node):
        if isinstance(node, list):
            return _Element_List([self._build_Element(n) for n in node])
        if not node is None:
            if isinstance(node, str):
                return _TextElement(node)
            return _Element(node)

    def __getattr__(self, name):
        # 让这个对象能使用 obj.xxx 来获取属性或搜索一个节点
        if name not in self.__dict__:
            result = self.get_attr(name, default=None)
            if result is None:
                result = self.find(name, sun_node=True)
            self.__dict__[name] = result
        return self.__dict__[name]

    def __getitem__(self, name):
        # 让这个对象能使用 obj['xxx'] 来获取属性
        return self.attrs[name]


class _TextElement(str):

    def __init__(self, value=''):
        self.base = value
        self.name = 'text'
        super().__init__()

    @property
    def string(self):
        return self

    @property
    def text(self):
        return self

    @property
    def is_element(self):
        return _base_library.is_element(self.base)

    @property
    def is_node_element(self):
        return False

    @property
    def is_text_element(self):
        return _base_library.is_text_element(self.base)

    @property
    def is_comment(self):
        return False

    def get_string(self):
        return self

    def get_text(self):
        return self

    def __getattr__(self, name):
        return None

    def __deepcopy__(self, memodict=None):
        return self


class Element(_Element):
    def __init__(self, src):
        if not _base_library.is_element(src):
            assert isinstance(src, str) and src, '只能传入etree对象或一个html结构的str类型, 你传入的是{}'.format(type(src))
            src = _base_library.to_etree(src)
        super().__init__(src)


def load(src):
    return Element(src)
