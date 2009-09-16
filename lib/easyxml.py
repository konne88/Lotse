#!/usr/bin/env python
#coding=utf-8

from xml.parsers.expat import ExpatError
import xml.dom.minidom as xml

# minidom
# http://docs.python.org/library/xml.dom.minidom.html

def append_element(doc,parent,name, attribute_name=None, attribute_value=None):
    n = doc.createElement(name)
    if attribute_name is not None:
        n.setAttribute(attribute_name,attribute_value)
    parent.appendChild(n)
    return n

def append_element_with_data(doc,parent, name, data,\
                             attribute_name=None, attribute_value=None):
    n = append_element(doc,parent,name, attribute_name, attribute_value)
    t = doc.createTextNode(str(data))
    n.appendChild(t)
    return n

def create_doc(root):
    impl = xml.getDOMImplementation()
    doc = impl.createDocument(None, root, None)
    
    
    return doc

if __name__ == "__main__":
    doc = create_doc('status')
    root = doc.documentElement
    root.setAttribute('version','1.1')
    append_element_with_data(doc,root,'fix','fix')
    append_element_with_data(doc,root,'latitude','latitude')
    append_element_with_data(doc,root,'longitude','longitude')
    append_element_with_data(doc,root,'altitude','altitude')
    append_element_with_data(doc,root,'time','time')
    append_element_with_data(doc,root,'speed','speed')
    append_element_with_data(doc,root,'heading','heading')

    print doc.toprettyxml()
