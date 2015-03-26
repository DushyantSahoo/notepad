import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import time
import threading
import smtplib
import os
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from email.Utils import formatdate
import time
import datetime
import sys
import csv
from ctypes import cdll

#initialise a window
root = Tk()
time_reminder = ""
msg_reminder = ""

#class that checks password
class Check:
	def __init__(self,root):
		#set the label and text field to enter the password
		self.lab = Label(root, text = 'Password')
		#self.ent = self.make_entry(root, "Password:", 16, show="*")		
		self.ent = Entry(root, bg = 'white',show="*")
		self.button = Button(root, text = 'Enter Password', command = self.GetPass)
		self.lab.pack()
		self.ent.pack()		
		self.button.pack()

	def GetPass(self):
		#check the input value using .get()
		password = self.ent.get()
		if password == 'a':
			#if true then iterate to display textpad
			m = mainmenu(root)
			mainmenu.mainloop()	
		else:
			tkMessageBox.showinfo("Entered a wrong password")
			root.destroy()

#class that display the notepad with menu: File, Edit, Options
class mainmenu:
	def __init__(self,root):
		root.destroy()
		#inistialise the parameter with window Name
		self.root1=Tkinter.Tk(className = "Add a TODO Note")
		#initialise the size of the window	
		self.textPad = ScrolledText(self.root1, width=100, height=80)
		menu = Menu(self.root1)
		self.root1.config(menu=menu)
		#file menu include new, open, save, saveas, select all, exit features
		filemenu = Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.new)
		#self.root1.bind('<Control-n>', self.new)
        	#self.root1.bind('<Control-N>', self.new)
 
		filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_command)
		filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_command)
		filemenu.add_command(label="Save as", accelerator="Ctrl+B", command=self.save_as)
		filemenu.add_command(label="Select All", accelerator="Ctrl+A", command=self.selectall_command)
		filemenu.add_separator()
		filemenu.add_command(label="Exit",accelerator="Ctrl+Q", command=self.exit_command)
		
		#Edit menu including Cut, Copy and Paste features
		editmenu = Menu(menu)
		editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
		editmenu.add_command(label="Copy", accelerator="Ctrl+C",command=self.copy)
		editmenu.add_command(label="Paste",accelerator="Ctrl+V", command=self.paste)
		editmenu.add_command(label="Delete", accelerator="Ctrl+D", command=self.delete_command)
		menu.add_cascade(label="Edit", menu=editmenu)
		
		#Option menu including Reminder and mailing features
		option = Menu(menu)
		Sourcemenu = Menu(menu)
		menu.add_cascade(label="Option", menu=option)
		
		option.add_command(label="Add Reminder", accelerator="Ctrl+R", command=self.reminder)
		option.add_command(label="Mailing Files", accelerator="Ctrl+M", command=self.send)
		option.add_cascade(label="Add Priority", menu = Sourcemenu)
		self._listi = ["High Priority","Medium Priority","Low Priority"]
		for l in self._listi:
		    Sourcemenu.add_command(label=l, command=lambda arg0=l: self.test(arg0))
		option.add_command(label="Display Notes", command=self.display)
		
		
		#Help menu including about us feature
		helpmenu = Menu(menu)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About", accelerator="Ctrl+H", command=self.about_command)
		#end of menu
		
		
        	#self.textPad.bind('<Control-m>', self.send)
        	#self.root1.bind('<Control-M>', self.send)
        	#self.root1.bind('<Control-d>', self.delete_command)
        	#self.root1.bind('<Control-D>', self.delete_command)
        	#self.root1.bind('<Control-q>', self.exit_command)
        	#self.root1.bind('<Control-Q>', self.exit_command)
        	#self.root1.bind('<Control-a>', self.selectall_command)
        	#self.root1.bind('<Control-A>', self.selectall_command)
        	#self.root1.bind('<Control-b>', self.save_as)
        	#self.root1.bind('<Control-B>', self.save_as)
		self.textPad.pack()
		self.root1.pack()
		self.root1.mainloop()
	
	def test(self, arg0): 
		fieldnames = ['time1','filename', 'priority']
		with open('priority.csv', 'ab+') as f_h:
			reader = csv.DictReader(f_h,delimiter=',')
			print len(list(reader))	
			print reader.fieldnames
			if not reader.fieldnames:
				print "empty"
				f_h.close()
				with open('priority.csv', 'ab+') as f_w:
					writer = csv.DictWriter(f_w, fieldnames=fieldnames, delimiter=',')
					writer.writeheader()
					f_w.close()
			else:
				print "present"	
				f_h.close()
				with open('priority.csv', 'ab+') as f_w:
					#fieldnames = ['time1','filename', 'priority']
					writer = csv.DictWriter(f_w, fieldnames=fieldnames, delimiter=',')
					date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
					print date
					if arg0 == 'High Priority':
						writer.writerow({'time1':date, 'filename':file.name, 'priority':arg0})
						tkMessageBox.showinfo("You added this note for", arg0)
					elif arg0 == 'Medium Priority':
			 			writer.writerow({'time1': date, 'filename': file.name , 'priority': arg0})
						tkMessageBox.showinfo("You added this note for", arg0)
					elif arg0 == 'Low Priority':
						writer.writerow({'time1': date,'filename': ile.name ,'priority': arg0})
						tkMessageBox.showinfo("You added this note for", arg0)
					else :
						print "wrong entry"
					f_w.close()				
		
	
	
	def display(self):
		#enter the label and entry to  take the date and check for the date in csv file 
		#date = datetime.strptime(row['Dispatch date'], '%Y-%m-%d %H:%M:%S')
		self.r = Tkinter.Tk(className = "Display Notes")
		self.lab_dis= Label(self.r, text = 'Enter the date in form of YYYY-MM-DD')		
		self.ent_dis = Entry(self.r, bg = 'white')
		self.button = Button(self.r, text = 'Display', command = self.GetData(ent))
		self.lab_dis.pack()
		self.ent_dis.pack()		
		self.button.pack()
		self.r.pack()
		self.r.mainloop()
	
	def GetData(self):
		fieldnames = ['time1','filename', 'priority']
		with open('priority.csv','r+') as csvfile:
		     	print "aa"
		     	reader = csv.DictReader(csvfile,fieldnames = fieldnames,delimiter=',')
			for row in reader:
				print "rr"
				print row['time1'].format()
		     		d = datetime.datetime.strptime(row['time1'], '%Y-%m-%d %H:%M:%S')
				date = d.date()
				print self.ent_dis
				while (self.ent_dis==[datetime.datetime.strftime(date,'%Y-%m-%d')]):
					print "ee"
					for date in row.items():
						tkMessageBox.showinfo(date, row['filename'],row['priority'])
					
		#tkMessageBox.showinfo("You added this note for", arg0)
		
		
	#function to select all the text on the textpad
	def selectall_command(self):
		self.textPad.tag_add(SEL, "1.0", END)
		self.textPad.mark_set(INSERT,"1.0")
		self.textPad.see(INSERT)
	
	#function that sends the mail from class sendmail1
	def send(self):
		self.sm = sendmail1()			
	
	#function that add a reminder to a note
	def reminder(self):
		self.remin_win = Toplevel(self.root1)
		self.GUI_remin =reminder_dialogue(self.remin_win)
		self.root1.wait_window(self.remin_win)
		self.t = threading.Timer(1.0, self.check_reminder)
		self.t.start()
	
	#function that checks if a reminder is added or not and how much time is left	
	def check_reminder(self):
		global time_reminder,msg_reminder
		#checks with the system time
		if(time_reminder == time.strftime("%H:%M")):
			tkMessageBox.showinfo("Reminder", msg_reminder)
			Tkinter.Tk().bell()
			self.t.cancel()
		else:
			self.root1.after(2000,self.check_reminder)
	
	#function that opens selected file using filedialogbox features
	def open_command(self):
		global file
		file = tkFileDialog.askopenfile(parent = self.root1,mode = 'rb', title = 'Select a file', initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		if file != None:
		    #delete the content present earlier on the textpad present and load the opened file data
		    self.textPad.delete(1.0,END)
		    contents = file.read()
		    self.textPad.insert('1.0',contents)
		    file.close()
	
	#function that delete multiple files
	def delete_command(self):			
		self.files = tkFileDialog.askopenfilenames(parent = self.root1,title = 'Select a file',filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		Input = self.root1.tk.splitlist(self.files)
		for file in Input:
			if os.path.isfile(file):
				if os.open(file,os.O_EXCL):
					self.root1.title("Untitled TextPad")
					self.file = None
					self.textPad.delete('1.0', END)		
				os.remove(file)
				self.top = Toplevel()
				self.top.title("Message")
				self.msg = Message(self.top, text="File/Files Deleted")
				self.msg.pack()
				self.button = Button(self.top, text="Dismiss", command=self.top.destroy)
				self.button.pack()
			else:
				print "Error: in deteling file: Fuck yeaa"
			
	#function that saves the opened file in any format	
	def save_command(self):
	    file = tkFileDialog.asksaveasfile(mode='w')
	    if file != None:
	    # slice off the last character from get, as an extra return is added
		data = self.textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()
		tkMessageBox.showinfo('FYI', 'File Saved')
	#function that resaves the file
	def save_as(self):
		fileName = tkFileDialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		if fileName != None:
			file = open(fileName,'w')
			# slice off the last character from get, as an extra return is added
			datad = self.textPad.get('1.0', END+'-1c')
			file.write(data)
			file.close()
			tkMessageBox.showinfo('FYI', 'File Saved')	
	    
	def make_entry(self,master, caption, width=None):
	    Label(master, text=caption).pack(side=LEFT)
	    self.entry = Entry(master)
	    if width:
		self.entry.config(width=width)
		self.entry.pack(side=LEFT, padx=4, fill=BOTH)
		return self.entry	
	  
	#function that cuts the selected data
	def cut(self):
		self.textPad.event_generate("<<Cut>>")
		self.copy()
		self.delete("sel.first","sel.last")
	
	#function that copy the selected data
	def copy(self):
		self.textPad.event_generate("<<Copy>>")
		self.clipboard_clear()
		self.text = self.get("sel.first","sel.last")
		self.clipboard_append(textPad)
	
	#function that pastes the selected data
	def paste(self):
		self.textPad.event_generate("<<Paste>>")
		self.textPad = self.selection_get(selection= 'CLIPBOARD')
		self.insert('insert',self.textPad)
	
	#function that exit the textpad	 
	def exit_command(self):
	    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
		self.root1.destroy()
	
	#function that defines about the notepad
	def about_command(self):
	    label = tkMessageBox.showinfo("About", message = '''
Editing Commands
    Ctrl-x : Cut selected text
    Ctrl-c : Copy selected text
    Ctrl-v : Paste cut/copied text

File Commands
    Ctrl-o : Open file
    Ctrl-s : Save current note
    Ctrl-a : Save current note as <filename>
    Ctrl-p : Print current note
    Ctrl-n : Open new note

General
    Ctrl-h : Display this help window
''')
	
	#function that creates a new textpad		 	
	def new(self):
		self.root1.title("Untitled TextPad")
		self.file = None
		self.textPad.delete('1.0', END)


#class that sends the mail on localhost through smtp	
class sendmail1():
	def __init__(self):
		self.master = Tkinter.Tk()
		self.master.title("Email")
		#create the label to enter the sender and reciever mail id's
		self.mailfromlab = Label(self.master, text = 'Users Mail ID')
		self.mailfrom = Entry(self.master, width = 20)
		self.mailtolab = Label(self.master,text='Receivers Mail ID')
		self.mailto = Entry(self.master, width = 20)
		#create the button that activates emailing feature
		self.b = Button(self.master, text="OK", width=5, command= self.email(self.master))	
		self.mailfrom.pack()
		self.mailfromlab.pack()
		self.mailto.pack()
		self.mailtolab.pack()
		self.b.pack()	
		self.master.mainloop()

	def email(self,server="localhost"): #mailing on localhost server
		self.frm = self.mailfrom.get()
		self.to = self.mailto.get()	
		self.subject = "Email File/Files"
		# Create message container - the correct MIME type is multipart/alternative.
		self.msg = MIMEMultipart()
		self.msg['Subject'] = self.subject
		self.msg['From'] = self.frm
		self.msg['To'] = ','.join(self.to)
		self.msg['Date'] = formatdate(localtime=True)
		#open the files to be send through mail
		self.files = tkFileDialog.askopenfiles(parent = self.master,mode = 'rb', title = 'Select a file',filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		# loop to attach the file as an attachment
		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		for file in self.files:
			part = MIMEBase('application', "octet-stream")
			part.set_payload( open(file.name,"rb").read())
			# msg is an instance of MIMEMultipart()
		        self.msg.attach(part) 	
		# Send the message via local SMTP server.
		self.s = smtplib.SMTP('smtp.gmail.com','587') 
		self.s.ehlo()			
		self.s.starttls()
		self.s.ehlo()
		self.s.login('Username','password')					
		self.sendmail(self.frm,self.to,self.msg.as_string())
		print "send"			
		#self.lab2 = Label(root, text = "mail send", height = 10 , width = 10)
		#self.lab2.pack()
		#destroy the smtp connection and mainloop
		self.s.quit()
		self.master.destroy()

#class that adds the reminder		
class reminder_dialogue():

	def __init__(self,master):
		self.master=master
		#window name and its size that holds message to be displayed on the set time
		master.title("Reminder")
		self.master.minsize(width=600, height=100)
		self.master.maxsize(width=600, height=100)
		self.e_1 = Entry(self.master,width = 10)
		self.e_1.pack()
		self.e_1.focus_set()
		self.e_1.place(x = 160 , y = 10)
		self.e_2 = Entry(self.master,width = 40)
		self.e_2.pack()
		self.e_2.focus_set()
		self.e_2.place(x = 160 , y = 40)
		self.b = Button(self.master, text="OK", width=5, command= self.callback)
		self.b.pack()
		self.b.place(x = 300 , y = 70)
		self.w = Label(master, text="Time in HH:MM format ")
		self.w.pack()
		self.w.place(x = 10 , y = 15)
		self.w_2 = Label(master, text="Reminder Msg ")
		self.w_2.pack()
		self.w_2.place(x = 10 , y = 40)

	#callback function that takes the input value from the label
	def callback(self):
		global time_reminder,msg_reminder
		time_reminder = self.e_1.get()
		print time_reminder
		msg_reminder = self.e_2.get()
		print msg_reminder
		self.master.destroy()
	
#main() that calls the password window to start the execution	
def main():
	foo = Check(root)
	root.title("Window")
	root.mainloop()	

main()
