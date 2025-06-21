import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import cv2
from pygrabber.dshow_graph import FilterGraph
import pythoncom
import webbrowser
from SAUIGeo import SAU

sauvernr = 1.03
version = "V1.04.1 Beta"
sauver = "SAU" + str(sauvernr) + " Beta Release"
release_date = "21/06/2025"

SAU.check()
SAU.verify(sauvernr)
var = SAU.start()
print(var)
default = var[0]
button = var[1]
combo = var[2]
cred = var[3]
scale = var[4]
title = var[5]
window_ui = var[6]
            
def get_input_devices():
    graph = FilterGraph()
    return graph.get_input_devices()


stop_event = threading.Event()

def camera_capture(selected_device_name, pixel_var, fps_var):
    pythoncom.CoInitialize()
    try:
        devices = get_input_devices()
        device_map = {name: index for index, name in enumerate(devices)}
        device_index = device_map.get(selected_device_name.get(), 0)
        cap = cv2.VideoCapture(device_index)

        if not cap.isOpened():
            print(f"Failed to open camera: {selected_device_name.get()}")
            l4.config((f"Failed to open camera: {selected_device_name.get()}"))
            return

        out = None
        frame_width = 1920
        frame_height = 1080
        last_fps = 0

        while not stop_event.is_set():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame")
                break

            current_pixel = pixel_var.get()
            pixel_size = max(1, current_pixel)
            small_dim = max(1, pixel_size)
            small_frame = cv2.resize(frame, (small_dim, small_dim), interpolation=cv2.INTER_LINEAR)
            pixelated_frame = cv2.resize(small_frame, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
            if (frame.shape[1] != frame_width) or (frame.shape[0] != frame_height) or (fps_var.get() != last_fps):
                frame_width, frame_height = frame.shape[1], frame.shape[0]
                if out:
                    out.release()

            if out:
                out.write(pixelated_frame)


            cv2.imshow(f'Camera {selected_device_name.get()}', pixelated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_event.set()
                break

            elapsed = time.time() - start_time
            if fps_var.get() == 0:
                fps = 1
            else:
                fps = fps_var.get()
            sleep_time = max(0, (1.0 / fps) - elapsed)
            time.sleep(sleep_time)

        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()

    finally:
        pythoncom.CoUninitialize()

def start_capture(selected_device_name, pixel_var, fps_var):
    stop_event.clear()
    t = threading.Thread(target=camera_capture, args=(selected_device_name, pixel_var, fps_var), daemon=True)
    t.start()

def stop_capture():
    stop_event.set()

def openlink(link):
    link_list = ["https://github.com/Geomedge/Camera-Quality-Reducer", "https://forms.office.com/r/x7Le5d2bbE", "https://discord.gg/QN5HrTAYYs"]
    webbrowser.open(link_list[link])

def version_info():
    ver_win = tk.Tk()
    ver_win.minsize(250, 130)
    ver_win.title("Version")
    ver_win.config(background="#333")

    l1 = tk.Label(ver_win, text="Version Information", **title)
    l1.pack(side="top", anchor="nw")

    l2 = tk.Label(ver_win, text=f"{version}", **cred)
    l2.pack(side="top")

    l3 = tk.Label(ver_win, text=f"{sauver}", **cred)
    l3.pack(side="top")

    l4 = tk.Label(ver_win, text=f"Release Date : {release_date}", **cred)
    l4.pack(side="top")

    l5 = tk.Label(ver_win, text="This is an Beta Build!", **cred)
    l5.pack(side="top")

def run_gui():
    root = tk.Tk()
    root.minsize(500, 450)
    root.title("Camera Quality Reducer")
    root.config(background="#333")

    #MENU BAR
    menubar = tk.Menu(root, **window_ui)

    #File Settings
    filemenu = tk.Menu(menubar, tearoff=0, **cred)
    filemenu.add_command(label="Exit", command=root.quit)

    #Settings
    settingsmenu = tk.Menu(menubar, tearoff=0, **cred)

#Theme Menu
    thememenu = tk.Menu(settingsmenu, tearoff=0, **cred)
    thememenu.add_command(label="Light", command=lambda:[SAU.set(0)])
    thememenu.add_command(label="Dark", command=lambda:[SAU.set(1)])
    thememenu.add_command(label="Mellow", command=lambda:[SAU.set(2)])
    thememenu.add_command(label="Hacker", command=lambda:[SAU.set(3)])

    #Theme Settings
    settingsmenu.add_cascade(label="Choose Theme (Experimental)", menu=thememenu)

    #Help Menu
    helpmenu = tk.Menu(menubar, tearoff=0, **cred)
    helpmenu.add_command(label="Open Discord Support Page", command=lambda:[openlink(2)])
    helpmenu.add_command(label="Open Github Page", command=lambda:[openlink(0)])
    helpmenu.add_separator()
    helpmenu.add_command(label="Report Bugs", command=lambda:[openlink(1)])
    helpmenu.add_separator()
    helpmenu.add_command(label="Version", command=lambda:[version_info()])
    
    #Menubar Itself
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Settings", menu=settingsmenu)
    menubar.add_cascade(label="Help", menu=helpmenu)
    

    root.config(menu=menubar)

    #VARIABLES
    pixel = tk.IntVar(master=root, value=1080)
    fps = tk.IntVar(master=root, value=60)
    selected_device = tk.StringVar(master=root)

    # Title
    t1 = tk.Label(root, text="Camera Quality Reducer", **title)
    t1.pack(anchor="nw")

    # Camera selection
    f1 = tk.Frame(root, bg="#111")
    l1 = tk.Label(f1, text="Select Camera", **default)
    l1.grid(row=0, column=0, padx=5, pady=2)

    devices = get_input_devices()
    device_names = devices if devices else ["No Devices Found"]
    if device_names:
        selected_device.set(device_names[0])
    dropdown = ttk.Combobox(f1, values=device_names, textvariable=selected_device, **combo)
    dropdown.grid(row=1, column=0, padx=5, pady=2)
    if device_names:
        dropdown.current(0)
    f1.pack(side='top', anchor='center', pady=5)

    # Pixel Count Slider
    f2 = tk.Frame(root, bg="#111")
    l2 = tk.Label(f2, text="Pixel Count", **default)
    l2.grid(row=0, column=0, padx=5, pady=2)
    s2 = tk.Scale(f2, variable=pixel, from_=0, to=1080, tickinterval=720, **scale)
    s2.grid(row=1, column=0, padx=5, pady=2)
    f2.pack(side='top', anchor='center', pady=5)

    # FPS Slider
    f3 = tk.Frame(root, bg="#111")
    l3 = tk.Label(f3, text="Frames Per Second", **default)
    l3.grid(row=0, column=0, padx=5, pady=2)
    s3 = tk.Scale(f3, variable=fps, from_=0, to=60, tickinterval=10, **scale)
    s3.grid(row=1, column=0, padx=5, pady=2)
    f3.pack(side='top', anchor='center', pady=5)

    #Buttons
    btn_frame = tk.Frame(root, bg="#333")

    start_btn = tk.Button(btn_frame, text="Start Capture", command=lambda: start_capture(selected_device, pixel, fps), **button)
    start_btn.pack(side='left', padx=10, pady=10)

    stop_btn = tk.Button(btn_frame, text="Stop Capture", command=stop_capture, **button)
    stop_btn.pack(side='left', padx=10, pady=10)

    btn_frame.pack()

    global l4
    l4 = tk.Label(root, text="", **cred)
    l4.pack()


    # Credits
    ver = tk.Label(root, text=version, **cred)
    ver.pack(side='left', anchor='sw', padx=5, pady=5)
    
    credit = tk.Label(root, text="Made By Geomedge", **cred)
    credit.pack(side='right', anchor='se', padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    run_gui()