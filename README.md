---

# 🔐 Cybersecurity Attack Detection System 🚀  

A **machine learning-powered** web application for detecting and classifying different types of cyber attacks.  
Built using **Streamlit, Scikit-Learn, XGBoost, TensorFlow**, and more! 🛡️  

---

## 📂 Project Structure 🏗️  

```plaintext
cybersecurity_detection/
├── Home.py                         # Main dashboard
├── pages/                          # Multi-page Streamlit app
│   ├── 1_Data_Analysis.py          # Data analysis & visualization
│   ├── 2_Model_Training.py         # Model training & evaluation
│   ├── 3_Single_Prediction.py      # Single attack prediction
│   └── 4_Batch_Prediction.py       # Bulk attack predictions
├── utils/                          # Utility functions
│   └── preprocessing.py            # Data preprocessing module
├── notebooks/                      # Jupyter Notebooks
│   └── model_development.ipynb     # ML model experimentation
├── data/
│   ├── sample/
│   │   ├── example_single.csv      # For single prediction
│   │   ├── example_batch.csv       # For batch prediction
│   │   └── training_sample.csv     # Sample training data
│   └── README.md                   # Data description
├── requirements.txt                # Required dependencies
├── LICENSE                         # MIT License
├── .gitignore                      # This .gitignore
└── README.md                       # Project documentation
```

---

## ✅ Prerequisites  

💻 **System Requirements:**  
- Python **3.8+** 🐍  
- `pip` (**Python package manager**)  🛠️ *(Pre-installed with Python but can be updated if needed)*  
- **Git** 🌍 *(Required for cloning the repository and version control)*   

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

# 💡 **Detailed Troubleshooting Guide**  

This guide provides solutions to **common installation issues, Streamlit errors, and model training challenges**.  

---

## ⚙️ **Common Installation Issues**  

### 🛠️ **1. Package Installation Errors**  

#### 🔹 **Windows**  
```bash
# Error: Microsoft Visual C++ 14.0 or greater is required
# Solution: Download and install Visual Studio Build Tools
# Visit: https://visualstudio.microsoft.com/downloads/
```

#### 🍏 **Mac**  
```bash
# Error: Permission denied
# Solution: Use sudo to install packages if necessary
sudo pip install -r requirements.txt
```

#### 🐧 **Linux**  
```bash
# Error: Missing Python.h
# Solution: Install python-dev package
sudo apt-get install python3-dev
```

---

## 🚀 **Streamlit Issues**  

### 🔥 **2. Port Already in Use**  
```bash
# Error: Address already in use
# Solution 1: Find and kill the process occupying the port
# Windows:
netstat -ano | findstr 8501

# Mac/Linux:
lsof -i :8501

# Solution 2: Run Streamlit on a different port
streamlit run Home.py --server.port 8502
```

### 🖥️ **3. Memory Issues**  
```bash
# Error: Memory error during batch processing
# Solution: Reduce batch size in code or increase system swap memory
```

---

## 🧠 **Model Training Issues**  

### ⚡ **4. CUDA Errors (if using GPU)**  
```bash
# Error: CUDA out of memory
# Solution: Reduce batch size or switch to CPU
```

### 📂 **5. Data Loading Issues**  
```bash
# Error: Unicode decode error
# Solution: Specify encoding format when reading CSV files
df = pd.read_csv("file.csv", encoding='utf-8')
```

---

## 💻 **OS-Specific Installation Guide**  

### 🏁 **Windows Setup**  

#### 1️⃣ **Install Python 3.8+**  
- Download from **[python.org](https://www.python.org/downloads/)**
- Ensure you check **"Add Python to PATH"** during installation  

#### 2️⃣ **Set up a virtual environment**  
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 3️⃣ **Common Windows Issues**  
- **If 'python' not found:** Use `py` instead  
- **If virtual environment activation fails:** Run PowerShell as administrator and execute:  
  ```powershell
  Set-ExecutionPolicy RemoteSigned
  ```

---

### 🍏 **MacOS Setup**  

#### 1️⃣ **Install Python using Homebrew**  
```bash
brew install python
```

#### 2️⃣ **Set up a virtual environment**  
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3️⃣ **M1/M2 Mac Specific Instructions**  
- Install **Rosetta 2** if needed for compatibility  
- Use **Miniforge** for ARM-based package installation  

---

### 🐧 **Linux Setup**  

#### 1️⃣ **Install Python and dependencies**  
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

#### 2️⃣ **Set up a virtual environment**  
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3️⃣ **Fix missing Tkinter (for GUI-related features)**  
```bash
sudo apt-get install python3-tk
```

---

## 📞 Contact & Support  

💬 **Have questions or found an issue?**  
📌 **Linkedin:** https://www.linkedin.com/in/dbkowrada (or)  Open an **issue** in the GitHub repository 🚀  
👨‍💻 We are welcome to improve this project! 🤝  

---

🔥 **Stay Secure, Stay Ahead!** 🛡️🚀  

---

