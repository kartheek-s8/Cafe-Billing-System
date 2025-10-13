# main_app.py - Main Entry Point for Cafe Management System
import tkinter as tk
from login_screen import LoginScreen


def launch_customer_app():
    """Launch customer ordering interface"""
    from customer_app import CafeBillingGUI

    root = tk.Tk()
    CafeBillingGUI(root)
    root.mainloop()


def launch_admin_dashboard():
    """Launch admin dashboard"""
    from admin_dashboard import AdminDashboard

    root = tk.Tk()
    AdminDashboard(root)
    root.mainloop()


def main():
    """Main function - shows login screen first"""
    root = tk.Tk()
    LoginScreen(root, launch_customer_app, launch_admin_dashboard)
    root.mainloop()


if __name__ == "__main__":
    main()
