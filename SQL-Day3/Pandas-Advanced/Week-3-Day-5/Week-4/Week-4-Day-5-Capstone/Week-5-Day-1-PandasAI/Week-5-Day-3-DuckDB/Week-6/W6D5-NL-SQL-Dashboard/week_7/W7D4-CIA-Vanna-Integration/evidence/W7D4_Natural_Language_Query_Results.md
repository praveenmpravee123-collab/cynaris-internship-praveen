# W7D4 – Natural Language Query Results

## CIA SQL Mode – Vanna Integration

**Database:** CRM SQLite Database  
**Table:** customers  
**LLM:** Ollama – qwen2.5:3b  
**API Endpoint:** POST `/cia/sql-analyst`

## Natural Language Query Tests

### 1. Total Customer Count

**Question:** How many customers are there in the CRM database?

**Vanna Result:** 100 customers.

### 2. Total Deal Value

**Question:** What is the total deal value of all customers?

**Vanna Result:** ₹24,875,000.

### 3. Won Deals

**Question:** How many deals are in the Won stage?

**Vanna Result:** 22 deals.

### 4. Lost Deals

**Question:** How many deals are in the Lost stage?

**Vanna Result:** 10 deals.

### 5. Customers by Lead Source

**Question:** How many customers came from each lead source?

**Vanna Result:**

- Cold Call: 11
- Email Campaign: 19
- LinkedIn: 19
- Referral: 24
- Trade Show: 17
- Website: 10

### 6. Customers by Sales Representative

**Question:** How many customers are handled by each sales representative?

**Vanna Result:**

- Aditi Rao: 13
- Arjun Das: 13
- Karthik Nair: 19
- Priya Shah: 20
- Rahul Menon: 19
- Sneha Iyer: 16

### 7. Highest Deal Value

**Question:** Who is the customer with the highest deal value? Show the customer name, company, and deal value.

**Vanna Result:**

- Customer: Ananya Iyer
- Company: DeltaWorks
- Deal Value: ₹500,000

### 8. Average Deal Value

**Question:** What is the average deal value of all customers?

**Vanna Result:** ₹248,750.

### 9. Negotiation Deals

**Question:** How many deals are currently in the Negotiation stage?

**Vanna Result:** 11 deals.

### 10. Deal Stage Distribution

**Question:** What is the distribution of customers across different deal stages?

**Vanna Result:**

- Lost: 10
- Negotiation: 11
- New Lead: 14
- Proposal: 15
- Qualified: 28
- Won: 22

## Verification Notes

All 10 Natural Language Query results were independently
verified against the CRM SQLite database.

The Vanna Agent responses matched the corresponding
SQL query results for all 10 test cases.

**Verification Status: PASS – 10/10 queries matched.**
