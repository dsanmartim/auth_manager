import tkinter as tk
from tkinter import messagebox, Menu, Toplevel, Label, Entry, Button
from tkinter.font import Font
from .manager import OTPManager


class OTPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2FA Manager")
        self.geometry("400x500")
        self.manager = OTPManager()

        # Fonts
        self.service_name_font = Font(family="Helvetica", size=16, weight="bold")
        self.code_font = Font(family="Helvetica", size=20, weight="bold")
        self.plus_font = Font(family="Helvetica", size=28, weight="bold")

        # Frame to hold all services
        self.services_frame = tk.Frame(self)
        self.services_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Plus button to add new service with a circle around it
        plus_button_canvas = tk.Canvas(
            self, width=40, height=40, highlightthickness=0, bg=None, cursor="hand2"
        )
        plus_button_canvas.place(relx=0.9, rely=0.9, anchor="center")
        plus_button_canvas.create_oval(5, 5, 38, 38, outline="#007BFF", width=2)
        plus_button_canvas.create_text(
            21, 19.5, text="+", font=self.plus_font, fill="#007BFF", anchor="center"
        )
        plus_button_canvas.bind("<Button-1>", lambda e: self.add_service())

        # Load and display existing services
        self.refresh_service_list()

    def refresh_service_list(self):
        for widget in self.services_frame.winfo_children():
            widget.destroy()

        for name in self.manager.services:
            self.create_service_card(name)

    def create_service_card(self, name):
        # Frame for each service "card"
        card_frame = tk.Frame(
            self.services_frame, bd=1, relief="solid", padx=10, pady=5
        )
        card_frame.pack(fill="x", pady=5)

        # Frame for service name and code
        text_frame = tk.Frame(card_frame)
        text_frame.pack(side="left", fill="x", expand=True)

        # Service name
        service_name_label = tk.Label(
            text_frame, text=name, font=self.service_name_font, anchor="w"
        )
        service_name_label.pack(side="top", anchor="w")

        # OTP code
        code = self.manager.get_code(name)
        code_label = tk.Label(text_frame, text=code, font=self.code_font, fg="blue")
        code_label.pack(side="top", anchor="w")

        # Three dots menu inside a circle
        canvas = tk.Canvas(
            card_frame,
            width=30,
            height=30,
            highlightthickness=0,
            bg=None,
            cursor="hand2",
        )
        canvas.pack(side="right", anchor="e", padx=5)
        canvas.create_oval(5, 5, 25, 25, outline="#A9A9A9", width=2)
        canvas.create_text(
            15,
            15,
            text="⋯",
            font=self.service_name_font,
            fill="#A9A9A9",
            width=2,
            anchor="center",
        )
        canvas.bind("<Button-1>", lambda e, n=name: self.show_options_menu(n, canvas))

    def show_options_menu(self, service_name, button):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Edit", command=lambda: self.edit_service(service_name))
        menu.add_command(
            label="Delete", command=lambda: self.delete_service(service_name)
        )
        menu.post(button.winfo_rootx(), button.winfo_rooty())

    def add_service(self):
        self.show_edit_dialog("Add Service")

    def edit_service(self, service_name):
        current_uri = self.manager.services[service_name]
        self.show_edit_dialog("Edit Service", service_name, current_uri)

    def show_edit_dialog(
        self,
        title,
        name="Service Name",
        uri="otpauth://totp/ServiceName?secret=JBSWX3DPEHPK3PXP",
    ):
        dialog = Toplevel(self)
        dialog.title(title)
        dialog.geometry("350x200")

        if title == "Add Service":
            # Service Name
            Label(dialog, text="Service Name:", anchor="w").pack(
                fill="x", pady=5, padx=10
            )
            name_entry = Entry(dialog, fg="gray")
            name_entry.pack(fill="x", pady=5, padx=10)
            name_entry.insert(0, "Service Name")
            name_entry.bind(
                "<FocusIn>", lambda e: self.clear_placeholder(e, name_entry)
            )
            name_entry.bind(
                "<FocusOut>",
                lambda e: self.add_placeholder(e, name_entry, "Service Name"),
            )

            # TOTP URI
            Label(dialog, text="TOTP URI:", anchor="w").pack(fill="x", pady=5, padx=10)
            uri_entry = Entry(dialog, fg="gray")
            uri_entry.pack(fill="x", pady=5, padx=10)
            uri_entry.insert(0, "otpauth://totp/ServiceName?secret=JBSWX3DPEHPK3PXP")
            uri_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, uri_entry))
            uri_entry.bind(
                "<FocusOut>",
                lambda e: self.add_placeholder(
                    e, uri_entry, "otpauth://totp/ServiceName?secret=JBSWX3DPEHPK3PXP"
                ),
            )

        else:
            # Service Name
            Label(dialog, text="Service Name:", anchor="w").pack(
                fill="x", pady=5, padx=10
            )
            name_entry = Entry(dialog)
            name_entry.pack(fill="x", pady=5, padx=10)
            name_entry.insert(0, name)

            # TOTP URI
            Label(dialog, text="TOTP URI:", anchor="w").pack(fill="x", pady=5, padx=10)
            uri_entry = Entry(dialog)
            uri_entry.pack(fill="x", pady=5, padx=10)
            uri_entry.insert(0, uri)

        # Save Button
        save_button = Button(
            dialog,
            text="Save",
            command=lambda: self.save_service(
                dialog, name_entry.get(), uri_entry.get(), name
            ),
        )
        save_button.pack(pady=10)

        # Make dialog responsive to content
        dialog.update_idletasks()
        dialog.minsize(400, dialog.winfo_height())

    def clear_placeholder(self, event, entry):
        if entry.get() in [
            "Service Name",
            "otpauth://totp/ServiceName?secret=JBSWX3DPEHPK3PXP",
        ]:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, event, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def save_service(self, dialog, new_name, new_uri, old_name=""):
        if new_name and new_uri:
            if old_name:
                self.manager.edit_service(old_name, new_name, new_uri)
            else:
                self.manager.add_service(new_name, new_uri)
            self.refresh_service_list()
            dialog.destroy()

    def delete_service(self, service_name):
        confirm = messagebox.askyesno(
            "Delete Service", f"Are you sure you want to delete '{service_name}'?"
        )
        if confirm:
            self.manager.delete_service(service_name)
            self.refresh_service_list()
