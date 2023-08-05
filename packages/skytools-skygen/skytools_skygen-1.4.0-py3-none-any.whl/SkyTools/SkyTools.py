# -*- coding: utf-8 -*-

import argparse, cmath, os, datetime, logging, math, shutil, socket
try:
    from Tkinter import *
except ImportError:
    try:
        from tkinter import *
    except ImportError:
        print("Tkinter is not installed, the functions using Tkinter can bug.")

try:
    import urllib, urllib2
except ImportError:
    import urllib.request
try:
    import BaseHTTPServer, CGIHTTPServer
except ImportError:
    import http.server

ver = "1.4.0"

def arguments(commands, text, commands2=None, action=None):
    arg = argparse.ArgumentParser()
    i = 0
    for command in commands:
        if action is None and commands2 is None:
            arg.add_argument(commands[i], help=text[i])
        elif commands2 is None:
            arg.add_argument(commands[i], help=text[i], action=action[i])
        elif action is None:
            arg.add_argument(commands[i], commands2[i], help=text[i])
        else:
            arg.add_argument(commands[i], commands2[i], help=text[i], action=action[i])
        i += 1
    return arg.parse_args()

def button(window, text, command, textvariable=None):
    button = Button(window, text=text, command=command, textvariable=textvariable)
    button.pack()
    return button

def canvas(window, width=100, height=100, color="white"):
    can = Canvas(window, width=width, height=height, background=color)
    can.pack()
    return can

def checkbutton(window, text, textvariable=None):
    checkbutton = Checkbutton(window, text=text, textvariable=textvariable)
    checkbutton.pack()
    return checkbutton

def cmd(command):
    return os.system(command)

def cmd_text(command):
    return os.popen(command)

