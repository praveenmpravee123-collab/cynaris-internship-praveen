# Brazilian E-Commerce Sales Analysis

## 1. Project Overview

This project analyzes Brazilian e-commerce data to understand sales performance, customer purchasing behavior, payment preferences, delivery performance, customer satisfaction, and seller performance.

The project uses the Brazilian E-Commerce Public Dataset by Olist. Python libraries are used to clean, process, analyze, and visualize the data to generate meaningful business insights.

## 2. Project Objectives

The main objectives of this project are:

- Analyze order status and order completion rates.
- Identify monthly order trends.
- Analyze monthly product sales.
- Identify the best-performing product categories.
- Understand customer purchasing behavior and repeat purchases.
- Analyze payment methods and payment values.
- Evaluate delivery performance.
- Understand customer satisfaction through review scores.
- Identify top-performing sellers.
- Provide actionable business recommendations.

## 3. Datasets Used

The project uses the following nine datasets:

1. Customers Dataset
2. Geolocation Dataset
3. Order Items Dataset
4. Order Payments Dataset
5. Order Reviews Dataset
6. Orders Dataset
7. Products Dataset
8. Sellers Dataset
9. Product Category Translation Dataset

These datasets provide information about customers, orders, products, sellers, payments, reviews, and geographical locations.

## 4. Tools and Technologies

The following tools and technologies were used:

- **Python:** Data analysis and processing.
- **Pandas:** Data manipulation and analysis.
- **NumPy:** Numerical operations.
- **Matplotlib:** Data visualization.
- **Seaborn:** Statistical visualization.
- **Jupyter Notebook:** Interactive analysis and documentation.
- **Visual Studio Code:** Development environment.

## 5. Data Cleaning and Preprocessing

The following data preparation activities were performed:

- Loaded the nine CSV datasets into Pandas DataFrames.
- Examined dataset dimensions and column information.
- Checked for duplicate records.
- Identified missing values.
- Converted order date columns into datetime format.
- Prepared data for monthly order and sales analysis.
- Merged related datasets to analyze product categories, customers, and sellers.
- Used product category translation data to display English category names.
- Calculated delivery durations and delivery delays.

Missing values were examined during data quality checks. Some missing dates in the orders dataset were retained because they can occur when orders are not fully processed or delivered.

## 6. Key Findings

### 6.1 Order Performance

- November 2017 recorded the highest monthly order volume, with **7,544 orders**.
- Monthly order volumes increased substantially throughout 2017.
- The order trend indicates that platform activity grew during the period covered by the dataset.
- The final months show a sharp decrease in recorded orders. This may be related to incomplete data at the end of the dataset and should not automatically be interpreted as a business decline.

### 6.2 Monthly Product Sales

- November 2017 recorded the highest monthly product sales, totaling **R$ 1,010,271.37**.
- Product sales generally increased during 2017 compared with the early months of the dataset.
- The analysis calculated product sales using the `price` column from the order items dataset.
- Freight charges were excluded from these product sales figures.

### 6.3 Product Category Performance

The top three product categories by product sales were:

1. **Health & Beauty:** R$ 1,258,681.34
2. **Watches & Gifts:** R$ 1,205,005.68
3. **Bed, Bath & Table:** R$ 1,036,988.68

Health & Beauty was the highest-performing category by product sales value in the analysis.

Other strong categories included Sports & Leisure, Computers & Accessories, and Furniture & Decor.

These findings can help the business identify categories that contribute substantially to product sales.

### 6.4 Customer Purchasing Behavior

The customer analysis focused on unique customers and successfully delivered orders.

- Total unique customers identified: **96,096**
- Customers with one delivered order: **90,557**
- Customers with multiple delivered orders: **2,801**
- Repeat customer percentage reported by the analysis: approximately **3.00%**

The results indicate that most customers in the analyzed data had only one delivered order.

The repeat-purchase rate suggests an opportunity to investigate customer retention and encourage customers to make additional purchases.

### 6.5 Payment Analysis

Payment analysis was performed using the order payments dataset.

The analysis examined:

- The number of payments by payment method.
- Total payment value by payment method.
- Average payment value by payment method.
- The most frequently used payment method.

