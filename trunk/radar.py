import gtk

class Radar(gtk.DrawingArea):
    def __init__(self):
        super(Radar,self).__init__()
        self.set_size_request(300, 300)
        self._pixmap = None
        
        self.connect('configure_event',self.configure_event)
        self.connect('expose_event',self.expose_event)

    # Create a new backing pixmap of the appropriate size
    def configure_event(self,widget, event):
        x, y, width, height = widget.get_allocation()
        self._pixmap = gtk.gdk.Pixmap(widget.window, width, height)
        self._pixmap.draw_rectangle(widget.get_style().white_gc,
                            True, 0, 0, width, height)
        rect = (int(x-5), int(y-5), 10, 10)
        self._pixmap.draw_rectangle(widget.get_style().black_gc, True,
                            rect[0], rect[1], rect[2], rect[3])
        
        return True

    # Redraw the screen from the backing pixmap
    def expose_event(self,widget, event):
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self._pixmap, x, y, x, y, width, height)
        return False
