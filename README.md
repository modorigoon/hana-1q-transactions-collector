## Hana bank 1Q PRO Transaction collector
<hr/>

Due to the nature of Hana bank's 1Q Pro HTS API, this program can run only on Windows OS and requires Hana 1Q API and securities account.

### Install

1. Install 1Q API
   
   Download: <a href="https://www.hanaw.com/main/customer/customer/CS_050600_T1.cmd">Hana 1Q API</a>

2. 1Q open API agent registration
   ```
   > CD 1QApiAgent
   1QApiAgent> regHFCommAgent.bat
   1QApiAgent> regsvr32 /S HFCommAgent.dll
   ```
   
3. Install Python (x86, 32bit)


4. requirements.txt install dependencies


### Execute
```
python main.py -e local -l WARN
```
Options
- e : Run mode (resource/environment-{mode}.json)
- l : Log level
