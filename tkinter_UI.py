from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from platform import system
import configparser, subprocess, os.path, os, threading, datetime, time


# DB PATH FETCHING FOR LINUX
def dbdir_check():
    global psql, pg_dump
    if system() == 'Linux':
        ps = subprocess.Popen(["which psql"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = ps.communicate()
        cod = ps.returncode
        op = output.strip()
        psql = op.decode('ascii')
        pg_dump = psql.replace("psql", "pg_dump")
        return cod
    elif system() == 'Windows':
        return 1


def property_app(window):
    global progress, psql
    lab1 = Label(window, text="Enter PostgreSQL PATH: ", background='#E05E08', textvariable=pospath)
    lab1.grid(row=1, column=0, padx=5, pady=5)

    window.dbpath = Entry(window, state=DISABLED, width=55, textvariable=dbdir)
    window.dbpath.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

    if dbdir_check() == 0:
        pospath.set("Found DataBase Path: ")
        dbdir.set(psql)
        ll1 = Label(window, text="DO NOT EDIT..!", background='red')
        ll1.grid(row=1, column=3, padx=5, pady=5)
    else:
        pospath.set("Enter PostgreSQL PATH: ")
        browsebutton0 = Button(window, text="BROWSE", command=lambda: folder("postpath"))
        browsebutton0.grid(row=1, column=3, padx=5, pady=5)

    lab2 = Label(window, text="Enter DataBase Name: ", background='#E05E08')
    lab2.grid(row=2, column=0, padx=5, pady=5)

    window.dbname = Entry(window, width=55, textvariable=dbn)
    window.dbname.grid(row=2, column=1, padx=5, pady=5)

    lab3 = Label(window, text="Enter DataBase Password: ", background='#E05E08')
    lab3.grid(row=3, column=0, padx=5, pady=5)

    window.password = Entry(window, width=55, textvariable=dbpw)
    window.password.grid(row=3, column=1, padx=5, pady=5)

    lab4 = Label(window, text="Enter DataBase Port: ", background='#E05E08')
    lab4.grid(row=4, column=0, padx=5, pady=5)

    window.dbport = Entry(window, width=55, textvariable=dbp)
    window.dbport.grid(row=4, column=1, padx=5, pady=5)

    lab5 = Label(window, text="Enter Path to save Backup: ", background='#E05E08')
    lab5.grid(row=5, column=0, padx=5, pady=5)

    destination = Entry(window, state=DISABLED, width=55, textvariable=downpath)
    destination.grid(row=5, column=1, padx=5, pady=5)

    browsebutton1 = Button(window, text="BROWSE", command=lambda: folder('path'))
    browsebutton1.grid(row=5, column=3, padx=5, pady=5)

    savebutton = Button(window, text="SAVE", command=save)
    savebutton.grid(row=6, column=0, padx=5, pady=5)

    submitbutton = Button(window, text=" BACKUP NOW ", command=destination_check)
    submitbutton.grid(row=6, column=3, padx=5, pady=5)

    progress = Progressbar(window, orient=HORIZONTAL, length=400, mode='indeterminate')
    progress.grid(row=7, column=1, padx=5, pady=5)


def main_app(window):
    global progress, psql, pg_dump
    label1 = Label(window, text="DataBase Name: ", background='#E05E08')
    label1.grid(row=1, column=0, padx=5, pady=5)

    dbname = Entry(window, state=DISABLED, width=55, textvariable=dbn)
    dbname.grid(row=1, column=1, padx=5, pady=5)

    label2 = Label(window, text="DataBase Port: ", background='#E05E08')
    label2.grid(row=2, column=0, padx=5, pady=5)

    dbport = Entry(window, state=DISABLED, width=55, textvariable=dbp)
    dbport.grid(row=2, column=1, padx=5, pady=5)

    label3 = Label(window, text="DataBase Path: ", background='#E05E08')
    label3.grid(row=3, column=0, padx=5, pady=5)

    dbpath = Entry(window, state=DISABLED, width=55, textvariable=dbdir)
    dbpath.grid(row=3, column=1, padx=5, pady=5)

    label4 = Label(window, text="Enter Path to save Backup: ", background='#E05E08')
    label4.grid(row=4, column=0, padx=5, pady=5)

    destination = Entry(window, state=DISABLED, width=55, textvariable=downpath)
    destination.grid(row=4, column=1, padx=5, pady=5)

    browsebutton1 = Button(window, text="BROWSE", command=lambda: folder('path'))
    browsebutton1.grid(row=4, column=3, padx=5, pady=5)

    editprop = Button(window, text="Edit Property File", command=lambda: edit("main"))
    editprop.grid(row=5, column=0, padx=5, pady=5)

    submitbutton = Button(window, text=" BACKUP ", command=destination_check)
    submitbutton.grid(row=5, column=3, padx=5, pady=5)

    progress = Progressbar(window, orient=HORIZONTAL, length=400, mode='indeterminate')
    progress.grid(row=6, column=1, padx=5, pady=5)


def edit(arg):
    global pgPass
    if arg == "main":
        for widget in window.winfo_children():
            widget.destroy()
        property_app(window)
        dbpw.set(pgPass)
    elif arg == "prop":
        for widget in window.winfo_children():
            widget.destroy()
        main_app(window)


def folder(path):
    global psql, pg_dump
    if path == 'path':
        if system() == 'Linux':
            dir = filedialog.askdirectory(initialdir="/home/")
            downpath.set(dir)
        elif system() == 'Windows':
            dir = filedialog.askdirectory(initialdir="C:\\")
            dir = dir.replace("/", "\\")
            downpath.set(dir)
    elif path == 'postpath':
        if system() == 'Linux':
            dir = filedialog.askdirectory(initialdir="/")
            dbdir.set(dir + "/bin/psql")
            psql = dbdir.get()
            pg_dump = psql.replace("psql", "pg_dump")
        elif system() == 'Windows':
            dir = filedialog.askdirectory(initialdir="C:\\")
            dir = dir.replace("/", "\\")
            dbdir.set(dir + "\\bin\\psql")
            psql = dbdir.get()
            pg_dump = psql.replace("psql", "pg_dump")

# DESTINATION CHECK
def destination_check():
    print(downpath.get(), "ds")
    if system() == 'Linux':
        if downpath.get() == "/home/" or downpath.get() == "":
            messagebox.showinfo('Info', "Please select a destination to take backup.")
            return 1
        else:
            print("paths", downpath.get(), "pp")
            print("PASSED")
            submit()
    elif system() == 'Windows':
        if downpath.get() == "C:\\" or downpath.get() == "":
            print(downpath.get(), "dd")
            messagebox.showinfo('Info', "Please select a destination to take backup.")
            return 1
        else:
            submit()

# SAVING DB DETAILS TO PROPERTY FILE
def save():
    global dpath
    dbname = dbn.get()
    dbport = dbp.get()
    dbpasswd = dbpw.get()
    dbpath = dbdir.get()
    if system() == 'Linux':
        config = configparser.ConfigParser()
        config['Default'] = {"db_name": dbname, 'db_port': dbport, 'db_password': dbpasswd, 'db_path': dbpath}
        with open(propfile, 'w') as file:
            config.write(file)
            file.close()
        messagebox.showinfo('Info', "Details saved")
        edit("prop")
    elif system() == 'Windows':
        print("WINDOWS PROP")
        config = configparser.ConfigParser()
        config['Default'] = {"db_name": dbname, 'db_port': dbport, 'db_password': dbpasswd, 'db_path': dbpath}
        with open(propfile, 'w') as file:
            config.write(file)
            file.close()
        messagebox.showinfo('Info', "Details saved")
        edit("prop")


# DB BACKUP FUNCTION
def backup(pg_dump, dbname, dbport, dbpass, path):
    global code
    print(pg_dump)
    os.putenv('PGPASSWORD', dbpass)
    if system() == 'Linux':
        ps = subprocess.Popen(
            [pg_dump, '-U', 'adempiere', '-p', dbport, '-Fc', dbname, '-f', path + '/' + date + '.cdmp'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif system() == 'Windows':
        path = path.replace("/", "\\")
        print(path + '\\' + date + '.cdmp')
        ps = subprocess.Popen(
            [pg_dump, '-U', 'adempiere', '-p', dbport, '-f', path + '\\' + date + '.cdmp', '-Fc', dbname],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(2)
    output, error = ps.communicate()
    code = ps.returncode
    if code == 0:
        messagebox.showinfo('Info', "Backup completed!")
        window.quit()
        sys.exit()
    else:
        messagebox.showinfo('Info', "Backup Failed..!!")
        window.quit()
        sys.exit()


# DB DETAILS VALIDATING
def db_check(pgpath, dbname, dbport, dbpass):
    eo = 'database' + ' ' + '"' + dbname + '"' + ' ' + 'does not exist'
    os.putenv('PGPASSWORD', dbpass)
    print(pgpath)
    ps = subprocess.Popen(
        [pgpath, '-U', 'adempiere', '-p', dbport, '-d', dbname, '-c', 'select name from ad_client;'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, error = ps.communicate()
    if ps.returncode == 0:
        print("OK TEST")
        return 0
    else:
        matchdbn = re.search(eo, str(error))
        matchdbp = re.search(dbport, str(error))
        if matchdbn:
            messagebox.showinfo('Info', "Invalid Database Name!")
            return 1
        elif matchdbp:
            messagebox.showinfo('Info', "Invalid Database Port")
            return 1
        else:
            messagebox.showinfo('Info', "Something went wrong! \n Please Try Again.")
            return 1


def submit():
    global code, psql, progress, pgPass
    print("DBName: ", dbn.get())
    print("DBPORT: ", dbp.get())
    print("DBPASS: ", dbpw.get())
    print("PG_PATH: ", dbdir.get())
    print("Dest: ", downpath.get())
    DbName = dbn.get()
    DbPort = dbp.get()
    Dbpass = dbpw.get()
    pgpath = dbdir.get()
    path = downpath.get()
    pg_dump = pgpath.replace("psql", "pg_dump")
    if Dbpass == "":
        Dbpass = pgPass
    print("pass", Dbpass)
    print("path", pg_dump)
    i = 10
    if db_check(pgpath, DbName, DbPort, Dbpass) == 0:
        thread1 = threading.Thread(target=backup, args=(pg_dump, DbName, DbPort, Dbpass, path))
        thread1.start()
        while code != 0:
            progress['value'] = i
            window.update_idletasks()
            time.sleep(0.1)
            i += 10
    else:
        print("windows")


# TAKING DB DETAILS FROM PROPERTY FILE
def db_details():
    global propfile, DbPort, DbName, pg, pgPass
    if os.path.isfile(propfile):
        conf = configparser.ConfigParser()
        conf.read(propfile)
        default = conf['Default']
        DbName = default["db_name"]
        DbPort = default["db_port"]
        pg = default["db_path"]
        pgPass = default["db_password"]
        return 0
    else:
        return 1


# DATE FETCHING
today = datetime.date.today()
date = today.strftime('%d' + '%b' + '%Y')

# WINDOW CREATION
window = Tk()
window.config(background='#E05E08')
window.geometry("800x270")
window.title("SIMPLE BACKUP TOOL")

# GLOBAL VARIABLES
dbn = StringVar()
dbp = StringVar()
dbpw = StringVar()
downpath = StringVar()
dbdir = StringVar()
pospath = StringVar()
psql, pg_dump, code, progress, DbName, DbPort, pg, pgPass = None, None, None, None, None, None, None, None

# PROPERTY FILE DEFINING
if system() == 'Linux':
    propfile = "/home/jishnu/PYTHON/db.prop"
elif system() == 'Windows':
    propfile = "C:\DATA\Pytest\db.prop"

# APP CALLING
if db_details() == 0:
    print(DbName, DbPort, pgPass, pg)
    main_app(window)
    dbn.set(DbName)
    dbp.set(DbPort)
    dbdir.set(pg)
else:
    print("passw", pgPass)
    property_app(window)
window.mainloop()
