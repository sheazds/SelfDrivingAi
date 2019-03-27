import tkinter as tk
from tkinter import *
import pyvjoy
from PIL import ImageTk, Image, ImageEnhance, ImageFilter, ImageGrab
from pywinauto import Application
import win32gui, win32ui, win32con, win32api, pyautogui, pywinauto
import time
import copy
import numpy

class GUI:
    def __init__(self):
        self.scale = 2;
        self.root = Tk()
        self.root.title = "Title"
        self.root.resizable(0,0)
        #self.root.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.root, width = 800*self.scale, height = 400*self.scale, bd = 1, highlightthickness = 0)
        self.canvas.pack()
        self.image_out = False;
        self.image_out_time = 0;
        self.image_out_count = 0;
        self.button_image_out = Button(self.root, text="ImageOut = No", command=self.action_image_out)
        self.button_image_out.place(x=400*self.scale, y=330*self.scale)
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

        self.games_list = ['RetroArch Genesis Plus GX v1.7.4 f5eed51', 'SomethingElse']
        for game in self.games_list :
            self.hwnd = win32gui.FindWindow(None, game)
            if (self.hwnd != 0) :
                self.self = win32gui.FindWindow(None, "tk")
                windowcor = win32gui.GetWindowRect(self.hwnd)
                self.w = windowcor[2] - windowcor[0]
                self.h = windowcor[3] - windowcor[1]
                wDC = win32gui.GetWindowDC(self.hwnd)
                self.dcObj = win32ui.CreateDCFromHandle(wDC)
                self.cDC = self.dcObj.CreateCompatibleDC()
                self.game = game
                break

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

    def action_image_out(self):
        if self.image_out :
            self.button_image_out.configure(text="ImageOut = No")
            self.image_out = False
        else :
            self.button_image_out.configure(text="ImageOut = Yes")
            self.image_out = True


    def draw(self):
        if (self.hwnd != 0) :
            self.dataBitMap = win32ui.CreateBitmap()
            self.dataBitMap.CreateCompatibleBitmap(self.dcObj, self.w, self.h)
            self.cDC.SelectObject(self.dataBitMap)
            self.cDC.BitBlt((0,-86), (self.w, self.h), self.dcObj, (0,0), win32con.SRCCOPY)
            bmpinfo = self.dataBitMap.GetInfo()
            bmpstr = self.dataBitMap.GetBitmapBits(True)
            self.img_source = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            self.img_main_orig = self.img_source
        else :
            self.img_main_orig = ImageGrab.grab(bbox=(0, 0, 800, 600)).resize((400, 300), Image.ANTIALIAS)

        self.img_main_orig = self.img_main_orig.resize((400*self.scale, 300*self.scale), Image.ANTIALIAS)
        self.img_main = ImageTk.PhotoImage(self.img_main_orig)
        self.id = self.canvas.create_image(0, 0, anchor=NW, image=self.img_main)

        self.img_cont_thresh = ImageEnhance.Contrast(self.img_main_orig).enhance(10.0)
        self.img_cont_thresh = self.img_cont_thresh.convert('1')
        print(self.direction(self.img_cont_thresh))
        '''
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
        '''

        if (self.image_out) :
            if (self.image_out_time == 3) :
                #out = self.img_main_orig
                out = ImageEnhance.Contrast(self.img_main_orig).enhance(10.0)
                out = out.convert('1')
                #out = out.filter(ImageFilter.FIND_EDGES)
                out.save("img_cont_thresh_" + str(self.image_out_count) + ".jpg")
                self.image_out_time = 0
                self.image_out_count += 1
            else :
                self.image_out_time += 1

        self.canvas.after(50, self.draw)

    def direction(self, image):
        image = image.crop((17*self.scale, 0*self.scale, 183*self.scale, 87*self.scale))
        x_width, y_height = image.size
        image.save("crop.jpg")
        pix_val = list(image.getdata())
        road_left = 0
        road_right = 0
        for pix_y in range(int(y_height / 2), y_height):
            for pix_x in range(0, x_width):
                pixel = (pix_y * x_width) + pix_x
                if pix_x < x_width / 2:
                    if pix_val[pixel] < 50:
                        road_left += 1
                else:
                    if pix_val[pixel] < 50:
                        road_right += 1

        if (road_left > road_right):
            return 1
        else :
            return 2

    def find_driver(self, image):
        image = image.crop((130*self.scale, 80*self.scale, 280*self.scale, 174*self.scale))
        image.save("find_driver.jpg")
        self.find_blobs(image)

    def find_blobs(self, image):
        x_width, y_height = image.size
        pix_val = list(image.getdata())
        all_blobs = list()
        # scan image 1 pixel in from top left corner so we can compare left and above
        for pix_y in range(1, y_height) :
            line_blobs = list()
            cur_blob = set()

            # traverse row and find contiguous white pixels as blobs
            last_pixel = 0
            for pix_x in range(1, x_width) :
                cur_pixel = (pix_y * x_width) + pix_x
                left_pixel = cur_pixel - 1

                # if current pixel is white
                if (pix_val[cur_pixel] > 225) :
                    # and last pixel is white
                    if (last_pixel > 225) :
                        print()
                    #
                    else :
                        print()
                    '''
                    if (left_pixel in cur_blob or len(cur_blob)) == 0 :
                        cur_blob.add(cur_pixel)
                    else :
                        line_blobs.append(cur_blob.copy())
                        cur_blob = set()
                        cur_blob.add(cur_pixel)
                    '''
                # current pixel not white, move on with last_pixel black
                else :
                    last_pixel = 0
            # append last blob in row to line_blobs
            if (len(cur_blob) > 0) :
                line_blobs.append(cur_blob)

            # merge blobs found in line with blobs found so far
            for line_blob in line_blobs :
                # extend blob up one pixel
                test_blob = line_blob.copy()
                for pixel in line_blob :
                    test_blob.add(pixel-x_width)
                new_blob = True
                for blob in all_blobs :
                    if len(blob.intersection(test_blob)) > 0 :
                        blob = blob.union(blob)
                        new_blob = False
                if new_blob :
                    all_blobs.append(line_blob)

            # merge all blobs
            last_blob = None
            for blob in all_blobs :
                if last_blob == None :
                    last_blob = blob
                else :
                    if last_blob >= blob :
                        all_blobs.remove(blob)

    def block_threshold(self, image, block_size, threshold):
        pix_val = numpy.array(image)
        for y in range(0, len(pix_val)-(block_size-1), block_size) :
            for x in range(0, len(pix_val[0])-(block_size-1), 2) :
                block_pixels = list()
                block_value = 0
                for block_y in range(0, block_size) :
                    for block_x in range(0, block_size):
                        block_pixels.append(((y + block_y), (x + block_x)))
                        block_value += pix_val[y + block_y][x + block_x]
                if (block_value/(block_size*block_size) > threshold/block_size) :
                    for pixel in block_pixels :
                        pix_val[pixel[0], pixel[1]] = 255
                else:
                    for pixel in block_pixels :
                        pix_val[pixel[0], pixel[1]] = 0
        image = Image.fromarray(pix_val)
        return image



hwnd=win32gui.GetDesktopWindow()
gui = GUI()
gui.draw()
gui.root.mainloop()


#im = Image.open('img_cont_thresh_5.jpg', 'r')
#gui.block_threshold(im, 2, 255).save('test.jpg')
#gui.find_driver(im)
#print(gui.direction(im))
