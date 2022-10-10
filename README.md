# Sink-Spike

A basic solution for recursively scanning local source code files for known insecure patterns or functions in order to find sinks as part of a vulnerability discovery workflow.



## Usage

Scan your current directory and below for PHP files that contain known PHP insecure patterns:
```
code_scan.py -t 'php' -d .
```

