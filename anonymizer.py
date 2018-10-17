import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os, re, subprocess, sys

def get_zippath():
	if os.path.isdir(r"C:\Program Files\7-Zip"):
		zippath = r"C:\Program Files\7-Zip\7z.exe"
		return zippath
	elif os.path.isdir(r"C:\Program Files (x86)\7-Zip"):
		zippath = r"C:\Program Files (x86)\7-Zip\7z.exe"
		return zippath
	else:
		messagebox.showinfo("7-Zip", "Unable to find 7-Zip installation")
		messagebox.showinfo("Find installation", "Browse and select 7-Zip installation")
		zippath = filedialog.askopenfilename(title="Select 7-Zip Installation", filetypes = [("7-zip", "7z.exe")])
		if zippath == '':
			messagebox.showerror("7-Zip", "Installation not found. Program will exit.")
			sys.exit()
		if zippath.lower().endswith('7z.exe'):
			messagebox.showinfo("7-Zip found", "7-Zip installation found")
			return zippath
		else:
			messagebox.showerror("7-Zip", "Installation not found. Program will exit.")
			sys.exit()

def exit():
	gui.destroy()
	sys.exit()

def anonymize():
	if sdl_files == []:
		return
	regex_variable = regex_choice.get()
	if regex_variable == "custom":
		regex_variable = w10_customtext.get()
		if re.match(r'\W', regex_variable):
			messagebox.showinfo("Invalid characters", "Only numbers and letters allowed")
			return
		else:
			regex_variable = r'\1' + regex_variable + '<'
	for sdl_file in sdl_files:
			if os.path.isfile(os.path.dirname(sdl_file) + "\\anonym\\" + os.path.basename(sdl_file)):
				messagebox.showinfo("File already exists", "The file " + sdl_file + " is already anonymized.")
				continue
			if not os.path.isfile(sdl_file):
				messagebox.showinfo("Error", "File " + sdl_file + " was not found.")
				continue
			if sdl_file.lower().endswith('.sdlxliff'):
				with open(sdl_file, 'r', encoding='utf-8') as xliff:
					xliff_contents = xliff.read()
				xliff_contents = re.sub(r'("last_modified_by">)([^<]+<)', regex_variable, xliff_contents, flags = re.M)
				xliff_contents = re.sub(r'("created_by">)([^<]+<)', regex_variable, xliff_contents, flags = re.M)
				if not os.path.isdir(os.path.dirname(sdl_file) + "\\anonym"):
					os.mkdir(os.path.dirname(sdl_file)+"\\anonym")
				with open(os.path.dirname(sdl_file) + "\\anonym\\" + os.path.basename(sdl_file), 'w', encoding='utf-8') as xliff:
					xliff.write(xliff_contents)
			elif sdl_file.lower().endswith('.sdlrpx') or sdl_file.lower().endswith('.wsxz'):
				packagepath = "-o" + os.path.dirname(sdl_file) + r"\_temp_anonymizer"
				cmd = [zippath, "x", sdl_file, packagepath, "-r"]
				subprocess.run(cmd)
				packagepath = packagepath[2:]
				for root, dirs, files in os.walk(packagepath):
					for file in files:
						if file.endswith(".sdlxliff"):
							xliffs_in_package.append(os.path.join(root, file))
				for file in xliffs_in_package:
					with open(file, 'r', encoding='utf-8') as xliff:
						xliffcontents = xliff.read()
					xliffcontents = re.sub(r'("last_modified_by">)([^<]+<)', regex_variable, xliffcontents, flags = re.M)
					xliffcontents = re.sub(r'("created_by">)([^<]+<)', regex_variable, xliffcontents, flags = re.M)
					with open(file, 'w', encoding='utf-8') as xliff:
						xliff.write(xliffcontents)
				packagename = os.path.dirname(sdl_file) + r'\anonym' + "\\" + os.path.basename(sdl_file) + ".zip"
				cmd = [zippath, "a", packagename, packagepath + "/*", "-sdel"]
				subprocess.run(cmd)
				os.rename(packagename, packagename.replace('.zip', ''))
				os.rmdir(packagepath)
			else:
				messagebox.showinfo("Error", "Invalid file type")
	w4_listbox.delete(0,tk.END)
	sdl_files.clear()
	xliffs_in_package.clear()
	messagebox.showinfo("Completed", "All files anonymized")
	return sdl_files

