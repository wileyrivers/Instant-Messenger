from tkinter import *
from tkinter import ttk
import tkinter as tk
from pyrebase import *
import datetime
import pdb

config = {
    "apiKey": "AIzaSyB3ykqcbTvipWwYNzGNygc5jSANxAKjKSc",
    "authDomain": "fir-test-52cba.firebaseapp.com",
    "databaseURL": "https://fir-test-52cba.firebaseio.com",
    "storageBucket": "fir-test-52cba.appspot.com",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
user = None
log_time = None
font_change = None
textbox = ""
user_change = []
user_access = None


def send_message(*args):
    # noinspection PyBroadException
    if t2.get('1.0', 'end').strip() == '':
        return
    try:
        day_tag = str(datetime.datetime.today())[:10:]
        message_text = t2.get('1.0', 'end').strip()
        message = {"message": message_text, "time": str(datetime.datetime.today()), "username": username.get()}
        db.child("Messages").child(day_tag).push(message)
        t2.delete('1.0', 'end')
    except:
        print("Error sending messages")


def update_messages(*args):
    global log_time, textbox, user_access
    # noinspection PyBroadException
    try:
        day_tag = str(datetime.datetime.today())[:10:]
        messages = db.child("Messages").child(day_tag).get()
        for message in messages:
            date_time_str = message.val()['time']
            message_date = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
            text = ("\n" + message.val()["message"] + '\n\n' + message.val()["username"] + " | "
                    + message.val()["time"][11:20] + "\n--------------------------------------"
                                                     "---------------------------------")
            if text not in textbox:
                textbox = textbox + text
                t1['state'] = 'normal'
                t1.insert("end -1 chars", "\n" + text)
                t1['state'] = 'disabled'
                t1.see('end')
            else:
                continue
        # t1['state'] = 'normal'
        # t1.insert("end -1 chars", "\n" + text_add)
        # t1['state'] = 'disabled'
    except:
        print("Error retrieving messages")
    else:
        root.after(500, update_messages)


def confirm_name_change(*args):
    global user_change, user_access
    info = {"username": username.get()}
    db.child('userdata').child(user_access).update(info)
    day_tag = str(datetime.datetime.today())[:10:]
    message = {"message": "Introducing... " + username.get(), "time": str(datetime.datetime.today()), "username": "SYSTEM"}
    db.child("Messages").child(day_tag).push(message)
    root.forget(user_change)
    root.grab_set()
    root.lift()


def change_username(*args):
    global user_change
    user_change = Toplevel()
    user_change.title("Change Username")
    user_change.geometry('-680+300')
    user_change.grab_set()
    user_change.lift(root)
    name_frame = ttk.Frame(user_change, padding='20')
    new_name_label = ttk.Label(name_frame, text="New Username:")
    new_name_entry = ttk.Entry(name_frame, textvariable=username)
    new_name_button = ttk.Button(name_frame, text="Submit", command=confirm_name_change)
    name_frame.grid(column=0, row=0, sticky=(N, S, E, W))
    new_name_label.grid(column=0, row=0, sticky=(W, E))
    new_name_entry.grid(column=1, row=0, sticky=(W, E))
    new_name_button.grid(column=1, row=1, columnspan=2, sticky=(W, E))
    user_change.bind('<Return>', confirm_name_change)


def change_font(*args):

    def confirm_font_change(*args):
        global user_access
        bold_italic_option = ""
        if bold.get() == 1:
            bold_italic_option = "bold"
        if italic.get() == 1 and len(bold_italic_option) > 0:
            bold_italic_option = bold_italic_option + " italic"
        if italic.get() == 1 and len(bold_italic_option) == 0:
            bold_italic_option = "italic"

        info = {"font": (font_name_selector.get(ACTIVE), font_size_selector.get(ACTIVE), bold_italic_option)}
        db.child('userdata').child(user_access).update(info)
        t1.configure(font=(font_name_selector.get(ACTIVE), font_size_selector.get(ACTIVE), bold_italic_option))
        root.forget(font_change)
        root.grab_set()
        root.lift()

    global font_change
    font_list = [
        'Times New Roman',
        'Arial',
        'Symbol',
        'Courier'
    ]
    font_sizes = [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18
    ]
    font_sizes = StringVar(value=font_sizes)
    font_list = StringVar(value=font_list)

    font_change = Toplevel()
    font_change.title("Change Font")
    font_change.geometry('-680+300')
    font_change.grab_set()
    font_change.lift(root)

    font_frame = ttk.Frame(font_change, padding='20')
    font_name_label = ttk.Label(font_frame, text='Font name:')
    font_name_selector = tk.Listbox(font_frame, exportselection=False,
                                    listvariable=font_list, height=5)
    font_size_label = ttk.Label(font_frame, text='Font size:')
    font_size_selector = tk.Listbox(font_frame, exportselection=False,
                                    listvariable=font_sizes, height=5)
    font_confirm_button = ttk.Button(font_frame, text="Submit", command=confirm_font_change)
    font_bold_check = ttk.Checkbutton(font_frame, text='Bold', variable=bold)
    font_italic_check = ttk.Checkbutton(font_frame, text='Italic', variable=italic)

    font_frame.grid(column=0, row=0, sticky=(N, S, E, W))
    font_name_label.grid(column=0, row=0, sticky=(E, W))
    font_name_selector.grid(column=1, row=0, sticky=(E, W))
    font_size_label.grid(column=2, row=0, sticky=(E, W))
    font_size_selector.grid(column=3, row=0, sticky=(E, W))
    font_confirm_button.grid(row=1, column=2, columnspan=2)
    font_bold_check.grid(row=1, column=2)
    font_italic_check.grid(row=3, column=2)


def change_text_color(*args):

    def confirm_text_color(*args):
        global user_access
        t1.configure(foreground=t1_listbox.get(ACTIVE))
        t2.configure(foreground=t2_listbox.get(ACTIVE))
        info = {"f1_color": t1_listbox.get(ACTIVE), "f2_color": t2_listbox.get(ACTIVE)}
        db.child("userdata").child(user_access).update(info)
        root.forget(font_color)
        root.grab_set()
        root.lift()


    color_list = [
        'Red',
        'Blue',
        'Green',
        'Black',
        'White',
        'Grey',
        'Yellow',
        'Purple',
        'Pink',
    ]
    color_list = StringVar(value=color_list)

    font_color = Toplevel()
    font_color.title("Change Font Color")
    font_color.geometry('-680+300')
    font_color.grab_set()
    font_color.lift(root)

    color_frame = ttk.Frame(font_color, padding='20')
    color_label = ttk.Label(color_frame, text='Choose a color:')
    t1_label = ttk.Label(color_frame, text='Top Text Box')
    t2_label = ttk.Label(color_frame, text='Bottom Text Box')
    t1_listbox = tk.Listbox(color_frame, exportselection=False, listvariable=color_list)
    t2_listbox = tk.Listbox(color_frame, exportselection=False, listvariable=color_list)
    submit_button = ttk.Button(color_frame, text='Submit', command=confirm_text_color)

    color_frame.grid(column=0, row=0, sticky=(N,S,E,W))
    color_label.grid(column=0, row=1, sticky=(E,W))
    t1_label.grid(column=1, row=0, sticky=(E,W))
    t2_label.grid(column=2, row=0, sticky=(E,W))
    t1_listbox.grid(column=1, row=1, sticky=(N,S,E,W))
    t2_listbox.grid(column=2, row=1, sticky=(N,S,E,W))
    submit_button.grid(column=1, row=2, sticky=(N,S,E,W))


def change_box_color(*args):

    def confirm_box_color(*args):
        global user_access
        t1.configure(background=b1_listbox.get(ACTIVE))
        t2.configure(background=b2_listbox.get(ACTIVE))
        info = {"b1_color": b1_listbox.get(ACTIVE), "b2_color": b2_listbox.get(ACTIVE)}
        db.child("userdata").child(user_access).update(info)
        root.forget(font_color)
        root.grab_set()
        root.lift()

    color_list = [
        'Red',
        'Blue',
        'Green',
        'Black',
        'White',
        'Grey',
        'Yellow',
        'Purple',
        'Pink',
    ]
    color_list = StringVar(value=color_list)

    font_color = Toplevel()
    font_color.title("Change Text Box Color")
    font_color.geometry('-680+300')
    font_color.grab_set()
    font_color.lift(root)

    color_frame = ttk.Frame(font_color, padding='20')
    color_label = ttk.Label(color_frame, text='Choose a color:')
    b1_label = ttk.Label(color_frame, text='Top Text Box')
    b2_label = ttk.Label(color_frame, text='Bottom Text Box')
    b1_listbox = tk.Listbox(color_frame, exportselection=False, listvariable=color_list)
    b2_listbox = tk.Listbox(color_frame, exportselection=False, listvariable=color_list)
    submit_button = ttk.Button(color_frame, text='Submit', command=confirm_box_color)

    color_frame.grid(column=0, row=0, sticky=(N,S,E,W))
    color_label.grid(column=0, row=1, sticky=(E,W))
    b1_label.grid(column=1, row=0, sticky=(E,W))
    b2_label.grid(column=2, row=0, sticky=(E,W))
    b1_listbox.grid(column=1, row=1, sticky=(N,S,E,W))
    b2_listbox.grid(column=2, row=1, sticky=(N,S,E,W))
    submit_button.grid(column=1, row=2, sticky=(N,S,E,W))


def log_in(*args):

    def login_func(*args):
        global user, user_access
        global log_time
        try:
            user = auth.sign_in_with_email_and_password((email.get()).lower(), password.get())
        except:
            ttk.Label(login, text="CREDENTIALS INCORRECT").grid(column=0, row=0, sticky=N, columnspan=2)
        else:
            log_time = datetime.datetime.today()
            username.set(email.get())
            user_access = re.sub('\.|\@', '', (username.get()).lower())
            try:
                info = db.child("userdata").child(user_access).get()
                # pdb.set_trace()
                t1.configure(font=(info.val()['font']), foreground=info.val()['f1_color'],
                             background=info.val()['b1_color'])
                t2.configure(foreground=info.val()['f2_color'], background=info.val()['b2_color'])
                username.set(info.val()['username'])
            except TypeError or KeyError:
                info = {"username": username.get(), "font": ('Times New Roman', 12, 'bold'),
                        "background": 'pink', "f2_color": "Black", "f1_color": "Black", "b2_color": "Grey",
                        "b1_color": "Grey"}
                db.child("userdata").child(user_access).set(info)
            finally:
                day_tag = str(datetime.datetime.today())[:10:]
                message = {"message": "Welcome, " + username.get(), "time": str(datetime.datetime.today()),
                           "username": "SYSTEM"}
                db.child("Messages").child(day_tag).push(message)
                root.forget(login)
                root.grab_set()
                root.lift()
                update_messages()

    login = Toplevel()
    login.title("A&W Login")
    login.geometry('-680+300')
    login.grab_set()
    login.lift(root)
    login.bind('<Return>', login_func)

    email = StringVar()
    password = StringVar()

    log_frame = ttk.Frame(login, padding="20")
    log_label = ttk.Label(log_frame, text="Email:")
    log_label2 = ttk.Label(log_frame, text="Password:")
    email_entry = ttk.Entry(log_frame, textvariable=email)
    pass_entry = ttk.Entry(log_frame, textvariable=password)
    login_button = ttk.Button(log_frame, text="Login", command=login_func)

    log_frame.grid(column=0, row=0, sticky=(N, S, E, W), padx=3, pady=3)
    log_label.grid(column=0, row=0, sticky=(N, W), padx=5, pady=5)
    log_label2.grid(column=0, row=1, sticky=W, padx=5, pady=5)
    email_entry.grid(column=1, row=0, sticky=(N, E), padx=5, pady=5)
    pass_entry.grid(column=1, row=1, sticky=E, padx=5, pady=5)
    login_button.grid(column=0, row=2, sticky=(S, E, W), columnspan=2)



root = Tk()
root.title("A&W Messenger")
root.geometry('400x500-670+290')
root.minsize(400, 500)
log_in()

text_body = StringVar()
username = StringVar()
bold = IntVar()
italic = IntVar()

mainframe = ttk.Frame(root, padding="5", borderwidth=5, relief='solid')
t1 = Text(mainframe, height=20, state='disabled', background='pink')
t1.configure(font=("Times New Roman", 12))
t2 = Text(mainframe, height=6)
send_button = ttk.Button(mainframe, text="Send", command=send_message)
s = ttk.Scrollbar(mainframe, orient=VERTICAL, command=Text.yview(t1))
t1.configure(yscrollcommand=s.set)

root.option_add('*tearOff', FALSE)
main_menu = tk.Menu(root)
root['menu'] = main_menu
menu_file = Menu(main_menu)
menu_edit = Menu(main_menu)
main_menu.add_cascade(menu=menu_file, label='File')
main_menu.add_cascade(menu=menu_edit, label='Style')

menu_font_color = Menu(main_menu)
menu_background = Menu(main_menu)

menu_edit.add_command(label='Change Text Color', command=change_text_color)
menu_edit.add_command(label='Change Font', command=change_font)
menu_edit.add_command(label='Change Background', command=change_box_color)

menu_file.add_command(label='Change Username', command=change_username)
menu_file.add_command(label='Logout', command=log_in)
menu_file.add_command(label='Exit', command=root.destroy)

mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
t1.grid(column=0, row=0, sticky=(N, S, E, W), pady=5)
t2.grid(column=0, row=1, columnspan=2, sticky=(N, S, E, W))
send_button.grid(column=0, row=2, sticky=(S, E))
s.grid(column=1, row=0, sticky=(N,S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)

t2.bind('<Return>', send_message)
root.mainloop()
