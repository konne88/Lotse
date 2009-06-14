#!/usr/bin/env python

import gtkgui
import session

if __name__ == "__main__":
    #   osso_c = osso.Context("osso_test_app", "0.0.1", False)
    #program  = hildon.Program()
    #  self.window = hildon.Window()
  
    ses = session.Session()
    lotse = gtkgui.LotseWindow(ses)
