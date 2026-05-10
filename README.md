# 📊 Data Dashboard Pro

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Pandas](https://img.shields.io/badge/Data-Pandas-orange)
![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-red)

> A powerful desktop data visualization tool built with **Python + Tkinter** that allows you to load, create, analyze, and visualize datasets with ease.

---
## 🚀 Installation & Demo

To run the application without setting up a local development environment, you can download the pre-compiled executable:

* **Windows (.exe):** [Download from Google Drive](https://drive.google.com/file/d/1sfL7WvOjH0g_EZsiXdpm_iaT4IhP-iw3/view?usp=drive_link)

---

## ✨ Features

### 📂 Data Handling

* Load datasets from:

  * CSV files
  * Excel files (.xlsx)
* Create **custom datasets manually** (up to 30 data points)
* Automatic column detection

---

### 📊 Visualization Options

* Line Plot
* Scatter Plot
* Bar Chart
* Histogram
* Box Plot

---

### 🎨 Customization

* Custom graph titles
* Multiple color options
* Line styles (Solid, Dashed, etc.)
* Marker styles (Circle, Square, Triangle, etc.)

---

### ⚙️ Advanced Features

* 📈 **Best Fit Line** (Linear regression using NumPy)
* 🧩 **Overlay Mode** for comparisons
* 🔲 Toggle grid and legend
* 🖱️ **Click-to-Annotate** points on graph
* 🧹 Clear graph instantly

---

### 📉 Data Insights

* Displays:

  * Mean
  * Median
  * Min / Max
* Missing value summary
* Dataset shape (rows × columns)

---

## 🖼️ UI Overview

* **Sidebar (Left)**

  * Data loading & creation
  * Graph configuration
  * Dataset statistics

* **Graph Panel (Right)**

  * Interactive Matplotlib canvas
  * Toolbar for zoom, pan, save

---

## 🚀 Getting Started

### 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/data-dashboard-pro.git
cd data-dashboard-pro
```

2. Install dependencies:

```bash
pip install pandas numpy matplotlib openpyxl
```

---

### ▶️ Run the Application

```bash
python main.py
```

---

## 📁 Supported File Formats

| Format        | Supported |
| ------------- | --------- |
| CSV           | ✅         |
| Excel (.xlsx) | ✅         |

---

## 🧠 How It Works

* Uses **Pandas** for data manipulation
* Uses **Matplotlib** for plotting
* Embeds plots inside Tkinter via:

  * `FigureCanvasTkAgg`
  * `NavigationToolbar2Tk`
* Applies **NumPy polyfit** for regression (best-fit line)

---

## ⚠️ Known Limitations

* Histogram and Box Plot only support **numeric data**
* Manual dataset limited to **30 entries**
* No persistent saving of graphs or sessions
* Large datasets may slow down UI rendering

---

## 💡 Future Improvements

* Multi-dataset comparison
* Real-time data streaming
* Drag-and-drop file upload
* Advanced analytics (correlation, heatmaps)

---

## 🏗️ Tech Stack

* **Python**
* **Tkinter** (GUI)
* **Pandas**
* **NumPy**
* **Matplotlib**

---

## 👨‍💻 Author

**Utkarsh Gupta**

---
