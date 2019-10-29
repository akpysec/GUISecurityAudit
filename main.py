import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import filedialog
from ttkwidgets import CheckboxTreeview

file = open("temp.txt", "w")
file.close()


def Main():
    window = tkinter.Tk()
    window.title('Security Checker')  # Title
    window.geometry('500x350+450+200')  # Resolution
    window['padx'] = 8
    # window.iconbitmap(default="Appwheel.ico")  # App icon
    title_font = tkfont.Font(family='Arial', size=10, weight="bold")  # Fonts within the App
    label1 = ttk.Label(text="Check the boxes:", font=title_font)  # Writings within the App
    label1.grid(row=0, column=0, sticky="nw", pady=8)

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=3)
    window.grid_columnconfigure(3, weight=2)
    window.grid_columnconfigure(4, weight=2)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=10)
    window.grid_rowconfigure(2, weight=2)
    window.grid_rowconfigure(3, weight=3)
    window.grid_rowconfigure(4, weight=3)

    tree = CheckboxTreeview  # Variable tree equals tree view
    # Edit dictionaries as you like
    # Dict #1
    cisco = {1: "enable secret", 2: "aaa new-model", 3: "service-password encryption", 4: "ip ssh version 2",
             5: "motd", 6: "no logging console", 7: "no logging monitor", 8: "vtp password"}
    # Dict 2
    smbv1_patch = {100: "KB4012598", 101: "KB4012212", 102: "KB4012215",
                   103: "KB4012213", 104: "KB4012216", 105: "KB4012214", 106: "KB4012217",
                   107: "KB4012606", 108: "KB4013198", 109: "KB4013429"}

    # What should not be present in a configuration files
    should_not_be = ["enable password", "snmp-server community public", "transport input telnet",
                     "EnableSMB1Protocol              : True"]

    scrollbar1 = ttk.Scrollbar(window, orient="vertical", command=tree.yview)  # Scroll bar
    scrollbar1.grid(row=1, column=6, sticky='nse')

    tree = CheckboxTreeview(yscrollcommand=scrollbar1)
    tree.grid(column=0, columnspan=6, row=1, sticky="news")  # Tree position

    tree.insert("", "end", "1", text="1. CISCO Hardening")
    tree.insert("1", "end", "sub0", text="1.1 Generic configs")
    tree.insert("sub0", "end", cisco[1], text="1.1.1 Password Hash")
    tree.insert("sub0", "end", cisco[3], text="1.1.2 Password Encryption")
    tree.insert("sub0", "end", cisco[2], text="1.1.3 AAA configuration")
    tree.insert("sub0", "end", cisco[4], text="1.1.4 SSH version 2")
    tree.insert("sub0", "end", cisco[5], text="1.1.5 MOTD")
    tree.insert("sub0", "end", cisco[8], text="1.1.6 VTP Password")
    tree.insert("sub0", "end", cisco[6], text="1.1.7 No logging console")
    tree.insert("sub0", "end", cisco[7], text="1.1.8 No logging monitor")

    tree.insert("", "end", "2", text="2. Microsoft SMBv1 Patching Check")
    tree.insert("2", "end", smbv1_patch[100], text="2.1 Windows Vista & Server 2008 (KB4012598)")
    tree.insert("2", "end", "sub10", text="2.2 Windows 7 & Server 2008 R2")
    tree.insert("sub10", "end", smbv1_patch[101], text="2.2 KB4012212")
    tree.insert("sub10", "end", smbv1_patch[102], text="2.3 KB4012215")

    tree.insert("2", "end", "sub11", text="2.4 Windows 8.1 & Server 2012 & 2012 R2")
    tree.insert("sub11", "end", smbv1_patch[103], text="2.4 KB4012213")
    tree.insert("sub11", "end", smbv1_patch[104], text="2.5 KB4012216")
    tree.insert("sub11", "end", smbv1_patch[105], text="2.6 KB4012214")
    tree.insert("sub11", "end", smbv1_patch[106], text="2.7 KB4012217")

    tree.insert("2", "end", "sub12", text="2.8 Windows 10 & Server 2016")
    tree.insert("sub12", "end", smbv1_patch[107], text="2.8 KB4012606")
    tree.insert("sub12", "end", smbv1_patch[108], text="2.7 KB4013198")
    tree.insert("sub12", "end", smbv1_patch[109], text="2.8 KB4013429")

    button2 = ttk.Button(text="Quit", command=sys.exit)             # Close Button
    button2.grid(row=4, column=0, sticky='ws', padx=10, pady=10)    # Close button position

    checked_boxes = list()          # List for appending selected boxes
    lines_in_conf_file = list()     # List for appending the read file
    passed = str('Passed\t\t')
    not_passed = str('Not Passed\t\t')

    def box_select(just):  # Function for appending selected boxes
        checked_boxes.append(tree.get_checked())

    tree.bind('<<TreeviewSelect>>', box_select)

    def file_open():

        if len(tree.get_checked()) > 0:
            readfile = filedialog.askopenfilename(
                initialdir="/", title="Select " "configuration" " file", filetypes=(("txt "
                                                                                     "files", "*.txt *.html"),
                                                                                    ("all " "files", "*.*")))

            try:
                with open(readfile, "r", encoding='utf-8') as opened_file:
                    for i in opened_file:
                        pass
                    encodings = 'utf-8'
            except UnicodeDecodeError:
                encodings = 'utf-16'

            with open(readfile, "r", encoding=encodings) as opened_file:
                for read_line in opened_file:
                    lines_in_conf_file.append(read_line.strip('\n'))
                with open("temp.txt", "a") as conf:  # Opens file --ONCE--
                    for clause in checked_boxes[-1]:  # Loops over selection
                        for line in lines_in_conf_file:  # Loops over conf file
                            if clause in line:  # Checks what equals between loops
                                conf.write("{}".format(passed) + clause + "\n")  # Writing them into a file
                                break  # Ends IF statement and continues with
                        else:  # a loop on a conf file
                            if clause in should_not_be:  # Checks if selection in not wanted list
                                conf.write("{}".format(passed) + clause + "\n")  # if yes, writes to a file "PASSED"
                            else:
                                conf.write("{}".format(not_passed) + clause + "\n")  # if not, writes to a file "NOT
                                # PASSED"

                checked_configs()

        else:
            pop_up_msg()

    def checked_configs():
        checked = tkinter.Tk()
        # checked.iconbitmap(default="Appwheel.ico")  # App icon
        checked.geometry('650x500+650+300')  # Resolution
        checked.wm_title("Security Checker")

        checked.grid_columnconfigure(0, weight=1)
        checked.grid_columnconfigure(1, weight=1)
        checked.grid_columnconfigure(2, weight=3)
        checked.grid_columnconfigure(3, weight=2)
        checked.grid_columnconfigure(4, weight=2)
        checked.grid_rowconfigure(0, weight=1)
        checked.grid_rowconfigure(1, weight=10)
        checked.grid_rowconfigure(2, weight=2)
        checked.grid_rowconfigure(3, weight=3)
        checked.grid_rowconfigure(4, weight=3)

        label2 = ttk.Label(checked, text='Security check report:', font=title_font)
        label2.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        button3 = ttk.Button(checked, text="Quit", command=sys.exit)
        button3.grid(row=4, column=0, sticky='ws', padx=10, pady=10)

        def save_report_to_file():
            save_file = filedialog.asksaveasfile(mode='w', defaultextension=".txt",
                                                 initialdir="/", title="Save " "report", filetypes=(("txt " "files",
                                                                                                     "*.txt"),
                                                                                                    ("all " "files",
                                                                                                     "*.*")))
            if save_file:
                with open('temp.txt', 'r') as temp_file:
                    for i in temp_file:
                        save_file.write(i)
                    else:
                        return

        button4 = ttk.Button(checked, text="Save to..", command=save_report_to_file)
        button4.grid(row=4, column=5, sticky='es', padx=10, pady=10)

        checked = Text(checked)
        checked.grid(column=0, columnspan=6, row=1, sticky="news")
        checked.insert('1.0', ''.join(open("temp.txt", "r")))

        checked.mainloop()

    def pop_up_msg():
        popup = tkinter.Tk()
        # popup.iconbitmap(default="Appwheel.ico")  # App icon
        popup.wm_title("Security Checker")

        label3 = ttk.Label(popup, text='Please select at least 1 checkbox to continue', font=title_font)
        label3.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        button5 = ttk.Button(popup, text="Okay", command=popup.destroy)
        button5.grid(row=1, column=0, padx=10, pady=10)

        popup.mainloop()

    button1 = ttk.Button(text="Next", command=file_open)
    button1.grid(row=4, column=5, sticky='es', padx=10, pady=10)  # Open's Browse Button

    window.mainloop()


Main()

