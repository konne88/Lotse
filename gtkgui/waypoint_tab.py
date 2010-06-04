import gtk
import gobject
from session.waypoint import Waypoint
from session.coordinates import Coordinates
from session.waypointloader import WaypointLoader
from session import Source

class WaypointTab(gtk.HBox):
    def __init__(self,session):
        super(WaypointTab,self).__init__()
        
        
        model = session.wpList
        
        self.wpLoader = WaypointLoader(session.wpList)
        
        self._listBox = gtk.VBox()
        self._filterEntry = gtk.Entry()
        self._filterEntry.connect( 'changed', self.on_filter_edited )
        self._listBox.pack_start(self._filterEntry,False,False)
        
        self.wpListFilter = model.filter_new(root=None)
        self.wpListFilter.set_visible_func(self.filter_wplist)
        self._wpListView = gtk.TreeView(self.wpListFilter)
        
        
        renderer = gtk.CellRendererText()
        renderer.set_property( 'editable', True )
        renderer.connect( 'edited', self.on_name_edited, model )
        column = gtk.TreeViewColumn("Name", renderer)
        column.set_cell_data_func(renderer, self.on_render_name)
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_alignment(0.5)
        column.resizable = True
        column.min_width = 50
        self._wpListView.append_column( column )
       
        self.renderer = gtk.CellRendererText()
        self.renderer.set_property( 'editable', True )
        self.renderer.connect( 'edited', self.on_latlon_edited, model )
        self.latlon_column = gtk.TreeViewColumn("Lat/Lon", self.renderer)
        self.latlon_column.set_cell_data_func(self.renderer, self.on_render_latlon)
        #self.latlon_column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.latlon_column.set_alignment(0.5)
        self.latlon_column.min_width = 50
        self.latlon_column.resizable = True
        self._wpListView.append_column( self.latlon_column )
        
        renderer = gtk.CellRendererText()
        renderer.set_property( 'editable', True )
        renderer.connect( 'edited', self.on_alt_edited, model )
        column = gtk.TreeViewColumn("Alt", renderer)
        column.set_cell_data_func(renderer, self.on_render_alt)
     #   column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_alignment(1)
        column.min_width = 50
        column.resizable = True
        self._wpListView.append_column( column ) 
                   
        #self._wpListView.set_fixed_height_mode(True)

                   
        bBox= gtk.VButtonBox()
        bBox.set_layout(gtk.BUTTONBOX_START)
        self._add = gtk.Button('Add')
        self._del = gtk.Button('Delete')
        self._import = gtk.Button('Import')
        self._select = gtk.Button('Select')
        
        bBox.pack_start(self._add, False,False)
        bBox.pack_start(self._del, False,False)
        bBox.pack_start(self._import, False,False)
        bBox.pack_start(self._select, False,False)
        
        self._scroll = gtk.ScrolledWindow()
        self._scroll.add(self._wpListView)
        self._listBox.pack_start(self._scroll)
        
        self.add(self._listBox)
        self.pack_start(bBox,False)
        
        self._add.connect('clicked',self.on_add)
        self._del.connect('clicked',self.on_del)
        self._import.connect('clicked',self.on_import)
        self._select.connect('clicked',self.on_select)
        
        self._session = session
    
    def on_filter_edited(self,widget):
         self._wpListView.collapse_all()
         self.wpListFilter.refilter()    
         self._wpListView.expand_all()
    
    def filter_wplist(self,model, iter):
        wp = model.get_value(iter, 0)
        if model.iter_has_child(iter) == False:
            text = self._filterEntry.get_text()            
            if text != "":
                return text in wp.name
                
        return True
        
    def on_render_name(self, column, cell, model, iter):        
        v = model.get_value(iter, 0)
        cell.set_property('text', v.name)
        
    def on_render_latlon(self, column, cell, model, iter):
        v = model.get_value(iter, 0)
        if type(v) == Waypoint:
            cell.set_property('text', v.strlatlon())
        else:
            cell.set_property('text', "")
        
    def on_render_alt(self, column, cell, model, iter):
        v = model.get_value(iter, 0)
        if type(v) == Waypoint:
            cell.set_property('text', str(v.alt))
        else:
            cell.set_property('text', "")
        
    def on_name_edited( self, cell, path, new_text, model ):
        model[path][0].name = new_text
        
    def on_latlon_edited( self, cell, path, new_text, model ):
        c = Coordinates.parse_string(new_text)
        wp = model[path][0]
        wp.lat = c.lat
        wp.lon = c.lon
        print wp.strlatlon()
            
    def on_alt_edited( self, cell, path, new_text, model ):
        try:
            model[path][0].alt = float(new_text)
        except(ValueError):
            pass
            
    def on_add(self, widget, data=None):
        clipboard = gtk.Clipboard()
        text = clipboard.wait_for_text()
        wp = None
        if text != None:
            try:
                coord = Coordinates.parse_string(text)
                wp =  Waypoint(coord.lat, coord.lon, coord.alt)
            except(ValueError):
                pass
        
        if wp == None:
            pos = self._session.sleek_position
            wp = Waypoint()
            wp.lat=pos.lat
            wp.lon=pos.lon
            wp.alt=pos.alt
        
        new_row = self._session.wpList.append(self._session.get_manual_list_iter(),(wp,))
            
        #self._wpListView.expand_row(m.get_path(i),True)
                    
            #self._wpListView.grab_focus()
             
    
    def on_del(self, widget, data=None):
    
        if self._wpListView.get_cursor() is not None:
            # get the Model inside the ListView, inside the Filter
            model=self._wpListView.get_model().get_model()
            iter=model.get_iter(self._wpListView.get_cursor()[0])
            value = model.get_value(iter,0)
            
            if issubclass(type(value),Waypoint):
                model.remove(iter)
            elif issubclass(type(value),Source): 
                model.remove(iter)
                if value == self._session.manualSource:    
                    model.append(None,(self._session.manualSource,))  
                
                    

      
    def on_import(self, widget, data=None):
        dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        #filter = gtk.FileFilter()
        #filter.set_name("All files")
        #filter.add_pattern("*")
        #dialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("Waypoints")
        filter.add_pattern("*.gpx")
        filter.add_pattern("*.GPX")
        #filter.add_pattern("*.kml")
        #filter.add_pattern("*.KML")      
        dialog.add_filter(filter)


        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print dialog.get_filename()
            self.wpLoader.load_from_file(dialog.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            pass
           
        dialog.destroy()
        
    def on_select(self, widget, data=None):
        
        if self._wpListView.get_cursor()!=None:
            model=self._wpListView.get_model()
            iter=model.get_iter(self._wpListView.get_cursor()[0])
            value = model.get_value(iter,0)
            if issubclass(type(value),Waypoint):
                self._session.set_target(value)
        
