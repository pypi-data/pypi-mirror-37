# -*- coding:utf-8 -*- 
# Date: 2018-03-07 16:41:50
# Author: dekiven

import os
from DKVTools.Funcs import *

if isPython3() :
    import tkinter as tk  
    from tkinter import ttk 
    from tkinter import *
    import tkinter.filedialog as fileDialog
    import tkinter.messagebox as messageBox
else:
    import Tkinter as tk  
    import  ttk
    from Tkinter import *
    import tkFileDialog as fileDialog
    import tkMessageBox as messageBox


Pathjoin = os.path.join
PathExists = os.path.exists
# curDir = os.getcwd()
curDir = os.path.split(sys.argv[0])[0]

def getTk() :
    '''return tk, ttk
    '''
    return tk, ttk

def GetEntry(root, default='', onKey=None) :
    et = StringVar()
    entry = ttk.Entry(root, textvariable=et)
    if isFunc(onKey) :
        entry.bind('<Key>', lambda event : onKey(event.char))

    def getValue() :
        return et.get()
    def setValue(value) :
        return et.set(str(value))
    entry.getValue = getValue
    entry.setValue = setValue
    setValue(default)

    return entry


def GetDirWidget(root, title='', titleUp='', pathSaved = None, callback = None, enableEmpty = False, showOpen = True):
    '''paramas:root, title='', titleUp='', pathSaved = None, callback = None, enableEmpty = False, showOpen = True
    root:           tk 父节点
    title:          显示在Entry左边的标题
    titleUp:        显示在Entry上面的文本
    pathSaved:      默认的路径，会显示都Entry
    callback:       选择好文件夹的回调
    enableEmpty:    没有选择文件夹时是否回调空串
    showOpen:       是否显示打开文件夹的按钮
    '''
    widget = Frame(root)
    widget.columnconfigure(1, weight=1)


    strTitle = StringVar()
    strTitle.set(title)
    Label(widget, textvariable = strTitle).grid(row = 1, column = 0, padx=5)

    strPathD = StringVar()
    strPathD.set(titleUp)
    Label(widget, textvariable = strPathD).grid(row = 0, column = 1, sticky=(N, S, W, E), pady=5)

    strTitle = StringVar()
    strTitle.set(title)
    et = StringVar()
    if pathSaved :
        et.set(pathSaved)

    Entry(widget, textvariable = et).grid(row = 1, column = 1, sticky=(N, S, W, E), pady=5)

    def btnCallback():
        def onChoosen(path):
            if path is not None and path != '' or enableEmpty :
                setValue(path)
                if callback is not None :
                    callback(path)
        ShowChooseDirDialog(onChoosen, initialdir=et.get())

    def openBtnCallback():
        path = et.get()
        if os.path.exists(path) :
            startFile(path)
        else :
            ShowInfoDialog('文件夹[%s]不存在！'%(str(path)))

    Button(widget, text = 'Search', command = btnCallback).grid(row = 1, column = 2, padx=5)
    if showOpen :
        Button(widget, text = 'Open', command = openBtnCallback).grid(row = 1, column = 3, padx=5)

    widget.strTitle = strTitle
    widget.strPathD = strPathD
    widget.et = et

    def setValue(value):
        et.set(value)
    widget.setValue = setValue

    return widget

def ShowChooseDirDialog(callback=None, **options):  
    '''ShowChooseDirDialog(callback=None, **options)
    callback 回调，传入选中的文件夹名
    options = {
        'defaultextension' : '.txt',
        'filetypes' : [('all files', '.*'), ('text files', '.txt')],
        'initialdir' : initDir,
        'initialfile' : 'myfile.txt',
        'parent' : root,
        'title' : 'This is a title',
    }可部分或全部不设置  
    '''
    path = fileDialog.askdirectory(**options)
    if isFunc(callback):
        # if not isinstance(path, str):
        #   path = path
        callback(path)


def ShowChooseFileDialog(callback=None, MultiChoose=False, **options):  
    '''ShowChooseFileDialog(callback=None, MultiChoose=False, **options)
    callback 回调，传入选中的文件名Tuple
    MultiChoose 是否是多选模式
    options = {
        'defaultextension' : '.txt',
        'filetypes' : [('all files', '.*'), ('text files', '.txt')],
        'initialdir' : initDir,
        'initialfile' : 'myfile.txt',
        'parent' : root,
        'title' : 'This is a title',
    }可部分或全部不设置
    '''
    path = None
    if MultiChoose :
        path = fileDialog.askopenfilenames(**options)
    else :
        path = fileDialog.askopenfilename(**options)
    if isFunc(callback) :
        # if not isinstance(path, str):
        #   path = path
        callback(path)

