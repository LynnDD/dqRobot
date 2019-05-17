#coding=utf-8
import os, sys
import tkinter as tk
from tkinter import messagebox
import fnmatch, re, threading, time, signal, subprocess, threading, codecs

#砖墙配色，底色，砖头1，砖头2, 砖头3
cl = ['#271609','#d78328','#965c28','#862c0c','white','blue']
#zboot，core 路径1，
zbootPath = ['Y:\\rk-linux\\rk_boot_all\\ztool\\']
codePath = ['Y:\\rk-linux\\', 'Y:\\repo\\', "Y:\\"]
exePath = ['C:\\Program Files (x86)\\Notepad++\\notepad++.exe']
monitor = 0
logFile = ''
pattern = ''

#=============================== FUNC ======================================
def note(text):
	messagebox.showinfo("Title", text)

def dqNote(text):
	dq["text"] = text

def heartbeat():
	while 1:
		time.sleep(10)

def monitorLog():
	global logFile, pattern, monitor
	print('logFile: ' + logFile + " pattern: " + pattern)
	p = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	monitor = 1
	count = 0
	dqNote('log on')
	while True:
		if count < 10:
			count = count + 1
			line = p.stdout.readline().decode().strip()
			if line:
				if pattern in line:
					monitor = 0
					note(line)
					p.kill()
					break
		else:
			count = 0
			time.sleep(1)
			p.kill()
			p = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if monitor == 0:
			p.kill()
			break

#获取zboot路径下的所有匹配tag的bat，并执行
def getAllZboot(tag):
	list = []
	dirs = os.listdir(zbootPath[0])
	for file in dirs:
		root, ext = os.path.splitext(file)
		if re.search(tag,root) and re.search(r'bat',ext):
			list.append(file)
	return list

#获取codePath路径下的所有匹配tag的dir，返回所有匹配值
def getDir(tag):
	list = []
	for t in codePath:
		dirs = os.listdir(t)
		for file in dirs:
			root, ext = os.path.splitext(file)
			if re.search(tag,root):
				list.append(t + file)
	return list
	
#=============================== EVEN ======================================
def buttonEvent(a):
	files = []

	if a == 'z0':
		project = e.get()
		files = getAllZboot(project)
		os.chdir(zbootPath[0])
		for bat in files:
			os.system(bat)
	elif a == 'z1':
		os.chdir(zbootPath[0])
		os.system("MergerLoader_rk3308_u2.bat")
	elif a == 'c0':
		code = e.get()
		if code == '':
			subprocess.Popen("explorer.exe " + codePath[0],  shell=True)
		else:
			files = getDir(code)
			for file in files:
				subprocess.Popen("explorer.exe " + file,  shell=True)
	elif a == 'c1':
		os.system("explorer.exe " + codePath[0])
	elif a == 'm0':
		global logFile, pattern
		logFile = e.get()
		pattern = e1.get()
		try:
			threading.Thread(target=monitorLog, name="thread_1").start()
			print("active thread num: ", threading.active_count())
		except:
			print("Error: unable to start thread")
	elif a == 'm1':
		global monitor
		monitor = 0
		dqNote('zzzZZZ')
	elif a == 'm2':
		logFile = e.get()
		logPath = os.path.dirname(os.path.abspath(logFile))
		subprocess.Popen("explorer.exe " + logPath,  shell=True)

#=============================== UI ======================================
root=tk.Tk()
root.configure(background=cl[0])
root.wm_attributes('-topmost',1)
rowNow = 0

photo=tk.PhotoImage(file=r"test.jpg")
label=tk.Label(root,image=photo, bd=0) .grid(row=rowNow, column=0, columnspan = 7)
rowNow+=1

e=tk.Entry(root)
e.grid(row=rowNow, column=0, columnspan = 5)
rowNow+=1
e1=tk.Entry(root)
e1.grid(row=rowNow, column=0, columnspan = 5)
dq = tk.Label(root, text ='zzzZZZ', bg=cl[2])
dq.grid(row=rowNow,column=4, columnspan = 4)
rowNow+=1

#add label
def addLabel(name, r, c, color):
	labelTemp = tk.Label(root, text =name, bg=color)
	labelTemp.grid(row=r,column=c)

#add button
def addButton(name, r, c, args, color):
	buttonTemp = tk.Button(root, text =name, bg=color, command = lambda :buttonEvent(args))
	buttonTemp.grid(row=r,column=c)

addButton('zboot', rowNow, 0, 'z0', cl[1])
addButton('rk3308', rowNow, 1, 'z1', cl[1])
rowNow+=1

addButton('文件资源', rowNow, 0, 'c0', cl[1])
rowNow+=1

addButton('log on', rowNow, 0, 'm0', cl[1])
addButton('off', rowNow, 1, 'm1', cl[1])
addButton('open', rowNow, 2, 'm2', cl[1])
rowNow+=1

threading.Thread(target=heartbeat, name="thread_0").start()

root.mainloop()
