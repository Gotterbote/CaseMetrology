# Office Engineering Dashboard

Copy `dashboard.py` and `install_dashboard_task.ps1` to the existing
`C:\CaseMetrologyReceiver` directory on the office PC.

Manual test:

```powershell
cd C:\CaseMetrologyReceiver
python -u .\dashboard.py
```

Then open:

`http://127.0.0.1:8767`

After manual verification, install the at-logon task:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_dashboard_task.ps1
```

The dashboard is read-only and uses the existing
`C:\CaseMetrologyReceiver\casemetrology.sqlite3` database by default.
