# 🔍 Nginx Log Analyzer

## 📌 Inventory
**Nginx Log Analyzer** — is an Nginx log analysis tool that:
- 📄 **Parsing logs** and converts them to CSV
- 🔎 **Filters** records by IP, status code, HTTP method, date range
- 🔀 **Sorts** records by response size, status code, etc.
- 🔄 **Automatically commits changes to the local Git repository**
- 🐳 **Has support for Docker**
- ⚙️ **Automated CI/CD with GitHub Actions**

---


## 🚀 How to launch?

### 🏗 1. Local launch (without Docker)
> 📌 Before starting, make sure you have **Python 3.12** and **Git** installed

#### 1.1. Set up dependencies:
   
```bash
pip install -r requirements.txt
```

#### 1.2. Run the log analysis script:

```
./run.sh --log-file logs/nginx.log --output-file formating-logs/logs.csv --sort-by size
```
> 📌 The script automatically initializes Git (if it does not exist) and commits changes




### 🐳 2. Launching via Docker
> 📌 You need to have Docker installed

#### 2.1. In the same directory as the Dockerfile, build the Docker image:

```
docker build -t log-analyzer .
```

#### 2.2. When the Docker image is successfully built, run the container:
```
docker run --rm \
  -e GIT_USER="Your username" \ 
  -e GIT_EMAIL="Your github email" \ 
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/formating-logs:/app/formating-logs \
  log-analyzer \
  --log-file logs/nginx.log --output-file formating-logs/logs.csv --sort-by size
```

### ⚙️ 3. Customize CI/CD (GitHub Actions)

#### The project uses GitHub Actions for automation:

- Runs on push to main
- Install Python and dependencies
- Performs a test run of the analyzer
- Creates a Docker image and pushes it to Docker Hub
- Automatically updates logs.csv in the repository
