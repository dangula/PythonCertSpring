#!/usr/bin/env python

"""
Example of the very basic, minimal framework for a wxPython application

This version adds a BoxSizer for laying out two buttons on the panel
"""

import wx
import os

#--------------------------------------------------------------

# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it to.
wildcard = "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"

#--------------------------------------------------------------

class AppLogic(object):
    """
    A class to hold the application Application Logic.

    You generally don't want the real logic of the app mixed
    in with the GUI

    In a real app, this would be a substantial collection of 
    modules, classes, etc...
    """

    def file_open(self, filename="default_name"):
        """This method opens a file"""
        print "Open a file: "
        print "I'd be opening file: %s now"%filename

    def file_close(self):
        """This method closes a file"""
        print "Close a file: "
        print "I'd be closing a file now"


class ButtonPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        ## add two buttons:
        theButton1 = wx.Button(self, label="Push Me")
        theButton1.Bind(wx.EVT_BUTTON, self.onButton)

        ## add two buttons:
        theButton2 = wx.Button(self, label="Push Me Also")
        theButton2.Bind(wx.EVT_BUTTON, self.onButton)

        ## do the layout
        ## (try uncommenting the other, and see what happens...)
        S = wx.BoxSizer(wx.VERTICAL)
        #S = wx.BoxSizer(wx.HORIZONTAL)
        
        S.Add(theButton1, 0, wx.GROW | wx.ALL, 4)
        S.Add(theButton2, 0, wx.GROW | wx.ALL, 4)
        
        self.SetSizerAndFit(S)
        
    def onButton(self, evt=None):
        but_label = evt.EventObject.Label
        print "You pushed buttons:", but_label


class TestFrame(wx.Frame):
    def __init__(self, app_logic, *args, **kwargs):
        kwargs.setdefault('title', "Simple test App")
        wx.Frame.__init__(self, *args, **kwargs)

        self.app_logic = app_logic

        # put the Panel on the frame
        self.buttonPanel = ButtonPanel(self)

        # Build up the menu bar:
        menuBar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        
        newMenuItem = fileMenu.Append(wx.ID_ANY, "&Save As...", "Create a new file")
        self.Bind(wx.EVT_MENU, self.onNew, newMenuItem )
        
        openMenuItem = fileMenu.Append(wx.ID_ANY, "&Open", "Open an existing file" )
        self.Bind(wx.EVT_MENU, self.onOpen, openMenuItem)

        closeMenuItem = fileMenu.Append(wx.ID_ANY, "&Close", "Close a file" )
        self.Bind(wx.EVT_MENU, self.onClose, closeMenuItem)

        exitMenuItem = fileMenu.Append(wx.ID_EXIT, "Exit", "Exit the application")
        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
        menuBar.Append(fileMenu, "&File")
        
        helpMenu = wx.Menu()
        helpMenuItem = helpMenu.Append(wx.ID_HELP, "Help", "Get help")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

    def onClose(self, evt=None):
        print "close menu selected"
        self.file_close()

    def onExit(self, evt=None):
        print "Exit the program here"
        print "The event passed to onExit is type ", type(evt),
        self.Close()

    def onNew ( self, evt=None ):
        """This method creates a new file"""

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'save' dialog.
        #
        # Unlike the 'open dialog' example found elsewhere, this example does NOT
        # force the current working directory to change if the user chooses a different
        # directory than the one initially set.
        dlg = wx.FileDialog(self,
                            message="Save file as ...",
                            defaultDir=os.getcwd(), 
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.SAVE )

        # This sets the default filter that the user will initially see. Otherwise,
        # the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "In onNew, the path is %s" % path
            # Normally, at this point you would save your data using the file and path
            # data that the user provided to you, but since we didn't actually start
            # with any data to work with, that would be difficult.
            # 
            # The code to do so would be similar to this, assuming 'data' contains
            # the data you want to save:
            #
            # fp = file(path, 'w') # Create file anew
            # fp.write(data)
            # fp.close()
            #
            # You might want to add some error checking :-)
            #
        else :
            print "The file dialog was canceled before anything was selected"

        # Note that the current working dir didn't change. This is good since
        # that's the way we set it up.

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()
        
    
    def onOpen(self, evt=None):
        """This method opens an existing file"""
        print "Open a file: "
        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.FileDialog( self,
                             message="Choose a file",
                             defaultDir=os.getcwd(), 
                             defaultFile="", 
                             wildcard=wildcard,
                             style=wx.OPEN | wx.CHANGE_DIR
                            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            print "I'd be opening file in onOpen ", path
            self.app_logic.file_open( path )
        else :
            print "The file dialog was canceled before anything was selected"

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()


    def file_close(self):
        """This method closes a file"""
        print "Close a file: "
        print "I'd be closing a file now"
 

class TestApp(wx.App):
    def OnInit(self):
        """
        App initilization goes here -- not much to do, in this case
        """
        app_logic = AppLogic()
        f = TestFrame(app_logic, parent=None)
        f.Show()

        return True

if __name__ == "__main__":
    app = TestApp(False)
    app.MainLoop()

