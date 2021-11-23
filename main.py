import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
from tkinter import messagebox
import random as rd
import pyperclip
import json

# Colours
BLUE = '#396EB0'
DARK_BLUE = '#2E4C6D'
SKIN = '#FC997C'
WHITE = '#DADDFC'


# ---------------------------- SEARCH  ------------------------------- #
def search():
    try:
        with open('data.json', 'r') as filehandle:
            data = json.load(filehandle)
            text = data[website_entry.get()]
            messagebox.showinfo(title='PASSWORD', message=f"Email Id : {text['email']}\nPassword : {text['password']}")
    except:
        messagebox.showerror(title='ERROR', message='File Does Not Exist!')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_gene():
    password_entry.delete(first=0, last='end')
    # Creating a pw out of random characters of length 12 characters
    generated_pw = ''.join([chr(rd.randint(33, 125)) for i in range(12)])
    pyperclip.copy(generated_pw)
    # Printing the password
    password_entry.insert(index=0, string=generated_pw)


# ---------------------------- SAVE PASSWORD ------------------------------- #

# Initializing the variables for data entry
website, email, password = str(), 'sample@gmail.com', str()


def save():
    # Checking if user has entered the data in proper format
    if len(email_entry.get()) == 0 or len(password_entry.get()) == 0 or len(website_entry.get()) == 0:
        messagebox.showerror(title='Warning!', message="Don't leave any fields empty!")
    else:
        # User Crosscheck
        check = messagebox.askyesno(title='Confirmation',
                                    message=f' Website : {website_entry.get()} \n Email : {email_entry.get()}\n Password : {password_entry.get()}')
        if check:
            # To save data
            global website, email, password
            website = website_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            save_data(website, email, password)
            new_data = {website: {'email': email, 'password': password, }}
            # To prevent the error in the first save
            try:
                with open('data.json', 'r') as file:
                    # Reading old data
                    file_temp = json.load(file)
                    file_temp.update(new_data)

                with open('data.json', 'w') as file:
                    # dumping new data
                    messagebox.showinfo(title='Saved!', message='Successfully Saved The Password!')
                    json.dump(file_temp, file, indent=4)
            except:
                with open('data.json', 'w') as file:
                    # creating + dumping new data
                    messagebox.showinfo(title='Saved!', message='Successfully Saved The Password!')
                    json.dump(new_data, file, indent=4)


            finally:
                # To remove the entered choices
                website_entry.delete(first=0, last=tk.END)
                password_entry.delete(first=0, last=tk.END)


def save_data(website, email, password):
    # Data entry in the CSV file
    temp_data = pd.DataFrame({'Email': [email], 'Website': [website], 'Password': [password]})
    temp_data.to_csv('storage.csv', mode='a+', header=False, index=False)


# ---------------------------- UI SETUP ------------------------------- #


root = tk.Tk()
root.title('Password Manager')
root.minsize(height=400, width=500)
root.config(bg=WHITE)
# Background logo
canvas = tk.Canvas(master=root, width=200, height=200, bg=WHITE, highlightthickness=0)
img = ImageTk.PhotoImage(Image.open('abc.png'))  # Logo credits goes to  : kmg design
canvas.create_image(85, 110, image=img)
canvas.grid(row=1, column=2)

# Website label
website_label = tk.Label(master=root, text='Website:', bg=WHITE, fg=DARK_BLUE, font=("bold"))
website_label.grid(row=2, column=1)
# Website entry
website_entry = tk.Entry(master=root, width=40)
website_entry.grid(row=2, column=2, columnspan=1)

# Email label
email_label = tk.Label(master=root, text='Email/Username: ', bg=WHITE, fg=DARK_BLUE, font=("bold"))
email_label.grid(row=3, column=1)
# Email entry
email_entry = tk.Entry(master=root, width=40)
email_entry.grid(row=3, column=2, columnspan=1, sticky='w')
email_entry.insert(index=0, string='sample@gmail.com')

# Password label
password_label = tk.Label(master=root, text='Password:', bg=WHITE, fg=DARK_BLUE, font=("bold"))
password_label.grid(row=4, column=1)
# Password entry
password_entry = tk.Entry(master=root, width=30)
password_entry.grid(row=4, column=2, sticky='w')

# Password Generator
password_generator = tk.Button(master=root, text='Generator', command=lambda: password_gene(), width=10,
                               relief='groove', activebackground=SKIN, bg=DARK_BLUE, fg=WHITE)
password_generator.grid(row=4, column=2, sticky='e')

# Space b'w passwords and save button
space = tk.Label(master=root, text='', bg=WHITE)
space.grid(row=5, column=2)

# Save button
save_button = tk.Button(master=root, text='Save', command=save, width=15,
                        relief='groove', activebackground=SKIN, bg=DARK_BLUE, fg=WHITE)
save_button.grid(row=6, column=2)

# Space b'w passwords and save button
space2 = tk.Label(master=root, text='', bg=WHITE)
space2.grid(row=7, column=2)

# Search button
search_button = tk.Button(master=root, text='Search', width=10, relief='groove', activebackground=SKIN, bg=DARK_BLUE,
                          fg=WHITE, command=search)
search_button.grid(row=2, column=2, sticky='e')

root.mainloop()
