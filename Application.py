import wx
import os
import platform
import subprocess
import wx.lib.agw.customtreectrl as customtree
import ntpath


class AppDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def SetApp(self, app):
        self.app = app

    def OnDropFiles(self, x, y, paths):
        if self.app:
            self.app.OnDropFiles(self, x, y, paths)
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

        self.panel1 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        self.panel1.SetBackgroundColour("Black")
        # panel2 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        # panel2.SetBackgroundColour("red")
        # panel3 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        # panel3.SetBackgroundColour("yellow")
        # panel4 = wx.Panel(panel, -1, style=wx.SUNKEN_BORDER)
        # panel4.SetBackgroundColour("grey")

        photo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.photo = wx.StaticBitmap(self.panel1, wx.ID_ANY)
        self.photo.SetBackgroundColour("Grey")
        photo_sizer.Add(self.photo, 1, wx.EXPAND)
        self.panel1.SetSizer(photo_sizer)
        self.panel1.SetAutoLayout(True)

        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(wx.StaticText(panel, label='Drag folder here'))

        # left_box.Add(panel2, 1, wx.EXPAND)
        self.list_box_root = wx.ListBox(panel, -1, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxRootSelect, self.list_box_root)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxRootDouble, self.list_box_root)

        drop = AppDropTarget(self)
        drop.SetApp(self)
        panel.SetDropTarget(drop)

        left_box.Add(self.list_box_root, 1, wx.EXPAND)

        left_box.Add(wx.StaticText(panel, label='file tree from folder'))

        # self.file_tree = wx.GenericDirCtrl(panel, -1, style=wx.DIRCTRL_DIR_ONLY)

        self.file_tree = customtree.CustomTreeCtrl(panel, -1, agwStyle=wx.TR_DEFAULT_STYLE | wx.TR_NO_BUTTONS)
        self.file_tree.SetBackgroundColour("White")
        # self.file_tree.SetBorderPen(wx.Pen("Black", 10))

        self.Bind(customtree.EVT_TREE_SEL_CHANGED, self.OnTreeFolderItemSelect, self.file_tree)
        self.Bind(customtree.EVT_TREE_ITEM_ACTIVATED, self.OnTreeFolderItemActived, self.file_tree)

        # self.file_tree = wx.GenericDirCtrl(panel, dir = wx.EmptyString, style=wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER)

        # file_tree = self.file_tree.GetTreeCtrl()
        # file_tree.AppendItem(file_tree.GetRootItem(), "/Users/lirui")

        left_box.Add(self.file_tree, 3, wx.EXPAND)

        left_box.Add(wx.StaticText(panel, label='photo files'))

        self.list_box_files = wx.ListBox(panel, -1, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxFilesSelect, self.list_box_files)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxFilesDouble, self.list_box_files)

        self.list_box_files.Bind(wx.EVT_KEY_UP, self.OnListBoxFilesKey)

        left_box.Add(self.list_box_files, 2, wx.EXPAND)

        box_all.Add(left_box, 2, wx.EXPAND)
        box_all.Add(self.panel1, 10, wx.EXPAND)

        #
        # p1 = wx.Panel(panel)
        # p1.SetBackgroundColour('#eded43')
        #
        # box_all.Add(p1, flag=wx.RIGHT|wx.EXPAND, border=8)
        #
        # box_all.Add(wx.Button(parent=panel, label=u'line one'), flag=wx.EXPAND, proportion=wx.EXPAND)



        panel.SetAutoLayout(True)

        panel.SetSizer(box_all)

        pass

    def OnListBoxRootDouble(self, event):
        print("double")
        print(event.GetEventObject().GetItems()[0])

        aaa = str(event.GetEventObject().GetItems()[0])

        self.open_file(aaa)

    def OnListBoxRootSelect(self, event):
        # indexSelected = event.GetEventObject().GetSelection()
        # print('选中Item的下标：', indexSelected)
        # print(event.GetEventObject().GetItems()[0])
        self.BuildFileTree(event.ClientData, False)
        pass

    def OnListBoxFilesKey(self, event):
        print(event.GetKeyCode())
        if event.GetKeyCode() == wx.WXK_RIGHT:
            print("r")
            self.FileTreeMove(True)
        elif event.GetKeyCode() == wx.WXK_LEFT:
            print("l")
            self.FileTreeMove(False)

    def FileTreeMove(self, _next=True):
        item = self.file_tree.GetSelection()
        parent = item.GetParent()
        index = 0
        total = len(parent.GetChildren())
        for i in range(0, total):
            if item == parent.GetChildren()[i]:
                index = i
                break

        print(index)
        if _next:
            if index < total - 1:
                self.file_tree.SelectItem(parent.GetChildren()[index + 1])
        else:
            if index > 0:
                self.file_tree.SelectItem(parent.GetChildren()[index - 1])

            pass

        pass

    def OnListBoxFilesDouble(self, event):
        print("double")
        print(event.GetEventObject().GetItems()[0])
        self.open_file(self.list_box_files_path)
        pass

    def OnListBoxFilesSelect(self, event):
        indexSelected = event.GetEventObject().GetSelection()
        # print('选中Item的下标：', indexSelected)
        # print(event.GetEventObject().GetItems()[0])
        # self.BuildFileTree(event.ClientData, False)
        self.ShowPic(os.path.join(self.list_box_files_path, event.GetEventObject().GetItems()[indexSelected]))
        pass

    def ShowPic(self, location):
        # print("pic!" + location)

        h = self.photo.Size.height
        w = self.photo.Size.width
        print("p1:" + str(w) + " " + str(h))#this will somehow change @#$%@#$R@#$%!!!

        h = self.panel1.Size.height
        w = self.panel1.Size.width
        print("p2:" + str(w) + " " + str(h))

        img = wx.Image(location)

        # img = bitmap.ConvertToImage()

        W = img.GetWidth()
        H = img.GetHeight()

        nW = W
        nH = H

        if W > w or H > h:

            r = h / w
            R = H / W

            if r >= R:
                # fit width
                nW = w
                nH = nW * R

            else:
                # fit height
                nH = h
                nW = nH * (1 / R)

            img = img.Scale(nW, nH, wx.IMAGE_QUALITY_HIGH)


        print("pic:" + str(W) + " " + str(H))
        print("sc:" + str(nW) + " " + str(nH))
        self.photo.SetBitmap(wx.Bitmap(img))
        posX = w/2-nW/2
        self.photo.SetPosition((posX, 0))
        pass

    def BuildFileTree(self, data, showFile=True):
        self.file_tree.DeleteAllItems()

        root_item = self.file_tree.AddRoot(data["path"], ct_type=0)

        for folders in data["folders"]:
            self.AddFileTreeBlock(folders, root_item, showFile)
        if showFile:
            for files in data["files"]:
                self.file_tree.AppendItem(root_item, files, ct_type=0)

                # item = self.file_tree.AppendItem(self.root, "wangjian", ct_type=0)
        self.file_tree.ExpandAll()
        # self.file_tree.Expand(root_item)

    def AddFileTreeBlock(self, data, root_item, showFile=True):
        item = self.file_tree.AppendItem(root_item, data["name"], ct_type=0, data=data)

        for folders in data["folders"]:
            self.AddFileTreeBlock(folders, item, showFile)
        if showFile:
            for files in data["files"]:
                self.file_tree.AppendItem(item, files, ct_type=0)

        pass

    def ListBoxFilesFill(self, path, f_names):
        self.list_box_files.Clear()
        self.list_box_files_path = path
        if len(f_names) > 0:
            for f in f_names:
                self.list_box_files.Append(f)
            self.list_box_files.AcceptsFocus()
            self.list_box_files.SetSelection(0)
            self.ShowPic(os.path.join(path, f_names[0]))
        pass

    def OnTreeFolderItemActived(self, event):
        print(event._item._data["path"])
        self.open_file(event._item._data["path"])

    def OnTreeFolderItemSelect(self, event):
        print(event._item._data["path"])
        self.ListBoxFilesFill(event._item._data["path"], event._item._data["files"])

    def OnDropFiles(self, target, x, y, paths):
        # print(target)
        # print(x)
        # print(y)
        # print(f_names)

        path = paths[0]

        if os.path.isdir(path):
            # data = self.MakeFolderTree(path)
            data = self.MakePhotoFolderTree(path)
            self.list_box_root.Append(path, data)
            self.BuildFileTree(data, False)

    def MakeFolderTree(self, path):
        name = ntpath.basename(path)
        folders = []
        files = []
        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)
            if os.path.isdir(full_path):
                folders.append(self.MakeFolderTree(full_path))
            else:
                files.append(file_name)
        return {"name": name, "path": path, "folders": folders, "files": files}

    def MakePhotoFolderTree(self, path):
        name = ntpath.basename(path)
        folders = []
        files = []
        for file_name in os.listdir(path):
            full_path = os.path.join(path, file_name)
            if os.path.isdir(full_path):
                folder_block = self.MakePhotoFolderTree(full_path)
                if len(folder_block["folders"]) != 0 or len(folder_block["files"]) != 0:
                    folders.append(folder_block)
            else:
                if file_name.endswith(".png") or file_name.endswith(".jpg"):
                    files.append(file_name)
        return {"name": name, "path": path, "folders": folders, "files": files}

    def open_file(self, path):
        if platform.system() == "Windows":
            subprocess.Popen(["explorer", "/select,", path])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])


if __name__ == '__main__':
    app = wx.App()
    Application(None, title="Border")
    app.MainLoop()
