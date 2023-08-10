from tkinter import *
import tkinter.messagebox as tkMessageBox
import pickle
import os
import subprocess
from imutils import paths
import cv2
import face_recognition

## main frame
root = Tk()
root.title("Facial Recognition System")
 
width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)


#=======================================VARIABLES=====================================
ADD_USERNAME = StringVar()
DEL_USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
current_frame = Frame()
data = {}
pending = []

#=======================================METHODS=======================================
def MainMenu():
	global current_frame, lbl_result1
	current_frame = Frame(root)
	btn_show_users = Button(current_frame, text="Show Users", font=('arial', 18), width=35, command=ToggleToShowUsers)
	btn_show_users.grid(row=1, pady=20)
	btn_del_users = Button(current_frame, text="Delete User", font=('arial', 18), width=35, command=ToggleToDelUser)
	btn_del_users.grid(row=2, pady=20)
	btn_add_users = Button(current_frame, text="Add User", font=('arial', 18), width=35, command=ToggleToAddUser)
	btn_add_users.grid(row=3, pady=20)
	btn_train = Button(current_frame, text="Train", font=('arial', 18), width=35, command=ToggleToTrainModel)
	btn_train.grid(row=4, pady=20)
	btn_quit = Button(current_frame, text="Quit", font=('arial', 14), width=35, command=lambda : root.quit())
	btn_quit.grid(row=5, pady=20)
	current_frame.pack(side=TOP, pady=30)

def ShowUsers():
	global current_frame, lbl_result1, data
	current_frame = Frame(root)

	loaddata()
	lbl_result1 = Label(current_frame, text="Users", font=('arial', 18))
	lbl_result1.grid(row=1)
	
	listNodes = Listbox(current_frame, width=40, height=15, font=("Helvetica", 12))
	listNodes.grid(row=2)

	scrollbar = Scrollbar(current_frame, orient="vertical")
	scrollbar.config(command=listNodes.yview)
	scrollbar.grid(row=2, column=1, sticky=NS)

	listNodes.config(yscrollcommand=scrollbar.set)

	names = list(set(data["names"]))
	names.sort()
	for name in names:
		listNodes.insert(END, name)
	
	lbl_back = Label(current_frame, text="Back", fg="Blue", font=('arial', 12))
	lbl_back.grid(row=0, sticky=W)
	lbl_back.bind('<Button-1>', ToggleToMainMenu)
	current_frame.pack(side=TOP, pady=40)

def AddUser():
	global current_frame, lbl_result1
	current_frame = Frame(root)
	lbl_result1 = Label(current_frame, text="", font=('arial', 18))
	lbl_result1.grid(row=1, columnspan=2)
	lbl_username = Label(current_frame, text="Username:", font=('arial', 20), bd=18)
	lbl_username.grid(row=2)
	lbl_result1 = Label(current_frame, text="", font=('arial', 18))
	lbl_result1.grid(row=3, columnspan=2)
	username = Entry(current_frame, font=('arial', 20), textvariable=ADD_USERNAME, width=15)
	username.grid(row=2, column=1)
	btn_login = Button(current_frame, text="Add", font=('arial', 18), width=35, command=UtilAddUser)
	btn_login.grid(row=4, columnspan=2, pady=20)
	lbl_back = Label(current_frame, text="Back", fg="Blue", font=('arial', 12))
	lbl_back.grid(row=0, sticky=W)
	lbl_back.bind('<Button-1>', ToggleToMainMenu)
	current_frame.pack(side=TOP, pady=80)

def DelUser():
	global current_frame, lbl_result1
	current_frame = Frame(root)
	lbl_result1 = Label(current_frame, text="", font=('arial', 18))
	lbl_result1.grid(row=1, columnspan=2)
	lbl_username = Label(current_frame, text="Username:", font=('arial', 20), bd=18)
	lbl_username.grid(row=2)
	lbl_result1 = Label(current_frame, text="", font=('arial', 18))
	lbl_result1.grid(row=3, columnspan=2)
	username = Entry(current_frame, font=('arial', 20), textvariable=DEL_USERNAME, width=15)
	username.grid(row=2, column=1)
	btn_login = Button(current_frame, text="Delete", font=('arial', 18), width=35, command=UtilDelUser)
	btn_login.grid(row=4, columnspan=2, pady=20)
	lbl_back = Label(current_frame, text="Back", fg="Blue", font=('arial', 12))
	lbl_back.grid(row=0, sticky=W)
	lbl_back.bind('<Button-1>', ToggleToMainMenu)
	current_frame.pack(side=TOP, pady=80)

