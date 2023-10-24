# Realtime Sync

This is a simple python script that will watch a list of predefined directories and files for changes. If a change is detected it will be synced to a specified target directory. Useful for keeping backups of your data e.g. to a NAS.

## Table of Contents

- [Installation](#installation)
- [Run as service (Mac OS)](service)

---

## Installation and Usage

1. Clone the repository:
   ```sh
   git clone https://github.com/masesor/RealtimeSync.git

2. Copy `config.yaml.example` to `config.yaml` and add array of source directories and a target directory

3. Execute
   ```sh
   python realtime_sync.py

Optionally, you can install as a service so it runs on startup automatically.

## Run as service (Mac OS)
1. Create plist file in ~/Library/LaunchAgents/com.myname.backupscript.plist

   ```xml
    <?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
	    <key>Label</key>
	    <string>com.yourname.backupscript</string>
	    <key>ProgramArguments</key>
	    <array>
		<string>python</string>
		<string>/path/to/realtime_sync.py</string>
	    </array>
	    <key>RunAtLoad</key>
	    <true/>
	    <key>KeepAlive</key>
	    <true/>
	    <key>StandardOutPath</key>
	    <string>/path/to/std.log</string>
	    <key>StandardErrorPath</key>
	    <string>/path/to/std.err</string>
	</dict>
	</plist>

2. Load plist
   ```sh
      load ~/Library/LaunchAgents/com.myname.backupscript.plist

3. To unload: 
   ```sh
      unload ~/Library/LaunchAgents/com.myname.backupscript.plist