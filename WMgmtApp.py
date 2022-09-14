#   import necessary packages
import sys
import tkinter as tk
from tkinter import font as tkfont, CENTER, messagebox
from tkinter.constants import BOTTOM
from tkinter.ttk import *
from tkinter import IntVar
import csv
import datetime
import smtplib
from email.message import EmailMessage

# declare global constants and variables
PERISHABLE_OPTIONS = ['Vegetables', 'Fruits', 'Bread', 'Dairy', 'Meat', 'Other']
NONPERISHABLE_OPTIONS = ['Books', 'Clothes', 'Dry Food', 'Household', 'Sanitary', 'Other']
form_items = {'radio': "", 'checkbutton': [], 'comment': "", 'name': "", 'street': "", 'city': "", 'state': "",
              'zip': "", 'phone': "", 'email': "", 'time_stamp': ""}
filename = 'donation_list.csv'


#   Controller frame class of the main app
class WMgmtApp(tk.Tk):

    def __init__(self):
        """

            Initiates the main app window

        """

        #   initialising the tkinter class and setting the main window and fonts
        tk.Tk.__init__(self)
        self.f = None
        self.title = self.title("Waste Management")
        self.title_font = tkfont.Font(family='Calibri', size=18, weight="bold", slant="italic")
        self.geometry("1000x1000")
        self.container = tk.Frame(self, bg="black")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        #   setting frames for each page
        for F in (WelcomePage, FormInput, ContactInfo):
            __page_name = F.__name__
            frame = F(controller=self)
            self.frames[__page_name] = frame

            # puts all the pages in the same location
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        """

            :param page_name: Name of the page
            :return: Returns the appropriate frame based on button clicks
            Show a frame for the given page name

        """

        frame = self.frames[page_name]
        frame.tkraise()

    def load_in_file(self):
        """

            Loads all donation items and contact info into file

        """

        form_items['time_stamp'] = str(datetime.datetime.now())
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)

            # writing fields
            csvwriter.writerow(list(form_items.values()))

    def info_validation(self):
        """

            Shows an error box every time a form is submitted without filling out necessary info

        """

        messagebox.showerror("Error!", "Fill out the fields marked with asterisk.")

    def close_program(self):
        """

            Exits program

        """
        self.destroy()

    def read_last_entry(self):
        """

            :return: Returns the most recent entry in file
            Shows the latest entry in file to assert that data has been loaded into csv file.

        """

        try:
            self.f = open(filename, 'rb')
        except IOError:
            print("File I/O error! Check for file in your directory:", filename)
            self.close_program()
        with self.f:
            recent_entry = self.f.readlines()[-1].strip()
        return recent_entry

    def __printdonation(self):
        """

            :return: Returns user's name and what they donated.

        """

        return f"{form_items['name']} has donated {form_items['checkbutton']} ({form_items['comment']})."

    def call_private_print_donation(self):
        """

            :return: Calls function to return current user's name and donation items

        """

        return self.__printdonation()

    def __repr__(self):
        """

            :return: Returns object representation of all frames
            repr function of class

        """
        return f"These are the object representations for all the pages/frames: {self.frames}"


#   Class for the first page shown whe program runs
class WelcomePage(tk.Frame):

    def __init__(self, controller):
        """

            :param controller: main window

        """

        #   initialises Tkinter's frame
        tk.Frame.__init__(self)
        self.controller = controller

        #   declaring and configuring widgets of the page: Label, and 2 buttons
        label = Label(self, text="Welcome!", font='Calibri 24 bold italic')
        label.place(relx=0.5, rely=0.35, anchor=CENTER)
        donate_button = Button(self, text="Click to Donate!",
                               command=lambda: controller.show_frame("FormInput"))
        donate_button.place(relx=0.5, rely=0.4, anchor=CENTER)
        exit_button = Button(self, text="Exit", command=lambda: controller.close_program())
        exit_button.place(relx=0.5, rely=0.45, anchor=CENTER)


