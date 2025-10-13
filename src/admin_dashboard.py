# admin_dashboard.py - Admin Dashboard with Analytics
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import tkinter.font as tkFont
from analytics import Analytics
import db


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Cafe Management")
        self.root.geometry("1400x850")

        self.analytics = Analytics()

        # Colors
        self.colors = {
            'primary': '#8B7355',
            'secondary': '#C4A57B',
            'accent': '#D4AF37',
            'bg': '#F5F0E8',
            'dark': '#4A3428',
            'light': '#FFF8F0',
            'card': '#FFFFFF',
            'success': '#6B8E23'
        }

        self.root.configure(bg=self.colors['bg'])

        # Fonts
        self.fonts = {
            'title': tkFont.Font(family='Garamond', size=28, weight='bold'),
            'heading': tkFont.Font(family='Georgia', size=16, weight='bold'),
            'body': tkFont.Font(family='Segoe UI', size=11),
            'stats': tkFont.Font(family='Arial', size=24, weight='bold')
        }

        self.create_ui()

    def create_ui(self):
        """Create admin dashboard UI"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🔐 ADMIN DASHBOARD",
            font=self.fonts['title'],
            bg=self.colors['dark'],
            fg=self.colors['light']
        ).pack(side='left', padx=30, pady=20)

        # Logout button
        tk.Button(
            header_frame,
            text="Logout",
            bg='#B85450',
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            command=self.logout
        ).pack(side='right', padx=30)

        # Navigation tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Tab 1: Dashboard (Analytics & Stats)
        self.dashboard_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.dashboard_tab, text='  📊 Dashboard  ')
        self.create_dashboard_tab()

        # Tab 2: Order Records
        self.orders_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.orders_tab, text='  📋 Order Records  ')
        self.create_orders_tab()

        # Tab 3: Menu Management
        self.menu_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.menu_tab, text='  🍽️ Menu Management  ')
        self.create_menu_tab()

    def create_dashboard_tab(self):
        """Create dashboard with stats and charts"""
        # Stats cards at top
        stats_frame = tk.Frame(self.dashboard_tab, bg=self.colors['bg'])
        stats_frame.pack(fill='x', padx=20, pady=20)

        # Today's Sales Card
        sales_card = tk.Frame(stats_frame, bg=self.colors['card'], relief='raised', bd=2)
        sales_card.pack(side='left', padx=10, fill='both', expand=True)

        tk.Label(
            sales_card,
            text="Today's Sales",
            font=self.fonts['heading'],
            bg=self.colors['card'],
            fg=self.colors['dark']
        ).pack(pady=(20, 10))

        today_sales = self.analytics.get_total_sales_today()
        tk.Label(
            sales_card,
            text=f"₹ {today_sales:.2f}",
            font=self.fonts['stats'],
            bg=self.colors['card'],
            fg=self.colors['success']
        ).pack(pady=(0, 20))

        # Today's Orders Card
        orders_card = tk.Frame(stats_frame, bg=self.colors['card'], relief='raised', bd=2)
        orders_card.pack(side='left', padx=10, fill='both', expand=True)

        tk.Label(
            orders_card,
            text="Today's Orders",
            font=self.fonts['heading'],
            bg=self.colors['card'],
            fg=self.colors['dark']
        ).pack(pady=(20, 10))

        today_orders = self.analytics.get_total_orders_today()
        tk.Label(
            orders_card,
            text=str(today_orders),
            font=self.fonts['stats'],
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(pady=(0, 20))

        # Refresh Dashboard button
        tk.Button(
            stats_frame,
            text="🔄 Refresh",
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.refresh_dashboard
        ).pack(side='left', padx=10)

        # Charts section
        self.charts_frame = tk.Frame(self.dashboard_tab, bg=self.colors['bg'])
        self.charts_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.load_charts()

    def load_charts(self):
        """Load all charts"""
        # Clear existing charts
        for widget in self.charts_frame.winfo_children():
            widget.destroy()

        # Left column - Top items
        left_chart_frame = tk.Frame(self.charts_frame, bg=self.colors['card'], relief='raised', bd=2)
        left_chart_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        chart1 = self.analytics.create_top_items_chart(left_chart_frame)
        if chart1:
            chart1.pack(padx=10, pady=10)

        # Middle column - Category pie
        mid_chart_frame = tk.Frame(self.charts_frame, bg=self.colors['card'], relief='raised', bd=2)
        mid_chart_frame.pack(side='left', fill='both', expand=True, padx=10)

        chart2 = self.analytics.create_category_chart(mid_chart_frame)
        if chart2:
            chart2.pack(padx=10, pady=10)

        # Right column - Weekly trend
        right_chart_frame = tk.Frame(self.charts_frame, bg=self.colors['card'], relief='raised', bd=2)
        right_chart_frame.pack(side='left', fill='both', expand=True, padx=(10, 0))

        chart3 = self.analytics.create_weekly_sales_chart(right_chart_frame)
        if chart3:
            chart3.pack(padx=10, pady=10)

    def refresh_dashboard(self):
        """Refresh dashboard stats and charts"""
        # Recreate entire dashboard tab
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()

        self.create_dashboard_tab()
        messagebox.showinfo("Refreshed", "Dashboard data has been updated!")

    def create_orders_tab(self):
        """Create order records viewer"""
        # Header
        tk.Label(
            self.orders_tab,
            text="Order History (Ctrl+Click for multiple selection)",
            font=self.fonts['heading'],
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(pady=(20, 10))

        # Orders table
        table_frame = tk.Frame(self.orders_tab, bg=self.colors['card'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame)
        y_scroll.pack(side='right', fill='y')

        x_scroll = ttk.Scrollbar(table_frame, orient='horizontal')
        x_scroll.pack(side='bottom', fill='x')

        # Treeview for orders with MULTIPLE SELECTION
        columns = ('Order ID', 'Item', 'Quantity', 'Amount', 'Date')
        self.orders_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            height=20,
            selectmode='extended'  # Enable multiple selection
        )

        y_scroll.config(command=self.orders_tree.yview)
        x_scroll.config(command=self.orders_tree.xview)

        # Column headings
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=150, anchor='center')

        self.orders_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Load orders
        self.load_order_records()

        # Buttons frame
        btn_frame = tk.Frame(self.orders_tab, bg=self.colors['bg'])
        btn_frame.pack(pady=(0, 20))

        # Refresh button
        tk.Button(
            btn_frame,
            text="🔄 Refresh Orders",
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            command=self.load_order_records
        ).pack(side='left', padx=10)

        # Delete selected orders button
        tk.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            bg='#B85450',
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            command=self.delete_selected_order
        ).pack(side='left', padx=10)

        # Delete ALL orders button
        tk.Button(
            btn_frame,
            text="🗑️ Delete All Orders",
            bg='#8B0000',
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            command=self.delete_all_orders
        ).pack(side='left', padx=10)

    def load_order_records(self):
        """Load all orders from database"""
        # Clear existing
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        # Fetch orders
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT o.order_id, m.name, o.quantity, o.total_amount, o.order_date
            FROM Orders o
            JOIN MenuItem m ON o.item_id = m.id
            ORDER BY o.order_date DESC
            LIMIT 100
        """)

        orders = cursor.fetchall()
        conn.close()

        # Insert into table
        for order in orders:
            order_id, item, qty, amount, date = order
            date_str = date.strftime('%Y-%m-%d %H:%M') if date else 'N/A'
            self.orders_tree.insert('', 'end', values=(order_id, item, qty, f'₹{amount:.2f}', date_str))

    def delete_selected_order(self):
        """Delete selected orders from database (supports multiple selection)"""
        selected = self.orders_tree.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please select order(s) to delete!")
            return

        # Get all selected order IDs
        order_ids = []
        for item in selected:
            values = self.orders_tree.item(item)['values']
            order_ids.append(values[0])

        # Confirm deletion
        count = len(order_ids)
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {count} order(s)?\nOrder IDs: {', '.join(map(str, order_ids))}\n\nThis action cannot be undone!"
        )

        if result:
            try:
                conn = db.get_connection()
                cursor = conn.cursor()

                # Delete all selected orders
                for order_id in order_ids:
                    cursor.execute("DELETE FROM Orders WHERE order_id = %s", (order_id,))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"{count} order(s) deleted successfully!")
                self.load_order_records()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete orders: {str(e)}")

    def delete_all_orders(self):
        """Delete ALL orders from database"""
        # Confirm deletion with strong warning
        result = messagebox.askyesno(
            "⚠️ WARNING: Delete All Orders",
            "Are you ABSOLUTELY SURE you want to delete ALL orders?\n\n"
            "This will permanently remove the entire order history!\n\n"
            "This action CANNOT be undone!",
            icon='warning'
        )

        if result:
            # Double confirmation
            confirm = messagebox.askyesno(
                "Final Confirmation",
                "Last chance! Click YES to delete ALL orders permanently.",
                icon='warning'
            )

            if confirm:
                try:
                    conn = db.get_connection()
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM Orders")
                    deleted_count = cursor.rowcount
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", f"All {deleted_count} orders deleted successfully!")
                    self.load_order_records()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete orders: {str(e)}")

    def create_menu_tab(self):
        """Create menu management interface"""
        tk.Label(
            self.menu_tab,
            text="Menu Items Management (Ctrl+Click for multiple selection)",
            font=self.fonts['heading'],
            bg=self.colors['bg'],
            fg=self.colors['dark']
        ).pack(pady=(20, 10))

        # Menu table
        table_frame = tk.Frame(self.menu_tab, bg=self.colors['card'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Scrollbar
        y_scroll = ttk.Scrollbar(table_frame)
        y_scroll.pack(side='right', fill='y')

        # Treeview for menu with MULTIPLE SELECTION
        columns = ('ID', 'Name', 'Price', 'Category')
        self.menu_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scroll.set,
            height=20,
            selectmode='extended'  # Enable multiple selection
        )

        y_scroll.config(command=self.menu_tree.yview)

        # Column headings
        self.menu_tree.heading('ID', text='ID')
        self.menu_tree.heading('Name', text='Name')
        self.menu_tree.heading('Price', text='Price')
        self.menu_tree.heading('Category', text='Category')

        self.menu_tree.column('ID', width=50, anchor='center')
        self.menu_tree.column('Name', width=300, anchor='w')
        self.menu_tree.column('Price', width=100, anchor='center')
        self.menu_tree.column('Category', width=150, anchor='center')

        self.menu_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Load menu
        self.load_menu_items()

        # Buttons frame
        btn_frame = tk.Frame(self.menu_tab, bg=self.colors['bg'])
        btn_frame.pack(pady=(0, 20))

        # Refresh button
        tk.Button(
            btn_frame,
            text="🔄 Refresh Menu",
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            command=self.load_menu_items
        ).pack(side='left', padx=10)

        # Delete menu item button
        tk.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            bg='#B85450',
            fg='white',
            font=self.fonts['body'],
            cursor='hand2',
            relief='flat',
            bd=0,
            padx=30,
            pady=10,
            command=self.delete_selected_menu_item
        ).pack(side='left', padx=10)

    def load_menu_items(self):
        """Load menu items from database"""
        # Clear existing
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)

        # Fetch menu
        menu_items = db.fetch_menu_items()

        # Insert into table
        for item in menu_items:
            item_id, name, price, category = item
            self.menu_tree.insert('', 'end', values=(item_id, name, f'₹{price:.2f}', category))

        messagebox.showinfo("Refreshed", "Menu items have been refreshed!")

    def delete_selected_menu_item(self):
        """Delete selected menu items (supports multiple selection)"""
        selected = self.menu_tree.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please select menu item(s) to delete!")
            return

        # Get all selected items
        items_to_delete = []
        for item in selected:
            values = self.menu_tree.item(item)['values']
            items_to_delete.append((values[0], values[1]))  # (id, name)

        # Confirm deletion
        count = len(items_to_delete)
        names = ', '.join([name for _, name in items_to_delete[:3]])
        if count > 3:
            names += f", and {count - 3} more..."

        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {count} menu item(s)?\n{names}\n\nThis action cannot be undone!"
        )

        if result:
            try:
                conn = db.get_connection()
                cursor = conn.cursor()

                # Delete all selected items
                for item_id, item_name in items_to_delete:
                    cursor.execute("DELETE FROM MenuItem WHERE id = %s", (item_id,))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"{count} menu item(s) deleted successfully!")
                self.load_menu_items()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete items: {str(e)}")

    def logout(self):
        """Logout and return to login screen"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.root.destroy()
            # Restart the application
            import main_app
            main_app.main()


def main():
    root = tk.Tk()
    AdminDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
