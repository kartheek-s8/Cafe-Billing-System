# login_screen.py - Login and Role Selection Screen
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import mysql.connector


class LoginScreen:
    def __init__(self, root, on_customer_login, on_admin_login):
        self.root = root
        self.on_customer_login = on_customer_login
        self.on_admin_login = on_admin_login

        self.root.title("Cafe Management System - Login")
        self.root.geometry("900x600")

        # Colors
        self.colors = {
            'primary': '#8B7355',
            'secondary': '#C4A57B',
            'accent': '#D4AF37',
            'bg': '#F5F0E8',
            'dark': '#4A3428',
            'light': '#FFF8F0',
            'card': '#FFFFFF'
        }

        self.root.configure(bg=self.colors['bg'])

        # Fonts
        self.fonts = {
            'title': tkFont.Font(family='Garamond', size=36, weight='bold'),
            'heading': tkFont.Font(family='Georgia', size=20, weight='bold'),
            'body': tkFont.Font(family='Segoe UI', size=12),
            'button': tkFont.Font(family='Georgia', size=14, weight='bold')
        }

        self.create_ui()

    def create_ui(self):
        """Create the login screen UI"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="☕ ARTISAN CAFÉ",
            font=self.fonts['title'],
            bg=self.colors['dark'],
            fg=self.colors['light']
        ).pack(pady=(25, 5))

        tk.Label(
            header_frame,
            text="Management System",
            font=self.fonts['body'],
            bg=self.colors['dark'],
            fg=self.colors['secondary']
        ).pack()

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, pady=50)

        # Role selection container
        role_container = tk.Frame(main_frame, bg=self.colors['bg'])
        role_container.pack(expand=True)

        # Title
        tk.Label(
            role_container,
            text="Select Your Role",
            font=self.fonts['heading'],
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(pady=(0, 40))

        # Buttons container
        buttons_frame = tk.Frame(role_container, bg=self.colors['bg'])
        buttons_frame.pack()

        # Customer button
        customer_frame = tk.Frame(buttons_frame, bg=self.colors['card'], relief='raised', bd=3)
        customer_frame.pack(side='left', padx=30)

        tk.Label(
            customer_frame,
            text="👤",
            font=tkFont.Font(size=48),
            bg=self.colors['card']
        ).pack(pady=(30, 10))

        tk.Label(
            customer_frame,
            text="Customer",
            font=self.fonts['heading'],
            bg=self.colors['card'],
            fg=self.colors['dark']
        ).pack()

        tk.Label(
            customer_frame,
            text="Place orders and view menu",
            font=self.fonts['body'],
            bg=self.colors['card'],
            fg='gray'
        ).pack(pady=(5, 20))

        tk.Button(
            customer_frame,
            text="Continue as Customer",
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['button'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            command=self.customer_login
        ).pack(pady=(0, 30), padx=40)

        # Admin button
        admin_frame = tk.Frame(buttons_frame, bg=self.colors['card'], relief='raised', bd=3)
        admin_frame.pack(side='left', padx=30)

        tk.Label(
            admin_frame,
            text="🔐",
            font=tkFont.Font(size=48),
            bg=self.colors['card']
        ).pack(pady=(30, 10))

        tk.Label(
            admin_frame,
            text="Administrator",
            font=self.fonts['heading'],
            bg=self.colors['card'],
            fg=self.colors['dark']
        ).pack()

        tk.Label(
            admin_frame,
            text="Manage system and view reports",
            font=self.fonts['body'],
            bg=self.colors['card'],
            fg='gray'
        ).pack(pady=(5, 20))

        tk.Button(
            admin_frame,
            text="Login as Admin",
            bg=self.colors['accent'],
            fg=self.colors['dark'],
            font=self.fonts['button'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=40,
            pady=12,
            command=self.show_admin_login
        ).pack(pady=(0, 30), padx=40)

    def customer_login(self):
        """Handle customer login"""
        self.root.destroy()
        self.on_customer_login()

    def show_admin_login(self):
        """Show admin login dialog"""
        # Create login popup
        login_window = tk.Toplevel(self.root)
        login_window.title("Admin Login")
        login_window.geometry("400x350")
        login_window.configure(bg=self.colors['light'])
        login_window.transient(self.root)
        login_window.grab_set()

        # Center the window
        login_window.update_idletasks()
        x = (login_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (login_window.winfo_screenheight() // 2) - (350 // 2)
        login_window.geometry(f"+{x}+{y}")

        # Header
        tk.Label(
            login_window,
            text="🔐 Admin Login",
            font=self.fonts['heading'],
            bg=self.colors['light'],
            fg=self.colors['dark']
        ).pack(pady=(30, 40))

        # Username
        tk.Label(
            login_window,
            text="Username:",
            font=self.fonts['body'],
            bg=self.colors['light'],
            fg=self.colors['dark']
        ).pack(anchor='w', padx=50, pady=(0, 5))

        username_entry = tk.Entry(
            login_window,
            font=self.fonts['body'],
            width=30,
            relief='solid',
            bd=1
        )
        username_entry.pack(padx=50, pady=(0, 20))
        username_entry.focus()

        # Password
        tk.Label(
            login_window,
            text="Password:",
            font=self.fonts['body'],
            bg=self.colors['light'],
            fg=self.colors['dark']
        ).pack(anchor='w', padx=50, pady=(0, 5))

        password_entry = tk.Entry(
            login_window,
            font=self.fonts['body'],
            width=30,
            show='●',
            relief='solid',
            bd=1
        )
        password_entry.pack(padx=50, pady=(0, 30))

        # Login button
        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showwarning("Missing Info", "Please enter both username and password!")
                return

            if self.verify_admin(username, password):
                login_window.destroy()
                self.root.destroy()
                self.on_admin_login()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password!")
                password_entry.delete(0, tk.END)

        tk.Button(
            login_window,
            text="Login",
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['button'],
            cursor='hand2',
            relief='flat',
            bd=0,
            width=20,
            pady=10,
            command=attempt_login
        ).pack(pady=(0, 10))

        # Cancel button
        tk.Button(
            login_window,
            text="Cancel",
            bg='gray',
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            width=20,
            pady=8,
            command=login_window.destroy
        ).pack()

        # Bind Enter key to login
        password_entry.bind('<Return>', lambda e: attempt_login())

    def verify_admin(self, username, password):
        """Verify admin credentials from database"""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='kartheek',
                database='cafe_billing'
            )
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM Admin WHERE username = %s AND password = %s",
                (username, password)
            )

            result = cursor.fetchone()
            conn.close()

            return result is not None

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False
