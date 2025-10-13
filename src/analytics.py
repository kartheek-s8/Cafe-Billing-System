# analytics.py - Analytics and Chart Generation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
from datetime import datetime, timedelta


class Analytics:
    def __init__(self):
        self.colors = {
            'primary': '#8B7355',
            'accent': '#D4AF37',
            'success': '#6B8E23',
            'chart_bg': '#F5F0E8'
        }

    def get_connection(self):
        """Get database connection"""
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='kartheek',
            database='cafe_billing'
        )

    def get_total_sales_today(self):
        """Get today's total sales"""
        conn = self.get_connection()
        cursor = conn.cursor()

        today = datetime.now().date()
        cursor.execute("""
            SELECT SUM(total_amount) FROM Orders 
            WHERE DATE(order_date) = %s
        """, (today,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result[0] else 0.0

    def get_total_orders_today(self):
        """Get today's total orders count"""
        conn = self.get_connection()
        cursor = conn.cursor()

        today = datetime.now().date()
        cursor.execute("""
            SELECT COUNT(DISTINCT order_id) FROM Orders 
            WHERE DATE(order_date) = %s
        """, (today,))

        result = cursor.fetchone()
        conn.close()

        return result[0] if result[0] else 0

    def get_top_selling_items(self, limit=5):
        """Get top selling menu items"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.name, SUM(o.quantity) as total_quantity
            FROM Orders o
            JOIN MenuItem m ON o.item_id = m.id
            GROUP BY o.item_id, m.name
            ORDER BY total_quantity DESC
            LIMIT %s
        """, (limit,))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_sales_by_category(self):
        """Get sales breakdown by category"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.category, SUM(o.total_amount) as total_sales
            FROM Orders o
            JOIN MenuItem m ON o.item_id = m.id
            GROUP BY m.category
            ORDER BY total_sales DESC
        """)

        results = cursor.fetchall()
        conn.close()

        return results

    def get_last_7_days_sales(self):
        """Get sales for last 7 days"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DATE(order_date) as date, SUM(total_amount) as total
            FROM Orders
            WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(order_date)
            ORDER BY date
        """)

        results = cursor.fetchall()
        conn.close()

        return results

    def create_top_items_chart(self, parent_frame):
        """Create bar chart for top selling items"""
        data = self.get_top_selling_items()

        if not data:
            return None

        items = [row[0][:15] for row in data]  # Truncate long names
        quantities = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.colors['chart_bg'])
        ax.set_facecolor('white')

        bars = ax.barh(items, quantities, color=self.colors['primary'])

        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height() / 2,
                    f'{int(width)}', ha='left', va='center', fontsize=10, fontweight='bold')

        ax.set_xlabel('Quantity Sold', fontsize=11, fontweight='bold')
        ax.set_title('Top 5 Selling Items', fontsize=13, fontweight='bold', pad=15)
        ax.invert_yaxis()
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()

        return canvas.get_tk_widget()

    def create_category_chart(self, parent_frame):
        """Create pie chart for sales by category"""
        data = self.get_sales_by_category()

        if not data:
            return None

        categories = [row[0] for row in data]
        sales = [float(row[1]) for row in data]

        fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.colors['chart_bg'])

        colors_palette = ['#8B7355', '#C4A57B', '#D4AF37', '#6B8E23']

        wedges, texts, autotexts = ax.pie(
            sales,
            labels=categories,
            autopct='%1.1f%%',
            colors=colors_palette,
            startangle=90
        )

        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        ax.set_title('Sales by Category', fontsize=13, fontweight='bold', pad=15)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()

        return canvas.get_tk_widget()

    def create_weekly_sales_chart(self, parent_frame):
        """Create line chart for last 7 days sales"""
        data = self.get_last_7_days_sales()

        if not data:
            return None

        dates = [row[0].strftime('%m/%d') for row in data]
        sales = [float(row[1]) for row in data]

        fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.colors['chart_bg'])
        ax.set_facecolor('white')

        ax.plot(dates, sales, marker='o', linewidth=2,
                markersize=8, color=self.colors['success'])

        # Fill area under the line
        ax.fill_between(range(len(dates)), sales, alpha=0.3, color=self.colors['success'])

        ax.set_xlabel('Date', fontsize=11, fontweight='bold')
        ax.set_ylabel('Sales (₹)', fontsize=11, fontweight='bold')
        ax.set_title('Last 7 Days Sales Trend', fontsize=13, fontweight='bold', pad=15)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()

        return canvas.get_tk_widget()
