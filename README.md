# 💬 WhatsApp Chat Analyzer

A Data Analytics web application that provides detailed insights and visualizations from WhatsApp chat exports. Upload your chat file and instantly discover messaging patterns, activity trends, most active users, word frequencies, emojis, and more.

---

# 🚀 Features

### 📊 Chat Statistics
- Total Messages
- Total Words
- Media Shared Count
- Links Shared Count

### 👥 User Analysis
- Most Active Users
- User Contribution Percentage
- Individual User Statistics

### 📈 Activity Analysis
- Daily Timeline
- Monthly Timeline
- Weekly Activity Pattern
- Monthly Activity Pattern

### ⏰ Heatmap Visualization
- Most Active Days
- Most Active Months
- Weekly Activity Heatmap

### 🔤 Text Analysis
- Most Common Words
- Word Frequency Analysis
- Stopword Removal

### 😀 Emoji Analysis
- Most Used Emojis
- Emoji Distribution Chart


---

# 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Regex
- Emoji Library

---

# 📂 Dataset

This project uses exported WhatsApp chat files in `.txt` format.

### Export Chat

1. Open WhatsApp
2. Open any chat/group
3. Click **More Options**
4. Select **Export Chat**
5. Choose **Without Media**
6. Upload the exported `.txt` file

---

# ⚙️ How It Works

### Data Preprocessing
- Parse WhatsApp chat format
- Extract dates and times
- Identify users and messages

### Feature Engineering
- Message count
- Word count
- Media detection
- Link extraction
- Emoji extraction

### Data Visualization
- Timelines
- Heatmaps
- Bar Charts
- Pie Charts

---



# 📁 Project Structure

```text
whatsapp-chat-analyzer/
│
├── app.py
├── helper.py
├── preprocessor.py
├── requirements.txt
├── README.md
```

---

# 🔧 Installation

### Clone Repository

```bash
git clone https://github.com/meetgajera12/whatsapp-chat-analyzer.git
```

### Navigate to Project Directory

```bash
cd whatsapp-chat-analyzer
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

# 🎯 Key Insights Generated

✅ Most active participant

✅ Peak chatting hours

✅ Daily and monthly activity trends

✅ Most used words

✅ Most used emojis

✅ Media sharing statistics

✅ Link sharing statistics

---

# 🌟 Future Enhancements

- Sentiment Analysis
- AI-based Conversation Summary
- Topic Modeling
- Multi-language Support
- Export Reports as PDF
- Advanced User Comparison

---

# 👨‍💻 Author

**Meet Gajera**

Data Science & Machine Learning Student

GitHub: https://github.com/meetgajera12

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Feedback and contributions are always welcome!
