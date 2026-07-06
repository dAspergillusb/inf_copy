<p align="right">
  <a href="README.md">🇬🇧 English</a> | 
  <a href="README.RU.md">🇷🇺 Русский</a>
</p>

# inf_copy

## What is it?

The project is named **inf_copy**, which originates from its very first version.

The program is written in Python. It relies solely on the Python standard libraries, which are available out of the box right after installation. The only main restriction is the Python version, which must be 3.8 or higher.

If the program needs to be run on a computer without Python installed, a standalone binary file "**_inf_copy.exe_**" is available. It can run on any Windows system. To ensure the program can perform all its automated actions correctly, it must be run with Administrative privileges.

If you are using the Python script version, you must first open the Command Prompt as an administrator, and only then execute the script. The exact steps are described below:

1. Open the Command Prompt as an Administrator:

   ![](https://hub.mos.ru/dietolife/inf_copy/-/raw/main/cmd_open/cmd_start.png)

2. Execute the following commands in the Command Prompt:
- If the program is located on a USB flash drive, you need to switch to that drive. To do this, run the command **_drive_letter:_** (in the screenshot, the letter is **Z**);
- Navigate to the folder containing the program. Enter the command **_cd "path_to_folder"_** (in the screenshot, the command is **cd inf_copy**);
- Run the program using the command **_python inf_copy_v.2.0.py_** (this works if Python was added to your system PATH during installation. If it wasn't, you must specify the full path to the Python executable, for example: **_"C:\Program Files\Python311\python.exe" inf_copy_v.2.0.py_**).

![](https://hub.mos.ru/dietolife/inf_copy/-/raw/main/cmd_open/cmd_window.png)

## Required Components
The program requires the following components to run successfully:

1. The "**doc_pics**" folder.
2. The "**resources**" folder (the folder along with its base content can be downloaded from this link (now not available): https://drive.google.com/drive/folders/1WpqFYJZdH0V00ndgPXq-H_e-maj8isea?usp=sharing). Inside it, you will find two specific folders: `EGE_KEGE` and `KEGE_program`. The first folder is for the "KEGE Station" settings, and the second is for the "KEGE Station" installation files. These folders are initially empty, so you must manually copy the necessary files into them. For `EGE_KEGE`, copy the contents of the "KEGE Station" settings folder as-is. For `KEGE_program`, copy the contents of the folder containing the "KEGE Station" installation files. Everything else is already provided at the link.
3. The "**modules**" folder is required only if you are running the source script **_inf_copy_v.2.0.py_**. If so, you will also need the **_InitPaths.py_** and **_inf_copy.png_** files.
4. If you are using the standalone binary executable, you must include the **__internal_** folder (available at the same link: https://drive.google.com/drive/folders/1WpqFYJZdH0V00ndgPXq-H_e-maj8isea?usp=sharing)(now not available). It contains the necessary libraries required to run the executable.

### Description
To begin with, let’s define some terms used throughout this description:
- "_The program_" — refers to this project, code-named inf_copy.
- "_Software_" — applications like Word, Excel, Python IDE, PyCharm, etc. In other words, everything required by a student taking the exam.
- "_Exam_" — a folder created for files that students need during the exam. It is located at `C:\Exam`. Inside, another folder is created using the exam date (for example, `C:\Exam\16.06.2024`).
- "_TRV_" — the technical readiness control phase (known in Russia as TRV / Technical Readiness Verification), a well-known and crucial step in exam preparation.

Alright, here we go...

This program was designed to streamline the TRV (Technical Readiness Verification) process for the 11th-grade Unified State Exam (EGE) in Computer Science.

Initially, the program was created solely to simplify the setup of the "KEGE Station" across multiple computers, saving a significant amount of time during the preparation phase. At that stage, its only features were creating the `Exam` directory structure and copying the folder with initial "KEGE Station" configurations. Later, the idea emerged to expand its functionality to achieve almost fully automated computer preparation for the computer science exam.

Currently, the program serves as a comprehensive tool for installing software, verifying version validity, and handling automated configurations for all software required during the exam.

Key features of the program:
1. Locates software via its default path, checks the installed version, and automatically installs or updates it if necessary.
2. Clears the desktop completely and creates clean shortcuts for all required software, as well as a shortcut to the `Exam` folder.
3. Copies the "KEGE Station" folder along with its initial configuration (this step can be disabled if not needed).
4. Features a dedicated configuration file that can be modified either directly or via the program's graphical user interface (GUI).
5. Supports a fully automated installation mode. It will verify everything, refresh the desktop, and copy the "KEGE Station" settings on its own, keeping you informed of its current actions via the "Status" field.
6. Includes a semi-automated mode (skips software installation) and a dedicated update mode specifically for the "KEGE Station" software.
7. Features a built-in documentation section with detailed usage instructions. I have tried to make this guide as user-friendly and clear as possible for everyone.

That covers the general overview of the project.

### Screenshots

| Feature | Image |
| ------ | ------ |
| Main Program Window |![](https://hub.mos.ru/dietolife/inf_copy/-/raw/8f47eb27845eff338d85aa4ff8ec23d98827a247/doc_pics/main.png)|
| "File" Menu |![](https://hub.mos.ru/dietolife/inf_copy/-/raw/8f47eb27845eff338d85aa4ff8ec23d98827a247/doc_pics/menu_file.png)|
| "Parameters" Menu |![](https://hub.mos.ru/dietolife/inf_copy/-/raw/8f47eb27845eff338d85aa4ff8ec23d98827a247/doc_pics/menu_params.png)|
| "Help" Menu |![](https://hub.mos.ru/dietolife/inf_copy/-/raw/8f47eb27845eff338d85aa4ff8ec23d98827a247/doc_pics/menu_help.png)|
| "Checklist" Window (Post-Scan) |![](https://hub.mos.ru/dietolife/inf_copy/-/raw/8f47eb27845eff338d85aa4ff8ec23d98827a247/doc_pics/programm_list_after.png)|
| Settings Window |![](https://hub.mos.ru/dietolife/inf_copy/-/raw/8f47eb27845eff338d85aa4ff8ec23d98827a247/doc_pics/settings.png)|
| Documentation Window | ![](https://hub.mos.ru/dietolife/inf_copy/-/raw/main/doc_pics/documentation.png) |

### How to Use?
The comprehensive guide on how to use the program is integrated directly into the application's "Documentation" window. 

### Support
For any questions or inquiries, please contact us via email at: dietolife@gmail.com.

### License
This project is licensed under the GNU GPL v3.

### Project Status
Currently, this program is fully functional within laboratory testing environments. It has been published here to gather feedback, optimize performance, and identify bugs across a broader user base. If you encounter any issues or have feature requests, please report them to dietolife@gmail.com.
