# 🎓 UiTM Student Arrears Monitoring System

A **Decision Support System (DSS)** built with Streamlit to help UiTM’s Finance/Admin department monitor and analyze student fee arrears efficiently.  
This app enables the university to identify high-risk students, analyze arrears trends by school and semester, and simulate reminder notifications.

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

---

## 🧠 Key Features

- 📂 Upload CSV dataset of student arrears
- 📊 Dashboard with interactive filters (school, level, payment status, risk level)
- 📈 Charts:
  - Risk level & fuzzy priority distribution
  - Total arrears by school
  - Payment status by program level
  - Semester arrears trend
  - Fine description wordcloud
  - Arrears histogram & payment status pie chart
- 📧 Send Reminder (mockup) to high-risk students
- 💬 Static chatbot and finance contact info for user support

---

## 📁 Sample Dataset Format

Your CSV file should include the following columns:

| Column Name        | Description                            |
|--------------------|----------------------------------------|
| `Student_ID`       | Unique student identifier              |
| `Student_Name`     | Name of the student                    |
| `Level`            | Program level (e.g., Degree, Master)   |
| `School`           | Student’s faculty or school            |
| `Total_Fee`        | Total tuition/fee                      |
| `Amount_Paid`      | Amount already paid                    |
| `Total_Fine`       | Total fines incurred                   |
| `Status`           | Payment status (Paid, Partial, Unpaid) |
| `Fine_Descriptions`| Reason for fines (optional)            |
| `Intake`           | Semester or intake (e.g. Sept 2023)    |

---

## 🚀 How to Run Locally

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/student-arrears-monitoring.git
   cd student-arrears-monitoring
