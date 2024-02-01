import win32api,win32gui,win32con
from keyboardData import VK_CODE
from time import sleep
class Click:
    def __init__(self,windowsname):
        self.windowsname = windowsname
    def gethwid(self):
        hwid = win32gui.FindWindow('LDPlayerMainFrame',self.windowsname)
        childs = win32gui.FindWindowEx(hwid,None,'RenderWindow','TheRender')
        return childs
    
    def getfirefoxid(self):
        hwid = win32gui.FindWindow('MozillaWindowClass',self.windowsname)
        return hwid
    
    def getchromeid(self):
        hwid = win32gui.FindWindow('Chrome_WidgetWin_1',self.windowsname)
        return hwid   
       

    
    def control_click(self,hwid,x,y):
        l_param = win32api.MAKELONG(x,y)
        win32gui.SendMessage(hwid,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,l_param)
        win32gui.SendMessage(hwid,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,l_param)
        # Constants for Windows messages
        
        
    def send_key(self,hwid,key):
        keycode = VK_CODE[key]
        print(VK_CODE[key])
        #OX70 คือ F11 เอามาจาก 
        #http://www.kbdedit.com/manual/low_level_vk_list.html
        win32api.SendMessage(hwid, win32con.WM_KEYDOWN,keycode, 0)
        win32api.SendMessage(hwid, win32con.WM_KEYUP,keycode, 0)
        win32api.SendMessage(hwid, win32con.WM_CHAR, keycode, 0)
           
    def send_backspace(self,hwid,key):
        keycode = VK_CODE[key]
        win32api.SendMessage(hwid, win32con.WM_CHAR, keycode, 0)
        
    def send_ctrl_v(self,hwid):
        ctrl_key = 0x11  # Ctrl key virtual key code
        v_key = 0x56  # V key virtual key code
        # Press Ctrl key
        win32api.SendMessage(hwid, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
        sleep(.1)
        win32api.SendMessage(hwid, win32con.WM_KEYDOWN, v_key, 0)
        sleep(.1)
        # Release V key
        win32api.SendMessage(hwid, win32con.WM_KEYUP, v_key, 0)
        sleep(.1)
        # Release Ctrl key
        win32api.SendMessage(hwid, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)
        sleep(.1)

     
    def send_input(self,hwid, msg):
        for c in msg:
            if c == "\n":
                win32api.SendMessage(hwid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(hwid, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32api.SendMessage(hwid, win32con.WM_CHAR, ord(c), 0)   
            
            
       # Function to simulate drag and drop
    def drag_and_drop(self,hwid, start_pos, end_pos):
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        WM_MOUSEMOVE = 0x0200
        # Convert coordinates to Windows format
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        start_point = win32api.MAKELONG(start_x, start_y)
        end_point = win32api.MAKELONG(end_x, end_y)
        # Simulate left button down event
        win32api.PostMessage(hwid, WM_LBUTTONDOWN, win32con.MK_LBUTTON, start_point)
        # Simulate mouse movement while dragging
        win32api.PostMessage(hwid, WM_MOUSEMOVE, 0, end_point)
        # Simulate left button up event
        win32api.PostMessage(hwid, WM_LBUTTONUP, 0, end_point)

    # Function to simulate click-and-hold
    def click_and_hold(self,hwid, position, hold_duration=0.1):
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        # Convert coordinates to Windows format
        x, y = position
        point = win32api.MAKELONG(x, y)
        # Simulate left button down event
        win32api.PostMessage(hwid, WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)
        # Hold the click for the specified duration
        #sleep(hold_duration)
        # Simulate left button up event
        #win32api.PostMessage(hwnd, WM_LBUTTONUP, 0, point)    
    # Function to simulate click-and-hold with mouse movement
    def click_hold_and_move(self,hwnd, start_position, end_position, hold_duration):
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        WM_MOUSEMOVE = 0x0200
        # Convert coordinates to Windows format
        start_x, start_y = start_position
        end_x, end_y = end_position
        start_point = win32api.MAKELONG(start_x, start_y)
        end_point = win32api.MAKELONG(end_x, end_y)
        # Simulate left button down event
        win32api.PostMessage(hwnd, WM_LBUTTONDOWN, win32con.MK_LBUTTON, start_point)
        # Calculate the distance to move
        dx = end_x - start_x
        dy = end_y - start_y
        # Calculate the number of steps for mouse movement
        num_steps = max(abs(dx), abs(dy))
        # Calculate the delay between each step
        delay = hold_duration / num_steps
        # Perform mouse movement
        for step in range(1, num_steps + 1):
            # Calculate the intermediate position
            x = start_x + int(dx * step / num_steps)
            y = start_y + int(dy * step / num_steps)
            point = win32api.MAKELONG(x, y)
            # Simulate mouse movement
            win32api.PostMessage(hwnd, WM_MOUSEMOVE, 0, point)
            # Delay between each step
            sleep(delay)
        # Simulate left button up event
        win32api.PostMessage(hwnd, WM_LBUTTONUP, 0, end_point)        