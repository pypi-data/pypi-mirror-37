EasyXML presents a simplified view of an XML document.

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
  is performed.
