import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk

#fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False

detector = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

total = 0
cwd = os.getcwd()
userName = sys.argv[1]
output = cwd + "\\dataset\\" + userName
print(output)

try:
    os.makedirs(output, exist_ok = True)
    print("[INFO] directory created successfully")
except OSError as error:
    print("[INFO] directory already exist")



def prompt_ok(event = 0):
	global cancel, button_capture, button1, button2, button_quit
	cancel = True

	button_capture.place_forget()
	button_quit.place_forget()
	button1 = tk.Button(mainWindow, text="Good Image!", command=save)
	button2 = tk.Button(mainWindow, text="Try Again", command=resume)
	button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
	button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
	button1.focus()

def save(event = 0):
	global prevImg, origImg, total

	p = output + "/" + str(total).zfill(5) + ".png"
	cv2.imwrite(p, origImg)
	total += 1
	resume()


def resume(event = 0):
	global button1, button2, button_capture, lmain, cancel

	cancel = False

	button1.place_forget()
	button2.place_forget()

	mainWindow.bind('<Return>', prompt_ok)
	button_capture.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
	button_quit.place(bordermode=tk.INSIDE, relx=0.9, rely=0.9, anchor=tk.E, width=100, height=25)
	lmain.after(10, show_frame)


#try:
#	f = open(fileName, 'r')
#	camIndex = int(f.readline())
#except:

camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()
if not success:
	if camIndex == 0:
		# print("Error, No webcam found!")
		sys.exit(1)
	else:
		success, frame = cap.read()
		if not success:
			# print("Error, No webcam found!")
			sys.exit(1)


mainWindow = tk.Tk(screenName=None)
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button_capture = tk.Button(mainWindow, text="Capture", command=prompt_ok)
button_quit = tk.Button(mainWindow, text="Quit", command=lambda : mainWindow.quit())

lmain.pack()
button_capture.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
button_capture.focus()
button_quit.place(bordermode=tk.INSIDE, relx=0.9, rely=0.9, anchor=tk.E, width=100, height=25)


def show_frame():
	global cancel, prevImg, button_capture, origImg

	_, frame = cap.read()
	origImg = frame.copy()
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(
		cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
	
	# loop over the face detections and draw them on the frame
	for (x, y, w, h) in rects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	prevImg = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))
	imgtk = ImageTk.PhotoImage(image=prevImg)
	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)
	if not cancel:
		lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()