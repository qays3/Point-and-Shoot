Win
```ps
cd backend
python -m venv myenv
.\myenv\Scripts\activate
pip install -r .\requirements.txt
python .\run.py
```

Linux
```bash
cd backend
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
nohup python3 run.py > server.log 2>&1 &
```
