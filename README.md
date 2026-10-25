# Web Server Log Analysis Using Hadoop

A Big Data project that analyzes web server access logs using **Apache Hadoop MapReduce and Java**. The project processes HTTP access logs to identify request methods, requested resources, and HTTP status codes. It also generates visualizations of the analysis results and supports processing input files stored in Amazon S3.

## Table of Contents

1. [Project Overview](#1-project-overview)

2. [Project Objectives](#2-project-objectives)

3. [Technologies Used](#3-technologies-used)

4. [System Requirements](#4-system-requirements)

5. [Project Structure](#5-project-structure)

6. [How the Project Works](#6-how-the-project-works)

7. [Environment Setup](#7-environment-setup)

8. [Verify Java and Hadoop](#8-verify-java-and-hadoop)

9. [Dataset Information](#9-dataset-information)

10. [Build the Java MapReduce Program](#10-build-the-java-mapreduce-program)

11. [Run the Project Locally](#11-run-the-project-locally)

12. [Understand the Output](#12-understand-the-output)

13. [Analyze the Full Dataset](#13-analyze-the-full-dataset)

14. [Generate Visualizations](#14-generate-visualizations)

15. [Apache Hadoop Configuration](#15-apache-hadoop-configuration)

16. [Amazon S3 Integration](#16-amazon-s3-integration)

17. [Run MapReduce Using Data Stored in S3](#17-run-mapreduce-using-data-stored-in-s3)

18. [View and Download Results from S3](#18-view-and-download-results-from-s3)

19. [AWS Security Best Practices](#19-aws-security-best-practices)

20. [Troubleshooting](#20-troubleshooting)

21. [Future Improvements](#21-future-improvements)

22. [Conclusion](#22-conclusion)

23. [Upload the Project to GitHub](#23-upload-the-project-to-github)

## 1. Project Overview

Web servers generate large volumes of access logs whenever users visit websites, request resources, submit forms, or encounter errors.

Analyzing these logs can reveal useful information about website traffic, commonly requested resources, HTTP methods, and server responses.

This project uses **Apache Hadoop MapReduce** to process web server access logs and summarize the information contained in them.

The Java program parses access-log entries and produces three categories of statistics:

- **HTTP status codes:** Counts of responses such as `200`, `302`, `404`, and `500`.

- **Request resources:** Counts of requests for resources such as `/`, `/login`, and `/products`.

- **HTTP methods:** Counts of methods such as `GET` and `POST`.

The project also includes analysis results and Python-based visualization support.

Amazon S3 integration allows the MapReduce program to read input logs from an S3 bucket and write its output back to S3.

### Current Project Environment

| Component | Configuration |

|---|---|

| Operating system | Windows 11 |

| Linux environment | WSL Ubuntu |

| Code editor | Visual Studio Code |

| Programming language | Java |

| Java version | OpenJDK 17 |

| Hadoop version | Apache Hadoop 3.3.6 |

| MapReduce execution mode | Local mode |

| Cloud storage | Amazon S3 |

| AWS region | `eu-north-1` |

| Python visualization | Python with Matplotlib |

| Version control | Git and GitHub |

## 2. Project Objectives

The main objectives of this project are:

1. Understand how web server access logs are structured.

2. Process log data using Java.

3. Understand the MapReduce programming model.

4. Use Hadoop to process and summarize log records.

5. Identify the most common HTTP status codes.

6. Identify frequently requested web resources.

7. Count HTTP methods used in requests.

8. Examine successful responses, redirects, client errors, and server errors.

9. Generate visualizations to make the results easier to understand.

10. Integrate Hadoop with Amazon S3 for cloud-based input and output.

11. Maintain the source code and documentation in GitHub.

## 3. Technologies Used

### 3.1 Java

Java is used to implement the MapReduce program that reads, parses, and analyzes web server access logs.

### 3.2 Apache Hadoop

Hadoop provides the MapReduce framework used to process the input data and aggregate the results.

This project uses Hadoop 3.3.6.

### 3.3 Hadoop MapReduce

The program uses the MapReduce model:

- **Mapper:** Reads individual log entries and emits categorized key-value pairs.

- **Reducer:** Aggregates values for matching keys and calculates their totals.

### 3.4 Amazon S3

Amazon Simple Storage Service (S3) stores input log files and MapReduce output files.

Hadoop accesses S3 through its S3A filesystem connector.

### 3.5 Python

Python is used to generate visualizations from the analysis results.

### 3.6 Matplotlib

Matplotlib provides chart-generation functionality for the project's analysis results.

### 3.7 Git and GitHub

Git tracks changes to the project, while GitHub hosts the repository.

## 4. System Requirements

Before running the project, ensure that the following software is available.

| Requirement | Purpose |

|---|---|

| Windows 11 | Host operating system |

| WSL with Ubuntu | Linux environment for Hadoop |

| Java JDK 17 | Compiling and running Java code |

| Apache Hadoop 3.3.6 | MapReduce execution |

| Visual Studio Code | Editing project files |

| Python 3 | Running visualization scripts |

| Git | Version control |

| AWS CLI | Managing Amazon S3 resources |

| AWS account | Accessing the S3 bucket |

An internet connection is required to install dependencies and access AWS services.

## 5. Project Structure

The repository contains the following main files and directories.

```text

web-server-log-analysis/

│

├── .gitignore

│

├── README.md

│

├── ANALYSIS_REPORT.md

│

├── requirements.txt

│

├── src/

│   └── WebServerLogAnalysis.java

│

├── dataset/

│   ├── calgary_access_log

│   └── calgary_access_log.gz

│

├── build/

│   ├── WebServerLogAnalysis.jar

│   └── compiled Java classes

│

├── results/

│   └── analysis-output.txt

│

├── graphs/

│   └── generated visualization images

│

└── generate_graphs.py

```

**Note:** The exact contents of `build/`, `dataset/`, `results/`, and `graphs/` may vary as the project develops. Some files and directories are excluded from Git through `.gitignore`.

### Important Files

| File or Directory | Description |

|---|---|

| `src/WebServerLogAnalysis.java` | Main Java MapReduce source code |

| `dataset/` | Local web server access-log files |

| `build/` | Compiled Java classes and JAR |

| `results/` | Analysis output and related files |

| `graphs/` | Generated visualization images |

| `generate_graphs.py` | Python visualization script |

| `requirements.txt` | Python dependency list |

| `ANALYSIS_REPORT.md` | Detailed analysis report |

| `README.md` | Project documentation |

| `.gitignore` | Files and directories excluded from Git |

## 6. How the Project Works

The project follows this general workflow:

```text

Web Server Access Logs

          |

          v

   Input Log File

          |

          v

  Java MapReduce Program

          |

          v

        Mapper

          |

          v

 Categorized Key-Value Pairs

          |

          v

        Reducer

          |

          v

 Aggregated Analysis Results

          |

          v

  Output Text Files

          |

          v

 Results Analysis and Graphs

```

When Amazon S3 is used, the input and output locations can be changed to S3 paths.

### 6.1 Input

The program receives a web server access-log file as input.

Each line represents a request recorded by the web server.

### 6.2 Parsing

The Java program reads log entries and extracts relevant information.

Depending on the record, the extracted information can include the HTTP method, requested resource, and response status code.

Some records may not match the parser's expected format and may therefore be excluded from the valid-record statistics.

### 6.3 Mapping

The Mapper generates categorized keys.

Examples include:

```text

METHOD:GET

METHOD:POST

RESOURCE:/

RESOURCE:/login

STATUS:200

STATUS:404

```

The values associated with these keys are aggregated by the Reducer.

### 6.4 Reducing

The Reducer combines matching keys and calculates their total counts.

For example:

```text

STATUS:200    6

STATUS:404    3

STATUS:500    1

```

These are example results from the small sample dataset, not the full Calgary dataset.

### 6.5 Output

The final results are written to an output directory.

The output can be stored locally or, when the S3A connector is configured correctly, in Amazon S3.

## 7. Environment Setup

This project is developed on Windows 11 using WSL Ubuntu.

### Step 1: Open Ubuntu

Open the Ubuntu terminal through the Windows Start menu or Windows Terminal.

### Step 2: Open the Project Directory

Run:

```bash

cd \~/web-server-log-analysis

```

Check the current directory:

```bash

pwd

```

The expected path is similar to:

```text

/home/hi/web-server-log-analysis

```

The username in the path may differ on another system.

### Step 3: List the Project Files

Run:

```bash

ls -la

```

The repository should contain files such as:

```text

README.md

ANALYSIS_REPORT.md

src

dataset

results

graphs

requirements.txt

generate_graphs.py

```

Some generated or ignored directories may not appear in every checkout.

### Step 4: Open the Project in Visual Studio Code

If the VS Code command is available in WSL, run:

```bash

code .

```

This opens the current project directory in Visual Studio Code.

## 8. Verify Java and Hadoop

### 8.1 Verify Java

Run:

```bash

java -version

```

Check the Java compiler:

```bash

javac -version

```

The project environment uses OpenJDK 17.

### 8.2 Verify Hadoop

Run:

```bash

hadoop version

```

The expected Hadoop version is:

```text

Hadoop 3.3.6

```

### 8.3 Verify the Hadoop Installation Directory

The Hadoop installation used in this project is:

```text

/home/hi/hadoop-3.3.6

```

Check the directory:

```bash

ls \~/hadoop-3.3.6

```

### 8.4 Check the Hadoop Environment Variable

Run:

```bash

echo "$HADOOP_HOME"

```

The configured value should point to the Hadoop installation directory.

If the environment variable is not configured in the current terminal, set it for that session:

```bash

export HADOOP_HOME="$HOME/hadoop-3.3.6"

export PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"

```

Then verify:

```bash

hadoop version

```

These exports apply to the current terminal session unless they are also configured in the shell's startup file.

## 9. Dataset Information

The project uses web server access logs, including the Calgary access-log dataset.

The local dataset directory is:

```text

dataset/

```

The main log file used in the full local analysis is:

```text

dataset/calgary_access_log

```

A compressed version is also present:

```text

dataset/calgary_access_log.gz

```

### 9.1 Inspect the Dataset

From the repository root, run:

```bash

ls -lh dataset/

```

To view the first few records:

```bash

head -n 10 dataset/calgary_access_log

```

To count the number of lines in the uncompressed file:

```bash

wc -l dataset/calgary_access_log

```

To inspect the compressed file without extracting it:

```bash

zcat dataset/calgary_access_log.gz | head -n 10

```

### 9.2 Understanding an Access-Log Record

A typical access-log record contains information about a web request, such as:

- Client IP address

- Timestamp

- Request method

- Requested resource

- HTTP protocol

- Response status code

- Response size

The exact fields depend on the log format.

### 9.3 Why the Dataset Is Useful

Web server logs can be analyzed to understand:

- Which resources receive the most requests.

- Which HTTP methods are commonly used.

- How many requests receive successful responses.

- How many requests receive redirects or errors.

- Whether particular resources may be frequently missing.

The project focuses on method, resource, and HTTP status-code counts.

## 10. Build the Java MapReduce Program

The main Java source file is:

```text

src/WebServerLogAnalysis.java

```

The compiled JAR is:

```text

build/WebServerLogAnalysis.jar

```

If the JAR does not exist or the source code has changed, rebuild it.

### Step 1: Enter the Project Directory

```bash

cd \~/web-server-log-analysis

```

### Step 2: Create the Build Directory

```bash

mkdir -p build

```

### Step 3: Compile the Java Source

Run:

```bash

javac -classpath "$(hadoop classpath)" -d build src/WebServerLogAnalysis.java

```

This command compiles the Java source file using the Hadoop libraries available in the current Hadoop installation.

### Step 4: Create the JAR File

Run:

```bash

jar -cvf build/WebServerLogAnalysis.jar -C build .

```

### Step 5: Verify the JAR

Run:

```bash

ls -lh build/WebServerLogAnalysis.jar

```

Inspect the JAR contents:

```bash

jar -tf build/WebServerLogAnalysis.jar

```

The JAR should contain the compiled `WebServerLogAnalysis` class and any additional classes generated from the source code.

**Important:** Rebuild the JAR after changing the Java source code. Otherwise, Hadoop may continue executing an older compiled version.

## 11. Run the Project Locally

The Java program accepts two command-line arguments:

1. Input path

2. Output path

The general command is:

```bash

hadoop jar build/WebServerLogAnalysis.jar WebServerLogAnalysis \<input-path> \<output-path>

```

The input and output paths may refer to local files, HDFS paths, or supported filesystem locations such as S3A, provided the corresponding Hadoop filesystem configuration is correct.

### 11.1 Run Against the Sample Dataset

The small sample dataset stored in S3 can be used to verify the program.

For a local test, use a sample log file that exists on your local system.

For example, if you have saved the sample as `dataset/sample-access.log`, run:

```bash

hadoop jar build/WebServerLogAnalysis.jar WebServerLogAnalysis dataset/sample-access.log results/sample-output

```

**Important:** Hadoop generally requires the output path not to exist already. If `results/sample-output` already exists, choose a new output directory or remove the old output directory only after confirming that you no longer need its contents.

### 11.2 Read Local Output

Inspect the output directory:

```bash

ls -lh results/sample-output/

```

If the output contains a reducer part file, display it using:

```bash

cat results/sample-output/part-r-00000

```

The exact output filenames may vary depending on the execution configuration.

### 11.3 Execution Mode

This project is configured to use Hadoop's local MapReduce execution mode.

In local mode, Hadoop executes the MapReduce job within the local environment instead of submitting it to a YARN cluster.

This configuration allows the project to run without starting a separate ResourceManager and NodeManager cluster.

## 12. Understand the Output

The Java program produces categorized counts for methods, resources, and HTTP status codes.

### 12.1 HTTP Method Counts

Example:

```text

METHOD:GET     9

METHOD:POST    1

```

Interpretation:

- `GET` requests retrieve resources.

- `POST` requests commonly submit data to a server.

- The numbers represent the counts found in the input data.

### 12.2 Resource Counts

Example:

```text

RESOURCE:/                  3

RESOURCE:/login             3

RESOURCE:/missing.html      2

RESOURCE:/products          2

```

Interpretation:

- `/` represents the root resource.

- `/login` represents the login resource.

- `/missing.html` represents a requested resource that may not exist.

- `/products` represents the products resource.

These counts describe the sample input and should not be interpreted as the results of the full dataset.

### 12.3 HTTP Status-Code Counts

Example:

```text

STATUS:200    6

STATUS:404    3

STATUS:500    1

```

Interpretation:

| Status Code | Meaning |

|---|---|

| `200` | Successful response |

| `301` | Permanent redirect |

| `302` | Temporary redirect |

| `304` | Not modified |

| `400` | Bad request |

| `401` | Unauthorized |

| `403` | Forbidden |

| `404` | Resource not found |

| `500` | Internal server error |

| `501` | Not implemented |

These are general HTTP status-code meanings. Not every code will necessarily appear in the input dataset.

## 13. Analyze the Full Dataset

The full Calgary access-log dataset was analyzed locally.

The recorded results are:

| Metric | Count |

|---|---:|

| Input records | 726,739 |

| Valid parsed records | 723,300 |

| Records not parsed | 3,439 |

The counts reconcile as follows:

```text

726,739 input records

- 723,300 valid parsed records

\=   3,439 records not parsed

```

The parser may skip records that do not match its expected format.

### 13.1 HTTP Status-Code Results

The recorded status-code counts from the full local analysis are:

| HTTP Status Code | Count |

|---|---:|

| `200` | 566,861 |

| `302` | 30,274 |

| `304` | 97,792 |

| `400` | 13 |

| `401` | 46 |

| `403` | 4,743 |

| `404` | 23,486 |

| `500` | 42 |

| `501` | 43 |

These are the recorded results from the earlier full local analysis. Rerunning the program against a different dataset, parser version, or configuration may produce different results.

### 13.2 Interpretation

**Successful responses:** Status code `200` accounts for the largest share of the recorded status-code counts.

**Caching and redirects:** Status codes `302` and `304` are also present in significant numbers.

**Missing resources:** Status code `404` indicates requests that received a not-found response.

**Access restrictions:** Status code `403` indicates forbidden responses.

**Server errors:** Status codes `500` and `501` appear much less frequently than the common successful and redirect responses.

These results summarize response counts. They do not, by themselves, establish the underlying causes of errors or user behavior.

### 13.3 View the Analysis Report

The detailed report is stored in:

```text

ANALYSIS_REPORT.md

```

Open it from the project directory:

```bash

cat ANALYSIS_REPORT.md

```

To browse it more comfortably:

```bash

less ANALYSIS_REPORT.md

```

Press `q` to exit `less`.

## 14. Generate Visualizations

The project includes a Python script for generating charts:

```text

generate_graphs.py

```

Generated chart images are stored in:

```text

graphs/

```

### 14.1 Check Python

Run:

```bash

python3 --version

```

### 14.2 Install Dependencies

From the repository root, run:

```bash

python3 -m pip install -r requirements.txt

```

If the Python environment prevents system-wide package installation, use a virtual environment:

```bash

python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

```

If the virtual environment is activated, use `python` to run the script.

### 14.3 Generate Charts

Run:

```bash

python3 generate_graphs.py

```

If you are using the virtual environment:

```bash

python generate_graphs.py

```

The script must be configured to read the expected analysis data. If the script requires a specific input file or directory, ensure that file exists before running it.

### 14.4 Inspect Generated Images

Run:

```bash

ls -lh graphs/

```

The images can be opened using Visual Studio Code or another image viewer.

### 14.5 Purpose of Visualizations

Charts can make the following patterns easier to understand:

- Distribution of HTTP status codes.

- Frequently requested resources.

- Distribution of HTTP methods.

- Differences between common and uncommon responses.

The charts depend on the data and input files used by the visualization script.

## 15. Apache Hadoop Configuration

Hadoop uses configuration files to determine how jobs run and how filesystem paths are accessed.

The configuration directory in this project is:

```text

\~/hadoop-3.3.6/etc/hadoop/

```

### 15.1 `core-site.xml`

File:

```text

\~/hadoop-3.3.6/etc/hadoop/core-site.xml

```

This file contains core Hadoop settings, including the default filesystem and S3A configuration.

The current project configuration uses HDFS as the default filesystem:

```xml

\<property>

    \<name>fs.defaultFS\</name>

    \<value>hdfs\://localhost:9000\</value>

\</property>

```

The S3A credential-provider setting is:

```xml

\<property>

    \<name>fs.s3a.aws.credentials.provider\</name>

    \<value>com.amazonaws.auth.EnvironmentVariableCredentialsProvider\</value>

\</property>

```

The S3 region is configured as:

```xml

\<property>

    \<name>fs.s3a.endpoint.region\</name>

    \<value>eu-north-1\</value>

\</property>

```

The environment-variable credential provider allows the S3A filesystem to use AWS credentials supplied through the current process environment.

**Security note:** Never put AWS access keys or secret access keys directly in a public configuration file or GitHub repository.

### 15.2 `mapred-site.xml`

File:

```text

\~/hadoop-3.3.6/etc/hadoop/mapred-site.xml

```

The project uses local MapReduce execution mode:

```xml

\<property>

    \<name>mapreduce.framework.name\</name>

    \<value>local\</value>

\</property>

```

This setting allows Hadoop to execute MapReduce jobs locally.

### 15.3 S3A Connector

The Hadoop S3A connector and AWS SDK dependencies must be available for Hadoop to read and write S3 paths.

The project environment includes these Hadoop libraries:

```text

$HADOOP_HOME/share/hadoop/tools/lib/hadoop-aws-3.3.6.jar

$HADOOP_HOME/share/hadoop/tools/lib/aws-java-sdk-bundle-1.12.367.jar

```

The project also enables the optional Hadoop AWS tools through its Hadoop environment configuration.

If the connector is missing, incompatible, or unavailable on the Hadoop classpath, S3A operations may fail.

## 16. Amazon S3 Integration

Amazon S3 is used to store the project's input files and MapReduce results.

### 16.1 S3 Configuration

The tested project configuration is:

| Setting | Value |

|---|---|

| AWS service | Amazon S3 |

| Bucket name | `bda-web-log-analysis-rohitsasmal-2026` |

| AWS region | `eu-north-1` |

| Hadoop filesystem | S3A |

| Hadoop version | 3.3.6 |

| Execution mode | Local MapReduce |

### 16.2 S3 Bucket Structure

The bucket contains input files and output directories.

An example structure is:

```text

bda-web-log-analysis-rohitsasmal-2026/

│

├── input/

│   ├── sample-access.log

│   └── full-data/

│       └── full-access-50KB.accesslog

│

└── output/

    ├── ip-output/

    ├── status-output/

    ├── url-output/

    └── current-project-test-007/

```

The exact contents may change as more input files and outputs are added.

S3 does not have conventional directories in the same way as a local filesystem. Paths such as `input/` and `output/` generally represent prefixes in object keys.

### 16.3 Install or Verify AWS CLI

Check whether the AWS CLI is installed:

```bash

aws --version

```

If it is installed, the command displays the installed version.

### 16.4 Configure AWS CLI

If AWS CLI has not been configured, run:

```bash

aws configure

```

Enter the required AWS credentials and default region when prompted.

For this project, the region is:

```text

eu-north-1

```

Do not paste credentials into project documentation, source code, chat messages, or public repositories.

If AWS CLI is already configured, do not run this step unnecessarily.

### 16.5 Verify AWS Authentication

Run:

```bash

aws sts get-caller-identity

```

A successful response confirms that AWS CLI can authenticate using the configured credentials.

### 16.6 Verify the S3 Bucket

Run:

```bash

aws s3 ls s3://bda-web-log-analysis-rohitsasmal-2026/

```

To list the input files:

```bash

aws s3 ls s3://bda-web-log-analysis-rohitsasmal-2026/input/ --recursive

```

To list the output files:

```bash

aws s3 ls s3://bda-web-log-analysis-rohitsasmal-2026/output/ --recursive

```

### 16.7 Provide Credentials to Hadoop

The tested S3A configuration uses environment variables for AWS authentication.

In the Ubuntu terminal, run:

```bash

export AWS_ACCESS_KEY_ID="$(aws configure get aws_access_key_id)"

export AWS_SECRET_ACCESS_KEY="$(aws configure get aws_secret_access_key)"

```

These commands retrieve the configured credentials and export them into the current shell environment.

Verify that the variables are set without printing their secret values:

```bash

test -n "$AWS_ACCESS_KEY_ID" && echo "AWS access key is set"

test -n "$AWS_SECRET_ACCESS_KEY" && echo "AWS secret key is set"

```

If you open a new terminal, you may need to export the variables again.

Never run commands that print the secret access key when sharing terminal output.

### 16.8 Verify S3A Access Through Hadoop

Run:

```bash

hadoop fs -ls s3a://bda-web-log-analysis-rohitsasmal-2026/input/

```

A successful response lists objects under the input prefix.

If this command fails, verify the AWS credentials, region, S3 permissions, Hadoop configuration, and S3A connector dependencies before running the MapReduce job.

## 17. Run MapReduce Using Data Stored in S3

The project has successfully executed its Java MapReduce program against the sample access log stored in Amazon S3.

### 17.1 Verify the Project and Build

Run:

```bash

cd \~/web-server-log-analysis

```

Check that the JAR exists:

```bash

ls -lh build/WebServerLogAnalysis.jar

```

If the Java source has changed since the JAR was built, rebuild the JAR using the instructions in Section 10.

### 17.2 Export AWS Credentials

Run:

```bash

export AWS_ACCESS_KEY_ID="$(aws configure get aws_access_key_id)"

export AWS_SECRET_ACCESS_KEY="$(aws configure get aws_secret_access_key)"

```

### 17.3 Execute the MapReduce Job

The tested sample input is:

```text

s3a://bda-web-log-analysis-rohitsasmal-2026/input/sample-access.log

```

The following command runs the program against that input:

```bash

hadoop jar build/WebServerLogAnalysis.jar WebServerLogAnalysis s3a://bda-web-log-analysis-rohitsasmal-2026/input/sample-access.log s3a://bda-web-log-analysis-rohitsasmal-2026/output/README-test-run-001

```

The command uses:

- The compiled project JAR.

- The `WebServerLogAnalysis` main class.

- The sample log file stored in S3.

- An S3 output prefix for the MapReduce results.

**Important:** Hadoop generally cannot write to an output path that already contains the output of a previous job. Use a new output prefix for each run, or carefully remove the previous output only when it is no longer needed.

### 17.4 Verify the Job Output

Run:

```bash

aws s3 ls s3://bda-web-log-analysis-rohitsasmal-2026/output/README-test-run-001/

```

A successful run created the following objects:

```text

_SUCCESS

part-r-00000

```

The `_SUCCESS` marker indicates that the MapReduce job completed successfully.

The `part-r-00000` file contains the reducer output.

### 17.5 Confirmed Sample Test Results

The sample test processed 10 input records.

The recorded MapReduce counters were:

| Counter | Result |

|---|---:|

| Map input records | 10 |

| Map output records | 30 |

| Reduce output records | 9 |

| Input data read | 772 bytes |

| Output data written | 143 bytes |

The output was:

```text

METHOD:GET             9

METHOD:POST            1

RESOURCE:/             3

RESOURCE:/login        3

RESOURCE:/missing.html 2

RESOURCE:/products     2

STATUS:200             6

STATUS:404             3

STATUS:500             1

```

These are the verified results of the small S3 sample test.

**The successful sample test does not mean that the full Calgary dataset has already been processed through S3.** The full Calgary dataset results documented in Section 13 came from the earlier local analysis.

## 18. View and Download Results from S3

After a MapReduce job completes, its results can be inspected using AWS CLI.

### 18.1 List the Output

Run:

```bash

aws s3 ls s3://bda-web-log-analysis-rohitsasmal-2026/output/README-test-run-001/

```

### 18.2 Display the Results Without Downloading Them Permanently

Run:

```bash

aws s3 cp s3://bda-web-log-analysis-rohitsasmal-2026/output/README-test-run-001/part-r-00000 -

```

The final `-` tells AWS CLI to write the downloaded object to standard output.

### 18.3 Download the Results to the Project

Run:

```bash

mkdir -p results/s3-output

```

Then:

```bash

aws s3 cp s3://bda-web-log-analysis-rohitsasmal-2026/output/README-test-run-001/part-r-00000 results/s3-output/part-r-00000

```

Read the downloaded file:

```bash

cat results/s3-output/part-r-00000

```

The downloaded output can be used for further inspection or analysis.

### 18.4 Download All Objects from an Output Prefix

If an output directory contains multiple part files, download the prefix recursively:

```bash

aws s3 cp s3://bda-web-log-analysis-rohitsasmal-2026/output/README-test-run-001/ results/s3-output/ --recursive

```

This copies the objects under that prefix to the local destination.

## 19. AWS Security Best Practices

AWS credentials provide access to cloud resources and must be protected.

Follow these practices:

1. Never commit AWS access keys or secret access keys to GitHub.

2. Do not hard-code AWS credentials in Java source files.

3. Do not include credentials in the README.

4. Do not share terminal output containing secret values.

5. Use IAM permissions appropriate to the tasks being performed.

6. Prefer temporary credentials or IAM roles where appropriate.

7. Restrict permissions to the required bucket and actions when practical.

8. Review IAM permissions periodically.

9. Keep local AWS credential files private.

10. If credentials are accidentally exposed, revoke or rotate them promptly.

The project uses the AWS CLI credential configuration together with environment variables for the tested Hadoop S3A setup.

The `.aws` configuration directory should remain outside the Git repository.

## 20. Troubleshooting

This section covers common issues that may occur when building or running the project.

### 20.1 `hadoop: command not found`

**Possible cause:** Hadoop is not installed correctly or its `bin` directory is missing from `PATH`.

Check:

```bash

echo "$HADOOP_HOME"

```

Temporarily configure it if necessary:

```bash

export HADOOP_HOME="$HOME/hadoop-3.3.6"

export PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"

```

Verify:

```bash

hadoop version

```

### 20.2 `javac: command not found`

**Possible cause:** The Java development kit is missing or not configured correctly.

Check:

```bash

java -version

javac -version

```

Java runtime availability alone does not guarantee that the Java compiler is available.

### 20.3 JAR File Not Found

**Possible cause:** The JAR has not been built, or the command is being run from the wrong directory.

Check:

```bash

cd \~/web-server-log-analysis

ls -lh build/WebServerLogAnalysis.jar

```

If the JAR is missing, follow Section 10 to compile the source and build the JAR.

### 20.4 Output Directory Already Exists

**Possible cause:** Hadoop is trying to write to a path that already contains output from an earlier run.

Use a fresh output path, such as:

```text

s3a://bda-web-log-analysis-rohitsasmal-2026/output/test-run-002

```

Make sure the chosen path is new before running the job.

### 20.5 `NoAuthWithAWSException`

**Possible cause:** Hadoop S3A cannot obtain valid AWS credentials.

Verify AWS CLI authentication:

```bash

aws sts get-caller-identity

```

Export the configured credentials:

```bash

export AWS_ACCESS_KEY_ID="$(aws configure get aws_access_key_id)"

export AWS_SECRET_ACCESS_KEY="$(aws configure get aws_secret_access_key)"

```

Verify that the variables are set without printing their values:

```bash

test -n "$AWS_ACCESS_KEY_ID" && echo "Access key is set"

test -n "$AWS_SECRET_ACCESS_KEY" && echo "Secret key is set"

```

Then retry the S3A listing command.

### 20.6 S3 Access Denied

**Possible cause:** The authenticated AWS identity does not have sufficient permissions for the requested operation.

Check the identity:

```bash

aws sts get-caller-identity

```

Verify the applicable IAM policies and bucket policies.

Remember that listing, reading, writing, and deleting objects can require different permissions.

### 20.7 S3A Filesystem or Classpath Errors

**Possible cause:** Hadoop cannot load the required S3A connector or a compatible AWS SDK dependency.

Verify that the expected libraries exist:

```bash

ls "$HADOOP_HOME/share/hadoop/tools/lib/hadoop-aws-3.3.6.jar"

```

```bash

ls "$HADOOP_HOME/share/hadoop/tools/lib/aws-java-sdk-bundle-1.12.367.jar"

```

If either library is missing, or a version mismatch is reported, investigate the Hadoop and AWS SDK compatibility before changing dependencies.

### 20.8 Resource Manager or YARN Errors

**Possible cause:** Hadoop is attempting to submit a job to YARN instead of using local execution mode.

Check:

```bash

grep -A 3 -B 1 'mapreduce.framework.name' "$HADOOP_HOME/etc/hadoop/mapred-site.xml"

```

The project uses:

```xml

\<property>

    \<name>mapreduce.framework.name\</name>

    \<value>local\</value>

\</property>

```

Make sure this property is inside the `\<configuration>` element.

### 20.9 Invalid or Unparsed Log Records

**Possible cause:** Some records do not match the format expected by the Java parser.

Inspect the original records and the parsing logic in:

```text

src/WebServerLogAnalysis.java

```

Do not assume that every line in an access log will be counted as a valid parsed record.

### 20.10 Python Dependency Errors

**Possible cause:** Python packages are missing or installed in a different environment.

Run:

```bash

python3 -m pip install -r requirements.txt

```

If a virtual environment is being used, activate it before running the visualization script.

## 21. Future Improvements

Possible future improvements include:

1. Process the complete Calgary dataset through Amazon S3.

2. Compare local processing with cloud-based storage workflows.

3. Add IP-address-based analysis.

4. Add user-agent analysis.

5. Identify the most frequently requested resources.

6. Analyze request traffic over time.

7. Improve parsing of unusual log formats.

8. Produce more detailed visualizations.

9. Automate the build and execution process.

10. Improve AWS IAM security by restricting permissions to the required resources.

11. Add automated tests for the log parser.

12. Add a more detailed performance evaluation.

13. Document the behavior of each Mapper and Reducer operation.

14. Explore running MapReduce on a properly configured distributed Hadoop cluster.

These are potential improvements and should not be considered completed features unless they have been implemented and tested.

## 22. Conclusion

The Web Server Log Analysis project demonstrates how Java and Hadoop MapReduce can be used to extract useful statistics from web server access logs.

The project analyzes HTTP methods, requested resources, and response status codes. It also includes a full local analysis of the Calgary access-log dataset and a Python-based visualization workflow.

Amazon S3 integration extends the project by allowing Hadoop to read input data from an S3 bucket and write MapReduce results back to S3 using the S3A filesystem connector.

The small S3 sample test completed successfully, demonstrating that the configured Hadoop environment can read a sample log from S3, execute the MapReduce job locally, and write the results back to S3.

The project provides a practical foundation for learning big-data processing, MapReduce, cloud storage integration, data analysis, and version control.

## 23. Upload the Project to GitHub

The project repository is:

**GitHub repository:** https\://github.com/sasmalrohit2004/web-server-log-analysis

Git is used to track changes, while GitHub hosts the project remotely.

### 23.1 Check Git

Run:

```bash

git --version

```

### 23.2 Enter the Project Directory

```bash

cd \~/web-server-log-analysis

```

### 23.3 Check the Repository Status

```bash

git status

```

### 23.4 Review the Changes

To see the differences in tracked files:

```bash

git diff

```

To check for whitespace errors:

```bash

git diff --check

```

### 23.5 Check the README

Confirm that the complete README has been saved:

```bash

head -n 30 README.md

```

Check its length:

```bash

wc -l README.md

```

### 23.6 Stage the README

To stage only the README change:

```bash

git add README.md

```

If you have made other project changes that should also be included, inspect them carefully before staging.

### 23.7 Commit the Changes

```bash

git commit -m "Improve project documentation and S3 integration guide"

```

If Git reports that there is nothing to commit, check whether the file was changed and saved.

### 23.8 Push to GitHub

```bash

git push origin main

```

### 23.9 Verify the Update

Open the GitHub repository and check that the new README appears correctly.

Ensure that the headings, tables, code blocks, and table of contents render properly.

### 23.10 Important Git Security Checks

Before pushing, make sure that:

- AWS credentials are not included.

- Private configuration files are not accidentally staged.

- Large datasets are handled according to the project's `.gitignore` rules.

- Generated build files are included or excluded intentionally.

- No sensitive information is committed.

You can inspect staged files before committing:

```bash

git status --short

```

To inspect the files staged for commit:

```bash

git diff --cached --stat

```
