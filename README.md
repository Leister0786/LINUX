# Linux Administration Dashboard

A local Flask web dashboard that gathers real system information by running bundled Linux shell scripts.

## Features
- CPU utilization using `top`
- RAM usage using `free`
- Root filesystem usage using `df`
- Uptime using `uptime`
- Hostname and kernel using `hostname` and `uname`
- Process list using `ps`
- Local user accounts using `getent passwd`
- Running systemd services using `systemctl`
- Filesystem table using `df -hP`
- Automatic refresh every 15 seconds

## Requirements
- Ubuntu or another Linux distribution with Bash and standard Linux utilities
- Python 3.10+
- `systemctl` is needed for the running-services panel (where systemd is used)

## Run in Ubuntu / Linux

Open this folder in VS Code. In the integrated terminal, make sure the terminal is in the folder containing `app.py`, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x scripts/*.sh
python app.py
```

Open `http://127.0.0.1:5000`.

## Run in Windows PowerShell

This project uses Linux commands and is intended to run on Ubuntu/Linux. If you are using Windows, run it inside Ubuntu through WSL and open the project from the WSL filesystem. Do not run the Linux scripts directly in PowerShell.

## Folder structure

```text
linux-admin-dashboard-full/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── scripts/
    ├── system_metrics.sh
    ├── processes.sh
    ├── users.sh
    ├── services.sh
    ├── disk_usage.sh
    └── README.md
```

## Security notes
- The app only runs fixed scripts included in this project; it does not accept arbitrary shell commands from the browser.
- It is a monitoring/demo project. It does not create/delete users, kill processes, or start/stop services.
- Flask debug mode is for local development only. Do not expose this server to the internet.
- Some process/user details can vary based on the account running Flask. Do not run the app with `sudo` unless you understand the additional privileges being granted.

## Customization
Copy your own existing shell scripts into `scripts/` and integrate them through explicit, fixed backend functions. Validate all inputs and avoid passing browser-supplied strings into shell commands.
