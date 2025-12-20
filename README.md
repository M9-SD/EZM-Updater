# EZM-Updater
One-click installer for Enhanced Zeus Modules (an Arma 3 Zeus composition that gives game master access to 100's of new modules).

EZM: https://github.com/expung3d/Enhanced-Zeus-Modules/

How the EZM Updater works:
1. Downloads ezm sqf file from github to temp folder
2. Builds new composition.sqe and header.sqe files
3. Creates/copies/overwrites EZM_Comp folder in arma 3 profile

The exe essentially installs the composition for you. 
It can then be accessed in Zeus > Custom Compositions > Enhanced Zeus Modules > EZM V...

For automatic updates, you can create a shortcut of the exe and place it in the windows startup folder, allowing EZM to be updated everytime you start your PC.

---

How to Access the Startup Folder

Press Win + R: to open the Run dialog box. 
Type one of the following commands: and press Enter or click OK: 

For your user account: 

shell:startup (Opens: %userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup)

For all users: 

shell:common startup (Opens: %ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup)

---

Alternatively, you can use Task Scheduler to periodically run the exe and update EZM.

https://learn.microsoft.com/en-us/answers/questions/2845465/windows-10-task-scheduler-schedule-to-run-an-exe-f
