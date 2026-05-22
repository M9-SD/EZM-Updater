# EZM-Updater

**One-click installer/updater for [Enhanced Zeus Modules (EZM)](https://github.com/expung3d/Enhanced-Zeus-Modules/)**

Just [download](https://github.com/M9-SD/EZM-Updater/releases/download/V0.1/EZM_Updater.exe) and run the executable to install EZM!

---

## Background

Since the official Enhanced Zeus Modules [composition](https://community.bistudio.com/wiki/Eden_Editor:_Custom_Composition) was removed from the Steam workshop, EZM users had to manually create the composition by copying the script from github and pasting it into Eden every time a new version came out...

With this one-click installer/updater for [Enhanced Zeus Modules (EZM)](https://github.com/expung3d/Enhanced-Zeus-Modules/), you no longer need to manually create the composition in the Arma 3 editor.

EZM-Updater automatically downloads the latest EZM script (SQF file) from the official github repository, builds the required composition structure, and installs it directly into your Arma 3 profile for immediate use in Zeus.

---

## Features

- Automatic installation of the latest EZM release
- Builds required `composition.sqe` and `header.sqe` files
- Installs directly into the Arma 3 custom compositions directory
- Optionally supports automatic updates through Windows Startup or Task Scheduler
- No manual file extraction or profile editing required

---

## How It Works

The updater performs the following steps:

1. Downloads the latest EZM `.sqf` data from GitHub
2. Generates:
   - `composition.sqe`
   - `header.sqe`
3. Creates or updates the `EZM_Comp` folder inside your Arma 3 profile directory – no configuration required, profile folders are automatically detected
4. Makes the composition immediately available in-game (you may need to re-join the session)

After installation, you can join a Zeus session and initialize EZM by placing down its custom composition: 

```text
Zeus → Custom Compositions → Enhanced Zeus Modules → EZM V...
```

---

## Requirements

- Windows 10/11
- Arma 3
- Internet connection (required for downloading EZM)
- Server must have [compositionScriptLevel parameter set to 2](https://community.bistudio.com/wiki/Description.ext#zeusCompositionScriptLevel) — half the official Zeus servers (even numbered) already have this enabled

---

Note: Before running this tool, it is recommended to make a backup of your profile folder.

## Typical Installation Instructions

1. Download the latest [release](https://github.com/M9-SD/EZM-Updater/releases) of `EZM-Updater.exe` 
2. Run the executable
3. Launch Arma 3
4. Join a server as Zeus, navigate to the compositions tab, place down EZM comp, and you're ready to use the modules

## Python User Installation Instructions

If you already have Python on your system, it is not necessary to use the application executable — it is merely a convenient way to distribute the tool and make it accesible for everyone. 
If you have the required python dependencies (package imports), you may simply call the python script by itself — or — alternatively, you can build your own exe from the source code using pyInstaller via the included [batch script](https://github.com/M9-SD/EZM-Updater/blob/main/make_exe.bat): `make_exe.bat`.

---

## Configuring Automatic Updates

Optionally, you may configure EZM-Updater to run automatically whenever your PC starts.
This way, you will not have to constantly check for new EZM version releases and run the updater manually. 
I purposefully didn't include such feature in the script itself, but if that is something you want, it is really easy to set up:

### Option 1 — Windows Startup Folder

1. Create a shortcut to `EZM-Updater.exe`
2. Open the Startup folder:

For the current user:

```text
shell:startup
```

For all users:

```text
shell:common startup
```

3. Place the shortcut inside the Startup folder

This allows EZM to automatically update each time Windows starts.

---

### Option 2 — Windows Task Scheduler

You can also configure periodic automatic updates using Windows Task Scheduler.

Microsoft guide:

https://learn.microsoft.com/windows/win32/taskschd/task-scheduler-start-page

Example setup:
- Trigger: At logon or daily
- Action: Start `EZM-Updater.exe`

---

## File Locations

EZM-Updater installs files into your Arma 3 profile compositions directory.

Typical location:

```text
Documents\Arma 3 - Other Profiles\<ProfileName>\compositions\
```

The updater creates or updates the following folder:

```text
EZM_Comp\
```

This folder represents the composition you place down. Arma 3 reads the .sqe files inside to get the name and contents of the composition.

---

## Security & Transparency

EZM-Updater is designed to be lightweight and transparent.
It is only active when the script is run by the user. The process only lasts until it is finished installing the composition.

### What the updater does

- Downloads EZM source code (SQF) from GitHub
- Generates local composition structure files (header/comp.sqe)
- Writes files into your Arma 3 profile directory only

### What the updater does NOT do

- Modify Arma 3 game binaries
- Install drivers or services
- Collect personal information
- Run background processes after completion
- Access unrelated files on your system

### Antivirus Warnings

Some antivirus software may flag unsigned executables or small utilities as suspicious due to:
- Low download reputation (uncommon file/low popularity)
- Lack of code signing (code signing & digital signature certificate costs range from $50 to $600+ per year)
- File system modification behavior (exactly what this tool does)

AV Scan:
https://www.virustotal.com/gui/file/34338ca336d22014cf1c14cf5d944278e65d3c216beabe05396dab26b48998bb

If you have any concerns, you are encouraged to:
- Review the source code yourself
- Build the executable from source if desired
- Verify all outbound requests point only to the EZM GitHub repository
- Verify correct hash of release files

---

## FAQ

### Does this install a mod?

No. EZM-Updater installs a Zeus composition into your Arma 3 profile. It does not install a traditional Arma 3 mod.
Compositions are typically a collection of objects (prefabs) for Game Masters to use, but this one just has an invisible helipad with an init script inside which invokes EZM on your client. This is a standard way of running scripts in official public zeus servers. 

---

### Does this overwrite existing compositions?

Only the `EZM_Comp` folder managed by the updater is overwritten or updated.

---

### Do I need to rerun the updater after EZM updates?

Yes — unless you configure automatic updates through Startup or Task Scheduler.

---

### Can I uninstall EZM-Updater?

Yes. Simply:
1. Delete `EZM-Updater.exe`
2. Remove the `EZM_Comp` folder from your Arma 3 profile if desired
3. If you implemented automatic updates, you should remove the shortcut from your startup folder or remove the task from windows task scheduler

---

### Does the updater require administrator privileges?

Typically, no. Standard user permissions are sufficient unless your Arma 3 profile is stored in a protected location.
Although, some Windows users might have the documents folder configured to request or grant permissions first.

---

### Is an internet connection required?

Yes. The updater downloads the latest EZM data from GitHub during execution.

---

### Can I use this with multiple Arma 3 profiles?

Yes, it actually installs EZM to all available A3 profiles by default to avoid the need for the user to configure directories manually.

---

### Why use this instead of manual installation?

EZM-Updater:
- Eliminates manual file copying
- Automatically rebuilds composition files
- Simplifies updates
- Reduces installation mistakes

---

## Credits

- EZM by the Enhanced Zeus Modules contributors  
  https://github.com/expung3d/Enhanced-Zeus-Modules/

---

## Disclaimer

This project is not affiliated with or endorsed by Bohemia Interactive.  
Arma 3 is a trademark of Bohemia Interactive.

If the EZM github repo is ever removed or privated, this tool will no longer work.

---

Feel free to raise an issue if you encounter any bugs. 
