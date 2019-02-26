from tkinter import *
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
from pywinauto import Application
import win32gui, win32ui, win32con, win32api, pyautogui, pywinauto
import time

class Ball:
    def __init__(self):
        self.game = 'RetroArch Genesis Plus GX v1.7.4 f5eed51'

        self.root = Tk()
        self.root.title = "Title"
        self.root.resizable(0,0)
        #self.root.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.root, width = 800, height = 400, bd = 1, highlightthickness = 0)
        self.canvas.pack()
        button_right = Button(self.root, text=">", command=self.action_right)
        button_right.place(x=150, y=330)
        button_up = Button(self.root, text="^", command=self.action_up)
        button_up.place(x=100, y=310)
        button_left = Button(self.root, text="<", command=self.action_left)
        button_left.place(x=50, y=330)
        button_down = Button(self.root, text="v", command=self.action_down)
        button_down.place(x=100, y=360)
        button_a = Button(self.root, text="a", command=self.action_a)
        button_a.place(x=200, y=330)
        button_b = Button(self.root, text="b", command=self.action_b)
        button_b.place(x=230, y=330)
        button_c = Button(self.root, text="c", command=self.action_c)
        button_c.place(x=260, y=330)

    def action_right(self):
        win32gui.SetForegroundWindow(self.hwnd)
        win32api.keybd_event(0x27, 0,1,0)
        time.sleep(.05)
        win32api.keybd_event(0x27, 0, win32con.WM_KEYUP, 0)
        #win32api.keybd_event(self.hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        win32gui.SetForegroundWindow(self.self)
    def action_up(self):
        print("up")
    def action_left(self):
        print("left")
    def action_down(self):
        print("left")
    def action_a(self):
        print("a")
    def action_b(self):
        print("b")
    def action_c(self):
        print("c")

    def draw(self):
        self.hwnd = win32gui.FindWindow(None, self.game)
        self.self = win32gui.FindWindow(None, "tk")
        windowcor = win32gui.GetWindowRect(self.hwnd)
        w = windowcor[2] - windowcor[0]
        h = windowcor[3] - windowcor[1]
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        self.dataBitMap = win32ui.CreateBitmap()
        self.dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(self.dataBitMap)
        cDC.BitBlt((0,0), (w, h), dcObj, (0,0), win32con.SRCCOPY)

        bmpinfo = self.dataBitMap.GetInfo()
        bmpstr = self.dataBitMap.GetBitmapBits(True)
        self.img_source = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        self.img_main_orig = self.img_source
        self.img_main_orig = self.img_main_orig.resize((400, 300), Image.ANTIALIAS)
        #self.img_main_orig = ImageGrab.grab(bbox=(0, 0, 800, 600)).resize((400, 300), Image.ANTIALIAS)
        self.img_main = ImageTk.PhotoImage(self.img_main_orig)
        self.id = self.canvas.create_image(0, 0, anchor=NW, image=self.img_main)

        self.img_small_orig = self.img_main_orig.resize((200,150), Image.ANTIALIAS)

        self.img_threshold_orig = ImageEnhance.Contrast(self.img_small_orig).enhance(-5.0)
        self.img_threshold_orig = self.img_threshold_orig.convert('1')
        self.img_threshold = ImageTk.PhotoImage(self.img_threshold_orig)
        self.id = self.canvas.create_image(400, 0, anchor=NW, image=self.img_threshold)

        self.img_grayscale_enhanced = self.img_threshold_orig.filter(ImageFilter.FIND_EDGES)
        self.img_grayscale_enhanced = ImageTk.PhotoImage(self.img_grayscale_enhanced)
        self.id = self.canvas.create_image(600, 0, anchor=NW, image=self.img_grayscale_enhanced)

        self.img_contrast_orig = ImageEnhance.Contrast(self.img_small_orig).enhance(10.0)
        self.img_contrast_orig = self.img_contrast_orig.convert('1')
        self.img_contrast = ImageTk.PhotoImage(self.img_contrast_orig)
        self.id = self.canvas.create_image(400, 150, anchor=NW, image=self.img_contrast)

        self.img_contrast_enhanced = self.img_contrast_orig.filter(ImageFilter.FIND_EDGES)
        self.img_contrast_enhanced = ImageTk.PhotoImage(self.img_contrast_enhanced)
        self.id = self.canvas.create_image(600, 150, anchor=NW, image=self.img_contrast_enhanced)

        self.canvas.after(50, self.draw)



hwnd=win32gui.GetDesktopWindow()
ball = Ball()
ball.draw()  #Changed per Bryan Oakley's comment.
ball.root.mainloop()


'''
window = Tk()
canvas = Canvas(window, width = 800, height = 300)
canvas.pack()

test = ImageGrab.grab(bbox=(0, 0, 800, 600)).resize((400, 300), Image.ANTIALIAS)
test = ImageTk.PhotoImage(test)
canvas.create_image(0, 0, anchor=NW, image=test)

window.mainloop()

mainGameImg = Image.open("img/RR_Example1.png").resize((400,300), Image.ANTIALIAS)
mainGameImg = ImageTk.PhotoImage(mainGameImg)
canvas.create_image(0, 0, anchor=NW, image=mainGameImg)

thresholdImg = Image.open("img/RR_Example1_A1_BWThreshold.png").resize((200, 150), Image.ANTIALIAS)
thresholdImg = ImageTk.PhotoImage(thresholdImg)
canvas.create_image(400, 0, anchor=NW, image=thresholdImg)

playerImg = Image.open("img/RR_Example1_A2_BoundryAndPlayer.png").resize((200, 150), Image.ANTIALIAS)
playerImg = ImageTk.PhotoImage(playerImg)
canvas.create_image(600, 0, anchor=NW, image=playerImg)

contrastImg = Image.open("img/RR_Example1_B1_ThresholdWContrast.png").resize((200, 150), Image.ANTIALIAS)
contrastImg = ImageTk.PhotoImage(contrastImg)
canvas.create_image(400, 150, anchor=NW, image=contrastImg)

roadImg = Image.open("img/RR_Example1_B1_Road.png").resize((200, 150), Image.ANTIALIAS)
roadImg = ImageTk.PhotoImage(roadImg)
canvas.create_image(600, 150, anchor=NW, image=roadImg)
'''
