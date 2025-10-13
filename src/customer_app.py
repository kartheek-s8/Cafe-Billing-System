# customer_app.py - Premium Aesthetic Tkinter GUI for Cafe Billing System
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
import db
import orders
import billing
from datetime import datetime


class CafeBillingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafe Billing System")
        self.root.geometry("1400x800")

        # Premium Earthy Color Palette (5-star cafe aesthetic)
        self.colors = {
            'primary': '#8B7355',  # Warm coffee brown
            'secondary': '#C4A57B',  # Light caramel
            'accent': '#D4AF37',  # Gold accent
            'bg': '#F5F0E8',  # Cream background
            'dark': '#4A3428',  # Dark espresso
            'light': '#FFF8F0',  # Soft ivory
            'success': '#6B8E23',  # Olive green
            'card': '#FFFFFF'  # Pure white for cards
        }

        self.root.configure(bg=self.colors['bg'])

        # Premium Fonts
        self.fonts = {
            'title': tkFont.Font(family='Garamond', size=32, weight='bold'),
            'heading': tkFont.Font(family='Georgia', size=18, weight='bold'),
            'subheading': tkFont.Font(family='Georgia', size=14, weight='bold'),
            'body': tkFont.Font(family='Segoe UI', size=11),
            'price': tkFont.Font(family='Arial', size=12, weight='bold'),
            'category': tkFont.Font(family='Georgia', size=13, weight='bold', slant='italic')
        }

        # Variables
        self.cart = []
        self.menu_items = []

        # Create GUI
        self.create_header()
        self.create_main_container()

        # Load menu items
        self.load_menu()

    def create_header(self):
        """Create elegant header section"""
        header_frame = tk.Frame(self.root, bg=self.colors['dark'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Title with coffee icon
        title = tk.Label(
            header_frame,
            text="☕ ARTISAN CAFÉ",
            font=self.fonts['title'],
            bg=self.colors['dark'],
            fg=self.colors['light']
        )
        title.pack(pady=25)

        # Subtitle
        subtitle = tk.Label(
            header_frame,
            text="— Point of Sale System —",
            font=self.fonts['body'],
            bg=self.colors['dark'],
            fg=self.colors['secondary']
        )
        subtitle.pack()

    def create_main_container(self):
        """Create main container with menu and cart"""
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=30, pady=30)

        # Left side - Menu
        self.create_menu_section(main_container)

        # Right side - Cart and Billing
        self.create_right_panel(main_container)

    def create_menu_section(self, parent):
        """Create premium menu display"""
        menu_container = tk.Frame(parent, bg=self.colors['bg'])
        menu_container.pack(side='left', fill='both', expand=True, padx=(0, 15))

        # Menu header
        header_frame = tk.Frame(menu_container, bg=self.colors['card'], relief='flat')
        header_frame.pack(fill='x', pady=(0, 15))

        tk.Label(
            header_frame,
            text="MENU SELECTION",
            font=self.fonts['heading'],
            bg=self.colors['card'],
            fg=self.colors['dark'],
            pady=15
        ).pack()

        # Scrollable menu frame
        canvas_frame = tk.Frame(menu_container, bg=self.colors['card'])
        canvas_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(canvas_frame, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        self.menu_container = tk.Frame(canvas, bg=self.colors['card'])

        self.menu_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.menu_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")

    def load_menu(self):
        """Load menu items with premium design"""
        self.menu_items = db.fetch_menu_items()

        current_category = None
        row = 0

        for item in self.menu_items:
            item_id, name, price, category = item[0], item[1], float(item[2]), item[3]

            # Category header with decorative line
            if category != current_category:
                if row > 0:
                    # Add spacing between categories
                    tk.Frame(self.menu_container, height=20, bg=self.colors['card']).grid(
                        row=row, column=0, columnspan=5, sticky='ew'
                    )
                    row += 1

                cat_frame = tk.Frame(self.menu_container, bg=self.colors['card'])
                cat_frame.grid(row=row, column=0, columnspan=5, sticky='ew', pady=(10, 8))

                tk.Label(
                    cat_frame,
                    text=f"✦ {category} ✦",
                    font=self.fonts['category'],
                    bg=self.colors['card'],
                    fg=self.colors['primary']
                ).pack()

                row += 1
                current_category = category

            # Premium item card
            item_card = tk.Frame(
                self.menu_container,
                bg=self.colors['light'],
                relief='solid',
                bd=1,
                highlightbackground=self.colors['secondary'],
                highlightthickness=1
            )
            item_card.grid(row=row, column=0, columnspan=5, sticky='ew', padx=10, pady=6)

            # Item name
            name_label = tk.Label(
                item_card,
                text=name,
                font=self.fonts['subheading'],
                bg=self.colors['light'],
                fg=self.colors['dark'],
                anchor='w'
            )
            name_label.grid(row=0, column=0, padx=20, pady=12, sticky='w')

            # Price with rupee symbol
            price_label = tk.Label(
                item_card,
                text=f"₹ {price:.2f}",
                font=self.fonts['price'],
                bg=self.colors['light'],
                fg=self.colors['accent']
            )
            price_label.grid(row=0, column=1, padx=15)

            # Quantity frame
            qty_frame = tk.Frame(item_card, bg=self.colors['light'])
            qty_frame.grid(row=0, column=2, padx=10)

            tk.Label(
                qty_frame,
                text="Qty:",
                font=self.fonts['body'],
                bg=self.colors['light'],
                fg=self.colors['dark']
            ).pack(side='left', padx=(0, 5))

            qty_entry = tk.Entry(
                qty_frame,
                width=4,
                font=self.fonts['body'],
                justify='center',
                relief='solid',
                bd=1
            )
            qty_entry.pack(side='left')
            qty_entry.insert(0, "1")

            # Elegant Add button
            add_btn = tk.Button(
                item_card,
                text="Add to Cart",
                bg=self.colors['primary'],
                fg='white',
                font=self.fonts['body'],
                cursor='hand2',
                relief='flat',
                bd=0,
                padx=20,
                pady=8,
                activebackground=self.colors['dark'],
                activeforeground='white',
                command=lambda i=item_id, n=name, p=price, q=qty_entry: self.add_to_cart(i, n, p, q)
            )
            add_btn.grid(row=0, column=3, padx=15, pady=8)

            row += 1

    def create_right_panel(self, parent):
        """Create cart and billing panel"""
        right_panel = tk.Frame(parent, bg=self.colors['bg'], width=450)
        right_panel.pack(side='right', fill='both', padx=(15, 0))
        right_panel.pack_propagate(False)

        # Cart section
        self.create_cart_section(right_panel)

        # Billing section
        self.create_billing_section(right_panel)

    def create_cart_section(self, parent):
        """Create elegant cart display"""
        cart_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat')
        cart_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Header
        header = tk.Frame(cart_frame, bg=self.colors['primary'], height=50)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text="CURRENT ORDER",
            font=self.fonts['heading'],
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=12)

        # Cart items display
        self.cart_text = scrolledtext.ScrolledText(
            cart_frame,
            width=50,
            height=15,
            font=tkFont.Font(family='Consolas', size=10),
            bg=self.colors['light'],
            fg=self.colors['dark'],
            relief='flat',
            padx=15,
            pady=15
        )
        self.cart_text.pack(fill='both', expand=True, padx=15, pady=15)
        self.update_cart_display()

        # Action buttons
        btn_frame = tk.Frame(cart_frame, bg=self.colors['card'])
        btn_frame.pack(fill='x', padx=15, pady=(0, 15))

        clear_btn = tk.Button(
            btn_frame,
            text="Clear Order",
            bg='#B85450',
            fg='white',
            font=self.fonts['body'],
            width=15,
            cursor='hand2',
            relief='flat',
            bd=0,
            pady=10,
            activebackground='#8B3A3A',
            command=self.clear_cart
        )
        clear_btn.pack(side='left', padx=(0, 10))

        bill_btn = tk.Button(
            btn_frame,
            text="Generate Bill",
            bg=self.colors['success'],
            fg='white',
            font=self.fonts['subheading'],
            cursor='hand2',
            relief='flat',
            bd=0,
            pady=10,
            activebackground='#556B2F',
            command=self.generate_bill
        )
        bill_btn.pack(side='right', fill='x', expand=True)

    def create_billing_section(self, parent):
        """Create billing summary"""
        bill_frame = tk.Frame(parent, bg=self.colors['dark'], relief='flat')
        bill_frame.pack(fill='x')

        # Title
        tk.Label(
            bill_frame,
            text="BILL SUMMARY",
            font=self.fonts['heading'],
            bg=self.colors['dark'],
            fg=self.colors['accent'],
            pady=15
        ).pack()

        # Billing details
        details_frame = tk.Frame(bill_frame, bg=self.colors['dark'])
        details_frame.pack(fill='x', padx=30, pady=10)

        self.subtotal_label = tk.Label(
            details_frame,
            text="Subtotal: ₹ 0.00",
            font=self.fonts['body'],
            bg=self.colors['dark'],
            fg=self.colors['light'],
            anchor='w'
        )
        self.subtotal_label.pack(fill='x', pady=5)

        self.gst_label = tk.Label(
            details_frame,
            text="GST (5%): ₹ 0.00",
            font=self.fonts['body'],
            bg=self.colors['dark'],
            fg=self.colors['light'],
            anchor='w'
        )
        self.gst_label.pack(fill='x', pady=5)

        # Separator
        tk.Frame(bill_frame, height=2, bg=self.colors['accent']).pack(fill='x', padx=30, pady=10)

        # Grand total
        self.total_label = tk.Label(
            bill_frame,
            text="TOTAL: ₹ 0.00",
            font=self.fonts['heading'],
            bg=self.colors['dark'],
            fg=self.colors['accent'],
            pady=15
        )
        self.total_label.pack()

    def add_to_cart(self, item_id, name, price, qty_entry):
        """Add item to cart"""
        try:
            quantity = int(qty_entry.get())
            if quantity <= 0:
                messagebox.showwarning("Invalid Quantity", "Please enter a quantity greater than 0!")
                return

            # Check if item already in cart
            for i, item in enumerate(self.cart):
                if item[0] == item_id:
                    self.cart[i] = (item_id, name, price, item[3] + quantity)
                    self.update_cart_display()
                    qty_entry.delete(0, tk.END)
                    qty_entry.insert(0, "1")
                    messagebox.showinfo("Added", f"{name} quantity updated!")
                    return

            # Add new item
            self.cart.append((item_id, name, price, quantity))
            self.update_cart_display()
            qty_entry.delete(0, tk.END)
            qty_entry.insert(0, "1")
            messagebox.showinfo("Added", f"{name} added to cart!")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def update_cart_display(self):
        """Update cart display"""
        self.cart_text.delete(1.0, tk.END)

        if not self.cart:
            self.cart_text.insert(tk.END, "\n\n\n")
            self.cart_text.insert(tk.END, "         🛒 Your cart is empty\n")
            self.cart_text.insert(tk.END, "\n         Start adding items from the menu!")
            return

        self.cart_text.insert(tk.END, f"{'ITEM':<28} {'QTY':<6} {'PRICE':<10} {'TOTAL':<10}\n")
        self.cart_text.insert(tk.END, "─" * 58 + "\n")

        subtotal = 0
        for item_id, name, price, qty in self.cart:
            total = price * qty
            subtotal += total
            name_display = name[:25] + "..." if len(name) > 25 else name
            self.cart_text.insert(
                tk.END,
                f"{name_display:<28} {qty:<6} ₹{price:<9.2f} ₹{total:<9.2f}\n"
            )

        gst = subtotal * 0.05
        grand_total = subtotal + gst

        self.subtotal_label.config(text=f"Subtotal: ₹ {subtotal:.2f}")
        self.gst_label.config(text=f"GST (5%): ₹ {gst:.2f}")
        self.total_label.config(text=f"TOTAL: ₹ {grand_total:.2f}")

    def clear_cart(self):
        """Clear cart"""
        if not self.cart:
            messagebox.showinfo("Empty", "Cart is already empty!")
            return

        result = messagebox.askyesno("Clear Order", "Remove all items from cart?")
        if result:
            self.cart = []
            self.update_cart_display()

    def generate_bill(self):
        """Generate final bill"""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items first!")
            return

        order_items = [(item_id, qty) for item_id, _, _, qty in self.cart]
        order_id, total = orders.create_order(order_items)

        if order_id:
            self.show_bill_window(order_id, order_items)
            self.cart = []
            self.update_cart_display()

    def show_bill_window(self, order_id, order_items):
        """Display elegant invoice"""
        bill_window = tk.Toplevel(self.root)
        bill_window.title(f"Invoice #{order_id}")
        bill_window.geometry("700x800")
        bill_window.configure(bg='white')

        bill_data = billing.calculate_bill(order_items)

        # Header
        header_frame = tk.Frame(bill_window, bg=self.colors['dark'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="☕ ARTISAN CAFÉ",
            font=self.fonts['title'],
            bg=self.colors['dark'],
            fg='white'
        ).pack(pady=(20, 5))

        tk.Label(
            header_frame,
            text="— INVOICE —",
            font=self.fonts['body'],
            bg=self.colors['dark'],
            fg=self.colors['secondary']
        ).pack()

        # Invoice details
        info_frame = tk.Frame(bill_window, bg='white')
        info_frame.pack(fill='x', padx=30, pady=20)

        tk.Label(
            info_frame,
            text=f"Invoice No: #{order_id}",
            font=self.fonts['subheading'],
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w')

        tk.Label(
            info_frame,
            text=f"Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            font=self.fonts['body'],
            bg='white',
            fg=self.colors['dark']
        ).pack(anchor='w', pady=5)

        # Bill content
        bill_text = scrolledtext.ScrolledText(
            bill_window,
            width=75,
            height=22,
            font=tkFont.Font(family='Consolas', size=11),
            bg='#FAFAFA',
            relief='flat',
            padx=20,
            pady=20
        )
        bill_text.pack(padx=30, pady=10, fill='both', expand=True)

        bill_text.insert(tk.END, f"{'ITEM':<40} {'QTY':<6} {'PRICE':<12} {'TOTAL':<12}\n")
        bill_text.insert(tk.END, "═" * 72 + "\n\n")

        for item in bill_data['items']:
            bill_text.insert(
                tk.END,
                f"{item['name']:<40} {item['quantity']:<6} "
                f"₹ {item['price']:<10.2f} ₹ {item['total']:<10.2f}\n"
            )

        bill_text.insert(tk.END, "\n" + "─" * 72 + "\n")
        bill_text.insert(tk.END, f"{'Subtotal:':<58} ₹ {bill_data['subtotal']:.2f}\n")
        bill_text.insert(tk.END, f"{'GST (5%):':<58} ₹ {bill_data['gst_amount']:.2f}\n")
        bill_text.insert(tk.END, "═" * 72 + "\n")
        bill_text.insert(tk.END, f"{'GRAND TOTAL:':<58} ₹ {bill_data['grand_total']:.2f}\n")
        bill_text.insert(tk.END, "═" * 72 + "\n\n")
        bill_text.insert(tk.END, " " * 18 + "Thank you for visiting Artisan Café!\n")
        bill_text.insert(tk.END, " " * 22 + "Please visit us again! ☕")

        bill_text.config(state='disabled')

        # Close button
        tk.Button(
            bill_window,
            text="Close Invoice",
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['subheading'],
            width=20,
            cursor='hand2',
            relief='flat',
            bd=0,
            pady=12,
            command=bill_window.destroy
        ).pack(pady=20)


def main():
    root = tk.Tk()
    CafeBillingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
