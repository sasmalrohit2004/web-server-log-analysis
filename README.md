# Web Server Log Analysis Using Hadoop

## 1. Project Overview

This project analyzes web server access logs using Apache Hadoop MapReduce. It processes a large log dataset and calculates statistics about HTTP request methods, response status codes, and requested resources.

The goal is to demonstrate how distributed data processing can be used to extract useful information from web server logs.

## 2. Objectives

- Analyze web server access logs using Hadoop MapReduce.
- Count HTTP request methods.
- Count HTTP response status codes.
- Identify frequently requested resources.
- Store and process data using the Hadoop Distributed File System (HDFS).

## 3. Technologies Used

- Java
- Apache Hadoop 3.3.6
- Hadoop MapReduce
- Hadoop Distributed File System (HDFS)
- Ubuntu on Windows Subsystem for Linux (WSL)
- Visual Studio Code

## 4. Dataset

The project uses the Calgary HTTP access log dataset.

Source: https://ita.ee.lbl.gov/html/contrib/Calgary-HTTP.html

The dataset contains web server requests, including timestamps, request methods, requested resources, HTTP status codes, and response sizes.

## 5. Project Structure

```text
web-server-log-analysis/
├── build/
│   └── WebServerLogAnalysis.jar
├── dataset/
│   ├── calgary_access_log
│   └── calgary_access_log.gz
├── results/
│   └── analysis-output.txt
├── src/
│   └── WebServerLogAnalysis.java
└── README.md
```

## 6. Analysis Performed

The MapReduce program calculates:

1. **HTTP methods:** Number of GET, HEAD, and POST requests.
2. **HTTP status codes:** Number of requests associated with each response status.
3. **Requested resources:** Number of requests for individual resources, such as HTML pages and image files.

## 7. Dataset Processing Results

The Hadoop job processed 726,739 input log records.

- Map input records: 726,739
- Map output records: 2,169,900
- Malformed lines skipped: 3,439
- Valid records parsed: 723,300
- Final aggregated output records: 11,886

## 8. Key Findings

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

HTTP status code 200 was the most common response. Status code 404 indicates that the requested resource was not found. Status code 304 indicates that a resource was not modified.

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

## 9. Output

The final MapReduce output is saved locally at:

`results/analysis-output.txt`

The output is also stored in HDFS at:

`/user/hi/web-server-log-analysis/output/`

## 10. Conclusion

This project demonstrates how Apache Hadoop MapReduce can process web server access logs and generate aggregated statistics. The results provide insights into HTTP request patterns, server response codes, and frequently accessed resources.

## 11. Author

Rohit Sasmal
