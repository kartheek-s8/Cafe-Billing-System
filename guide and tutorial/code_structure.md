# Artisan Café Management System - Code Structure

## 📁 Project Directory Structure


Cafe-Billing-System/
│
├── src/ # Source code directory
│ ├── main_app.py # Main entry point - launches login screen
│ ├── login_screen.py # Role selection & authentication
│ ├── customer_app.py # Customer ordering interface (GUI)
│ ├── admin_dashboard.py # Admin control panel with analytics
│ ├── analytics.py # Data analytics & chart generation
│ ├── db.py # Database connection & queries
│ ├── orders.py # Order management logic
│ └── billing.py # Bill calculation & invoice generation
│
├── sql/ # Database scripts
│ ├── schema.sql # Database schema (tables creation)
│ └── seed.sql # Sample data for testing
│
├── guide and tutorial/ # Documentation
│ ├── code_structure.md # This file - project structure
│ └── steps_before_u_start_coding.md # Setup instructions
│
└── reports/ # Generated reports (future use)




---

## 🔧 Module Descriptions

### 1. **main_app.py** - Application Entry Point
**Purpose:** Main launcher that displays the login screen first

**Key Functions:**
- `main()` - Entry point, creates login window
- `launch_customer_app()` - Opens customer ordering interface
- `launch_admin_dashboard()` - Opens admin control panel

**Flow:**


Run main_app.py → Login Screen → Customer/Admin Mode

---

### 2. **login_screen.py** - Authentication System
**Purpose:** User role selection and admin authentication

**Key Features:**
- Dual-mode selection (Customer vs Admin)
- Admin password verification via database
- Professional UI with role cards
- Database credential validation

**Classes:**
- `LoginScreen` - Handles login UI and authentication

**Database Connection:**
- Queries `Admin` table for username/password verification
- Default credentials: `admin` / `cafe123`

---

### 3. **customer_app.py** - Customer Interface
**Purpose:** Beautiful GUI for customers to browse menu and place orders

**Key Features:**
- Scrollable menu display by category
- Add items to cart with quantity selection
- Live cart preview with running total
- Real-time GST calculation (5%)
- Professional invoice generation

**Classes:**
- `CafeBillingGUI` - Main customer interface

**Key Methods:**
- `load_menu()` - Fetches and displays menu items
- `add_to_cart()` - Adds items with validation
- `update_cart_display()` - Updates cart view and totals
- `generate_bill()` - Creates order and shows invoice
- `show_bill_window()` - Displays formatted receipt

**Design:**
- Premium color palette (coffee browns, cream, gold accents)
- Custom fonts (Garamond, Georgia, Segoe UI)
- Professional layout with cards and sections

---

### 4. **admin_dashboard.py** - Admin Control Panel
**Purpose:** Complete admin interface with analytics and management

**Key Features:**
- 3 tabbed interface (Dashboard, Orders, Menu)
- Real-time sales statistics
- Interactive data tables
- Bulk delete operations (Ctrl+Click multi-select)
- Refresh functionality

**Classes:**
- `AdminDashboard` - Main admin interface

**Tabs:**

#### Tab 1: Dashboard (Analytics)
- Today's sales card
- Today's orders count card
- Top 5 selling items (bar chart)
- Sales by category (pie chart)
- Weekly sales trend (line chart)
- Refresh button

**Methods:**
- `create_dashboard_tab()` - Build analytics view
- `load_charts()` - Render all visualizations
- `refresh_dashboard()` - Reload all data

#### Tab 2: Order Records
- Complete order history table
- Multi-select support (Ctrl+Click)
- Delete selected orders
- Delete all orders (double confirmation)
- Refresh orders

**Methods:**
- `create_orders_tab()` - Build orders table
- `load_order_records()` - Fetch from database
- `delete_selected_order()` - Bulk delete with confirmation
- `delete_all_orders()` - Clear entire history

#### Tab 3: Menu Management
- All menu items in table format
- Multi-select support (Ctrl+Click)
- Delete selected items
- Refresh menu

**Methods:**
- `create_menu_tab()` - Build menu table
- `load_menu_items()` - Fetch from database
- `delete_selected_menu_item()` - Bulk delete items

---

### 5. **analytics.py** - Data Analytics Engine
**Purpose:** Generate charts and calculate business metrics

**Key Features:**
- Sales trend analysis
- Top items calculation
- Category breakdown
- Chart generation using matplotlib

**Classes:**
- `Analytics` - Data processing and visualization

**Key Methods:**
- `get_total_sales_today()` - Today's revenue
- `get_total_orders_today()` - Today's order count
- `get_top_selling_items(limit)` - Most popular items
- `get_sales_by_category()` - Revenue by category
- `get_last_7_days_sales()` - Weekly trend data
- `create_top_items_chart()` - Horizontal bar chart
- `create_category_chart()` - Pie chart
- `create_weekly_sales_chart()` - Line chart with area fill

**Technologies:**
- matplotlib for charts
- matplotlib.backends.backend_tkagg for Tkinter integration
- Custom color schemes matching cafe theme

---

### 6. **db.py** - Database Layer
**Purpose:** Centralized database connection and queries

**Key Functions:**
- `get_connection()` - Creates MySQL connection
- `fetch_menu_items()` - Retrieves all menu items with category
- `add_menu_item(name, price, category)` - Insert new item
- `add_order(order_id, item_id, quantity, total)` - Record order

**Configuration:**




**Error Handling:**
- Try-except blocks for connection errors
- Graceful failure with error messages

---

### 7. **orders.py** - Order Management
**Purpose:** Handle order creation and processing

**Key Functions:**
- `create_order(order_items)` - Process new order
  - Generates unique order ID
  - Inserts each item into Orders table
  - Returns order_id and total amount
