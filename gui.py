import tkinter as tk
from tkinter import *
import pyvjoy
from PIL import ImageTk, Image, ImageEnhance, ImageDraw, ImageGrab
import pywinauto
import win32gui, win32ui, win32con, win32api
import numpy
import threading
import time
import math

class GUI:
    def __init__(self):
        # Scale GUI by constant factor, used for different DPI screens
        self.scale = 2;

        #Initialize Gui Components and size
        self.root = Tk()
        self.root.resizable(0,0)
        self.canvas = Canvas(self.root, width = (400*self.scale), height = (300*self.scale), bd = 1, highlightthickness = 0)
        self.canvas.pack()

        #Initialize Button toggle variables
        self.ai_run = False
        self.image_out = False
        self.image_out_time = 0
        self.image_out_count = 0
        self.driver_pos = (205*self.scale, 155*self.scale)
        self.driver_conf = 0

        #Initialize Buttons
        self.button_image_out = Button(self.root, text="ImageOut = No", command=self.action_image_out)
        self.button_image_out.place(x=200*self.scale, y=230*self.scale)

        self.button_ai_run = Button(self.root, text="Go", command=self.action_ai_run)
        self.button_ai_run.place(x=200*self.scale, y=260*self.scale)

        button_right = Button(self.root, text=">")
        button_right.bind("<ButtonPress>", self.action_right_press)
        button_right.bind("<ButtonRelease>", self.action_right_release)
        button_right.place(x=60*self.scale, y=250*self.scale)

        button_up = Button(self.root, text="^")
        button_up.bind("<ButtonPress>", self.action_up_press)
        button_up.bind("<ButtonRelease>", self.action_up_release)
        button_up.place(x=30*self.scale, y=230*self.scale)

        button_left = Button(self.root, text="<")
        button_left.bind("<ButtonPress>", self.action_left_press)
        button_left.bind("<ButtonRelease>", self.action_left_release)
        button_left.place(x=0*self.scale, y=250*self.scale)

        button_down = Button(self.root, text="v")
        button_down.bind("<ButtonPress>", self.action_down_press)
        button_down.bind("<ButtonRelease>", self.action_down_release)
        button_down.place(x=30*self.scale, y=270*self.scale)

        button_a = Button(self.root, text="a")
        button_a.bind("<ButtonPress>", self.action_a_press)
        button_a.bind("<ButtonRelease>", self.action_a_release)
        button_a.place(x=90*self.scale, y=260*self.scale)

        button_b = Button(self.root, text="b")
        button_b.bind("<ButtonPress>", self.action_b_press)
        button_b.bind("<ButtonRelease>", self.action_b_release)
        button_b.place(x=120*self.scale, y=260*self.scale)

        button_c = Button(self.root, text="c")
        button_c.bind("<ButtonPress>", self.action_c_press)
        button_c.bind("<ButtonRelease>", self.action_c_release)
        button_c.place(x=150*self.scale, y=260*self.scale)

        button_start = Button(self.root, text="start")
        button_start.bind("<ButtonPress>", self.action_start_press)
        button_start.bind("<ButtonRelease>", self.action_start_release)
        button_start.place(x=100 * self.scale, y=230 * self.scale)
        self.gamepad = pyvjoy.VJoyDevice(1)

        # Find game from list of valid window titles
        # If no game found then gui will use a screengrab of the display
        self.games_list = ['RetroArch Genesis Plus GX v1.7.4 f5eed51', 'RetroArch Genesis Plus GX v1.7.4 53e043d']
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

    def action_start_press(self, event):
        self.gamepad.set_button(4, 1)
    def action_start_release(self, event):
        self.gamepad.set_button(4, 0)


    # Toggle image out button text and control variable
    def action_image_out(self):
        if self.image_out :
            self.button_image_out.configure(text="ImageOut = No")
            self.image_out = False
        else :
            self.button_image_out.configure(text="ImageOut = Yes")
            self.image_out = True

    # Toggle Go button text and control variable
    def action_ai_run(self):
        if self.ai_run :
            self.button_ai_run.configure(text="Go")
            self.ai_run = False
            self.gamepad.set_button(2, 0)
        else :
            self.button_ai_run.configure(text="Stop")
            self.ai_run = True
            self.gamepad.set_button(2, 1)

    # take screenshot of game, run filters on image and display it. Repeat
    # If Run variable is set then call self driving methods
    def draw(self):
        # if compatible game running take screenshot of it.
        if (self.hwnd != 0) :
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(self.dcObj, self.w, self.h)
            self.cDC.SelectObject(dataBitMap)
            self.cDC.BitBlt((0,(-43 * self.scale)), (self.w, self.h), self.dcObj, (0,0), win32con.SRCCOPY)
            bmpinfo = dataBitMap.GetInfo()
            bmpstr = dataBitMap.GetBitmapBits(True)
            self.img_main = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)
            self.img_main = self.img_main.crop((7*self.scale, 0, 445*self.scale, 225*self.scale))
            self.img_main = self.img_main.resize((400 * self.scale, 225 * self.scale))
        # no compatbile game running, use screengrab
        else :
            self.img_main = ImageGrab.grab(bbox=(0, 0, 800, 450)).resize((400*self.scale, 225*self.scale))

        # create copy of img_main to display bounding box and output to gui
        #self.img_main.save("Source_Base.jpg")
        self.img_main = ImageEnhance.Contrast(self.img_main).enhance(50.0)
        self.img_main = ImageEnhance.Brightness(self.img_main).enhance(0.9)
        #self.img_main.save("Source_Contrast.jpg")
        self.img_main = self.img_main.convert('1')
        #self.img_main.save("Source_Threshold.jpg")
        #self.img_main = Image.fromarray(self.block_threshold(numpy.array(self.img_main, dtype='uint8'), 2), mode="L")
        #self.img_main.save("Source_Block_Contrast.jpg")
        self.display = self.img_main.copy()
        draw_box = ImageDraw.Draw(self.display)
        draw_box.rectangle(self.get_bounding_box(), fill=None, outline='white', width=(3 * self.scale))
        del draw_box
        self.display = ImageTk.PhotoImage(self.display)
        self.id = self.canvas.create_image(0, 0, anchor=NW, image=self.display)

        # if image_out button is checked, save image in incremental files
        if self.image_out : self.output_image()

        #if Go clicked then run driving ai
        if (self.ai_run):
            go = threading.Thread(target=self.drive())
            go.start()
        # redraw repeat
        self.canvas.after(50, self.draw)

    # Self Driving routine
    # Find the driver inside the bounding box
    # If driver is left of centre, turn right
    # If driver is right of centre, turn left
    def drive(self):
        self.find_driver()
        #road_balance = self.road_left_right_of_driver()
        turn = 0;
        turn_degree = ((0.02
                      + (abs(self.driver_pos[0] - (200 * self.scale)) / (200 * self.scale) / 2))
                      #+ (road_balance / 4)
                      * self.driver_conf)
        if self.driver_pos[0] < 200 * self.scale:
            turn = 2
        else:
            turn = 1
        #print(turn_degree)
        t = threading.Thread(target=self.turn(turn, turn_degree))
        t.start()

    # Start turn in direction given then sleep for length given before stopping turn
    def turn(self, direction, length):
        if(direction == 1) :
            self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x0)
        if(direction == 2):
            self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x8000)
        time.sleep(length)
        self.gamepad.set_axis(pyvjoy.HID_USAGE_X, 0x4000)

    # Search the bounding_box for the character
    def find_driver(self):
        # isolate bounding box
        bounding_box = self.get_bounding_box()
        image = self.img_main.crop(bounding_box)
        #image.save("find_driver.jpg")
        # Search bounding box for all blobs
        driver = self.find_driver_blob(image)
        if driver is not None:
            # adjust driver position and confidence
            self.driver_conf = (self.driver_conf + (self.driver_pos[0] / driver[1][0])) / 2
            self.driver_pos = driver[1]
        else :
            # couldn't find driver, lower confidence
            self.driver_conf = self.driver_conf/1.5
            if self.driver_conf < 0.2 :
                self.driver_pos = (int((self.driver_pos[0] + (205 * self.scale)) / 2), int((self.driver_pos[1] + (155 * self.scale)) / 2))


    # Find contiguous areas of white in image
    def find_driver_blob(self, image):
        x_width, y_height = image.size
        if x_width < 10 or y_height < 10:
            return None
        pix_val = numpy.array(image, dtype='uint8')
        pix_val = self.block_threshold(pix_val, 2)

        bounding_box = self.get_bounding_box()
        searched = set()
        test_range = ((0, 1), (1, 0), (0, -1), (-1, 0))
        driver = None
        driver_conf = 0

        # Scan across image, any accessed pixel is marked as searched
        # When white pixel is found add all surrounding un-searched pixels to blob and search queue
        # search through rest of queue before continuing scan across image
        for pix_y in range(0, y_height) :
            for pix_x in range(0, x_width) :
                pixel = (pix_y, pix_x)
                if pixel not in searched:
                    searched.add(pixel)
                    # if white pixel found then add surrounding pixels to explore queue
                    if pix_val[pixel] :
                        explore_queue = list()
                        explore_queue.append(pixel)
                        blob = set()
                        # track blob pixel boundries
                        p_left = x_width
                        p_right = 0
                        p_top = y_height
                        p_bot = 0
                        blob.add(pixel)
                        # search surrounding pixels for more pixels to add to blob
                        # all explored pixels are counted as searched
                        while explore_queue :
                            pixel = explore_queue.pop()
                            for position in test_range:
                                test_y = int(pixel[0] + position[0])
                                test_x = int(pixel[1] + position[1])
                                if test_y < y_height and test_y >= 0 and test_x < x_width and test_x >= 0:
                                    test_pixel = (test_y, test_x)
                                    if test_pixel not in searched :
                                        searched.add(test_pixel)
                                        if pix_val[test_pixel]:
                                            explore_queue.append(test_pixel)
                                            blob.add(test_pixel)
                                            if (test_y > p_bot) : p_bot = test_y
                                            if (test_y < p_top): p_top = test_y
                                            if (test_x > p_right): p_right = test_x
                                            if (test_x < p_left): p_left = test_x
                        # Large blob found, check how likely it's the character's blob
                        if len(blob) > 500*self.scale :
                            blob_width = p_right - p_left
                            blob_height = p_bot - p_top
                            if blob_width > 10 * self.scale and blob_width < 50 * self.scale:
                                if blob_height > 20 * self.scale and blob_height < 60 * self.scale:
                                    blob_conf = 1 - (( abs(blob_width - (31 * self.scale)) / (31 * self.scale))
                                                    + (abs(blob_height - (39 * self.scale)) / (39 * self.scale))
                                                    + (abs(len(blob) - (1000 * self.scale)) / (1000 * self.scale)))
                                    if blob_conf > driver_conf:
                                        driver_conf = blob_conf
                                        driver = (blob, (int((p_left + p_right) / 2) + bounding_box[0],
                                                         int((p_bot + p_top) / 2) + bounding_box[1]))
        return driver

    # Define the bounding_box around where the character is expected to be
    # Box size is weighted by the confidence of the characters position
    def get_bounding_box(self):
        bounding_box = (max(0, self.driver_pos[0] - ((50 + (180 * (1 - self.driver_conf))) * self.scale))
                        , max(125 *self.scale, self.driver_pos[1] - ((60 + (60 * (1 - self.driver_conf))) * self.scale))
                        , min(400 * self.scale, self.driver_pos[0] + ((50 + (180 * (1 - self.driver_conf))) * self.scale))
                        , min(225 * self.scale, self.driver_pos[1] + ((60 + (60 * (1 - self.driver_conf))) * self.scale)))
        return bounding_box

    # Scan a pixel array with a block of a given size
    # if half of the pixels in the block are black then make all pixels in the block black
    # if more are white then make them all white
    def block_threshold(self, pix_val, block_size:int):
        # Scan image in block sized chunks
        for y in range(-1, len(pix_val) - block_size+1, block_size) :
            for x in range(-1, len(pix_val[0]) - block_size+1, block_size) :
                block_pixels = list()
                block_value = 0
                # scan the pixels in the block and count the number of white
                for block_y in range(0, block_size) :
                    for block_x in range(0, block_size):
                        block_pixels.append(((y + block_y), (x + block_x)))
                        if pix_val[y + block_y][x + block_x] :
                            block_value += 1
                # Apply Threshold to block
                if block_value <= int((block_size*block_size)/2) :
                    for pixel in block_pixels :
                        pix_val[pixel] = 0
                else :
                    for pixel in block_pixels :
                        pix_val[pixel] = numpy.uint8(255)
        return pix_val

    # Find the largest division of black space left or right of the driver position
    # Not currently used
    def road_left_right_of_driver(self):
        x_width, y_height = self.img_main.size
        image = self.img_main.crop((0, y_height/1.8, x_width, y_height))
        x_width, y_height = image.size
        #image.save("crop.jpg")
        pix_val = numpy.array(image)
        road_left = 0
        road_right = 0
        for pix_y in range(0, y_height):
            for pix_x in range(0, x_width):
                pixel = (pix_y, pix_x)
                #print(str(pixel) + "," + str(self.driver_pos[0]) + "," + str(pix_val[pixel]))
                #print(pix_val[pixel])
                if pix_val[pixel] == False:
                    if pix_x < self.driver_pos[0]:
                        road_left += 1
                else:
                        road_right += 1


        if (road_left > road_right):
            return 1 - (road_right/road_left)
        else :
            return 1 - (road_left/road_right)

    # save an image every 3rd time this is called
    def output_image(self):
        if (self.image_out_time == 3):
            out = self.img_main
            out.save("img_cont_thresh_" + str(self.image_out_count) + ".jpg")
            self.image_out_time = 0
            self.image_out_count += 1
        else:
            self.image_out_time += 1



hwnd=win32gui.GetDesktopWindow()
gui = GUI()
gui.draw()
gui.root.mainloop()