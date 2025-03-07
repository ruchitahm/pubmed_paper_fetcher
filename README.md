# 📝 PubMed Paper Fetcher

This Python-based command-line tool fetches research papers from **PubMed** based on a user-provided query.  
It filters results to identify papers with **at least one author affiliated with a pharmaceutical or biotech company**  
and saves the results in a CSV file.

---

## 📁 **Project Structure**
```
pubmed_paper_fetcher/
├── papers_fetcher/        # Main package
│   ├── __init__.py        # Marks this as a package
│   ├── fetch_papers.py    # Main script to fetch papers
├── pyproject.toml         # Poetry configuration & dependencies
├── README.md              # Documentation
```

---

## ⚙️ **Installation & Setup**

### **1️⃣ Install Poetry (If Not Installed)**
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### **2️⃣ Clone the Repository**
```sh
git clone <YOUR_GITHUB_REPO_URL>
cd pubmed_paper_fetcher
```

### **3️⃣ Install Dependencies**
```sh
poetry install
```

---

## 🚀 **Usage**

### **Run the Program**
```sh
poetry run get-papers-list
```
- **It will prompt for a search query**  
- **Results are saved in `pubmed_papers.csv` by default**  

---

### **CLI Options**
| Option | Description |
|---------|-------------|
| `-h` or `--help` | Show usage instructions |
| `-d` or `--debug` | Print debug information during execution |
| `-f <filename>` | Save results to a specified CSV file |

#### **Example Usage**
```sh
poetry run get-papers-list -f results.csv
```
*Fetches papers & saves them to `results.csv` instead of `pubmed_papers.csv`*  

---

## 🛠 **Tools & Libraries Used**
### **🔹 Python Libraries**
- **[Requests](https://docs.python-requests.org/en/latest/)** - Fetch data from PubMed API  
- **[Pandas](https://pandas.pydata.org/)** - Process & save data in CSV format  
- **[Click](https://click.palletsprojects.com/)** - Build a user-friendly CLI  

### **🔹 Large Language Models (LLMs) Used**
- **ChatGPT (GPT-4o)** - Assisted in code design, debugging, and optimizations  

---

## 🛠 **Troubleshooting**
❌ **Command Not Found (`poetry`)?**  
✔️ Run:  
```sh
export PATH="$HOME/.local/bin:$HOME/.poetry/bin:$PATH"
```

❌ **No Results Found?**  
✔️ Try a broader search query. Example:  
```sh
Enter your search query: "cancer treatment"
```

---

## 📌 **Contributing**
Feel free to submit **pull requests** or open an **issue** if you encounter any problems!  

---

## 📝 **License**
MIT License © 2025 Ruchita Makwana

