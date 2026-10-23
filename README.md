# Web Server Log Analysis Using Hadoop

## 1. Project Overview

This project analyzes web server access logs using Apache Hadoop MapReduce. It processes HTTP access logs and calculates statistics about request methods, response status codes, and requested resources.

The project demonstrates how Java and Hadoop MapReduce can process large datasets and extract useful information from web server logs.

## 2. Objectives

- Analyze web server access logs using Hadoop MapReduce.
- Count HTTP request methods.
- Count HTTP response status codes.
- Identify frequently requested resources.
- Store and process data using HDFS.
- Generate aggregated results for further analysis.

## 3. Technologies Used

- Java OpenJDK 17
- Apache Hadoop 3.3.6
- Java MapReduce
- Hadoop Distributed File System (HDFS)
- Ubuntu on Windows Subsystem for Linux (WSL)
- Visual Studio Code
- Git and GitHub

## 4. Dataset

This project uses the Calgary HTTP access log dataset.

**Official dataset source:** https://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html

The dataset contains web server log entries with timestamps, request methods, requested resources, HTTP status codes, and response sizes.

The dataset used in this project contains 726,739 input log records and occupies approximately 50 MiB after extraction.

## 5. Project Structure

```text
web-server-log-analysis/
├── .gitignore
├── README.md
├── dataset/
│   ├── calgary_access_log
│   └── calgary_access_log.gz
├── results/
│   └── analysis-output.txt
└── src/
    └── WebServerLogAnalysis.java
```

The `build/` directory is generated during compilation and is excluded from Git using `.gitignore`.

The dataset is kept locally and is not included in the GitHub repository.

## 6. Environment Setup

The project was developed in Ubuntu on Windows Subsystem for Linux (WSL), using Java OpenJDK 17 and Apache Hadoop 3.3.6.

Verify Java:

```bash
java -version
```

Verify the Java compiler:

```bash
javac -version
```

Verify Hadoop:

```bash
hadoop version
```

Verify HDFS:

```bash
hdfs version
```

Make sure Hadoop is configured and its required services are running before executing the MapReduce job.

## 7. Download the Dataset

Download the Calgary HTTP dataset from the official source:

https://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html

Place the downloaded compressed file in the project's `dataset/` directory.

The expected local paths are:

```text
dataset/calgary_access_log.gz
dataset/calgary_access_log
```

If the compressed file is already present, extract it with:

```bash
gunzip -k dataset/calgary_access_log.gz
```

The `-k` option preserves the compressed file.

If the extracted file already exists, do not extract it again.

## 8. Compile the Java Program

Open the Ubuntu terminal and navigate to the project directory:

```bash
cd ~/web-server-log-analysis
```

Create the build directory:

```bash
mkdir -p build
```

Compile the source code using the Hadoop classpath:

```bash
javac -classpath "$(hadoop classpath)" -d build src/WebServerLogAnalysis.java
```

Package the compiled classes into a JAR:

```bash
jar -cvf build/WebServerLogAnalysis.jar -C build .
```

The resulting JAR is:

```text
build/WebServerLogAnalysis.jar
```

## 9. Prepare HDFS Input

Create the HDFS input directory:

```bash
hdfs dfs -mkdir -p /user/hi/web-server-log-analysis/input
```

Upload the extracted log file:

```bash
hdfs dfs -put -f dataset/calgary_access_log /user/hi/web-server-log-analysis/input/
```

Verify the uploaded file:

```bash
hdfs dfs -ls /user/hi/web-server-log-analysis/input
```

The commands above use the HDFS paths configured in the development environment. If running under a different Hadoop user, adjust `/user/hi/` accordingly.

## 10. Run the MapReduce Job

Run the Java MapReduce program:

```bash
hadoop jar build/WebServerLogAnalysis.jar WebServerLogAnalysis /user/hi/web-server-log-analysis/input /user/hi/web-server-log-analysis/output
```

Hadoop creates the output directory automatically when the job succeeds.

**Important:** Hadoop does not allow a job to write to an output directory that already exists. To rerun the job, remove only the previous project output directory first:

