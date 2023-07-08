from __future__ import print_function
from tkinter import *
import utils
from client import Client

logger = utils.setup_logger("status.log")


class ZapperGUI:
    def __init__(self, filter_addresses, search_query):
        self.client = Client()
        self.emails = self.client.fetch_emails(filter_addresses, search_query)
        self.email_ids = [email['id'] for email in self.emails]
        self.current_email_index = 0

        self.window = Tk()
        self.window.title("Gmail Zapper!")

        self.email_label = Label(self.window, text="Email", font=("Helvetica", 16, "bold"))
        self.email_label.pack(pady=10)

        self.sender_label = Label(self.window, text="", font=("Helvetica", 12, "bold"))
        self.sender_label.pack()

        self.date_label = Label(self.window, text="", font=("Helvetica", 12))
        self.date_label.pack()

        self.subject_label = Label(self.window, text="", font=("Helvetica", 12, "bold"))
        self.subject_label.pack()

        self.body_label = Label(self.window, text="Body", font=("Helvetica", 14, "bold"))
        self.body_label.pack()

        self.body_text = Text(self.window, width=80, height=20)
        self.body_text.pack()

        self.previous_button = Button(self.window, text="Previous",
                                      command=self.show_previous_email,
                                      state=DISABLED)
        self.previous_button.pack(pady=10)

        self.next_button = Button(self.window, text="Next",
                                  command=self.show_next_email)
        self.next_button.pack(pady=10)

        self.show_current_email()

        self.window.mainloop()

    def show_current_email(self):
        if self.current_email_index < len(self.email_ids):
            email_id = self.email_ids[self.current_email_index]
            message = self.client.service.users().messages().get(userId='me', id=email_id, format='full').execute()
            payload = message['payload']
            body = utils.get_email_body(payload)
            headers = message['payload']['headers']

            sender = ""
            date = ""
            subject = ""

            for header in headers:
                name = header['name']
                value = header['value']
                if name == 'From':
                    sender = value
                elif name == 'Date':
                    date = value
                elif name == 'Subject':
                    subject = value

            self.sender_label.configure(text=f"From: {sender}")
            self.date_label.configure(text=f"Date: {date}")
            self.subject_label.configure(text=f"Subject: {subject}")
            self.body_text.delete(1.0, END)
            self.body_text.insert(END, body)

            # Enable/Disable Previous button
            if self.current_email_index == 0:
                self.previous_button.configure(state=DISABLED)
            else:
                self.previous_button.configure(state=NORMAL)

            # Enable/Disable Next button
            if self.current_email_index == len(self.email_ids):
                self.next_button.configure(state=DISABLED)
            else:
                self.next_button.configure(state=NORMAL)
        else:
            self.sender_label.configure(text="")
            self.date_label.configure(text="")
            self.subject_label.configure(text="")
            self.body_text.delete(1.0, END)
            self.body_text.insert(END, "No more emails to display.")
            # Disable Next button
            self.next_button.configure(state=DISABLED)

    def show_next_email(self):
        self.current_email_index += 1
        self.show_current_email()

    def show_previous_email(self):
        self.current_email_index -= 1
        self.show_current_email()


if __name__ == '__main__':
    FILTER_FROM_ADDRESSES = ['support@keychron.de']  # List of sender addresses to filter
    SEARCH_QUERY = ''  # Search query for email title and body
    ZapperGUI(FILTER_FROM_ADDRESSES, SEARCH_QUERY)
