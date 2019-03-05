from tkinter import *
import pyvjoy
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
from pywinauto import Application
import win32gui, win32ui, win32con, win32api, pyautogui, pywinauto
import time

class GUI:
    def __init__(self):
        self.scale = 3;
        self.game = 'RetroArch Genesis Plus GX v1.7.4 f5eed51'
        self.root = Tk()
        self.root.title = "Title"
        self.root.resizable(0,0)
        #self.root.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.root, width = 800*self.scale, height = 400*self.scale, bd = 1, highlightthickness = 0)
        self.canvas.pack()
        button_right = Button(self.root, text=">")
        button_right.bind("<ButtonPress>", self.action_right_press)
        button_right.bind("<ButtonRelease>", self.action_right_release)
        button_right.place(x=150*self.scale, y=330*self.scale)
        button_up = Button(self.root, text="^")
        button_up.bind("<ButtonPress>", self.action_up_press)
        button_up.bind("<ButtonRelease>", self.action_up_release)
        button_up.place(x=100*self.scale, y=310*self.scale)
        button_left = Button(self.root, text="<")
        button_left.bind("<ButtonPress>", self.action_left_press)
        button_left.bind("<ButtonRelease>", self.action_left_release)
        button_left.place(x=50*self.scale, y=330*self.scale)
        button_down = Button(self.root, text="v")
        button_down.bind("<ButtonPress>", self.action_down_press)
        button_down.bind("<ButtonRelease>", self.action_down_release)
        button_down.place(x=100*self.scale, y=360*self.scale)
        button_a = Button(self.root, text="a")
        button_a.bind("<ButtonPress>", self.action_a_press)
        button_a.bind("<ButtonRelease>", self.action_a_release)
        button_a.place(x=200*self.scale, y=330*self.scale)
        button_b = Button(self.root, text="b")
        button_b.bind("<ButtonPress>", self.action_b_press)
        button_b.bind("<ButtonRelease>", self.action_b_release)
        button_b.place(x=230*self.scale, y=330*self.scale)
        button_c = Button(self.root, text="c")
        button_c.bind("<ButtonPress>", self.action_c_press)
        button_c.bind("<ButtonRelease>", self.action_c_release)
        button_c.place(x=260*self.scale, y=330*self.scale)

        self.gamepad = pyvjoy.VJoyDevice(1)

    def action_right_press(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x8000)
    def action_right_release(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x4000)

    def action_up_press(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
    def action_up_release(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_Y, 0x4000)

    def action_left_press(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x1)
    def action_left_release(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x4000)

    def action_down_press(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_Y, 0x8000)
    def action_down_release(self, event):
        self.gamepad.set_axis(pyvjoy.HID_USAGE_Y, 0x4000)

    def action_a_press(self, event):
        self.gamepad.set_button(1, 1)
    def action_a_release(self, event):
        self.gamepad.set_button(1, 0)

    def action_b_press(self, event):
        self.gamepad.set_button(2, 1)
    def action_b_release(self, event):
        self.gamepad.set_button(2, 0)

    def action_c_press(self, event):
        self.gamepad.set_button(3, 1)
    def action_c_release(self, event):
        self.gamepad.set_button(3, 0)

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
        cDC.BitBlt((0,-86), (w, h), dcObj, (0,0), win32con.SRCCOPY)

        bmpinfo = self.dataBitMap.GetInfo()
        bmpstr = self.dataBitMap.GetBitmapBits(True)
        self.img_source = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        self.img_main_orig = self.img_source
        self.img_main_orig = self.img_main_orig.resize((400*self.scale, 300*self.scale), Image.ANTIALIAS)
        #self.img_main_orig = ImageGrab.grab(bbox=(0, 0, 800, 600)).resize((400, 300), Image.ANTIALIAS)
        self.img_main = ImageTk.PhotoImage(self.img_main_orig)
        self.id = self.canvas.create_image(0, 0, anchor=NW, image=self.img_main)

        self.img_small_orig = self.img_main_orig.resize((200*self.scale, 150*self.scale), Image.ANTIALIAS)

        self.img_threshold_orig = ImageEnhance.Contrast(self.img_small_orig).enhance(-5.0)
        self.img_threshold_orig = self.img_threshold_orig.convert('1')
        self.img_threshold = ImageTk.PhotoImage(self.img_threshold_orig)
        self.id = self.canvas.create_image(400*self.scale, 0, anchor=NW, image=self.img_threshold)

        self.img_grayscale_enhanced = self.img_threshold_orig.filter(ImageFilter.FIND_EDGES)
        self.img_grayscale_enhanced = ImageTk.PhotoImage(self.img_grayscale_enhanced)
        self.id = self.canvas.create_image(600*self.scale, 0, anchor=NW, image=self.img_grayscale_enhanced)

        self.img_contrast_orig = ImageEnhance.Contrast(self.img_small_orig).enhance(10.0)
        self.img_contrast_orig = self.img_contrast_orig.convert('1')
        self.img_contrast = ImageTk.PhotoImage(self.img_contrast_orig)
        self.id = self.canvas.create_image(400*self.scale, 150*self.scale, anchor=NW, image=self.img_contrast)

        self.img_contrast_enhanced = self.img_contrast_orig.filter(ImageFilter.FIND_EDGES)
        self.img_contrast_enhanced = ImageTk.PhotoImage(self.img_contrast_enhanced)
        self.id = self.canvas.create_image(600*self.scale, 150*self.scale, anchor=NW, image=self.img_contrast_enhanced)

        self.canvas.after(50, self.draw)



hwnd=win32gui.GetDesktopWindow()
gui = GUI()
gui.draw()
gui.root.mainloop()
