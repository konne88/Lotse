import string
import os
import time
import xml.dom.minidom as xml
import lib.easyxml as easyxml
from logger import Logger

class GPXLogger(Logger):
    def __init__(self,session,filename):
        super(GPXLogger,self).__init__(session)
        self._filename = filename
        #<gpx version="1.1" creator="Lotse"
        #xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        #xmlns="http://www.topografix.com/GPX/1.1"
        #xsi:schemaLocation="http://www.topografix.com/GPS/1/1
        #http://www.topografix.com/GPX/1/1/gpx.xsd">

        self._doc = easyxml.create_doc('gpx')
        gpx_node = self._doc.documentElement
        gpx_node.setAttribute('version','1.1')
        gpx_node.setAttribute('creator','lotse')
        gpx_node.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
        gpx_node.setAttribute('xmlns','http://www.topografix.com/GPX/1.1') 
        gpx_node.setAttribute('xsi:schemaLocation',\
        'http://www.topografix.com/GPS/1/1 #http://www.topografix.com/GPX/1/1/gpx.xsd')    

        #<metadata>
        #<name>Lotse</name>
        #<author>Niklas Schnelle</author>
        #<copyright>BSD or GPL v 2.0</copyright>
        #</metadata>
        metadata_node = easyxml.append_element(self._doc,gpx_node,'metadata')
        easyxml.append_element_with_data(self._doc,metadata_node,'name','Lotse')
        easyxml.append_element_with_data(self._doc,metadata_node,'author','Niklas Schnelle')
        easyxml.append_element_with_data(self._doc,metadata_node,'copyright','GPL v 2.0')

        #<trk>
        self._trk_node = easyxml.append_element(self._doc,gpx_node,'trk')
        self._segment_node = None

    def start(self):
        super(GPXLogger,self).start()
        if self._segment_node == None:
            self._segment_node = easyxml.append_element(self._doc,self._trk_node,'trkseg')

    def stop(self):
        super(GPXLogger,self).stop()   
        self._segment_node = None
    
    def flush(self):
        file = open(self._filename, 'w')
        self._doc.writexml(file,' ',' ','\n', 'UTF-8')    
        file.close()
        
    def get_name(self):
        return 'GPXLogger: '+self._filename

    name  =  property(get_name)

    def on_position_changed(self):
        #Example
        #<trkpt lat="48.737799" lon="9.136677">
        #<ele>430.488113</ele>
        #<time>2008-09-04T19:19:40Z</time>
        #<fix>2d</fix>
        #</trkpt>
        if self._session.position.fix>1:
            trkpt_node = easyxml.append_element(self._doc,self._segment_node,'trkpt')
            trkpt_node.setAttribute('lat','%f'%(self._session.sleek_position.lat))
            trkpt_node.setAttribute('lon','%f'%(self._session.sleek_position.lon))

            easyxml.append_element_with_data(self._doc,trkpt_node,'ele',\
                '%.2f'%(self._session.sleek_position.alt))

            easyxml.append_element_with_data(self._doc,trkpt_node,'time',\
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self._session.position.time)))

            easyxml.append_element_with_data(self._doc,trkpt_node,'fix','%dd'%(self._session.position.fix))

        #print 'Time: '+time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self._session.time))

