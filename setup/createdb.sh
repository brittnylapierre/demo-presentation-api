python3 ./parseExport.py
curl -u admin:YOURPASSWORD -X PUT localhost:5984/manifest
python3 ./import.py