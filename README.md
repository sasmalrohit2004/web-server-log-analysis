# Web Server Log Analysis Using Hadoop

## 1. Project Overview

This project analyzes web server access logs using Apache Hadoop
MapReduce. It calculates statistics about HTTP request methods, response
status codes, and requested resources. Python and Matplotlib generate
visualizations from the aggregated Hadoop output.

## 2. Objectives

-   Analyze web server access logs using Hadoop MapReduce.
-   Count HTTP request methods and response status codes.
-   Identify frequently requested resources.
-   Store and process data using HDFS.
-   Generate visualizations and document findings, limitations, and
    future improvements.

## 3. Technologies Used

-   Java OpenJDK 17
-   Apache Hadoop 3.3.6 and Java MapReduce
-   Hadoop Distributed File System (HDFS)
-   Python 3.14.4 and Matplotlib 3.11.2
-   Ubuntu on Windows Subsystem for Linux (WSL)
-   Visual Studio Code
-   Git and GitHub

## 4. Dataset

This project uses the [Calgary HTTP access log
dataset](https://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html).

The dataset contains historical web server log entries. The local
dataset used in this project contains 726,739 input log records and
occupies approximately 50 MiB after extraction.

  Metric                                              Result
  ------------------------------------------------ ---------
  Total input log records                            726,739
  Records not parsed by the project                    3,439
  Valid records included in aggregate statistics     723,300

The project parser did not recognize 3,439 records according to its
implemented parsing logic. These records were excluded from aggregate
statistics. Their causes have not been independently investigated.

## 5. Project Structure

``` text
web-server-log-analysis/
├── .gitignore
├── README.md
├── ANALYSIS_REPORT.md
├── requirements.txt
├── generate_graphs.py
├── src/
│   └── WebServerLogAnalysis.java
├── results/
│   └── analysis-output.txt
└── graphs/
    ├── http_status_distribution.png
    ├── request_methods.png
    └── top_10_resources.png
```

The `build/` directory is generated during compilation and excluded from
Git. The original dataset and Python virtual environment (`.venv/`) are
also excluded from the GitHub repository.

## 6. Environment Setup

The project was developed in Ubuntu on Windows Subsystem for Linux
(WSL), using Java OpenJDK 17 and Apache Hadoop 3.3.6.

Verify Java:

``` bash
java -version
```

Verify the Java compiler:

``` bash
javac -version
```

Verify Hadoop:

``` bash
hadoop version
```

Verify HDFS:

``` bash
hdfs version
```

Make sure Hadoop is configured and its required services are running
before executing the MapReduce job.

## 7. Download the Dataset

Download the Calgary HTTP dataset from the [official
source](https://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html) and place
the compressed file in `dataset/`.

Expected local paths:

``` text
dataset/calgary_access_log.gz
dataset/calgary_access_log
```

If the compressed file is present, extract it with:

``` bash
gunzip -k dataset/calgary_access_log.gz
```

The `-k` option preserves the compressed file. If the extracted file
already exists, do not extract it again.

## 8. Compile the Java Program

Navigate to the project directory:

``` bash
cd ~/web-server-log-analysis
mkdir -p build
javac -classpath "$(hadoop classpath)" -d build src/WebServerLogAnalysis.java
jar -cvf build/WebServerLogAnalysis.jar -C build .
```

The resulting JAR is `build/WebServerLogAnalysis.jar`.

## 9. Prepare HDFS Input

Create the HDFS input directory:

``` bash
hdfs dfs -mkdir -p /user/hi/web-server-log-analysis/input
```

Upload the extracted log file:

``` bash
hdfs dfs -put -f dataset/calgary_access_log /user/hi/web-server-log-analysis/input/
```

Verify the uploaded file:

``` bash
hdfs dfs -ls /user/hi/web-server-log-analysis/input
```

These commands use the HDFS paths configured in the development
environment. If using a different Hadoop user, adjust `/user/hi/`
accordingly.

## 10. Run the MapReduce Job

``` bash
hadoop jar build/WebServerLogAnalysis.jar WebServerLogAnalysis /user/hi/web-server-log-analysis/input /user/hi/web-server-log-analysis/output
```

Hadoop creates the output directory when the job succeeds. To rerun the
job, remove only the previous project output directory first:

``` bash
hdfs dfs -rm -r /user/hi/web-server-log-analysis/output
```

Then run the MapReduce command again. Do not delete the HDFS input
directory or format the NameNode when rerunning this project.

## 11. View and Save the Results

Display the complete output:

``` bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000
```

Display status-code counts:

``` bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000 | grep '^STATUS:'
```

Display method counts:

``` bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000 | grep '^METHOD:'
```

Display the ten most requested resources:

``` bash
hdfs dfs -cat /user/hi/web-server-log-analysis/output/part-r-00000 | grep '^RESOURCE:' | sort -k2,2nr | head -10
```

Copy the output to the local results directory:

``` bash
mkdir -p results
hdfs dfs -get -f /user/hi/web-server-log-analysis/output/part-r-00000 results/analysis-output.txt
```

## 12. Dataset Processing Results

The successful Hadoop job reported these counters:

  Metric                        Result
  ------------------------ -----------
  Map input records            726,739
  Map output records         2,169,900
  Combine output records        11,886
  Reduce output records         11,886
  Malformed lines                3,439
  Output bytes                 258,755
  Valid records parsed         723,300

The valid parsed record count is 726,739 − 3,439 = 723,300. "Malformed
lines" is the counter name used by the program; it means the records
were not parsed by the current parsing logic and does not by itself
prove that the original records were corrupt.

## 13. Key Findings

### HTTP Request Methods

  Method        Request Count   Approximate Share
  ----------- --------------- -------------------
  GET                 722,605              99.90%
  HEAD                    592               0.08%
  POST                    103               0.01%
  **Total**       **723,300**            **100%**

GET was the most frequently used method, accounting for approximately
99.90% of recognized method records. Percentages are rounded.

### HTTP Response Status Codes

  Status Code     Request Count Meaning
  ------------- --------------- -----------------------
  200                   566,861 OK
  302                    30,274 Found / Redirect
  304                    97,792 Not Modified
  400                        13 Bad Request
  401                        46 Unauthorized
  403                     4,743 Forbidden
  404                    23,486 Not Found
  500                        42 Internal Server Error
  501                        43 Not Implemented
  **Total**         **723,300**

HTTP 200 was the most common response, accounting for approximately
78.37% of valid parsed records. HTTP 304 indicates that a resource was
not modified, often in a cache-validation scenario; it is not itself an
error. HTTP 302 represents a redirect.

The listed 4xx and 5xx responses total 28,373, approximately 3.92% of
valid parsed records. Status codes 302 and 304 are not included in that
error count.

### Top 10 Most-Requested Resources

    Rank Resource       Request Count
  ------ ------------ ---------------
       1 index.html           139,526
       2 3.gif                 24,006
       3 2.gif                 23,595
       4 4.gif                  8,018
       5 244.gif                5,148
       6 5.html                 5,010
       7 4097.gif               4,874
       8 8870.jpg               4,492
       9 6733.gif               4,278
      10 8472.gif               3,843

`index.html` was the most frequently requested resource, with 139,526
requests. These counts represent requests recorded in the logs, not
unique visitors or unique page views.

## 14. Visualizations

The graphs below are generated from `results/analysis-output.txt` by
`generate_graphs.py`.

### HTTP Status-Code Distribution

![HTTP Status-Code Distribution](graphs/http_status_distribution.png)

### HTTP Request-Method Distribution

![HTTP Request-Method Distribution](graphs/request_methods.png)

### Top 10 Most-Requested Resources

![Top 10 Most-Requested Resources](graphs/top_10_resources.png)

## 15. Generate the Graphs

Requirements: Python 3 and Matplotlib, listed in `requirements.txt`.

Activate the project's virtual environment if one is available:

``` bash
source .venv/bin/activate
```

Install the dependency:

``` bash
python -m pip install -r requirements.txt
```

Run the script from the project root:

``` bash
python generate_graphs.py
```

The script creates these files:

``` text
graphs/
├── http_status_distribution.png
├── request_methods.png
└── top_10_resources.png
```

Ensure that `results/analysis-output.txt` exists before running the
script. The script needs the aggregated Hadoop output; it does not run
Hadoop itself.

## 16. Detailed Analysis Report

The separate [`ANALYSIS_REPORT.md`](ANALYSIS_REPORT.md) file provides a
detailed discussion of the dataset, Hadoop processing, status-code and
method analysis, most-requested resources, findings, limitations, and
future improvements.

## 17. Output Files

-   Local aggregated output: `results/analysis-output.txt`
-   HDFS output directory: `/user/hi/web-server-log-analysis/output/`
-   Graph images: `graphs/`
-   Detailed analysis report: `ANALYSIS_REPORT.md`

## 18. GitHub Repository

The source code, documentation, and analysis output are hosted in the
[project's GitHub
repository](https://github.com/sasmalrohit2004/web-server-log-analysis).

The original dataset, generated build files, and Python virtual
environment are kept out of the repository.

## 19. Updating the GitHub Repository

Check the changes:

``` bash
git status
```

Stage only the intended files:

``` bash
git add README.md .gitignore requirements.txt generate_graphs.py ANALYSIS_REPORT.md graphs/ results/analysis-output.txt src/
```

Do not stage `dataset/`; it is intentionally excluded from the
repository.

Review staged changes:

``` bash
git diff --cached --check
git status
```

Commit and push:

``` bash
git commit -m "Add analysis report and visualizations"
git push origin main
```

## 20. Limitations and Future Improvements

### Limitations

-   **Historical dataset:** The analysis describes the Calgary HTTP
    dataset, not current web traffic.
-   **Parsing coverage:** The parser did not recognize 3,439 records.
    Their causes have not been independently investigated.
-   **Aggregate counts:** The project focuses on totals rather than
    detailed request histories.
-   **No unique-visitor analysis:** The current analysis does not
    calculate unique visitors.
-   **No session analysis:** User sessions and navigation paths are not
    analyzed.
-   **No response-time analysis:** The current results do not measure
    request latency or response duration.
-   **No time-series analysis:** The current output does not establish
    traffic patterns by hour, day, or month.
-   **Limited causal conclusions:** Counts alone cannot explain why a
    request failed, why a resource was popular, or why a redirect
    occurred.

### Future Improvements

-   Investigate records that the parser does not recognize and improve
    parsing coverage.
-   Add hourly or daily request-trend analysis if timestamps are
    reliably available.
-   Investigate frequently requested missing resources.
-   Create separate visualizations for client errors and server errors.
-   Add automated tests for log parsing and aggregation.
-   Build an interactive dashboard for exploring results.
-   Compare traffic patterns across different log datasets.
-   Document performance measurements for processing the dataset.

## 21. Conclusion

This project demonstrates how Apache Hadoop MapReduce can process web
server access logs and generate aggregated statistics. The program
processed 726,739 input records, with 723,300 records included in the
aggregate statistics. HTTP 200 was the most common response status, GET
was the dominant request method, and `index.html` was the most
frequently requested resource.

The project combines Hadoop-based processing with Python visualizations
and written analysis, creating a workflow from log processing to
interpretation.

## 22. Author

**Rohit Sasmal**