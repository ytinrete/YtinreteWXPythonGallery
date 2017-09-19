import wx


class AppDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def SetApp(self, app):
        self.app = app

    def OnDropFiles(self, x, y, f_names):
        if self.app:
            self.app.OnDropFiles(self, x, y, f_names)
        return 0


class Application(wx.Frame):
    def __init__(self, parent, title):
        super(Application, self).__init__(parent, title=title, size=(800, 600))
        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        panel = wx.Panel(self)

        box_all = wx.BoxSizer(wx.HORIZONTAL)

        panel1 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel1.SetBackgroundColour("Black")
        panel2 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel2.SetBackgroundColour("red")
        panel3 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel3.SetBackgroundColour("yellow")
        panel4 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        panel4.SetBackgroundColour("grey")

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(wx.StaticText(panel, label='Drag folder here and double click'))
        left_box.Add(panel2, 1, wx.EXPAND)
        left_box.Add(wx.StaticText(panel, label='file tree from folder'))
        left_box.Add(panel3, 3, wx.EXPAND)
        left_box.Add(wx.StaticText(panel, label='photo files'))
        left_box.Add(panel4, 2, wx.EXPAND)

        box_all.Add(left_box, 2, wx.EXPAND)
        box_all.Add(panel1, 10, wx.EXPAND)

        #
        # p1 = wx.Panel(panel)
        # p1.SetBackgroundColour('#eded43')
        #
        # box_all.Add(p1, flag=wx.RIGHT|wx.EXPAND, border=8)
        #
        # box_all.Add(wx.Button(parent=panel, label=u'line one'), flag=wx.EXPAND, proportion=wx.EXPAND)



        panel.SetAutoLayout(True)

        panel.SetSizer(box_all)

        drop = AppDropTarget(panel2)
        drop.SetApp(self)

        panel2.SetDropTarget(drop)

    pass

    def OnDropFiles(self, target, x, y, f_names):
        print(target)
        print(x)
        print(y)
        print(f_names)

    def InitUI2(self):
        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Class Name')
        st1.SetFont(font)

        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, label='Case Sensitive')
        cb1.SetFont(font)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, label='Nested Classes')
        cb2.SetFont(font)
        hbox4.Add(cb2, flag=wx.LEFT, border=10)
        cb3 = wx.CheckBox(panel, label='Non-Project classes')
        cb3.SetFont(font)
        hbox4.Add(cb3, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)


if __name__ == '__main__':
    app = wx.App()
    Application(None, title="Border")
    app.MainLoop()