- `get_order_details(order_id)` - Fetch specific order
- `display_order_summary(order_id)` - Show order info

**Order Flow:**

Customer adds items → create_order() → Database insertion → Return order_id


---

### 8. **billing.py** - Billing Engine
**Purpose:** Calculate bills and generate invoices

**Key Functions:**
- `calculate_bill(order_items)` - Compute totals
  - Fetches item prices from database
  - Calculates subtotal
  - Applies 5% GST
  - Returns detailed breakdown
- `generate_bill(order_id, order_items)` - Display formatted invoice

**Bill Structure:**
Items List (name, quantity, price, total)
─────────────────────────────
Subtotal
GST (5%)
═════════════════════════════
GRAND TOTAL


---

## 🗄️ Database Schema

### Table: `MenuItem`
id INT PRIMARY KEY AUTO_INCREMENT
name VARCHAR(100) NOT NULL
price DECIMAL(10,2) NOT NULL
category VARCHAR(50)



**Purpose:** Store all cafe menu items

### Table: `Orders`
order_id INT NOT NULL
item_id INT
quantity INT
total_amount DECIMAL(10,2)
order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
FOREIGN KEY (item_id) REFERENCES MenuItem(id)


**Purpose:** Record all customer orders

### Table: `Admin`
id INT PRIMARY KEY AUTO_INCREMENT
username VARCHAR(50) NOT NULL UNIQUE
password VARCHAR(100) NOT NULL
role VARCHAR(20) DEFAULT 'admin'
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP



**Purpose:** Store admin credentials for authentication

---

## 🎨 Design System

### Color Palette
Primary (Coffee Brown): #8B7355
Secondary (Caramel): #C4A57B
Accent (Gold): #D4AF37
Background (Cream): #F5F0E8
Dark (Espresso): #4A3428
Light (Ivory): #FFF8F0
Card (White): #FFFFFF
Success (Olive): #6B8E23



### Fonts

Title: Garamond, 28-36pt, Bold
Heading: Georgia, 16-20pt, Bold
Body: Segoe UI, 11-12pt
Stats: Arial, 24pt, Bold



---

## 🔄 Application Flow

### Customer Flow
main_app.py
↓
login_screen.py (Click "Continue as Customer")
↓
customer_app.py (Browse Menu)
↓
Add items to cart
↓
Generate Bill (orders.py + billing.py)
↓
Show Invoice


### Admin Flow
main_app.py
↓
login_screen.py (Click "Login as Admin")
↓
Enter credentials (verified against Admin table)
↓
admin_dashboard.py
↓
Dashboard Tab: View analytics & charts (analytics.py)
Orders Tab: Manage order history
Menu Tab: Manage menu items
↓
Logout → Back to login



---

## 📊 Data Flow

### Order Processing
Customer → customer_app.py → orders.py → db.py → MySQL
↓
billing.py (calculate)
↓
Display Invoice



### Analytics Generation
admin_dashboard.py → analytics.py → db.py → MySQL
↓
matplotlib charts
↓
Display in dashboard



---

## 🛠️ Technologies Used

**Frontend:**
- Python Tkinter (GUI framework)
- tkinter.ttk (Enhanced widgets)

**Backend:**
- Python 3.x
- MySQL Connector

**Database:**
- MySQL Server

**Data Visualization:**
- matplotlib
- pandas (optional)
- numpy (optional)

**Design:**
- Custom fonts (Garamond, Georgia, Segoe UI)
- Professional color scheme
- Responsive layouts

---

## 🚀 Key Features Implementation

### 1. Authentication System
- **File:** `login_screen.py`
- **Method:** Database verification
- **Security:** Password validation against Admin table

### 2. Real-time Cart Management
- **File:** `customer_app.py`
- **Feature:** Live updates with running total
- **Technology:** Tkinter StringVar and Label updates

### 3. Data Visualization
- **File:** `analytics.py`
- **Charts:** Bar, Pie, Line with custom styling
- **Integration:** matplotlib embedded in Tkinter

### 4. Bulk Operations
- **Files:** `admin_dashboard.py`
- **Feature:** Multi-select with Ctrl+Click
- **Method:** Treeview `selectmode='extended'`

### 5. Modular Architecture
- **Separation of concerns:** Each file has specific purpose
- **Reusability:** Functions can be called from multiple places
- **Maintainability:** Easy to update individual modules

---

## 📝 Code Quality

### Best Practices Followed:
✅ Modular design (separate files for each function)
✅ Clear function names and documentation
✅ Error handling (try-except blocks)
✅ Database connection management (open/close)
✅ User input validation
✅ Confirmation dialogs for destructive actions
✅ Consistent naming conventions
✅ Professional UI/UX design
✅ Comments for complex logic

---

## 🔮 Future Enhancements

**Potential features to add:**
1. Add/Edit menu items from GUI
2. Export reports to PDF
3. Email invoice functionality
4. Payment method selection (Cash/Card/UPI)
5. Customer loyalty program
6. Inventory management
7. Employee management
8. Table reservation system
9. Multi-location support
10. Mobile app integration

---

## 📚 Learning Resources

**Python Tkinter:**
- Official Tkinter Documentation
- Real Python Tkinter Tutorials

**MySQL with Python:**
- MySQL Connector Documentation
- Database Design Best Practices

**Data Visualization:**
- matplotlib Documentation
- Chart Design Guidelines

---

## 👨‍💻 Developer Information

**Project:** Artisan Café Management System
**Level:** Class 12 CBSE Computer Science Project
**Academic Year:** 2025-2026
**Technologies:** Python, Tkinter, MySQL, matplotlib
**Lines of Code:** 1000+ lines
**Development Time:** 30 day intensive development


---

**Last Updated:** October 13, 2025
