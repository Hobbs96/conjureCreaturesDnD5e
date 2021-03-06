#!/bin/python

import wx
import wx.lib.buttons as buttons
from ConjureCreaturesGenerator import ConjureCreaturesGenerator

class ConjureCreaturesGeneratorFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ConjureCreaturesGeneratorFrame, self).__init__(*args, **kw)
        # create a panel in the frame
        self.panel = wx.Panel(self)
        self.Size = (500, 300)
        # and put some text with a larger bold font on it
        st = wx.StaticText(self.panel, label="Conjure Creatures v0.2.0", pos=(7,7))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()
        self.makeConjureButton()
        self.makeTextControl()
        self.makeEmptyCreatureList()
        self.generateTerrainCheckBoxes()

    def makeMenuBar(self): 
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        loadFileItem = fileMenu.Append(-1, "&Load File...\tCtrl-L", 
                "Choose a .json file to load as the creature set")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.onExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.onLoadFile, loadFileItem)

    def makeTextControl(self):
        self.CRTextBox = wx.TextCtrl(self.panel, pos=(25, 80), size=(90, 20))
        self.CRTextBox.Bind(wx.EVT_TEXT_ENTER, self.onConjureButton)

    def makeConjureButton(self):
        self.conjureButton = buttons.GenButton(self.panel, -1, "Conjure!", pos=(25, 50))
        self.conjureButton.Bind(wx.EVT_BUTTON, self.onConjureButton)

    def makeEmptyCreatureList(self):
        self.creatureList = wx.ListCtrl(self.panel, wx.ID_ANY, style=wx.LC_REPORT, pos=(120, 50))
        self.creatureList.InsertColumn(0, 'Creature', wx.LIST_FORMAT_CENTER, width=140)
        self.creatureList.InsertColumn(1, 'Number', wx.LIST_FORMAT_LEFT, width = 70)

    def onExit(self, event):
        self.Close(True)

    def onLoadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                      "JSON file (*.json)|*.json", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        # Proceed loading the file chosen by the user
        pathname = openFileDialog.GetPath()
        try:
            self.creatureGenerator = ConjureCreaturesGenerator(pathname)
        except IOError:
            wx.LogError("Cannot open file '%s'." % pathname)
        openFileDialog.Destroy()


    def onAbout(self, event):
        wx.MessageBox("This is a wxPython GUI for the Conjure Creatures spell in D&D 5e." +
                      "\nSee clark-lindsay on github for more.", 
                      "About Conjure Creatures",
                      wx.OK|wx.ICON_INFORMATION)

    def onConjureButton(self, event):
        textBoxInput = self.CRTextBox.GetValue()
        try:
            textBoxInput = float(textBoxInput)
        except Exception as e:
            wx.LogError('Incorrect input given to text box; not convertible to float')
            return
        self.generateCreatureList(textBoxInput)
    
    def generateCreatureList(self, requestedCR):
        terrains = set()
        if self.landCheckBox.GetValue():
            terrains.add('Land')
        if self.waterCheckBox.GetValue():
            terrains.add('Water')
        if self.skyCheckBox.GetValue():
            terrains.add('Air')
        conjuredCreatures = self.creatureGenerator(requestedCR, terrains)
        self.creatureList.DeleteAllItems()
        for key, value in conjuredCreatures.items():
            self.creatureList.Append([key.name, value])

    def generateTerrainCheckBoxes(self):
        self.landCheckBox = wx.CheckBox(self.panel, label = 'Land', pos = (25,110)) 
        self.waterCheckBox = wx.CheckBox(self.panel, label = 'Water', pos = (25,130)) 
        self.skyCheckBox = wx.CheckBox(self.panel, label = 'Air', pos = (25, 150)) 
        self.landCheckBox.SetValue(True)



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ConjureCreaturesGeneratorFrame(None, title='Conjure Creatures')
    frm.Show()
    app.MainLoop()
