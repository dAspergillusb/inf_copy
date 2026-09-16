<p align="right">
  <a href="README.md">🇬🇧 English</a> |
  <a href="README.RU.md">🇷🇺 Русский</a>
</p>

# inf_copy

Windows workstation preparation and software deployment automation for computer science exam environments.

The project was created to reduce repetitive manual setup across multiple exam workstations. It checks required software, compares installed versions, performs silent installations or updates, prepares the exam directory structure, refreshes desktop shortcuts, and copies the required KEGE Station configuration.

## Why this project exists

Preparing many Windows computers for a high-stakes computer science exam involves the same configuration steps on every workstation. Performing them manually is slow and error-prone.

`inf_copy` automates this workflow and provides a GUI so the operator can monitor or configure the process instead of repeating the same installation tasks by hand.

## Key Features

- detects required software using configured installation paths
- checks installed application versions
- automatically installs missing software
- automatically updates outdated software
- supports silent installation where available
- creates and prepares the exam directory structure
- copies KEGE Station configuration files
- rebuilds desktop shortcuts for the required software
- supports fully automated and semi-automated workflows
- provides a dedicated KEGE Station update mode
- includes configurable paths and parameters
- displays current operation status in the GUI
- includes integrated user documentation

## Tech Stack

- Python
- Python standard library
- Windows command-line tooling
- filesystem and process automation
- GUI-based configuration and progress reporting

The source version requires **Python 3.8+**. The project can also be packaged as a standalone Windows executable for machines where Python is not installed.

## Automation Workflow

```text
Start
  │
  ▼
Read configuration
  │
  ▼
Inspect workstation
  │
  ├── required software present?
  │        │
  │        ├── no  → install
  │        └── yes → compare version → update if needed
  │
  ▼
Prepare exam folders
  │
  ▼
Copy KEGE Station configuration
  │
  ▼
Refresh desktop shortcuts
  │
  ▼
Report current status
```

## Project Structure

```text
.
├── inf_copy_v.2.0.py
├── InitPaths.py
├── modules/
├── config/
├── doc_pics/
├── log/
├── inf_copy.png
├── README.md
└── README.RU.md
```

## Running from Source

The application performs system-level configuration tasks, so run the terminal with Administrator privileges.

Clone the repository:

```bash
git clone https://github.com/dAspergillusb/inf_copy.git
cd inf_copy
```

Run the application:

```bash
python inf_copy_v.2.0.py
```

If Python is not available in `PATH`, use the full path to the Python executable.

## Operating Modes

### Fully Automated

Checks the workstation, installs or updates required software, prepares the desktop and exam folders, and copies the configured KEGE Station resources.

### Semi-Automated

Runs the preparation workflow while skipping automatic software installation.

### KEGE Station Update

Provides a dedicated workflow for updating the KEGE Station software/configuration when a full workstation rebuild is unnecessary.

## Configuration

The application uses configurable paths and settings for required software and exam resources. Configuration can be edited directly or through the graphical interface.

Some exam-specific resources are intentionally not stored in this public repository and must be supplied separately when deploying the tool in a real exam environment.

## Background

This project grew from a small utility for copying KEGE Station configuration into a broader workstation automation tool. It reflects practical experience with:

- Python automation
- Windows administration
- software deployment
- version detection
- filesystem operations
- subprocess / command-line integration
- repeatable workstation configuration
- reducing manual setup across multiple machines

## Status

The project has been used and tested as a workstation-preparation tool in a laboratory environment. The public repository is maintained as a portfolio and feedback version of the project.

## Author

**Nikita Zelentsov**  
Python Backend Developer / Automation Engineer

GitHub: [@dAspergillusb](https://github.com/dAspergillusb)

## License

GNU GPL v3