def ShowSaveAsFileDialog(callback=None, **options):
    '''ShowSaveAsFileDialog(callback=None, **options)
    callback 回调，传入保存的文件名
    options = {
        'defaultextension' : '.txt',
        'filetypes' : [('all files', '.*'), ('text files', '.txt')],
        'initialdir' : initDir,
        'initialfile' : 'myfile.txt',
        'parent' : root,
        'title' : 'This is a title',
    }可部分或全部不设置  
    '''
    path = fileDialog.asksaveasfilename(**options)
    if isFunc(callback) :
        # if not isinstance(path, str):
        #   path = path
        callback(path)

def ShowInfoDialog(msg, title = 'Tips'):
    '''显示一个按钮的消息框。'''
    return messageBox.showinfo(title = title, message = msg)

def ShowAskDialog(msg, title = 'Asking'):
    '''显示有Yes，NO两个选项的提示框。'''
    return messageBox.askokcancel(title = title, message = msg)

def isTkWidget(widget) :
    '''返回widget是否是tk.Widget实例
    '''
    return isinstance(widget, Widget)

def isTK(widget) :
    '''返回widget是否是TK实例
    '''
    return isinstance(widget, Tk)

def getToplevel(widget) :
    '''获取tk(ttk) widget的Toplevel(根节点)
    '''
    if isTkWidget(widget) :
        return widget.winfo_toplevel()
    else :
        if isTK(widget) :
            return widget
        return None

def centerToplevel(widget) :
    '''将给定widget的Toplevel移到屏幕中央
    最好是在UI布局完成后调用
    '''
    top = getToplevel(widget)
    if top :
        top.update()
        topH = top.winfo_reqheight()
        topW = top.winfo_reqwidth()
        screenW, screenH = top.maxsize()
        top.geometry('+%d+%d'%((screenW-topW)/2, (screenH-topH)/2))

def getScreenSize(widget) :
    '''通过widget获取屏幕大小（toplevel的最大大小）
    '''
    top = getToplevel(widget)
    if top :
        return top.maxsize()

__quitHandleFuncs = {}
def handleToplevelQuit(widget, callback) :
    '''捕获给定widget的Toplevel的关闭事件。当Toplevel关闭时调用callback'''
    top = getToplevel(widget)

    funcs = __quitHandleFuncs.get(str(top))
    if funcs is None :
        funcs = []
    if not callback in funcs :
        funcs.append(callback)
    __quitHandleFuncs[str(top)] = funcs

    def quit(*args, **dArgs):
        for f in funcs :
            if isFunc(f) :
                f()
        del __quitHandleFuncs[str(top)]
        top.quit()

    if top is not None and isFunc(callback) :
        top.protocol('WM_DELETE_WINDOW', quit)

def startTk(viewCotr, *args, **dArgs) :
    '''传入tk.View的子类构造函数（类名）和除parent之外的参数启动一个tk窗口
如:   startTk(GetDirWidget,  u'选择路径', 'test')
'''
    root = tk.Tk()

    app = viewCotr(root, *args, **dArgs)
    # app.loadConfigs('config/projConfig.json')
    app.pack(fill=tk.BOTH, expand=True)
    centerToplevel(app)
    app.focus_set()
    root.mainloop()

# ==================鼠标Enter提示Label  begin----------------
class __ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0

    def showtip(self, **labelConfig):
        "Display text in tooltip window"
        if self.tipwindow :
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()
        y = y + cy + self.widget.winfo_rooty() - 50
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        keys = list(labelConfig.keys())

        if 'bg' not in keys and 'background' not in keys :
            labelConfig['bg'] = '#aaaaff'
        label = ttk.Label(tw, **labelConfig)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def regEnterTip(widget, **labelConfig) :
    '''regEnterTip(widget, **labelConfig)
    给widget注册事件，当鼠标移到widget中时显示toolTip
    labelConfig 是tk.Label的构造参数，如：text='toolTip', bg = '#aaaaff'
    '''
    toolTip = __ToolTip(widget)
    def enter(event):
        toolTip.showtip(**labelConfig)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
# ----------------鼠标Enter提示Label  end==================


# ---------------------------------------------test begin --------------------------------------------------

def __testHandleToplevelQuit() :
    f = Frame()
    f.grid()

    l = Label(f, text='test')
    f.grid()

    def handleF() :
        print('f')

    def handleL() :
        print('l')

    handleToplevelQuit(f, handleF)
    handleToplevelQuit(l, handleL)

    f.mainloop()

def __testAskFile() :
    def func(*args, **dArgs) :
        print(args, dArgs)

    ShowChooseFileDialog(func)
    ShowChooseFileDialog(func, True)

def __testGetDirWid() :
    # root = Tk()
    # v = GetDirWidget(root, '选择路径', 'test')
    # v.pack(expand=YES, fill=BOTH)
    # centerToplevel(v)
    # v.mainloop()
    startTk(GetDirWidget,  u'选择路径', 'test')

def __testCenterTop() :
    app = tk.Tk()
    centerToplevel(app)
    app.mainloop()

def __main():
    # __testAskFile()
    # __testHandleToplevelQuit()
    __testGetDirWid()
    # __testCenterTop()


if __name__ == '__main__':
    __main()
# ============================================test end ===========================================
