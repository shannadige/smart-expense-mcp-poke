# Smart Expense Tracker - Poke MCP Hackathon

## 🎯 Hackathon Strategy
**Target Prize**: Most Practical MCP Automation
- Universal need - everyone tracks expenses
- Simple concept, sophisticated execution
- Perfect for iMessage interface

## 💡 Core Concept
An intelligent expense tracker that works through natural language via Poke's iMessage interface. Users text expenses naturally, and the MCP automatically categorizes, stores, and provides insights.

### Example Interactions:
- **User**: "Spent $15 on lunch at McDonald's"
- **Poke**: "✅ Logged $15 food expense. You've spent $45 on food this week (75% of budget)"

- **User**: "How much did I spend on coffee this month?"
- **Poke**: "You spent $67 on coffee this month across 14 purchases. That's $23 more than last month!"

## 🛠 Technical Architecture

### Phase 1: Core MVP (6-8 hours)
#### Tools to Implement:
1. **`log_expense(description: str, amount: float, category: str = None)`**
   - Parse natural language: "spent $15 on lunch" → amount: 15, category: "food"
   - Store in local database

2. **`get_spending_summary(period: str = "week")`**
   - Return spending by category for week/month/year

3. **`search_expenses(query: str, limit: int = 10)`**
   - Find expenses by description, category, or amount range

#### Data Storage:
- SQLite database with expenses table
- Schema: id, amount, category, description, date, location (optional)

#### Smart Categorization:
- Rule-based system with keyword matching
- Categories: Food, Transportation, Shopping, Entertainment, Bills, Health, Other

### Phase 2: Intelligence Layer (4-6 hours)
#### Additional Tools:
4. **`set_budget(category: str, amount: float, period: str = "month")`**
   - Set spending limits by category

5. **`get_budget_status()`**
   - Show progress toward budgets with alerts

6. **`analyze_spending_patterns()`**
   - Weekly patterns, location-based insights, trend analysis

#### Smart Features:
- Location detection from description
- Duplicate detection
- Spending alerts and warnings

### Phase 3: Advanced Features (if time allows)
7. **`split_expense(description: str, amount: float, people: list)`**
   - Handle shared expenses and bill splitting

8. **`predict_monthly_spend(category: str = None)`**
   - Forecast spending based on current patterns

## 📊 Data Model
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE budgets (
    id INTEGER PRIMARY KEY,
    category TEXT UNIQUE,
    amount REAL NOT NULL,
    period TEXT DEFAULT 'month',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Implementation Timeline
- **Day 1 Morning**: Setup, core expense logging
- **Day 1 Afternoon**: Categorization, basic queries
- **Day 1 Evening**: Budget tracking, alerts
- **Day 2 Morning**: Smart insights, pattern analysis
- **Day 2 Afternoon**: Polish, testing, deployment

## 🎪 Demo Strategy
1. **Setup demo expenses** across different categories
2. **Show natural language parsing**: "grabbed coffee for $4.50"
3. **Demonstrate insights**: spending patterns, budget alerts
4. **Highlight practicality**: "This could replace my expense tracking apps"

## 🏆 Competitive Advantages
- **Effortless logging**: No app switching, just text
- **Smart categorization**: Learns from your descriptions
- **Contextual insights**: Not just tracking, but understanding
- **iMessage native**: Fits naturally into daily workflow