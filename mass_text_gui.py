"""Tkinter interface for sending a message to recipients through Twilio.

Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and
TWILIO_MESSAGING_SERVICE_SID in the environment before sending.
"""

import csv
import os
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from twilio.rest import Client


class GUI:
    """Build and manage the message-sending window."""

    def __init__(self, window):
        self.win = window
        self.win.title("Mass Text — Twilio")
        self.win.geometry("720x640")
        self.win.minsize(560, 500)

        self.phone_numbers = []
        self._events = queue.Queue()
        self._sending = False
        self._sent_count = 0
        self._send_error = None
        self._active_total = 0

        self._build_layout()

    def _build_layout(self):
        content = ttk.Frame(self.win, padding=24)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(2, weight=1)

        ttk.Label(content, text="Message campaign", font=("TkDefaultFont", 18, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            content,
            text="Choose opted-in recipients, write your message, and review before sending.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 18))

        recipients = ttk.LabelFrame(content, text="Recipients", padding=12)
        recipients.grid(row=2, column=0, sticky="nsew", pady=(0, 16))
        recipients.columnconfigure(0, weight=1)
        recipients.rowconfigure(1, weight=1)

        file_controls = ttk.Frame(recipients)
        file_controls.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.file_label = ttk.Label(file_controls, text="No CSV selected", anchor="w")
        self.file_label.pack(side="left", fill="x", expand=True)
        self.choose_file_button = ttk.Button(
            file_controls, text="Choose CSV...", command=self.getFile
        )
        self.choose_file_button.pack(side="right", padx=(8, 0))
        self.clear_button = ttk.Button(
            file_controls, text="Clear", command=self.clearRecipients
        )
        self.clear_button.pack(side="right")

        list_frame = ttk.Frame(recipients)
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        self.recipient_list = tk.Listbox(
            list_frame, height=7, exportselection=False, activestyle="none"
        )
        self.recipient_list.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.recipient_list.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.recipient_list.configure(yscrollcommand=scrollbar.set)
        self.recipient_count = ttk.Label(recipients, text="0 recipients")
        self.recipient_count.grid(row=2, column=0, sticky="w", pady=(8, 0))

        message_frame = ttk.LabelFrame(content, text="Message", padding=12)
        message_frame.grid(row=3, column=0, sticky="ew", pady=(0, 16))
        message_frame.columnconfigure(0, weight=1)
        self.message_text = tk.Text(message_frame, height=6, wrap="word", undo=True)
        self.message_text.grid(row=0, column=0, sticky="ew")
        self.message_text.bind("<<Modified>>", self._on_message_changed)
        self.character_count = ttk.Label(message_frame, text="0 characters")
        self.character_count.grid(row=1, column=0, sticky="e", pady=(6, 0))

        footer = ttk.Frame(content)
        footer.grid(row=4, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)
        self.status = ttk.Label(footer, text="Select a CSV file to get started.", anchor="w")
        self.status.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.send_button = ttk.Button(
            footer, text="Send message", command=self.sendMessage, state="disabled"
        )
        self.send_button.grid(row=0, column=1, sticky="e")

    def _on_message_changed(self, _event=None):
        self.message_text.edit_modified(False)
        self.character_count.configure(
            text=f"{len(self.message_text.get('1.0', 'end-1c'))} characters"
        )
        self._refresh_send_button()

    def _refresh_send_button(self):
        can_send = bool(self.phone_numbers) and bool(
            self.message_text.get("1.0", "end-1c").strip()
        )
        self.send_button.configure(
            state="normal" if can_send and not self._sending else "disabled"
        )
        control_state = "disabled" if self._sending else "normal"
        self.choose_file_button.configure(state=control_state)
        self.clear_button.configure(state=control_state)
        self.message_text.configure(state=control_state)

    def _update_recipient_list(self):
        self.recipient_list.delete(0, "end")
        for number in self.phone_numbers:
            self.recipient_list.insert("end", number)
        count = len(self.phone_numbers)
        self.recipient_count.configure(
            text=f"{count} recipient" if count == 1 else f"{count} recipients"
        )
        self._refresh_send_button()

    def clearRecipients(self):
        """Clear the currently loaded recipients."""
        self.phone_numbers = []
        self.file_label.configure(text="No CSV selected")
        self._update_recipient_list()
        self.status.configure(text="Recipient list cleared.")

    def getFile(self):
        """Load the first column of a CSV as the recipient phone numbers."""
        filename = filedialog.askopenfilename(
            title="Choose recipient CSV",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
        )
        if not filename:
            return

        try:
            with open(filename, "r", newline="", encoding="utf-8-sig") as csv_file:
                recipients = [
                    row[0].strip()
                    for row in csv.reader(csv_file)
                    if row and row[0].strip()
                ]
        except (OSError, csv.Error, UnicodeError) as error:
            messagebox.showerror("Could not read CSV", str(error), parent=self.win)
            return

        if not recipients:
            messagebox.showwarning(
                "No recipients found",
                "The selected CSV has no phone numbers in its first column.",
                parent=self.win,
            )
            return

        self.phone_numbers = recipients
        self.file_label.configure(text=os.path.basename(filename))
        self._update_recipient_list()
        self.status.configure(text="Review the recipient list and message before sending.")

    def sendMessage(self):
        """Confirm the send and start sending messages without blocking the UI."""
        message = self.message_text.get("1.0", "end-1c").strip()
        if not self.phone_numbers or not message:
            return

        credentials = {
            "TWILIO_ACCOUNT_SID": os.environ.get("TWILIO_ACCOUNT_SID"),
            "TWILIO_AUTH_TOKEN": os.environ.get("TWILIO_AUTH_TOKEN"),
            "TWILIO_MESSAGING_SERVICE_SID": os.environ.get(
                "TWILIO_MESSAGING_SERVICE_SID"
            ),
        }
        missing = [name for name, value in credentials.items() if not value]
        if missing:
            messagebox.showerror(
                "Twilio configuration missing",
                "Set these environment variables before sending:\n"
                + "\n".join(missing),
                parent=self.win,
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm send",
            f"Send this message to {len(self.phone_numbers)} recipients?\n\n"
            f"{message[:240]}",
            parent=self.win,
        )
        if not confirmed:
            return

        client = Client(
            credentials["TWILIO_ACCOUNT_SID"], credentials["TWILIO_AUTH_TOKEN"]
        )
        self._sending = True
        self._sent_count = 0
        self._send_error = None
        self._active_total = len(self.phone_numbers)
        self.status.configure(text=f"Sending to 0 of {self._active_total} recipients...")
        self._refresh_send_button()

        thread = threading.Thread(
            target=self._send_messages,
            args=(
                client,
                credentials["TWILIO_MESSAGING_SERVICE_SID"],
                self.phone_numbers.copy(),
                message,
            ),
            daemon=True,
        )
        thread.start()
        self.win.after(100, self._process_send_events)

    def _send_messages(self, client, messaging_service_sid, recipients, message):
        try:
            for recipient in recipients:
                client.messages.create(
                    messaging_service_sid=messaging_service_sid,
                    body=message,
                    to=recipient,
                )
                self._events.put(("sent", None))
        except Exception as error:
            self._events.put(("failed", f"{type(error).__name__}: {error}"))
        finally:
            self._events.put(("finished", None))

    def _process_send_events(self):
        finished = False
        while True:
            try:
                event, detail = self._events.get_nowait()
            except queue.Empty:
                break

            if event == "sent":
                self._sent_count += 1
                self.status.configure(
                    text=f"Sending to {self._sent_count} of {self._active_total} recipients..."
                )
            elif event == "failed":
                self._send_error = detail
            elif event == "finished":
                finished = True

        if not finished:
            self.win.after(100, self._process_send_events)
            return

        self._sending = False
        self._refresh_send_button()
        if self._send_error:
            self.status.configure(
                text=f"Stopped after {self._sent_count} of {self._active_total} sends."
            )
            messagebox.showerror(
                "Sending stopped",
                f"Sent {self._sent_count} of {self._active_total} messages.\n\n"
                f"{self._send_error}",
                parent=self.win,
            )
        else:
            self.status.configure(text=f"Sent {self._sent_count} messages.")
            messagebox.showinfo(
                "Sending complete",
                f"Sent {self._sent_count} messages.",
                parent=self.win,
            )


if __name__ == "__main__":
    window = tk.Tk()
    GUI(window)
    window.mainloop()
