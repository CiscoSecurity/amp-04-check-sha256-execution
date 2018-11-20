[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/AMP-for-Endpoints "Gitter chat")

### AMP for Endpoints check SHA256 for execution:

Takes a SHA256 as input and queries the environment for GUIDs that have seen the file. Then queries the trajectory of each GUID to verify the endpoint has executed the file. If a SHA256 is not provided as a command line argument, the script will prompt for one.

### Before using you must update the following:
- client_id 
- api_key

### Usage:
```
python check_for_execution_simplified.py
```
or
```
python check_for_execution_simplified.py db06c3534964e3fc79d2763144ba53742d7fa250ca336f4a0fe724b75aaff386
```

### Example script output:  
```
check_for_execution_simplified.py db06c3534964e3fc79d2763144ba53742d7fa250ca336f4a0fe724b75aaff386

Computers that have seen the file: 15

Hosts observed executing the file:
14dcfce3-9663-434d-9beb-c8836de035ce - Demo_AMP_Intel
  File: cmd.exe
  Path: /c:/windows/system32/cmd.exe

43ea5bb6-a4ec-48fa-876c-59cc304fda17 - Demo_AMP
  File: cmd.exe
  Path: /c:/windows/system32/cmd.exe
```
