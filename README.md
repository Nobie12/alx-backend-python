# Python Generators for Efficient Data Streaming and Processing

## 📖 About the Project

This project introduces the advanced usage of **Python Generators** to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations.

The focus is on leveraging Python’s `yield` keyword to implement generators that provide **iterative access to data**, promoting **optimal resource utilization** and **improved performance** in data-driven applications.

---

## 🎯 Learning Objectives

By completing this project, you will:

✅ **Master Python Generators:**  
Learn how to create and use generators for iterative data processing, enabling **memory-efficient** operations on large datasets.

✅ **Handle Large Datasets:**  
Implement **batch processing** and **lazy loading** techniques to work with extensive datasets without exhausting system memory.

✅ **Simulate Real-World Scenarios:**  
Develop solutions that simulate **live data streaming and updates**, applying generators to **real-time data contexts**.

✅ **Optimize Performance:**  
Use generators to compute aggregate functions (like averages) on large datasets while minimizing memory consumption.

✅ **Apply SQL Knowledge:**  
Integrate **SQL queries** dynamically with Python to fetch, manage, and stream data from databases in a **robust and scalable** manner.

---

## ⚙️ Technologies Used

- **Python 3.x**
- **MySQL / SQLite**
- **SQL Queries**
- **CSV Data Processing**
- **Python Generators (`yield`)**
- **Git & GitHub**

---

## 📌 Project Structure

```bash
├── seed.py               # Core script for database setup and data streaming
├── user_data.csv         # Sample dataset for seeding the database
├── 0-main.py             # Main script for testing the database operations
└── README.md             # Project documentation
```

## 🏗️ Key Features

- ✅ **Database Setup:**  
  Creates a **MySQL** database `ALX_prodev` and a table `user_data` with **UUID-based primary keys**.

- ✅ **Data Seeding:**  
  Reads user data from a **CSV file** and populates the database while **preventing duplicate entries**.

- ✅ **Data Streaming:**  
  Implements a **Python generator** to stream rows **one by one** from the database, ensuring **low memory footprint**.

- ✅ **Live Data Simulation:**  
  Demonstrates how **generators** can be used to **mimic real-time data streaming**.

---

## 📥 Requirements

To get the most out of this project, you should have:

- Proficiency in **Python 3.x**.
- A solid understanding of `yield` and **Python generator functions**.
- Familiarity with **SQL** and **MySQL database operations**.
- Basic knowledge of **database schema design** and **data seeding**.
- The ability to use **Git** and **GitHub** for **version control** and **submission**.
