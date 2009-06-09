import gtk

class RadarWidget(gtk.DrawingArea)
    def __init__(self)
        self.set_size_request(300, 300)
        self._pixmap = gtk.gdk.Pixmap(self, 300, 300, depth=-1)

    # Create a new backing pixmap of the appropriate size
    def configure_event(self,widget, event):
        x, y, width, height = widget.get_allocation()
        pixmap = gtk.gdk.Pixmap(widget.window, width, height)
        pixmap.draw_rectangle(widget.get_style().white_gc,
                            True, 0, 0, width, height)
        return True

    # Redraw the screen from the backing pixmap
    def expose_event(widget, event):
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    pixmap, x, y, x, y, width, height)
        return False

    # Draw a rectangle on the screen
    def draw_brush(widget, x, y):
        rect = (int(x-5), int(y-5), 10, 10)
        pixmap.draw_rectangle(widget.get_style().black_gc, True,
                            rect[0], rect[1], rect[2], rect[3])
        widget.queue_draw_area(rect[0], rect[1], rect[2], rect[3])
