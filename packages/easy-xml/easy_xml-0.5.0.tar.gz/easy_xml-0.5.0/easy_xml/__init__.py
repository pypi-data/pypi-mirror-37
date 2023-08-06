"""EasyXML - a simplified view of an XML document.  See the `easy_xml.EasyXML`
class for details.
"""

VERSION = '0.5.0'

import xml.sax.saxutils
from StringIO import StringIO

class EasyXML(object):
    """EasyXML presents a simplified view of an XML document.

Elements in the XML document, including the root-level document,
are represented by EasyXML objects.  Each EasyXML object has a
`_name` attribute holding the name of the element represented by
the EasyXML object, a dictionary called `_attrs` holding the element's
attributes, and a sequence called `_content` holding the content
of the element.  The `_content` sequence contains strings for the
character data within the element (with whitespace stripped from
the beginning and end), and other EasyXML objects for nested XML
elements.

The content of the EasyXML object can be accessed directly as if it
were a sequence itself.  In addition, the element's attributes
themselves may be accessed by name on the EasyXML object.

For example, the XML fragment ``<zip code="12345">Schenectady,
NY</zip>`` would be returned as an EasyXML object where *name*.``_name``
is ``'zip'``, *name*.``_attrs`` is ``{'code': '12345'}``, *name*.
``_content`` is ``['Schenectady, NY']``, *name*.``code`` is ``'12345'``,
and *name*.``[0]`` is ``'Schenectady, NY'``.

Usage:

::

    # Import the EasyXML class
    from easy_xml import EasyXML

    # Parse the file-like object `stream` into an EasyXML structure.
    xmldoc = EasyXML.parseXML(stream)

    # Find the first ``<hello>`` node in the document.
    # If it exists, record its content in the `hello` variable.
    # If not, record ``world`` in `hello`, and create a new
    # ``<hello>world</hello>`` XML element at the top of the document.

    for element in xmldoc:
        if isinstance(element,EasyXML) and element._name == 'hello':
            hello = ' '.join(element._content)
            break

    if hello is None:
        hello = 'world'
        element = EasyXML('hello', content=[hello])
        xmldoc._content.insert(0, element)

    # Convert the EasyXML structure back into a valid XML document.
    xmlfile = str(xmldoc)

Notes:

* Processing instructions and comments are ignored.
* Only basic entity processing (``&lt;``, ``&gt;``, and ``&amp;``)
  is performed."""

    def __init__(self, name, attrs={}, content=[]):
        """
        Create a new EasyXML object.  `name` is the element name, and
        must be a string (or unicode string).  `attrs` holds the element
        attributes, and must map strings to strings.  `content` must be
        a sequence of strings and other EasyXML objects.

        Raises ValueError if any of the values are not of the correct type.
        """
        if name is not None and not isinstance(name, basestring):
            raise ValueError("name must be a string.")
        if len(filter(lambda (k, v):not isinstance(k, basestring) or \
                      not isinstance(v, basestring), attrs.items())) > 0:
            raise ValueError("attribute names and values must be strings.")
        if len(filter(lambda v:not isinstance(v, (EasyXML, basestring)),
                      content)) > 0:
            raise ValueError("content values must be strings and EasyXML objects.")
        self.__name = name
        self.__attrs = dict(attrs)
        self.__content = list(content)

    def append(self, value):
        """Appends `value` to the EasyXML object's content.

        Raises ValueError if `value` is neither a string nor an EasyXML object.
        """
        if not isinstance(value, (EasyXML, basestring)):
            raise ValueError("content values must be strings and EasyXML objects.")
        self.__content.append(value)

    def extend(self, values):
        """Extends the EasyXML object's content with values, which must
        be a sequence or iterable returning either strings or EasyXML
        objects.

        Raises ValueError without modifying the EasyXML object if any of
        the values returned by `values` are not a string or EasyXML
        object.
        """
        for val in values:
            self.append(val)

    def index(self, value, i=0, j=None):
        """Returns the smallest k such that _content[k] == value and i <= k < j.
        If value is an EasyXML object, this compares the element names and any
        attributes listed in value, but no content or other attributes.

        Raises ValueError if value is not found.
        """
        if i < 0:
            i += len(self.__content)
        if i < 0:
            i = 0
        if j is None:
              j = len(self.__content)
        elif j < 0:
            j += len(self.__content)
            if j < 0:
                j = 0
        if isinstance(value, EasyXML):
            while i < j:
                if isinstance(self.__content[i], EasyXML) and self.__content[i].__name == value.__name:
                    found = True
                    search_items = self.__content[i].items()
                    for looking_for in value.items():
                        if looking_for not in search_items:
                            found = False
                            break
                    if found:
                        break
                i += 1
        else:
            while i < j and self.__content[i] != value:
                i += 1
        if i == j:
            raise ValueError(value)
        return i

    def count(self, value):
        """Returns the number of times value appears in the element's
        content.  If value is an EasyXML object, this only compares the
        element names, NOT attributes or element content.
        """
        c = 0
        try:
            i = -1
            while True:
                i = self.index(value, i + 1)
                # This is not reached if the value was not found.
                c += 1
        except ValueError:
            pass
        return c

    def insert(self, i, value):
        """Inserts value into the element's content at position i.  If
        i is past the end of the content, this will insert at the end of
        the content.  If i is negative, it will be relative to the end
        of the content.

        Raises ValueError if value is neither a string nor an EasyXML
        object.
        """
        if not isinstance(value, (basestring, EasyXML)):
            raise ValueError("content values must be strings and EasyXML objects.")
        return self.__content.insert(i, value)

    def pop(self, i= -1):
        """Removes and returns the value at index i in the EasyXML
        object's content.  Equivalent to ``x = content[i]; del content[i];
        return x``
        """
        return self.__content.pop(i)

    def remove(self, value):
        """Removes the first instance of value from the EasyXML object's
        content.  Equivalent to del content[content.index(value)]

        Raises ValueError if the value is not found.
        """
        del self.__content[self.index(value)]

    def reverse(self):
        """Reverses the order of the EasyXML object's content.
        """
        self.__content.reverse()

    def items(self):
        """Returns the list of (attribute, value) pairs in this EasyXML node."""
        return self.__attrs.items()

    def __len__(self):
        return len(self.__content)

    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self.__attrs[key]
        else:
            return self.__content[key]

    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            if not isinstance(value, basestring):
                raise ValueError("attribute values must be strings.")
            self.__attrs[key] = value
        else:
            if not isinstance(value, (basestring, EasyXML)):
                raise ValueError("content values must be strings and EasyXML objects.")
            self.__content[key] = value

    def __delitem__(self, key):
        if isinstance(key, basestring):
            del self.__attrs[key]
        else:
            del self.__content[key]

    def __iter__(self):
        return iter(self.__content)

    def __reversed__(self):
        return reversed(self.__content)

    def __contains__(self, value):
        try:
            self.index(value)
            return True
        except ValueError:
            return False

    def __getattr__(self, key):
        if key == '_name':
            return self.__name
        elif key == '_attrs':
            return self.__attrs
        elif key == '_content':
            return self.__content
        elif isinstance(key, basestring):
            return self.__attrs[key]
        else:
            return self.__content[key]

    def __setattr__(self, key, value):
        # check if we're coming from within this class:
        if key.startswith('_EasyXML__'):
            super(EasyXML, self).__setattr__(key, value)
        elif key == '_name':
            if isinstance(value, basestring):
                self.__name = key
            else:
                raise ValueError("_name must be a string")
        elif isinstance(key, basestring):
            if not isinstance(value, basestring):
                raise ValueError("attribute values must be strings.")
            else:
                self.__attrs[key] = value
        else:
            if not isinstance(value, (basestring, EasyXML)):
                raise ValueError("content values must be strings or EasyXML objects.")
            else:
                self.__content[key] = value

    def __str__(self):
        s = ""
        if self.__name is not None:
            s += "<%s%s" % (self.__name,"".join(map(lambda (k, v):
                    " %s=%s" % (k, xml.sax.saxutils.quoteattr(v)),
                    self.__attrs.items())))
            if len(self.__content) > 0:
                s += ">"
        if len(self.__content) > 0:
	    for content in self.__content:
	        if isinstance(content, EasyXML):
		    s += str(content)
		else:
		    s += str(content).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if self.__name is not None:
            if len(self.__content) > 0:
                s += "</%s>" % (self.__name,)
            else:
                s += "/>"
        return s

    def __repr__(self):
        return "EasyXML(%s, %s, %s)" % (repr(self.__name),
                repr(self.__attrs), repr(self.__content))

    def pretty(self, indent=4):
        s = ""
        if not isinstance(indent, basestring):
            indent = " "*int(indent)
        if self.__name is not None:
            s += "<%s%s" % (self.__name,"".join(map(lambda (k, v):
                    " %s=%s" % (k, xml.sax.saxutils.quoteattr(v)),
                    self.__attrs.items())))
            if len(self.__content) > 0:
                s += ">"
        if len(self.__content) > 0:
            if len(self.__content) == 1 and isinstance(self.__content[0], basestring):
                s += str(self.__content[0])
            else:
                s += "".join(map(lambda c:((isinstance(c, EasyXML) and ("\n" + c.pretty(indent),)) or ("\n" + str(c),))[0], self.__content)).replace('\n', '\n' + indent) + "\n"
        if self.__name is not None:
            if len(self.__content) > 0:
                s += "</%s>" % (self.__name,)
            else:
                s += "/>"
        return s

    def __repr__(self):
        return "EasyXML(%s, %s, %s)" % (repr(self.__name),
                repr(self.__attrs), repr(self.__content))

    # private class for parsing an XML document
    class __xmlTreeSaxHandler(xml.sax.handler.ContentHandler):

        def startDocument(self):
            self.__top = EasyXML(None)
            self.__stack = [self.__top]
            self.__done = False

        def endDocument(self):
            self.__done = True

        def getDocument(self):
            if self.__done:
                return self.__top[0]
            raise EOFError("XML Document is not ready yet.")

        def startElement(self, name, attrs):
            if len(self.__stack[-1]) > 0 and isinstance(self.__stack[-1][-1], basestring) and self.__stack[-1][-1].isspace():
                del self.__stack[-1][-1]
            elem = EasyXML(name, dict(attrs.items()))
            self.__stack[-1].append(elem)
            self.__stack.append(elem)

        def endElement(self, name):
            if len(self.__stack[-1]) > 0 and isinstance(self.__stack[-1][-1], basestring) and self.__stack[-1][-1].isspace():
                del self.__stack[-1][-1]
            if len(self.__stack) > 1:
                if not self.postprocess(self.__stack[-1], self.__stack[-2]):
                    del self.__stack[-2][-1]
            self.__stack.pop(-1)

        def characters(self, text):
            if len(self.__stack[-1]) > 0 and isinstance(self.__stack[-1][-1], basestring):
                self.__stack[-1][-1] += text
            else:
                self.__stack[-1].append(text)

        def ignorableWhitespace(self, text):
            pass

        def postprocess(self, elem, parent):
            return True

    @staticmethod
    def parseXML(stream, postprocess=None):
        if '_EasyXML__parser' not in EasyXML.__dict__:
            EasyXML.__parser = xml.sax.make_parser()
            EasyXML.__handler = EasyXML.__xmlTreeSaxHandler()
            EasyXML.__parser.setContentHandler(EasyXML.__handler)
        if isinstance(stream, basestring):
            stream = StringIO(stream)
        if postprocess is None:
            EasyXML.__handler.postprocess = lambda e,p:True
        else:
            EasyXML.__handler.postprocess = postprocess
        EasyXML.__parser.parse(stream)
        return EasyXML.__handler.getDocument()
