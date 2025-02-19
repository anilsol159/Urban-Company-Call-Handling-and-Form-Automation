# Urban Company Lead Management Automation  

## 📌 Overview  
This project automates lead handling on Urban Company's **ops.urbanclap.com** platform using **Python, Selenium, and Keyboard automation**. It streamlines the process of:  
- Accessing lead details  
- Connecting calls automatically  
- Handling form submissions  
- Closing tabs with a keypress (ALT key)  

This automation significantly **reduces manual effort** in managing and updating lead statuses.  

---

## 🚀 Features  
- **Automated Lead Selection**: Clicks on each lead sequentially.  
- **Call Handling**: Detects and clicks the "Connect" button automatically.  
- **Form Submission**: Detects if the call was connected or not, then auto-fills the lead status accordingly.  
- **Manual Review Support**: Allows users to manually update connected calls before proceeding.  
- **Keypress-based Workflow**:  
  - Press **SPACE** after a call ends to proceed.  
  - Press **ALT** to close the active tab and move to the next lead.  

---

## 🛠️ Tech Stack  
- **Python**  
- **Selenium** – for web automation  
- **Keyboard** – for user input detection  
- **Chrome WebDriver** – to control browser automation  

---

## ⚙️ Setup Instructions  

### 1️⃣ Install Dependencies  
Make sure you have Python installed, then install the required libraries:  
```bash
pip install selenium keyboard

### 2️⃣ Download Chrome WebDriver  
Ensure **Chrome WebDriver** is installed and matches your Chrome version.  
- Download from: [ChromeDriver](https://sites.google.com/chromium.org/driver/)  
- Place `chromedriver.exe` in the project directory.  

---

### 3️⃣ Configure Chrome Profile  
Update the following in the script to match your Chrome profile path:  
```python
options.add_argument("--user-data-dir=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("--profile-directory=YourProfile")
