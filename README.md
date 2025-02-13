---

# 🔐 Cybersecurity Attack Detection System 🚀  

A **machine learning-powered** web application for detecting and classifying different types of cyber attacks.  
Built using **Streamlit, Scikit-Learn, XGBoost, TensorFlow**, and more! 🛡️  

---

## 📂 Project Structure 🏗️  

```plaintext
cybersecurity_detection/
├── Home.py                   # Main dashboard
├── pages/                    # Multi-page Streamlit app
│   ├── 1_Data_Analysis.py     # Data analysis & visualization
│   ├── 2_Model_Training.py    # Model training & evaluation
│   ├── 3_Single_Prediction.py # Single attack prediction
│   └── 4_Batch_Prediction.py  # Bulk attack predictions
├── utils/                     # Utility functions
│   └── preprocessing.py        # Data preprocessing module
├── notebooks/                 # Jupyter Notebooks
│   └── model_development.ipynb # ML model experimentation
├── data/
│   ├── sample/
│   │   ├── example_single.csv     # For single prediction
│   │   ├── example_batch.csv      # For batch prediction
│   │   └── training_sample.csv    # Sample training data
│   └── README.md                  # Data description
├── requirements.txt            # Required dependencies
├── LICENSE                     # MIT License
├── .gitignore                  # This .gitignore
└── README.md                   # Project documentation
```

---

## ✅ Prerequisites  

💻 **System Requirements:**  
- Python **3.8+** 🐍  
- `pip` (**Python package manager**)  

---

## ⚙️ Installation Steps 🛠️  

### 1️⃣ Clone the repository  

```bash
git clone https://github.com/yourusername/cybersecurity_detection.git
cd cybersecurity_detection
```

### 2️⃣ Set up a virtual environment  

#### For Windows 🏁  

```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux 🐧  

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install required dependencies  

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application  

### 1️⃣ Start the Streamlit app  

```bash
streamlit run Home.py
```

### 2️⃣ Access the web interface  

- Open your browser  
- Visit 👉 **http://localhost:8501**  

---

## 🛠️ Using the Application  

### 📊 **1. Data Analysis**  
🔹 Upload your cybersecurity dataset (CSV) 📂  
🔹 View statistics, distributions, and interactive visualizations 📈  

### 🤖 **2. Model Training**  
🔹 Upload labeled training data 🎯  
🔹 Select a **Machine Learning Model**:  
   - **Random Forest** 🌲  
   - **XGBoost** 🚀  
   - **Gradient Boosting** 🌟  
   - **Neural Network** 🧠  
🔹 Train & evaluate models with performance metrics  

### 🎯 **3. Making Predictions**  
🔹 **Single Prediction:** Enter individual network event details manually 📌  
🔹 **Batch Prediction:** Upload a CSV file for bulk attack detection 📑  

---

## 📥 Input Data Format  

Your **CSV file** must contain the following columns:  

- `Source Port`  
- `Destination Port`  
- `Packet Length`  
- `Anomaly Scores`  
- `Attack Signature`  
- `Source IP Address`  
- `Destination IP Address`    

---

## 🛠️ Troubleshooting & FAQs  

💡 **Issue: "Port already in use"**  
🔹 Run on a different port:  

```bash
streamlit run Home.py --server.port 8502
```

💡 **Issue: "Package installation errors"**  
🔹 Try upgrading pip and reinstalling dependencies:  

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

💡 **Performance Issues?**  
🔹 Optimize CSV file size before uploading  
🔹 Close unnecessary applications to free up RAM  

---

## 📞 Contact & Support  

💬 **Have questions or found an issue?**  
📌 Open an **issue** in the GitHub repository 🚀  
👨‍💻 We are welcome to improve this project! 🤝  

---

🔥 **Stay Secure, Stay Ahead!** 🛡️🚀  

---
