from tkinter import Tk, Label, Text, Button, Entry, ttk, messagebox
import utils
from client import Client

logger = utils.setup_logger("status.log", __name__)


class EmailViewerMenu:
    def __init__(self, parent, client):
        self.client = client
        self.emails = []
        self.email_ids = []
        self.current_email_index = 0

        self.window = ttk.Frame(parent)
        parent.add(self.window, text="Email Viewer")

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

    def set_emails(self, emails):
        self.emails = emails
        self.email_ids = [email['id'] for email in self.emails]
        self.current_email_index = 0
        self.show_current_email()

    def show_current_email(self):
        if self.current_email_index < len(self.email_ids):
            email_id = self.email_ids[self.current_email_index]
            message = self.client.service.users().messages().get(userId='me', id=email_id, format='full').execute()
            payload = message['payload']
            body = utils.get_email_body(payload)
            headers = message['payload']['headers']

            header_mapping = {
                'From': self.sender_label,
                'Date': self.date_label,
                'Subject': self.subject_label
            }

            for header in headers:
                name = header['name']
                value = header['value']
                if name in header_mapping:
                    label = header_mapping[name]
                    label.configure(text=f"{name}: {value}")

            self.body_text.delete(1.0, "end")
            self.body_text.insert("end", body)

            self.previous_button.configure(state="normal" if self.current_email_index > 0 else "disabled")
            self.next_button.configure(state="normal" if self.current_email_index < len(self.email_ids) else "disabled")
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


class FetchEmailMenu:
    def __init__(self, parent, client, email_viewer):
        self.parent = parent
        self.client = client
        self.email_viewer = email_viewer

        self.page = ttk.Frame(parent)
        parent.insert(0, self.page, text="Fetch Email")  # Insert at index 0

        self.address_label = Label(self.page, text="Enter email addresses (comma-separated):")
        self.address_label.pack(pady=10)
        self.address_entry = Entry(self.page)
        self.address_entry.pack()

        self.query_label = Label(self.page, text="Enter search query (optional):")
        self.query_label.pack(pady=10)
        self.query_entry = Entry(self.page)
        self.query_entry.pack()

        self.submit_button = Button(self.page, text="Submit", command=self.handle_submit)
        self.submit_button.pack(pady=20)

    def handle_submit(self):
        addresses = self.address_entry.get()
        query = self.query_entry.get()
        filter_addresses = addresses.split(",")
        search_query = query.strip()

        emails = self.client.fetch_emails(filter_addresses, search_query)
        self.email_viewer.set_emails(emails)
        self.parent.select(1)  # Switch to Email Viewer page


class GmailZapperApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Gmail Zapper")

        self.notebook = ttk.Notebook(self.root)

        self.client = Client()  # Create the Gmail client

        self.email_viewer = EmailViewerMenu(self.notebook, self.client)
        self.fetch_email_menu = FetchEmailMenu(self.notebook, self.client,
                                               self.email_viewer)

        self.notebook.add(self.fetch_email_menu.page, text="Fetch Email")
        self.notebook.add(self.email_viewer.window, text="Email Viewer")

        self.notebook.select(0)
        self.notebook.pack()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = GmailZapperApp()
    app.run()
