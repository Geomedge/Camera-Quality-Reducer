import tkinter as tk
from tkinter import ttk
import threading
import time
import cv2
from pygrabber.dshow_graph import FilterGraph
import pythoncom

version = "V1.03.1"

try:
    title_font = ("Aptos", 18, "bold")
    default_font = ("Aptos", 12)
    credit_font = ("Aptos", 10)
except:
    title_font = ("Segoe UI", 18, "bold")
    default_font = ("Segoe UI", 11)
    credit_font = ("Segoe UI", 9)

def get_input_devices():
    graph = FilterGraph()
    return graph.get_input_devices()


default = {
    'font':default_font,
    'background':"#111",
    'foreground':"#FFF",
        }

button = {
    'font':default_font,
    'background':"#333",
    'foreground':"#FFF",
        }


combo = {
    'font':default_font,
    'background':"#111",
    'foreground':"#111",
    'width':40,
}

cred = {
    'font':credit_font,
    'bg':"#333",
    'fg':"#FFF",
}

scale = {
    'font':default_font,
    'bg':"#222",
    'fg':"#FFF",
    'highlightbackground':"#333",
    'troughcolor':"#333",
    'orient':"horizontal",
    'length':350,
    'width':15,
}

title = {
    'font':title_font,
    'bg':"#333",
    'fg':"#FFF",
}

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

def run_gui():
    root = tk.Tk()
    root.minsize(500, 450)
    root.title("Camera Quality Reducer")
    root.config(background="#333")

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