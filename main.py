from tkinter import Tk, Label, Text, Button, Entry
import utils
from client import Client

logger = utils.setup_logger("status.log")


class EmailViewerGUI:
    def __init__(self, filter_addresses, search_query):
        self.client = Client()
        self.emails = self.client.fetch_emails(filter_addresses, search_query)
        self.email_ids = [email['id'] for email in self.emails]
        self.current_email_index = 0

        self.window = Tk()
        self.window.title("Email Viewer")

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

        self.previous_button = Button(self.window, text="Previous", command=self.show_previous_email, state="disabled")
        self.previous_button.pack(pady=10)

        self.next_button = Button(self.window, text="Next", command=self.show_next_email)
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
            self.body_text.delete(1.0, "end")
            self.body_text.insert("end", body)

            # Enable/Disable previous button
            if self.current_email_index > 0:
                self.previous_button.configure(state="normal")
            else:
                self.previous_button.configure(state="disabled")

            # Enable/Disable next button
            if self.current_email_index < len(self.email_ids):
                self.next_button.configure(state="normal")
            else:
                self.next_button.configure(state="disabled")
        else:
            self.sender_label.configure(text="")
            self.date_label.configure(text="")
            self.subject_label.configure(text="")
            self.body_text.delete(1.0, "end")
            self.body_text.insert("end", "No more emails to display.")
            self.next_button.configure(state="disabled")

    def show_next_email(self):
        self.current_email_index += 1
        self.show_current_email()

    def show_previous_email(self):
        self.current_email_index -= 1
        self.show_current_email()


def open_email_viewer(filter_addresses, search_query):
    EmailViewerGUI(filter_addresses, search_query)


def open_main_menu():
    def handle_submit():
        addresses = address_entry.get()
        query = query_entry.get()
        filter_addresses = addresses.split(",")
        search_query = query.strip()
        root.destroy()
        open_email_viewer(filter_addresses, search_query)

    root = Tk()
    root.title("Gmail Zapper - Main Menu")

    address_label = Label(root, text="Enter email addresses (comma-separated):")
    address_label.pack(pady=10)
    address_entry = Entry(root)
    address_entry.pack()

    query_label = Label(root, text="Enter search query (optional):")
    query_label.pack(pady=10)
    query_entry = Entry(root)
    query_entry.pack()

    submit_button = Button(root, text="Submit", command=handle_submit)
    submit_button.pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    open_main_menu()