```bash
hdfs dfs -rm -r /user/hi/web-server-log-analysis/output
```

Then run the MapReduce command again.

Do not delete the HDFS input directory or format the NameNode when rerunning this project.

## 11. View the Results

Display the complete output:

```bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000
```

Display HTTP status code counts:

```bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000 | grep '^STATUS:'
```

Display HTTP method counts:

```bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000 | grep '^METHOD:'
```

Display the ten most requested resources:

```bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000 | grep '^RESOURCE:' | sort -k2,2nr | head -10
```

Copy the final output from HDFS to the local results directory:

```bash
mkdir -p results
hdfs dfs -get -f /user/hi/web-server-log-analysis/output/part-r-00000 results/analysis-output.txt
```

The local results file is:

```text
results/analysis-output.txt
```

## 12. Analysis Performed

The MapReduce program calculates three categories of statistics:

1. **HTTP methods:** Counts GET, HEAD, POST, and other successfully parsed request methods.
2. **HTTP status codes:** Counts requests grouped by their HTTP response status.
3. **Requested resources:** Counts requests for individual resources, including HTML pages and image files.

## 13. Dataset Processing Results

The successful Hadoop job reported the following counters:

| Metric | Result |
|---|---:|
| Map input records | 726,739 |
| Map output records | 2,169,900 |
| Malformed lines skipped | 3,439 |
| Valid records parsed | 723,300 |
| Final aggregated output records | 11,886 |

The valid parsed record count equals the input record count minus the malformed lines:

726,739 − 3,439 = 723,300.

## 14. Key Findings

### HTTP Request Methods

| Method | Request Count |
|---|---:|
| GET | 722,605 |
| HEAD | 592 |
| POST | 103 |

GET was the most frequently used HTTP request method.

### HTTP Response Status Codes

| Status Code | Request Count |
|---|---:|
| 200 | 566,861 |
| 302 | 30,274 |
| 304 | 97,792 |
| 400 | 13 |
| 401 | 46 |
| 403 | 4,743 |
| 404 | 23,486 |
| 500 | 42 |
| 501 | 43 |

HTTP status code 200 was the most common response. Status code 404 indicates that a resource was not found. Status code 304 indicates that a resource was not modified.

### Most Requested Resources

| Resource | Request Count |
|---|---:|
| index.html | 139,526 |
| 3.gif | 24,006 |
| 2.gif | 23,595 |
| 4.gif | 8,018 |
| 244.gif | 5,148 |
| 5.html | 5,010 |
| 4097.gif | 4,874 |
| 8870.jpg | 4,492 |
| 6733.gif | 4,278 |
| 8472.gif | 3,843 |

The resource `index.html` was the most frequently requested resource in the analyzed dataset.

## 15. Output Files

The final analysis output is stored locally at:

```text
results/analysis-output.txt
```

The corresponding HDFS output directory is:

```text
/user/hi/web-server-log-analysis/output/
```

## 16. GitHub Repository

The source code, documentation, and analysis output are available in the project's GitHub repository:

https://github.com/sasmalrohit2004/web-server-log-analysis

The original dataset and generated build files are kept outside the GitHub repository.

## 17. Updating the GitHub Repository

After modifying project files, check the changes:

```bash
git status
```

Stage the intended changes:

```bash
git add README.md src/ results/
```

Create a commit:

```bash
git commit -m "Update project documentation and results"
```

Push the commit to GitHub:

```bash
git push
```

## 18. Limitations and Future Improvements

- Investigate the 3,439 malformed log lines to determine why they could not be parsed.
- Add additional analyses, such as hourly request trends and resource popularity by HTTP method.
- Improve handling of unusual or incomplete log entries.
- Generate charts to visualize request methods, status codes, and frequently accessed resources.

## 19. Conclusion

This project demonstrates how Apache Hadoop MapReduce can process web server access logs and generate aggregated statistics. The results provide insights into HTTP request patterns, server response codes, and frequently accessed resources.

## 20. Author

**Rohit Sasmal**