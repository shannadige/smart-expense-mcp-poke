#!/usr/bin/env python3
import os
import sqlite3
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastmcp import FastMCP

mcp = FastMCP("Smart Expense Tracker")

# Database setup
DB_PATH = "expenses.db"

def init_database():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE,
            amount REAL NOT NULL,
            period TEXT DEFAULT 'month',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def parse_expense_text(text: str) -> Dict[str, any]:
    """Parse natural language expense description."""
    # Extract amount (look for $X.XX or $X patterns)
    amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', text.lower())
    amount = float(amount_match.group(1)) if amount_match else 0.0

    # Category mapping based on keywords
    categories = {
        'food': ['lunch', 'dinner', 'breakfast', 'coffee', 'restaurant', 'food', 'meal', 'snack', 'groceries', 'grocery', 'mcdonalds', 'starbucks', 'pizza'],
        'transportation': ['uber', 'lyft', 'taxi', 'bus', 'train', 'metro', 'parking', 'gas', 'fuel'],
        'shopping': ['store', 'mall', 'amazon', 'target', 'walmart', 'clothes', 'shirt', 'shoes'],
        'entertainment': ['movie', 'concert', 'show', 'game', 'bar', 'club', 'netflix', 'spotify'],
        'health': ['doctor', 'pharmacy', 'medicine', 'hospital', 'clinic', 'gym', 'fitness'],
        'bills': ['rent', 'electric', 'water', 'internet', 'phone', 'insurance', 'subscription'],
    }

    category = 'other'
    text_lower = text.lower()
    for cat, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            category = cat
            break

    # Extract location (look for "at [location]")
    location_match = re.search(r'\bat\s+([^$\d]+?)(?:\s|$)', text, re.IGNORECASE)
    location = location_match.group(1).strip() if location_match else None

    return {
        'amount': amount,
        'category': category,
        'description': text.strip(),
        'location': location,
        'date': datetime.now().isoformat()
    }

@mcp.tool(description="Log an expense from natural language description like 'spent $15 on lunch at McDonald's'")
def log_expense(description: str) -> str:
    """Parse and log an expense from natural language."""
    expense_data = parse_expense_text(description)

    if expense_data['amount'] <= 0:
        return "❌ Could not extract amount from description. Please include a dollar amount like '$15' or '$4.50'"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO expenses (amount, category, description, location, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        expense_data['amount'],
        expense_data['category'],
        expense_data['description'],
        expense_data['location'],
        expense_data['date']
    ))

    conn.commit()
    conn.close()

    location_text = f" at {expense_data['location']}" if expense_data['location'] else ""
    return f"✅ Logged ${expense_data['amount']:.2f} {expense_data['category']} expense{location_text}"

@mcp.tool(description="Get spending summary for a time period (week, month, year)")
def get_spending_summary(period: str = "week") -> str:
    """Get spending summary by category for the specified period."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Calculate date range
    now = datetime.now()
    if period.lower() == "week":
        start_date = (now - timedelta(days=7)).isoformat()
        period_name = "this week"
    elif period.lower() == "month":
        start_date = (now - timedelta(days=30)).isoformat()
        period_name = "this month"
    elif period.lower() == "year":
        start_date = (now - timedelta(days=365)).isoformat()
        period_name = "this year"
    else:
        start_date = (now - timedelta(days=7)).isoformat()
        period_name = "this week"

    cursor.execute('''
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM expenses
        WHERE date >= ?
        GROUP BY category
        ORDER BY total DESC
    ''', (start_date,))

    results = cursor.fetchall()

    if not results:
        conn.close()
        return f"📊 No expenses found for {period_name}"

    # Calculate total
    total_spent = sum(row[1] for row in results)

    # Build summary
    summary = f"📊 Spending Summary for {period_name}:\n\n"
    summary += f"💰 Total: ${total_spent:.2f}\n\n"

    for category, amount, count in results:
        percentage = (amount / total_spent) * 100
        summary += f"• {category.title()}: ${amount:.2f} ({count} transactions, {percentage:.1f}%)\n"

    conn.close()
    return summary

@mcp.tool(description="Search expenses by description, category, or amount range")
def search_expenses(query: str, limit: int = 10) -> str:
    """Search for expenses matching the query."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Try to parse as amount search first
    amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', query)
    if amount_match:
        amount = float(amount_match.group(1))
        cursor.execute('''
            SELECT amount, category, description, location, date
            FROM expenses
            WHERE amount = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (amount, limit))
    else:
        # Search in description, category, and location
        search_term = f"%{query}%"
        cursor.execute('''
            SELECT amount, category, description, location, date
            FROM expenses
            WHERE description LIKE ? OR category LIKE ? OR location LIKE ?
            ORDER BY date DESC
            LIMIT ?
        ''', (search_term, search_term, search_term, limit))

    results = cursor.fetchall()

    if not results:
        conn.close()
        return f"🔍 No expenses found matching '{query}'"

    response = f"🔍 Found {len(results)} expense(s) matching '{query}':\n\n"

    for amount, category, description, location, date in results:
        date_obj = datetime.fromisoformat(date)
        date_str = date_obj.strftime("%m/%d")
        location_str = f" at {location}" if location else ""
        response += f"• {date_str}: ${amount:.2f} - {description}{location_str}\n"

    conn.close()
    return response

# Initialize database on startup
init_database()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    print(f"Starting Smart Expense Tracker MCP server on {host}:{port}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    print(f"Database initialized: {os.path.exists(DB_PATH)}")

    try:
        mcp.run(
            transport="http",
            host=host,
            port=port,
            stateless_http=True
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        raise
