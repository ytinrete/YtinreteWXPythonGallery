import wx
import wx.lib.agw.customtreectrl as customtree
import os
from pathlib import Path
import datetime
from random import randrange


class PhotoInfo:
    '''record all the info of a photo file'''
    fileParentFolderName: str
    fileName: str
    fileFullPath: str
    fileModifyDate: str


class State:
    '''record all the origin data from import'''
    originPhotoRootPath: str
    originPhotos: []
    filteredPhotos = []


class PhotoTree(customtree.CustomTreeCtrl):
    def __init__(self, parent):
        super().__init__(parent, agwStyle=wx.TR_HAS_BUTTONS | wx.TR_FULL_ROW_HIGHLIGHT)
        self.treeRoot = None
        self.treeGroup = {}

    def loadData(self, filteredPhotos):
        self.DeleteAllItems()
        self.treeGroup = {}
        self.treeRoot = self.AddRoot("root")

        folderPhotoMap = {}

        def sortFunc(photo):
            return photo.fileName

        for photo in filteredPhotos:
            if folderPhotoMap.get(photo.fileParentFolderName) is None:
                folderPhotoMap[photo.fileParentFolderName] = []
            folderPhotoMap[photo.fileParentFolderName].append(photo)

        folderList = list(folderPhotoMap.keys())
        folderList.sort()

        for folder in folderList:
            folderNode = self.AppendItem(self.treeRoot, folder, data=folder)
            photoList = folderPhotoMap[folder]
            photoList.sort(key=sortFunc)
            photoNodeList = []
            for photo in photoList:
                photoNode = self.AppendItem(folderNode, photo.fileName, data=photo)
                photoNodeList.append(photoNode)
            self.treeGroup[folderNode] = photoNodeList

        self.SelectItem(self.treeRoot)
        self.ExpandAll()
        # self.treeRoot.Expand()

    def setSelectForPhoto(self, choosePhoto):
        for folder, photoList in self.treeGroup.items():
            for photo in photoList:
                data = photo.GetData()
                if isinstance(data, PhotoInfo) and data.fileFullPath == choosePhoto.fileFullPath:
                    self.SelectItem(photo)
                    return