def TrainModel():
	global current_frame, lbl_result1, pending
	current_frame = Frame(root)

	loadpending()
	lbl_result1 = Label(current_frame, text="Training Left For", font=('arial', 18))
	lbl_result1.grid(row=1)
	
	listNodes = Listbox(current_frame, width=40, height=12, font=("Helvetica", 12))
	listNodes.grid(row=2)

	scrollbar = Scrollbar(current_frame, orient="vertical")
	scrollbar.config(command=listNodes.yview)
	scrollbar.grid(row=2, column=1, sticky=NS)

	listNodes.config(yscrollcommand=scrollbar.set)

	if len(pending) != 0:
		for name in pending:
			listNodes.insert(END, name)

	btn_train = Button(current_frame, text="Start Training", width=25, font=('arial', 18), command=UtilTrainModel)
	btn_train.grid(row=3, pady=35)

	lbl_back = Label(current_frame, text="Back", fg="Blue", font=('arial', 12))
	lbl_back.grid(row=0, sticky=W)
	lbl_back.bind('<Button-1>', ToggleToMainMenu)
	current_frame.pack(side=TOP, pady=50)

def DestroyFrame(event=None):
	global current_frame
	current_frame.destroy()

def ToggleToMainMenu(event=None):
	DestroyFrame()
	MainMenu()

def ToggleToShowUsers(event=None):
	DestroyFrame()
	ShowUsers()

def ToggleToAddUser(event=None):
	DestroyFrame()
	AddUser()

def ToggleToDelUser(event=None):
	DestroyFrame()
	DelUser()

def ToggleToTrainModel(event=None):
	DestroyFrame()
	TrainModel()

MainMenu()

#========================================UTIL FUNCTIONS===================================
def UtilDelUser():
	if len(DEL_USERNAME.get()) == 0:
		tkMessageBox.showerror("Error", "Username field cannot be empty")
	loaddata()
	if data["names"].count(DEL_USERNAME.get()) == 0:
		tkMessageBox.showerror("Error", "User doesn't exist")
	else:
		while data["names"].count(DEL_USERNAME.get()) > 0:
			idx =  data["names"].index(DEL_USERNAME.get())
			data["encodings"].pop(idx)
			data["names"].pop(idx)
		savedata()
		tkMessageBox.showinfo("Success", DEL_USERNAME.get()+" deleted successfully")

	print("UtilDelUser:", DEL_USERNAME.get())

def UtilAddUser():
	global ADD_USERNAME, pending, data
	if len(ADD_USERNAME.get()) == 0:
		tkMessageBox.showerror("Error", "Username field cannot be empty")
	loaddata()
	if data["names"].count(ADD_USERNAME.get()) > 0:
		tkMessageBox.showerror("Error", "User already exist")
		DestroyFrame()
		ADD_USERNAME.set("")
		AddUser()
	else:
		# os.system('python capture.py ' + ADD_USERNAME.get(), )
		subprocess.call("python capture.py " + ADD_USERNAME.get(), shell=True)
		tkMessageBox.showinfo("Success", ADD_USERNAME.get()+" added successfully\nNow training of the model is left")
		pending.append(ADD_USERNAME.get())
		savepending()
		DestroyFrame()
		AddUser()
	print("UtilAddUser:",  ADD_USERNAME.get())

def UtilTrainModel():
	global pending, data
	if len(pending) == 0:
		tkMessageBox.showerror("Error", "No user left for training")
	else:
		loaddata()
		imagePaths = list(paths.list_images("dataset"))
		print(pending)
		for (i, imagePath) in enumerate(imagePaths):
			name = imagePath.split(os.path.sep)[-2]
			print(name)
			if(pending.count(name) == 0): 
				continue
			print("[INFO] processing ", name, "'s image ", " {}/{}".format(i + 1, len(imagePaths)))
			
			image = cv2.imread(imagePath)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			boxes = face_recognition.face_locations(rgb, model="hog")
			
			encodings = face_recognition.face_encodings(rgb, boxes)
			
			for encoding in encodings:
				data["encodings"].append(encoding.tolist())
				data["names"].append(name)

		pending.clear()
		savepending()
		savedata()
		tkMessageBox.showinfo("Success", "Model trained successfully")
		DestroyFrame()
		TrainModel()	

def loaddata():
	global data
	if os.path.exists("encodings.pickle"):
		data = pickle.loads(open("encodings.pickle", "rb").read())
	else:
		data = {"encodings": [], "names": []}

def savedata():
	global data
	f = open("encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	#print(data)
	f.close()

def loadpending():
	global pending
	if os.path.exists("pending.pickle"):
		pending = pickle.loads(open("pending.pickle", "rb").read())
	else:
		pending = []

def savepending():
	global pending
	f = open("pending.pickle", "wb")
	f.write(pickle.dumps(pending))
	#print(pending)
	f.close()

#========================================INITIALIZATION===================================
if __name__ == '__main__':
	root.mainloop()
