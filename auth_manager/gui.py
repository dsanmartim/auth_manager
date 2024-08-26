import subprocess
import sys
import tkinter as tk
from tkinter import Button, Entry, Label, Menu, Toplevel, messagebox
from tkinter.font import Font

from .manager import OTPManager


class OTPApp(tk.Tk):
    """
    A class representing the OTPApp, which is a GUI application for managing 2FA codes.

    Attributes:
        manager (OTPManager): An instance of the OTPManager class for managing OTP codes.
        is_dark_mode (bool): A flag indicating whether the application is in dark mode.
        bg_color (str): The background color of the application.
        fg_color (str): The text color of the application.
        card_bg_color (str): The background color of the service cards.
        card_fg_color (str): The text color of the service cards.
        code_color (str): The color of the OTP code.
        plus_color (str): The color of the plus sign button.
        service_name_font (Font): The font for the service names.
        code_font (Font): The font for the OTP codes.
        plus_font (Font): The font for the plus sign button.
        services_frame (tk.Frame): The frame that holds all the service cards.
        countdown_id (int): The ID of the countdown timer.
        service_cards (list): A list of tuples containing the service name, code label,
            and countdown label for each service card.

    Methods:
        detect_dark_mode(): Detects whether the system is in dark mode.
        apply_theme(): Applies the theme (dark or light) to the application.
        refresh_service_list(): Refreshes the list of services and displays them.
        create_service_card(name): Creates a service card for the given service name.
        copy_to_clipboard(label): Copies the text of the given label to the clipboard.
        update_code(service_name, code_label): Updates the OTP code for the given
            service name.
        start_countdown(remaining): Starts the countdown timer for refreshing the
            OTP codes.
        refresh_all_codes(): Refreshes the OTP codes for all services.
        show_options_menu(service_name, button): Shows the options menu for the given
            service name.
        add_service(): Shows the dialog for adding a new service.
        edit_service(service_name): Shows the dialog for editing the given service.
        show_edit_dialog(
            title, name="Service Name", uri="otpauth://totp/ServiceName?secret=
            JBSWX3DPEHPK3PXP"): Shows the edit dialog for adding or editing a service.
        clear_placeholder(event, entry): Clears the placeholder text when the entry
            field is focused.
        save_service(dialog, name, uri, original_name): Saves the service with the given
        name and URI.
    """

    def __init__(self):
        super().__init__()
        self.title("2FA Manager")
        self.geometry("400x500")
        self.manager = OTPManager()

        # Detect and apply the system theme
        self.is_dark_mode = self.detect_dark_mode()
        self.apply_theme()

        # Fonts
        self.service_name_font = Font(family="Helvetica", size=16, weight="bold")
        self.code_font = Font(family="Helvetica", size=20, weight="bold")
        self.plus_font = Font(family="Helvetica", size=28, weight="bold")

        # Frame to hold all services
        self.services_frame = tk.Frame(self, bg=self.bg_color)
        self.services_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Plus button to add new service (without a circle around it)
        plus_button = tk.Label(
            self,
            text="+",
            font=self.plus_font,
            fg=self.plus_color,
            cursor="hand2",
            bg=self.bg_color,
        )
        plus_button.place(relx=0.9, rely=0.92, anchor="center")
        plus_button.bind("<Button-1>", lambda e: self.add_service())

        # Variable to track the countdown ID
        self.countdown_id = None

        # Load and display existing services
        self.refresh_service_list()

    def detect_dark_mode(self):
        if sys.platform == "darwin":
            try:
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True,
                    text=True,
                )
                return "Dark" in result.stdout
            except subprocess.CalledProcessError:
                return False
        else:
            return False

    def apply_theme(self):
        if self.is_dark_mode:
            self.bg_color = None  # Dark background color
            self.fg_color = "#FFFFFF"  # Light text color
            self.card_bg_color = "#444444"  # Card background color
            self.card_fg_color = "#FFFFFF"  # Card text color
            self.code_color = "#FFA500"  # Orange for the OTP code in dark mode
            self.plus_color = "#007BFF"  # Color for the plus sign
        else:
            self.bg_color = None  # Light background color
            self.fg_color = "#000000"  # Dark text color
            self.card_bg_color = "#F9F9F9"  # Card background color
            self.card_fg_color = "#000000"  # Card text color
            self.code_color = "#0000FF"  # Blue for the OTP code in light mode
            self.plus_color = "#007BFF"  # Color for the plus sign

        self.configure(bg=self.bg_color)

    def refresh_service_list(self):
        # Cancel any ongoing countdown
        if self.countdown_id:
            self.after_cancel(self.countdown_id)

        for widget in self.services_frame.winfo_children():
            widget.destroy()

        self.service_cards = []
        for name in self.manager.services:
            self.create_service_card(name)

        # Start the countdown for all services
        self.start_countdown(30)

    def create_service_card(self, name):
        card_frame = tk.Frame(
            self.services_frame,
            bd=1,
            relief="solid",
            padx=10,
            pady=5,
            bg=self.card_bg_color,
        )
        card_frame.pack(fill="x", pady=5)

        text_frame = tk.Frame(card_frame, bg=self.card_bg_color)
        text_frame.pack(side="left", fill="x", expand=True)

        service_name_label = tk.Label(
            text_frame,
            text=name,
            font=self.service_name_font,
            anchor="w",
            fg=self.card_fg_color,
            bg=self.card_bg_color,
        )
        service_name_label.pack(side="top", anchor="w")

        code_frame = tk.Frame(text_frame, bg=self.card_bg_color)
        code_frame.pack(side="top", anchor="w")

        code_label = tk.Label(
            code_frame,
            text=self.manager.get_code(name),
            font=self.code_font,
            fg=self.code_color,
            bg=self.card_bg_color,
        )
        code_label.pack(side="left", anchor="w")
        code_label.bind("<Button-1>", lambda e: self.copy_to_clipboard(code_label))

        countdown_label = tk.Label(
            code_frame,
            text="30",
            font=self.service_name_font,
            fg="red",
            bg=self.card_bg_color,
        )
        countdown_label.pack(side="left", padx=10)

        self.service_cards.append((name, code_label, countdown_label))

        canvas = tk.Canvas(
            card_frame,
            width=30,
            height=30,
            highlightthickness=0,
            bg=self.card_bg_color,
            cursor="hand2",
        )
        canvas.pack(side="right", anchor="e", padx=5)
        canvas.create_oval(5, 5, 25, 25, outline=self.card_fg_color, width=2)
        canvas.create_text(
            15,
            15,
            text="⋯",
            font=self.service_name_font,
            fill=self.card_fg_color,
            width=2,
            anchor="center",
        )
        canvas.bind("<Button-1>", lambda e, n=name: self.show_options_menu(n, canvas))

    def copy_to_clipboard(self, label):
        self.clipboard_clear()
        self.clipboard_append(label.cget("text"))

        original_text = label.cget("text")
        original_color = label.cget("fg")

        label.config(text="Copied!", fg="green")
        self.after(1000, lambda: label.config(text=original_text, fg=original_color))

    def update_code(self, service_name, code_label):
        code = self.manager.get_code(service_name)
        code_label.config(text=code)

    def start_countdown(self, remaining):
        if remaining >= 0:
            for _, code_label, countdown_label in self.service_cards:
                countdown_label.config(text=f"{remaining}")
            remaining -= 1
            self.countdown_id = self.after(1000, self.start_countdown, remaining)
        else:
            self.refresh_all_codes()
            self.start_countdown(30)

    def refresh_all_codes(self):
        for name, code_label, _ in self.service_cards:
            self.update_code(name, code_label)

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
            Label(
                dialog,
                text="Service Name:",
                anchor="w",
                bg=self.bg_color,
                fg=self.fg_color,
            ).pack(fill="x", pady=5, padx=10)
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

            Label(
                dialog, text="TOTP URI:", anchor="w", bg=self.bg_color, fg=self.fg_color
            ).pack(fill="x", pady=5, padx=10)
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
            Label(
                dialog,
                text="Service Name:",
                anchor="w",
                bg=self.bg_color,
                fg=self.fg_color,
            ).pack(fill="x", pady=5, padx=10)
            name_entry = Entry(dialog)
            name_entry.pack(fill="x", pady=5, padx=10)
            name_entry.insert(0, name)

            Label(
                dialog, text="TOTP URI:", anchor="w", bg=self.bg_color, fg=self.fg_color
            ).pack(fill="x", pady=5, padx=10)
            uri_entry = Entry(dialog)
            uri_entry.pack(fill="x", pady=5, padx=10)
            uri_entry.insert(0, uri)

        save_button = Button(
            dialog,
            text="Save",
            command=lambda: self.save_service(
                dialog, name_entry.get(), uri_entry.get(), name
            ),
        )
        save_button.pack(pady=10)

        dialog.update_idletasks()
        dialog.minsize(400, dialog.winfo_height())

    def clear_placeholder(self, event, entry):
        if entry.get() in [
            "Service Name",
            "otpauth://totp/ServiceName?secret=JBSWX3DPEHPK3PXP",
        ]:
            entry.delete(0, tk.END)
            entry.config(fg=self.fg_color)

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
