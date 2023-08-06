# Logger

Module to facilitate the creation of logs with logging

### **Installation**

```powershell
pip install Logger
```

### **Example**: 

Types of log

```python
DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4
```

```python
 from Logger import log
 
 #log.create("filename", "text", type_logger)
 log.create("skynet_log", "deu merda ......", log.ERROR)
 ```
 Output (terminal and file)
 
 ```txt
 2018-10-29 13:47:50,359 - (path: '../skynet.py', line number (approximate): 666) - ERROR - deu merda ...... 
```
