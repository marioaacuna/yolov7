import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, window, window_title, video_source):
        self.window = window
        self.window.title(window_title)
        self.vid = cv2.VideoCapture(video_source)
        self.length = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Create a slider for frame navigation
        self.slider = tk.Scale(window, from_=0, to=self.length-1, orient='horizontal', command=self.slider_changed)
        self.slider.pack(fill='x', expand=True)

        # Create an entry for frame input
        self.frame_entry = tk.Entry(window)
        self.frame_entry.pack()

        # Create a button to jump to the frame
        self.jump_btn = tk.Button(window, text="Jump to Frame", command=self.jump_to_frame)
        self.jump_btn.pack()

        self.update_canvas(0)

    def update_canvas(self, frame=0):
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def slider_changed(self, value):
        self.update_canvas(int(value))

    def jump_to_frame(self):
        frame_num = self.frame_entry.get()
        if frame_num.isdigit():
            frame_num = int(frame_num)
            if 0 <= frame_num < self.length:
                self.slider.set(frame_num)
                self.update_canvas(frame_num)
            else:
                messagebox.showerror('Error', 'Frame number out of range.')
        else:
            messagebox.showerror('Error', 'Please enter a valid frame number.')

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def select_video():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    video_path = filedialog.askopenfilename()  # Ask the user to select a video file
    root.destroy()  # Destroy the root window
    return video_path

def main():
    video_path = select_video()
    if video_path:
        root = tk.Tk()
        VideoPlayer(root, "Tkinter Video Player", video_path)
        root.mainloop()
    else:
        print("No video selected.")

if __name__ == '__main__':
    main()
