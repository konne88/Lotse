from xml.parsers.expat import ExpatError
import xml.dom.minidom as xml

# minidom
# http://docs.python.org/library/xml.dom.minidom.html

def append_element(doc,parent,name):
	n = doc.createElement(name)
	parent.appendChild(n)
	return n

def append_element_with_data(doc,parent,name,data):
	n = append_element(doc,parent,name)
	t = doc.createTextNode(str(data))
	n.appendChild(t)
	return n

def create_doc(root):
    impl = xml.getDOMImplementation()
    doc = impl.createDocument(None, root, None)
    return doc

""" if the functions above are defined in the namespace xml, writing a xml doc
that looks like 
<status>
    <fix>...</fix>
    <latitude>...</lati

is a simple as:
    
doc = xml.create_doc('status')
        root = doc.documentElement
        xml.append_element_with_data(doc,root,'fix',self.fix)
        xml.append_element_with_data(doc,root,'latitude',self.latitude)
        xml.append_element_with_data(doc,root,'longitude',self.longitude)
        xml.append_element_with_data(doc,root,'altitude',self.altitude)
        xml.append_element_with_data(doc,root,'time',self.time)
        xml.append_element_with_data(doc,root,'speed',self.speed)
        xml.append_element_with_data(doc,root,'heading',self.heading)
        
        """