def add_files():
	selected_files = filedialog.askopenfilenames(title="Select files", filetypes = [("sdl files", "*.sdlxliff *.wsxz *.sdlrpx")])
	selected_files = list(selected_files)
	if selected_files == []:
		return
	else:
		for sdl_file in selected_files:
			if sdl_file in sdl_files:
				continue
			if os.path.isfile(os.path.dirname(sdl_file) + "\\anonym\\" + os.path.basename(sdl_file)):
				messagebox.showinfo("File already exists", "The file " + os.path.basename(sdl_file) + " is already anonymized.")
				continue
			if sdl_file.lower().endswith('.sdlrpx'):
				sdl_files.append(sdl_file)
				w4_listbox.insert(tk.END,sdl_file)
			elif sdl_file.lower().endswith('.wsxz'):
				sdl_files.append(sdl_file)
				w4_listbox.insert(tk.END,sdl_file)
			elif sdl_file.lower().endswith('.sdlxliff'):
				sdl_files.append(sdl_file)
				w4_listbox.insert(tk.END,sdl_file)
			else:
				messagebox.showinfo("File type not supported", os.path.basename(sdl_file) + " is not a supported file type.")
				continue
	return sdl_files

def remove_files():
	if sdl_files ==[]:
		return
	remove_file = w4_listbox.get(w4_listbox.curselection())
	w4_listbox.delete(tk.ANCHOR)
	sdl_files.remove(remove_file)
	return sdl_files




gui = tk.Tk()

regex_choice = tk.StringVar()
regex_choice.set(r'\1EVS<')
sdl_files = []
xliffs_in_package = []
zippath = get_zippath()

logo = tk.PhotoImage(file="anon.gif")
logo = logo.subsample(5)
gui.title("Anonymizer")
gui.configure(bg="black")
gui.geometry("370x450")
gui.resizable(0,0)
w1_title = tk.Label(gui, text="Anonymizer", fg="white", bg="black", font="none 16 bold").grid(row=0, column=1, sticky='E'+'W')
w2_logo = tk.Label(gui, image=logo, borderwidth=0).grid(row=1, column=2, sticky='E')
w3_text = tk.Label(gui, text="Files to anonymize:", fg="white", bg="black", font="none 10").grid(row=1, column=0, sticky='W'+'S')
w4_listbox = tk.Listbox(gui, selectmode=tk.SINGLE)
w4_listbox.grid(row=3, column=0, columnspan=4, sticky='W'+'E')
w5_add = tk.Button(gui, text="Add", fg="black", bg="white", command=add_files).grid(row=4, column=0, sticky='E'+'W', pady=5)
w6_remove = tk.Button(gui, text="Remove", fg="black", bg="white", command=remove_files).grid(row=4, column=2, sticky='E'+'W')
tk.Radiobutton(gui, text="Standard (EVS)", fg="white", bg="black", variable=regex_choice, value=r'\1EVS<', selectcolor="black", activebackground="black").grid(row=5, column=1, sticky='W')
tk.Radiobutton(gui, text="Continental (LSP2)", fg="white", bg="black", variable=regex_choice, value=r'\1LSP2<', selectcolor="black", activebackground="black").grid(row=6, column=1, sticky='W')
tk.Radiobutton(gui, text="Custom", fg="white", bg="black", variable=regex_choice, value="custom", selectcolor="black", activebackground="black").grid(row=7, column=1, sticky='W')
w10_customtext = tk.Entry(gui)
w10_customtext.grid(row=7, column=2)
w11_anonymize = tk.Button(gui, text="Anonymize", fg="black", bg="white", command=anonymize).grid(row=8, column=0, sticky='E'+'W')
w12_exit = tk.Button(gui, text="Exit", fg="black", bg="white", command=exit).grid(row=8, column=2, sticky='E'+'W')



gui.mainloop()