class directory:
    def __init__(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.path = os.path.abspath(path)

    def __repr__(self):
        return self.path

    def cd(self, path):
        return directory(self.path + "/" + path)

    def file_delete(self, name):
        file(self.path + "/" + name).delete()

    def files_replace(self, text1, text2, start="", end=".txt", no_print=False):
        files = self.ls(True, start=start, end=end)
        files_edited = []
        for file_name in files:
            file_replace = files[file_name].replace(text1, text2)
            files_edited.append(file_replace)
            if not no_print and file_replace["content1"] != file_replace["content2"]:
                print(file_name)
                print(file_replace["content1"])
                print(file_replace["content2"])
                print(len(file_replace["content2"]) - len(file_replace["content1"]))
        return files_edited

    def open_file(self, name, create=False):
        if create:
            return file(self.path + "/" + name)
        else:
            if name in os.listdir(self.path):
                return file(self.path + "/" + name)
            else:
                return None

    def delete(self, delete_not_empty=False):
        if delete_not_empty:
            shutil.rmtree(self.path)
        else:
            os.rmdir(self.path)

    def ls(self, onlyfiles=False, start="", end=""):
        file_list = {}
        for file_name in os.listdir(self.path):
            if os.path.isdir(self.path + "/" + file_name):
                if not onlyfiles:
                    file_list[file_name] = directory(self.path + "/" + file_name)
            else:
                if file_name.startswith(start) and file_name.endswith(end):
                    file_list[file_name] = file(self.path + "/" + file_name)
        return file_list

def equation(a=0, b=0, c=None):
    if c:
        d = b*b-4*a*c
        if d < 0:
            x = [(-c-complex(0, 1)*math.sqrt(-d))/(2*a), (-c+complex(0, 1)*math.sqrt(-d))/(2*a)]
        elif d == 0:
            x = [-b/(2*a), -b/(2*a)]
        else:
            x = [(-b-math.sqrt(d))/(2*a), (-b+math.sqrt(d))/(2*a)]
    else:
        x = -b/a
    return x

class file:
    def __init__(self, name):
        self.name = os.path.abspath(name)
        open(name, "a").close()

    def __repr__(self):
        return self.name

    def chmod(self):
        return oct(os.stat(self.name).st_mode)[-3:]

    def copy(self, name):
        path = os.path.abspath(os.path.join(os.path.dirname(self.name), name))
        shutil.copyfile(self.name, path)
        return file(path)

    def delete(self):
        file_delete(self.name)

    def dir(self):
        return directory(os.path.dirname(self.name))

    def read(self, n=None):
        return file_read(self.name, n)

    def readlines(self, n=None):
        with open(self.name, "r") as file_open:
            content = file_open.readlines(n)
            return content

    def rename(self, name):
        path = os.path.abspath(os.path.join(os.path.dirname(self.name), name))
        os.rename(self.name, path)
        self.name = path

    def replace(self, text1, text2, line=None):
        with open(self.name, "r") as file_open:
            content = "\n".join(file_open.readlines(line))
            content2 = content.replace(text1, text2)
        with open(self.name, "w") as file_open:
            file_open.write(content2)
        return {"name": self.name, "content1": content, "content2": content2}

    def size(self):
        return os.stat(self.name).st_size

    def write(self, text, delete_content=False):
        file_write(self.name, text, delete_content)

def file_delete(name):
    os.remove(name)

def file_read(name, n=None):
    with open(name, "r") as file_open:
        content = file_open.read(n)
        return content

def file_write(name, text, delete_content=False):
    if delete_content:
        with open(name, "w") as file_open:
            file_open.write(text)
    else:
        with open(name, "a") as file_open:
            file_open.write(text)

class form:
    def __init__(self, window):
        self.window = window
        self.canvas = canvas(self.window)
        self.buttons = []
        self.checkbuttons = []
        self.inputs = []
        self.labels = []

    def button(self, text_button, command, textvariable=None):
        button_tk = button(self.canvas, text_button, command, textvariable)
        self.buttons.append(button_tk)
        return button_tk

    def checkbutton(self, text_checkbutton, textvariable=None):
        checkbutton_tk = checkbutton(self.canvas, text_checkbutton, textvariable)
        self.checkbuttons.append(checkbutton_tk)
        return checkbutton_tk

    def input(self, width=20, textvariable=None, text_input=None):
        input_tk = input_text(self.canvas, text_input, width, textvariable)
        self.inputs.append(input_tk)
        return input_tk

    def input_label(self, text_label, width=20, textvariable=None, text_input=None):
        self.label(text_label)
        return self.input(width, textvariable, text_input)

    def label(self, text_label):
        label_tk = label(self.canvas, text_label)
        self.labels.append(label_tk)
        return label_tk

    def del_button(self, obj):
        self.buttons[self.buttons.index(obj)].destroy()
        del(self.buttons[self.buttons.index(obj)])

    def del_checkbutton(self, obj):
        self.checkbuttons[self.checkbuttons.index(obj)].destroy()
        del(self.checkbuttons[self.checkbuttons.index(obj)])

    def del_input(self, obj):
        self.inputs[self.inputs.index(obj)].destroy()
        del(self.inputs[self.inputs.index(obj)])

    def del_label(self, obj):
        self.labels[self.labels.index(obj)].destroy()
        del(self.labels[self.labels.index(obj)])

class function_math:
    def __init__(self, a, b=0, c=None):
        self.a = a
        self.b = b
        self.c = c
        if c:
            self.text = "f(x) = " + str(a) + "x²+" + str(b) + "x+" + str(c)
        else:
            self.text = "f(x) = " + str(a) + "x+" + str(b)

    def __str__(self):
        return self.text

    def f(self, value):
        return self.function_lambda()(value)

    def f_get_x(self, value):
        return equation(self.a, self.b, self.c-value)

    def function_lambda(self):
        if self.c:
            return lambda x: (self.a*x**2)+self.b*x+self.c
        else:
            return lambda x: self.a*x+self.b

    def values(self, start=-5, end=5, i=1):
        x = start
        values_list = {}
        while x <= end:
            if self.c:
                f = (self.a*x**2)+self.b*x+self.c
            else:
                f = self.a*x+self.b
            values_list[round(x, -round(math.log(i, 10)))] = f
            x += i
        return values_list

def gcd(n1, n2):
    while n2:
        n1, n2 = n2, n1%n2
    return n1

def input_text(window, text=None, width=20, textvariable=None):
    input_text = Entry(window, text=text, width=width, textvariable=textvariable)
    input_text.pack()
    return input_text

def label(window, text, bg=None):
    label = Label(window, text=text, bg=bg)
    label.pack()
    return label

def logs(logs_file_name, level = logging.INFO, logger_name="logs", formatter="[%(asctime)s] %(message)s", encoding="utf-8", mode="a"):
    formatter = logging.Formatter(formatter)
    handler = logging.FileHandler(logs_file_name, mode=mode, encoding=encoding)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def os_name():
    return os.name

def radiobutton(window, text, value_name=None, command=None):
    global value
    value = StringVar()
    radiobutton = Radiobutton(window, variable=value, text=text, value=value_name, command=command)
    radiobutton.pack()
    return radiobutton

def request(url, params=None):
    try:
        if params != None:
            site = urllib.request(url, urllib.urlencode(params))
        else:
            site = urllib.request(url)
        page1 = urllib.urlopen(site)
        page2 = page1.read()
    except TypeError:
        if params != None:
            site = urllib.request.Request(url, urllib.parse.urlencode(params).encode("utf-8"))
        else:
            site = urllib.request.Request(url)
        page1 = urllib.request.urlopen(site)
        page2 = page1.read().decode("utf-8")
    return page2

def sock(host, port):
    sock = socket.socket()
    sock.connect((host, port))
    return sock

def sock_server(port, host=""):
    sock = socket.socket()
    sock.bind((host, port))
    return sock

def time(f="%Y/%m/%d %H:%M:%S"):
    return datetime.datetime.now().strftime(f)

def time_add(datetime1, d=0, H=0, M=0, S=0):
    return datetime1+datetime.timedelta(days=d, hours=H, minutes=M, seconds=S)

def time_add_now(d=0, H=0, M=0, S=0):
    return datetime.datetime.now()+datetime.timedelta(days=d, hours=H, minutes=M, seconds=S)

def time_delta(datetime1, datetime2):
    return datetime2-datetime1

def time_delta_days(datetime1, datetime2):
    return time_delta(datetime1, datetime2).days

def time_delta_seconds(datetime1, datetime2):
    return time_delta(datetime1, datetime2).total_seconds()

def time_str_add(str_datetime1, d=0, H=0, M=0, S=0, f="%Y/%m/%d %H:%M:%S"):
    return time_strf(time_strp(str_datetime1, f)+datetime.timedelta(days=d, hours=H, minutes=M, seconds=S), f)

def time_str_add_now(d=0, H=0, M=0, S=0, f="%Y/%m/%d %H:%M:%S"):
    return time_strf(time_add_now(d, H, M, S), f)

def time_str_delta(str_datetime1, str_datetime2, f="%Y/%m/%d %H:%M:%S"):
    return time_strp(str_datetime2, f)-time_strp(str_datetime1, f)

def time_str_delta_days(str_datetime1, str_datetime2, f="%Y/%m/%d %H:%M:%S"):
    return time_delta(time_strp(str_datetime1, f), time_strp(str_datetime2, f)).days

def time_str_delta_seconds(str_datetime1, str_datetime2, f="%Y/%m/%d %H:%M:%S"):
    return time_delta(time_strp(str_datetime1, f), time_strp(str_datetime2, f)).total_seconds()

def time_strf(datetime1, f="%Y/%m/%d %H:%M:%S"):
    return datetime.datetime.strftime(datetime1, f)

def time_strp(str_datetime1, f="%Y/%m/%d %H:%M:%S"):
    return datetime.datetime.strptime(str_datetime1, f)

#KindleTune
def trx(value, array):
    best = array[0]
    for check in array:
        if abs(value - check) <= abs(value - best):
            best = check
    return best

def web_server(path=["."], port=80, host=""):
    try:
        http_server = BaseHTTPServer
        handler = CGIHTTPServer.CGIHTTPRequestHandler
    except NameError:
        http_server = http.server
        handler = http_server.CGIHTTPRequestHandler
    handler.cgi_directories = path
    return http_server.HTTPServer((host, port), handler)