#   Class for donation item selection page
class FormInput(tk.Frame):
    def __init__(self, controller):
        """

            :param controller: main window

        """

        #   initialising Tkinter's Frame class
        tk.Frame.__init__(self)

        #   attributes to store checkbutton and radiobutton selections
        self.__checkbutton_list = []
        self.options_variables = {}
        self.controller = controller

        #   widgets for the page
        label = Label(self, text="Choose your donations! *", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        style = Style(self)
        style.configure("TRadiobutton", font=("Calibri", 18))

        #   Shows checkboxes based on selection of radiobutton
        self.category_of_donation = {"Other": '0', "Perishable": '1', "Non-Perishable": '2'}
        self.var = tk.StringVar(None, '0')
        for text, value in self.category_of_donation.items():
            r = Radiobutton(self, text=text, variable=self.var, value=value, command=self.show_checkbox)
            r.pack(anchor=CENTER, padx=5, pady=5)
        self.comment = tk.StringVar()
        comment_title = Label(self, text="Comment (if any)", font=controller.title_font)
        comment_title.pack(side="left", fill="x", pady=250)
        self.comment_textbox = tk.Text(self, height=8, width=75)
        self.comment_textbox.pack(anchor="w", padx=30, pady=30, side="left", expand=True)
        self.submit_button = tk.Button(self, text="Submit",
                                       command=lambda: [controller.show_frame("ContactInfo"),
                                                        self.__get_comment()],
                                       height=2, width=20)
        self.submit_button.pack(anchor="w", padx=30, pady=30, side=BOTTOM)

    def show_checkbox(self):
        """

            :return: Returns checkbuttons based on radiobutton selections

        """
        form_items['checkbutton'].clear()
        while self.__checkbutton_list:
            self.__checkbutton_list.pop().destroy()
        form_items['radio'] = self.var.get()
        if self.var.get() == '0':
            options = []
        elif self.var.get() == '1':
            options = PERISHABLE_OPTIONS
        else:
            options = NONPERISHABLE_OPTIONS

        self.options_variables = {}  # dictionary for the variables

        for j in options:
            i = IntVar()
            self.options_variables[j] = i
            c = Checkbutton(self, text=j, variable=i, command=self.checkbox_selections)
            c.pack(anchor="center", padx=5, pady=5)
            self.__checkbutton_list.append(c)

    def checkbox_selections(self):
        """

            Stores checkbutton selections within the form item dictionary

        """
        for name, variable in self.options_variables.items():
            if variable.get() == 1:
                if name not in form_items['checkbutton']:
                    form_items['checkbutton'].append(name)
            else:
                if name in form_items['checkbutton']:
                    form_items['checkbutton'].remove(name)

    def __get_comment(self):
        """

            Gets comment box value from user's input when user clicks on Submit button

        """
        form_items['comment'] = self.comment_textbox.get("1.0", "end").strip()


#   Class for page that shows contact information form
class ContactInfo(tk.Frame):
    def __init__(self, controller):
        """

            :param controller: main window

        """

        #   initialising Tkinter's Frame class
        tk.Frame.__init__(self)

        #   declaring attributes for emailing
        self.__sender_password = "waste321#"
        self.__sender_email = "thewastemanagementteam@gmail.com"
        self.receiver_email = ""
        self.controller = controller

        #   widget declaration and configuration
        contact_info = Label(self, text="Contact Information\n(Enter all fields marked with asterisk and Validate)",
                             font=controller.title_font)
        name = Label(self, text="Name", font=("Calibri", 12))
        street = Label(self, text="Street *", font=("Calibri", 12))
        city = Label(self, text="City *", font=("Calibri", 12))
        state = Label(self, text="State (2 Letter) *", font=("Calibri", 12))
        zip_code = Label(self, text="ZIP Code *", font=("Calibri", 12))
        phone_number = Label(self, text="Phone Number (Enter digits only!)", font=("Calibri", 12))
        email_address = Label(self, text="Email Address *", font=("Calibri", 12))

        contact_info.grid(row=0, column=1)
        name.grid(row=20, column=0)
        street.grid(row=40, column=0)
        city.grid(row=60, column=0)
        state.grid(row=80, column=0)
        zip_code.grid(row=100, column=0)
        phone_number.grid(row=120, column=0)
        email_address.grid(row=140, column=0)

        self.name_field = Entry(self, font=("Calibri", 18))
        self.street_field = Entry(self, font=("Calibri", 18))
        self.city_field = Entry(self, font=("Calibri", 18))
        self.state_field = Entry(self, font=("Calibri", 18))
        self.zip_code_field = Entry(self, font=("Calibri", 18))
        self.phone_number_field = Entry(self, font=("Calibri", 18))
        self.email_address_field = Entry(self, font=("Calibri", 18))

        self.name_field.grid(row=20, column=1, ipadx="100", ipady="20")
        self.street_field.grid(row=40, column=1, ipadx="100", ipady="20")
        self.city_field.grid(row=60, column=1, ipadx="100", ipady="20")
        self.state_field.grid(row=80, column=1, ipadx="100", ipady="20")
        self.zip_code_field.grid(row=100, column=1, ipadx="100", ipady="20")
        self.phone_number_field.grid(row=120, column=1, ipadx="100", ipady="20")
        self.email_address_field.grid(row=140, column=1, ipadx="100", ipady="20")
        validate_button = Button(self, text="Validate", command=lambda: self.insert_contact_info(self.controller))
        validate_button.grid(row=480, column=100)
        self.home_button = Button(self, text="Submit & Exit", command=lambda: [controller.show_frame("WelcomePage"),
                                                                               controller.load_in_file(),
                                                                               self.send_email(),
                                                                               controller.close_program()],
                                  state='disabled')
        self.home_button.grid(row=500, column=100)

    def insert_contact_info(self, ctrl):
        """

            :param ctrl: main window
            inserts values from user's inputs in the form items dictionary

        """

        form_items['name'] = self.name_field.get()
        form_items['street'] = self.street_field.get()
        form_items['city'] = self.city_field.get()
        form_items['state'] = self.state_field.get()
        form_items['zip'] = self.zip_code_field.get()
        form_items['phone'] = self.phone_number_field.get()
        form_items['email'] = self.email_address_field.get()

        #   Validates user's inputs to make sure all required fields have been populated
        if form_items['street'] == "":
            ctrl.info_validation()
        elif form_items['city'] == "":
            ctrl.info_validation()
        elif form_items['state'] == "":
            ctrl.info_validation()
        elif form_items['zip'] == "":
            ctrl.info_validation()
        elif form_items['email'] == "":
            ctrl.info_validation()

        #   Enables submit button if all fiekds are satisfied
        else:
            self.home_button.config(state='normal')
            Label(self, text="Your entry has been validated!\nPlease click on Submit & Exit!",
                  font=("Calibri", 12)).grid(row=520, column=100)

    def send_email(self):
        """

            :return: Sends an email to user in the email address from user's input based on the clicking of the
            Submit button
            Sends email to user based on wich items users have decided to donate

        """

        #   storing different parts of the email in a dictionary
        message_dictionary = EmailMessage()
        message_dictionary['Subject'] = "Donation Received"
        message_dictionary['From'] = self.__sender_email
        message_dictionary['To'] = form_items['email']
        if form_items['radio'] == '1':
            message_dictionary.set_content("Hello,\n\nWe have received your donation request. Our trucks pick up "
                                           "perishable items everyday at 6am. Please keep your items in front of your "
                                           "doorstep accordingly.\n\nThank you for the donation!\n\nThe Waste "
                                           "Management Team")
        elif form_items['radio'] == '2':
            message_dictionary.set_content("Hello,\n\nWe have received your donation request. Our trucks pick up "
                                           "non-perishable items every Friday at 12pm. Please keep your items in front "
                                           "of your doorstep accordingly.\n\nThank you for the donation!\n\nThe Waste "
                                           "Management Team")
        else:
            message_dictionary.set_content("Hello,\n\nWe have received your donation request. Our trucks pick up "
                                           "perishable items everyday at 6am and non-perishable items every Friday at "
                                           "12pm. Please keep your items in front of your doorstep accordingly."
                                           "\n\nThank you for the donation!\n\nThe Waste Management Team")

        #   Calls method to establish a connection with the smtp port
        server, success_message = self.establish_connection()
        try:
            server.send_message(message_dictionary)
        except smtplib.SMTPRecipientsRefused:
            self.email_validate()
        else:
            print("Email sent")

    def email_validate(self):
        messagebox.showerror("Error!", "Email not found.\nYour entry was not saved.")
        sys.exit("Email invalid!")

    def establish_connection(self):
        """

            :return: Returns SMTP type object and successful connection message

        """
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()

        #   Call method to log in to sender's email
        conn_msg = self.__test_connection(s, self.__sender_email, self.__sender_password)
        return s, conn_msg

    def __test_connection(self, svr, s_email, s_pwd):
        """

            :param svr: SMTP type object
            :param s_email: sender's email
            :param s_pwd: sender's password
            :return: Successful message
            Logs in to sender's email

        """

        svr.login(s_email, s_pwd)
        return "Login successful"

    def __repr__(self):
        """

            :return: Sender's email

        """
        return f"This is the sender's email: {self.__sender_email}"


if __name__ == "__main__":

    #   Object declaration
    app = WMgmtApp()
    form_input = FormInput(app)
    contact_info_page = ContactInfo(app)

    #   starts the app
    app.mainloop()

    #   Catches error for when program ends prematurely
    try:
        minute = int(form_items['time_stamp'][14:16])
    except ValueError:
        sys.exit("Program exited prematurely!")

    #   Checks current time with last entry in file to assert that file has been appended with most recent input
    assert (datetime.datetime.now().strftime('%H:%M') == form_items['time_stamp'][11:16]) \
           or (datetime.datetime.now().strftime('%H:%M') ==
               f"{form_items['time_stamp'][11:13]}:{minute + 1})",
               f"{datetime.datetime.now().strftime('%H:%M')}, {form_items['time_stamp'][11:16]}"), "Data did not enter!"

    #   Asserts successful connection
    server_test, test_connection_msg = contact_info_page.establish_connection()
    assert test_connection_msg != "", "Connection was not successful"

    #   Prints certain verification items onto console
    print(app.__repr__())
    print(test_connection_msg)
    print(app.read_last_entry())
    print(app.call_private_print_donation())
    print(contact_info_page.__repr__())
