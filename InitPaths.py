import os
from sys import exit as crash_exit
from tkinter.messagebox import showerror
from datetime import datetime

class InitPaths:
	"""
	Класс, который инициирует все необходимые переменные,
	связанные с разными путями для программ, а тажке пути
	к log-файлу и конфигу по умолчанию.
	"""

	def __init__(self):
		if os.name == 'nt':
			self.conf_path_default = "config\\conf.ege"
			self.log_file_path = "log\\logs.log"
			self.sep = "\\"
			self.sublime_path = ""
			self.python_path = ""
			self.intellij_path = ""
			self.pycharm_path = ""
			self.chrome_path = ""
			self.jdk_path = ""
			self.wing_path = ""
			self.csp_filename = ""
			self.vs_20xx = ""
			self.c_prgm_f = "C:\\Program Files\\"
			self.c_prgm_f_x = "C:\\Program Files (x86)\\"
		elif os.name == "posix":
			self.conf_path_default = "config/conf.ege"
			self.log_file_path = "log/logs.log"
			self.sep = "/"
			self.kege_exe = "install.exe"
			self.csp_filename = "CSPSetup.exe"
			self.vs_20xx = ["Program Files", "2022"]
			self.python_path = "Python312"
			self.sublime_path = "Sublime Text"
			self.jdk_path = "jdk-21"
			self.wing_path = ("Program Files", "Wing 101 9")
			self.intellij_path = ("Program Files", "Intellij Idea Community")
			self.pycharm_path = ("Program Files", "Pycharm Community")
			self.chrome_path = "Program Files"

	def init_programs_paths(self):
		"""
		Метод ищет те exe-файлы программ, которые обычно лежат в разных местах. Проверяются некоторые пути и, если
		exe найден, то переменная принимает имя изменяемой части пути. Еслин нет, то путь по-умолчанию.
		Этот метод работает только для Windows.
		"""

		if os.name == "nt":

			kege_exe_count = 1 # Счётчик для определения того, что установочного фала нет.

			for item in os.listdir("resources\\KEGE_program"):
				if "exe" in item:
					self.kege_exe = item
					break
				elif kege_exe_count == len(os.listdir("resources\\KEGE_program")):
					if not os.path.exists(self.log_file_path):
						os.system("mkdir log")
					now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					with open(self.log_file_path, "a", encoding="utf-8") as log:
						log.write(f'{now} >> Установочный файл для программы "Станция КЕГЕ" не найден! Проверьте путь "resources\\KEGE_program"\n')
						showerror("Ошибка", message='Установочный файл для программы "Станция КЕГЕ" не найден!')
						crash_exit('FileNotFoundError - Смотри лог-файл программы.')
				kege_exe_count += 1

			for item in os.listdir(self.c_prgm_f):
				if "Wing" in item:
					self.wing_path = (self.c_prgm_f.split(sep="\\")[1], item)
				if "Python" in item:
					self.python_path = item if os.path.exists(f"{self.c_prgm_f}{item}\\pythonw.exe") else self.python_path
				if "Sublime Text" in item:
					self.sublime_path = item
				if "Intelli" in item:
					self.intellij_path = (self.c_prgm_f.split(sep="\\")[1], item)
				elif "JetBrains" in item and self.intellij_path == "":
					if len(os.listdir(f"{self.c_prgm_f}JetBrains")) == 2:
						if "Intelli" in os.listdir(f"{self.c_prgm_f}JetBrains")[0] or "Intelli" in os.listdir(f"{self.c_prgm_f}JetBrains")[1]:
							self.intellij_path = (
										self.c_prgm_f.split(sep="\\")[1],
										f"JetBrains\\{os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0] if 'Intelli' in os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0] else os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[1]}" # Скорее всего это IntelliJ
											)
					elif "Intelli" in os.listdir(f"{self.c_prgm_f}JetBrains")[0]:
						self.intellij_path = (
										self.c_prgm_f.split(sep="\\")[1],
										f"JetBrains\\{os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0]}"
										)
				if "PyCharm" in item or "Pycharm" in item:
					self.pycharm_path = (self.c_prgm_f.split(sep="\\")[1], item)
				elif "JetBrains" in item and self.pycharm_path == "":
					if len(os.listdir(f"{self.c_prgm_f}JetBrains")) == 2:
						if "PyCharm" in os.listdir(f"{self.c_prgm_f}JetBrains")[0] or "PyCharm" in os.listdir(f"{self.c_prgm_f}JetBrains")[1]:
							self.pycharm_path = (
										self.c_prgm_f.split(sep="\\")[1],
										f"JetBrains\\{os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[1] if 'PyCharm' in os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[1] else os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0]}" # Скорее всего это PyCharm
											)
					elif "PyCharm" in os.listdir(f"{self.c_prgm_f}JetBrains")[0]:
						self.pycharm_path = (
										self.c_prgm_f.split(sep="\\")[1],
										f"JetBrains\\{os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0]}" # Скорее всего это PyCharm
										)

			for item in os.listdir(self.c_prgm_f_x):
				if "Wing" in item and self.wing_path == "":
					self.wing_path = (self.c_prgm_f_x.split(sep="\\")[1], item)
				if "Intelli" in item and self.intellij_path == "":
					self.intellij_path = (self.c_prgm_f_x.split(sep="\\")[1], item)
				elif "JetBrains" in item and self.intellij_path == "":
					if len(os.listdir(f"{self.c_prgm_f_x}JetBrains")) == 2:
						self.intellij_path = (
										self.c_prgm_f_x.split(sep="\\")[1],
										f"JetBrains\\{os.listdir({self.c_prgm_f_x} + 'JetBrains')[0] if 'Intelli' in os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0] else os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[1]}"
										)
					else:
						self.intellij_path = (
										self.c_prgm_f_x.split(sep="\\")[1],
										f"JetBrains\\{os.listdir({self.c_prgm_f_x} + 'JetBrains')[0]}"
									)
				if ("PyCharm" in item or "Pycharm" in item) and self.pycharm_path == "":
					self.pycharm_path = (self.c_prgm_f_x.split(sep="\\")[1], item)
				elif "JetBrains" in item and self.pycharm_path == "":
					if len(os.listdir(f"{self.c_prgm_f_x}JetBrains")) == 2:
						self.pycharm_path = (
										self.c_prgm_f_x.split(sep="\\")[1],
										f"JetBrains\\{os.listdir({self.c_prgm_f_x} + 'JetBrains')[1] if 'PyCharm' in os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[1] else os.listdir(f'{self.c_prgm_f}' + 'JetBrains')[0]}" # Скорее всего это IntelliJ
									)
					else:
						self.pycharm_path = (
										self.c_prgm_f_x.split(sep="\\")[1],
										f"JetBrains\\{os.listdir({self.c_prgm_f_x} + 'JetBrains')[0]}"
									)

				if "Google" in item:
					self.chrome_path = "Program Files (x86)" if os.path.exists("C:\\Program Files (x86)\\Application\\chrome.exe") else "Program Files"

			if os.path.exists("C:\\Program Files\\Java\\"):
				for item in os.listdir("C:\\Program Files\\Java"):
					if "jdk" in item:
						self.jdk_path = item
						break
					else:
						self.jdk_path = "jdk-21"
			else:
				self.jdk_path = "jdk-21"
			for item in os.listdir(f"resources\\KEGE_program\\Prerequisites"):
				if "CSPSetup" in item:
					self.csp_filename = item
					break
			if os.path.exists("C:\\Program Files (x86)\\Microsoft Visual Studio\\2019"):
				self.vs_20xx = ["Program Files (x86)", "2019"]
			elif os.path.exists("C:\\Program Files (x86)\\Microsoft Visual Studio\\2022"):
				self.vs_20xx = ["Program Files (x86)", "2022"]
			elif os.path.exists("C:\\Program Files\\Microsoft Visual Studio\\2019"):
				self.vs_20xx = ["Program Files", "2019"]
			else:
				self.vs_20xx = ["Program Files", "2022"]

			self.python_path = "Python311" if self.python_path == "" else self.python_path
			self.sublime_path = "Sublime Text" if self.sublime_path == "" else self.sublime_path
			self.intellij_path = ("Program Files", "Intellij Idea Community") if self.intellij_path == "" else self.intellij_path
			self.chrome_path = "Program Files" if self.chrome_path == "" else self.chrome_path
			self.wing_path = ("Program Files", "Wing 101 9") if self.wing_path == "" else self.wing_path
			self.pycharm_path = ("Program Files", "Pycharm Community") if self.pycharm_path == "" else self.pycharm_path

	def get_conf_path_default(self):
		return self.conf_path_default

	def get_log_file_path(self):
		return self.log_file_path

	def get_sublime_path(self):
		return self.sublime_path

	def get_python_path(self):
		return self.python_path

	def get_intellij_path(self):
		return self.intellij_path

	def get_pycharm_path(self):
		return self.pycharm_path

	def get_chrome_path(self):
		return self.chrome_path

	def get_jdk_path(self):
		return self.jdk_path

	def get_wing_path(self):
		return self.wing_path

	def get_vs_20xx(self):
		return self.vs_20xx

	def get_install_strings(self):
		install_strings = {
							'Станция_КЕГЭ': f'start /wait resources\\KEGE_program\\{self.kege_exe} /verysilent /suppressmsgboxes /sp- /norestart',
							'Microsoft_Excel': 'start /wait resources\\Office\\setup.exe',
							'Libre_Calc': 'start /wait msiexec /i resources\\libreoffice.msi RebootYesNo=No /passive /norestart',
							'Microsoft_Word': '',
							'Libre_Writer': '',
							'Microsoft_PowerPoint': '',
							'Libre_Impress': '',
							'Sublime_Text': 'start /wait resources\\sublime_text.exe /VERYSILENT /NORESTART',
							'Кумир_Стандарт': 'start /wait resources\\kumir_standart.exe /S',
							'Кумир': 'start /wait resources\\kumir.exe /S',
							'Visual_Studio': f'start /wait resources\\vs{self.vs_20xx[1]}\\vs_community.exe --passive --norestart --wait --add Microsoft.VisualStudio.Workload.ManagedDesktop --add Microsoft.VisualStudio.Workload.NativeDesktop --add Component.GitHub.VisualStudio --add Microsoft.VisualStudio.Component.Git --includeRecommended',
							'CodeBlocks': 'start /wait resources\\codeblocks.exe /S',
							'Free_Pascal': 'start /wait resources\\fpc.exe /silent',
							'Pascal_ABC': 'start /wait resources\\pascalabc.exe /S',
							'Java_JDK': 'start /wait resources\\jdk.exe /s',
							'Intellij_Idea': 'start /wait resources\\ideaIC.exe /S /CONFIG=resources\\silent_IjIC.config /D=C:\\Program Files\\Intellij Idea Community',
							'Eclipse_IDE': f'start /wait xcopy /E /Y resources\\eclipse "C:\\Users\\{os.getlogin()}\\eclipse\\java-2021-09\\eclipse\\"',
							'Python_IDE': 'start /wait resources\\python3.exe /quiet InstallAllUsers=1 PrependPath=1',
							'Wing_IDE': 'start /wait resources\\wing.exe /VERYSILENT /NORESTART',
							'PyCharm': 'start /wait resources\\pycharm-community.exe /S /CONFIG=resources\\silent_pyCh.config /D=C:\\Program Files\\PyCharm Community',
							'Far_Manager': 'start /wait msiexec /qn /i resources\\farmanager.msi ADDLOCAL=ALL',
							'Total_Commander': 'start /wait resources\\tcmd64.exe /AHMGDU',
							'Google_Chrome': 'start /wait resources\\ChromeSetup.exe /silent /install'
					}
		return install_strings

	def get_ege_kege_commands(self):
		ege_kege_commands = (
								'"C:\\Program Files\\Станция КЕГЭ\\unins000.exe" /verysilent /suppressmsgboxes /norestart',
								f'start /wait resources\\KEGE_program\\Prerequisites\\{self.csp_filename} -args "KCLEVEL=1 /passive /quiet"  -noreboot -nodlg'
							)
		return ege_kege_commands

	def get_sublime_text_commands(self):
		sublime_text_commands = (
									f'"C:\\Program Files\\{self.sublime_path}\\unins000.exe" /silent /suppressmsgboxes /norestart'
								)
		return sublime_text_commands

	def get_prog_icons_paths(self):
		prog_icons_paths = {
								"Python_IDE": f'C:\\Program Files\\{self.python_path}\\Lib\\idlelib\\idle.pyw',
								'Free_Pascal': 'C:\\FPC\\3.2.0\\bin\\i386-win32\\fp32.ico',
								'Кумир': 'C:\\Program Files (x86)\\Kumir\\kumir.ico'
							}
		return prog_icons_paths

	def get_constant_list(self):
		CONSTANT_LIST = [
					"KEGE_VER", "EXCEL_VER", "CALC_VER", "WORD_VER", "WRITER_VER", "POWERPOINT_VER",
					"IMPRESS_VER", "SUBLIME_VER", "KUMIR_STD_VER", "KUMIR_VER", "VIS_STUD_VER",
					"CODEBLOCKS_VER", "FREE_PASCAL_VER", "PASCAL_ABC_VER", "JAVA_VER", "INT_IDEA_VER",
					"ECLIPSE_VER", "PYTHON_VER", "WING_VER", "PYCHARM_VER", "FAR_VER", "TOT_COMM_VER",
					"GOOG_CHR_VER"
						]
		return CONSTANT_LIST

	def get_vcpp_dict(self):
		vcpp_dict = {
						'vc_2010_(x86)': 'start /wait resources\\vcpp\\vc2010_x86.exe /install /quiet /norestart',
						'vc_2010_(x64)': 'start /wait resources\\vcpp\\vc2010_x64.exe /install /quiet /norestart',
						'vc_15-19_(x86)': 'start /wait resources\\vcpp\\vc1519_x86.exe /install /quiet /norestart',
						'vc_15-19_(x64)': 'start /wait resources\\vcpp\\vc1519_x64.exe /install /quiet /norestart'
					}
		return vcpp_dict