The results can help the business understand customer payment preferences and identify the payment methods contributing the most payment value.

The exact payment-method results should be taken from the Payment Analysis output in the notebook.

### 6.6 Delivery Performance

Delivery performance was analyzed using delivered orders with valid purchase, delivery, and estimated delivery dates.

The analysis calculated:

- Average actual delivery time in days.
- Average estimated delivery time in days.
- Average delivery delay.
- Percentage of orders delivered on time or early.
- Distribution of actual delivery times.

These metrics help evaluate whether orders reached customers within the estimated delivery period.

The exact delivery statistics should be taken from the Delivery Performance Analysis output in the notebook.

### 6.7 Customer Review Analysis

Customer review analysis examined review scores from 1 to 5.

The analysis calculated:

- Total number of reviews.
- Average review score.
- Number and percentage of positive reviews, defined as scores of 4 or 5.
- Number and percentage of negative reviews, defined as scores of 1 or 2.

These results can help the business understand customer satisfaction and identify potential areas for service improvement.

The exact review statistics should be taken from the Customer Review Analysis output in the notebook.

### 6.8 Seller Performance

Seller performance was analyzed using the order items and sellers datasets.

The analysis examined:

- Total number of sellers.
- Number of distinct orders associated with each seller.
- Number of items sold by each seller.
- Total product sales by seller.
- The top 10 sellers by product sales.

Product sales were calculated using item prices and did not include freight charges.

The top-performing seller can be identified from the Seller Performance Analysis output in the notebook.

## 7. Business Recommendations

Based on the analysis performed, the following recommendations are proposed.

### 7.1 Improve Customer Retention

Since most customers had only one delivered order, the business could investigate strategies to encourage repeat purchases.

Possible approaches include customer loyalty programs, personalized product recommendations, and targeted promotional campaigns.

### 7.2 Focus on High-Performing Categories

Health & Beauty and Watches & Gifts generated the highest product sales among the analyzed categories.

The business could examine customer demand, product availability, pricing, and marketing opportunities in these categories.

### 7.3 Monitor Monthly Sales Trends

Monthly order and product sales trends should be monitored regularly to identify strong and weak periods.

The business could use these patterns to support inventory planning, marketing campaigns, and sales forecasting.

### 7.4 Improve Delivery Performance

Delivery delays should be monitored to identify possible issues involving shipping, seller processing, and logistics.

The business could investigate late deliveries and work with sellers and delivery partners to improve the customer experience.

### 7.5 Monitor Customer Satisfaction

Customer review scores should be monitored to identify recurring complaints and service issues.

Low review scores can be examined alongside delivery performance and order information to identify opportunities for improvement.

### 7.6 Support Effective Payment Options

The business should review payment-method usage and payment values to understand customer preferences.

Maintaining reliable and convenient payment options can support a smoother purchasing experience.

### 7.7 Evaluate Seller Performance

Seller performance should be monitored using product sales, order volume, and customer feedback.

This can help identify successful sellers and highlight sellers who may require operational support.

## 8. Limitations

The analysis has the following limitations:

- The findings are based on the available historical dataset.
- The dataset covers a specific period and may not represent current market conditions.
- Some records contain missing dates.
- The final months of the dataset have very low recorded order volumes, which may indicate incomplete data.
- Product sales calculations exclude freight charges.
- The analysis identifies patterns and associations but does not establish the causes of business outcomes.
- Some business metrics require further investigation before making operational decisions.

## 9. Conclusion

This project analyzed Brazilian e-commerce data to understand order trends, product sales, customer purchasing behavior, payment preferences, delivery performance, customer reviews, and seller performance.

The analysis identified November 2017 as the highest month for both recorded order volume and product sales. Health & Beauty was the leading product category by sales value, followed by Watches & Gifts and Bed, Bath & Table.

The customer analysis also indicated that most customers had only one delivered order, suggesting a potential opportunity to improve customer retention.

Overall, this project demonstrates how Python-based data analysis and visualization can transform raw e-commerce data into useful business insights.

The findings can support further investigation and data-driven decisions related to sales growth, customer experience, delivery operations, and seller performance.