class Application(wx.Frame):
    def __init__(self, parent, title):
        super(Application, self).__init__(parent, title=title, size=(800, 600))
        self.state = State()
        self.__init_ui()
        self.Centre()
        self.Show()

    def __init_ui(self):

        '''
        main ui
        ---------
            -mainPanel
                -mainSizer
                    -leftPanel
                    -rightPanel
        '''
        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetAutoLayout(True)
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainPanel.SetSizer(self.mainSizer)

        '''
        left components
        ----------------
            -leftPanel
                -leftPanelSizer
                    -leftImportBtn
                    -Text 'Folder Files'
                    -leftFileTree
                    -Text 'Filter By Time'
                    -Text 'From'
                    -leftFilterByTimeFrom
                    -Text 'To'
                    -leftFilterByTimeTo
                    -leftFilterByTimeBtn
                    -Text 'Filter By keyword'
                    -leftFilterByKeyword
                    -leftFilterByKeywordBtn
                    -Text 'actions'
                    
        '''
        self.leftPanel = wx.Panel(self.mainPanel, -1, style=wx.SUNKEN_BORDER)
        self.leftPanel.SetAutoLayout(True)
        self.mainSizer.Add(self.leftPanel, 2, wx.EXPAND)

        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftPanel.SetSizer(self.leftSizer)

        self.leftImportBtn = wx.Button(self.leftPanel, -1, "import")
        self.leftImportBtn.Bind(wx.EVT_BUTTON, self.onImportBtnClick)
        self.leftSizer.Add(self.leftImportBtn, 0, wx.EXPAND | wx.BOTTOM, 20)

        self.leftSizer.Add(wx.StaticText(self.leftPanel, label='Folder Files'))

        self.leftFileTree = PhotoTree(self.leftPanel)
        self.leftFileTree.SetBackgroundColour("White")
        self.leftFileTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onPhotoTreeSelectionChange)
        # self.leftFileTree.Bind(wx.EVT_TREE_KEY_DOWN, self.onPhotoTreeKeyDown)
        self.leftSizer.Add(self.leftFileTree, 1, wx.EXPAND | wx.BOTTOM, 20)

        self.leftSizer.Add(wx.StaticText(self.leftPanel, label='Filter By Time'))
        self.leftSizer.Add(wx.StaticText(self.leftPanel, label='From'))
        self.leftFilterByTimeFrom = wx.TextCtrl(self.leftPanel)
        self.leftSizer.Add(self.leftFilterByTimeFrom, 0, wx.EXPAND)
        self.leftSizer.Add(wx.StaticText(self.leftPanel, label='To'))
        self.leftFilterByTimeTo = wx.TextCtrl(self.leftPanel)
        self.leftSizer.Add(self.leftFilterByTimeTo, 0, wx.EXPAND)
        self.leftFilterByTimeBtn = wx.Button(self.leftPanel, -1, "FilterByTime")
        self.leftFilterByTimeBtn.Bind(wx.EVT_BUTTON, self.onFilterByTimeBtnClick)
        self.leftSizer.Add(self.leftFilterByTimeBtn, 0, wx.EXPAND | wx.BOTTOM, 20)

        self.leftSizer.Add(wx.StaticText(self.leftPanel, label='Filter By keyword'))
        self.leftFilterByKeyword = wx.TextCtrl(self.leftPanel, style=wx.TE_PROCESS_ENTER)

        self.leftFilterByKeyword.Bind(wx.EVT_TEXT_ENTER, self.onFilterByKeywordTextCtrlEnter)

        self.leftSizer.Add(self.leftFilterByKeyword, 0, wx.EXPAND)
        self.leftFilterByKeywordBtn = wx.Button(self.leftPanel, -1, "FilterByKeyword")
        self.leftFilterByKeywordBtn.Bind(wx.EVT_BUTTON, self.onFilterByKeywordBtnClick)
        self.leftSizer.Add(self.leftFilterByKeywordBtn, 0, wx.EXPAND | wx.BOTTOM, 20)

        self.leftSizer.Add(wx.StaticText(self.leftPanel, label='Actions'))
        self.leftActionRandomSelectBtn = wx.Button(self.leftPanel, -1, "RandomSelect")
        self.leftActionRandomSelectBtn.Bind(wx.EVT_BUTTON, self.onActionRandomSelectBtnClick)
        self.leftSizer.Add(self.leftActionRandomSelectBtn, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 20)

        '''
                right photo parts
                -----------------
                    -rightPanel
                        -rightSizer
                            -rightPhoto
                '''
        self.rightPanel = wx.Panel(self.mainPanel, -1, style=wx.SUNKEN_BORDER)
        self.rightPanel.SetBackgroundColour("Grey")
        self.rightPanel.SetAutoLayout(True)
        self.mainSizer.Add(self.rightPanel, 10, wx.EXPAND)

        self.rightSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightPanel.SetSizer(self.rightSizer)

        self.rightPhoto = wx.StaticBitmap(self.rightPanel, wx.ID_ANY)
        self.rightPhoto.SetBackgroundColour("Grey")
        self.rightSizer.Add(self.rightPhoto, 1, wx.EXPAND)

    def onImportBtnClick(self, event):
        with wx.DirDialog(None, "Choose photo root folder directory", "",
                          wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            print("onImportBtnClick:" + pathname)
            self.state.originPhotoRootPath = pathname
            self.importNewPhotoRoot()

    def importNewPhotoRoot(self):
        print("importNewPhotoRoot:" + self.state.originPhotoRootPath)
        self.state.originPhotos = []
        for root, dirs, files in os.walk(self.state.originPhotoRootPath):
            for file in files:
                if not file.startswith(".") and os.path.getsize(os.path.join(root, file)) > 10 and (
                        file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png")):
                    print(os.path.join(root, file))
                    fullPath = Path(os.path.join(root, file))
                    photo = PhotoInfo()
                    photo.fileName = file
                    photo.fileFullPath = str(fullPath.absolute())
                    photo.fileParentFolderName = fullPath.parent.name
                    photo.fileModifyDate = datetime.datetime.fromtimestamp(
                        os.path.getmtime(photo.fileFullPath)).strftime("%Y%m%d")
                    self.state.originPhotos.append(photo)
                    print("loaded:" + file)
        self.leftFilterByTimeFrom.SetValue("")
        self.leftFilterByTimeTo.SetValue("")
        self.leftFilterByKeyword.SetValue("")
        self.doFilterByTime()
        self.resetFileTreeByFilteredData()

    def onFilterByTimeBtnClick(self, event):
        self.doFilterByTime()

    def doFilterByTime(self):
        self.leftFilterByKeyword.SetValue("")
        '''20220801'''
        fromTime = self.leftFilterByTimeFrom.GetValue()
        if len(fromTime) != 8 or fromTime.strip() == "":
            fromTime = "00000000"
        toTime = self.leftFilterByTimeTo.GetValue()
        if len(toTime) != 8 or toTime.strip() == "":
            print("invalid toTime")
            toTime = "99999999"

        print("fromTime:" + fromTime + " toTime:" + toTime)

        self.state.filteredPhotos = []
        for photo in self.state.originPhotos:
            if fromTime <= photo.fileModifyDate <= toTime:
                self.state.filteredPhotos.append(photo)
        self.resetFileTreeByFilteredData()

    def onFilterByKeywordBtnClick(self, event):
        self.doFilterByKeyword()

    def onFilterByKeywordTextCtrlEnter(self, event):
        self.doFilterByKeyword()

    def doFilterByKeyword(self):
        self.leftFilterByTimeFrom.SetValue("")
        self.leftFilterByTimeTo.SetValue("")
        keyword = self.leftFilterByKeyword.GetValue().strip()
        print("keyword:" + keyword)

        self.state.filteredPhotos = []
        for photo in self.state.originPhotos:
            if photo.fileName.find(keyword) >= 0 or keyword == "":
                self.state.filteredPhotos.append(photo)
        self.resetFileTreeByFilteredData()

    def resetFileTreeByFilteredData(self):
        self.leftFileTree.loadData(self.state.filteredPhotos)

    def onPhotoTreeSelectionChange(self, event):
        data = self.leftFileTree.GetSelection().GetData()
        if isinstance(data, PhotoInfo):
            self.showPicture(data.fileFullPath)

    def onActionRandomSelectBtnClick(self, event):
        selected = self.state.filteredPhotos[randrange(len(self.state.filteredPhotos))]
        self.leftFileTree.setSelectForPhoto(selected)
        self.showPicture(selected.fileFullPath)

    def onPhotoTreeKeyDown(self, event):
        # TODO moving by keyboard
        if event.GetKeyCode() == wx.WXK_DOWN:
            print("kkk")

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
                # see parent's next
                grand = parent.GetParent()
                index_p = 0
                total_p = len(grand.GetChildren())
                for i in range(0, total_p):
                    if parent == grand.GetChildren()[i]:
                        index_p = i
                        break
                if index_p != total_p - 1:
                    self.file_tree.SelectItem(grand.GetChildren()[index_p + 1].GetChildren()[0])
        else:
            if index > 0:
                self.file_tree.SelectItem(parent.GetChildren()[index - 1])
            else:
                # see parent's last
                grand = parent.GetParent()
                index_p = 0
                total_p = len(grand.GetChildren())
                for i in range(0, total_p):
                    if parent == grand.GetChildren()[i]:
                        index_p = i
                        break
                if index_p > 0:
                    self.file_tree.SelectItem(grand.GetChildren()[index_p - 1].GetChildren()[0])

    def showPicture(self, fileFullPath):
        print("showPicture:" + fileFullPath)
        h = self.rightPanel.Size.height
        w = self.rightPanel.Size.width
        print("p2:" + str(w) + " " + str(h))
        img = wx.Image(fileFullPath)
        W = img.GetWidth()
        H = img.GetHeight()
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
            img = img.Scale(int(nW), int(nH), wx.IMAGE_QUALITY_HIGH)
        else:
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
            img = img.Scale(int(nW), int(nH), wx.IMAGE_QUALITY_HIGH)

        print("pic:" + str(W) + " " + str(H))
        print("sc:" + str(nW) + " " + str(nH))
        self.rightPhoto.SetBitmap(wx.Bitmap(img))
        posX = int(w / 2 - nW / 2)
        posY = int(h / 2 - nH / 2)
        self.rightPhoto.SetPosition((posX, posY))
        self.rightPanel.Refresh()


if __name__ == '__main__':
    app = wx.App()
    Application(None, title="PhotoGallery")
    app.MainLoop()
