import os
from tkinter import Tk, Toplevel
from tkinter.ttk import Progressbar, Label, Entry
from time import sleep
from datetime import datetime
from threading import Thread
from tkinter.messagebox import showerror
try:
	from FilesOperations import create_shortcut, copy_folder_or_file
except ModuleNotFoundError:
	from modules.FilesOperations import create_shortcut, copy_folder_or_file


class InstallMethod:
	"""
	Класс содержит в себе возможные методы установки, настроки, создания ярлыков программ.
	"""

	def __init__(self, exam_date: str, window: Tk, progressbar: Progressbar, status: Label, entry: Entry, init_paths):
		self.exam_date = exam_date
		self.window = window
		self.progressbar = progressbar
		self.status = status
		self.entry = entry
		self.prog_icons_paths = init_paths.get_prog_icons_paths()
		self.ege_kege_commands = init_paths.get_ege_kege_commands()
		self.install_kege = init_paths.get_install_strings().get("Станция_КЕГЭ")
		self.install_strings = init_paths.get_install_strings()
		self.vcpp_dict = init_paths.get_vcpp_dict()
		self.log_file = init_paths.get_log_file_path()

	def install_only_kege(self):
		"""
		Метод устанавливает только программу "Станция КЕГЭ" без проверки её версии.
		Также не создаёт ярлыки на рабочем столе. Однако, она подчищает все папки Exam,
		удаляет ярлык "Exam.lnk" на рабочем столе и создаёт новый.
		Эта функция пригодится, когда нужно только обновить станцию КЕГЭ и изменить
		папку с датой экзамена в папке Exam.
		"""
		# Проверка имени папки в поле главного окна #######################
		for char in self.entry.get():
			if char in r'<>:"/\|?*':
				showerror("Ошибка в имени папки",
						message='Имя папки не должно содержать\n' + \
								r'следующих знаков - < > : " / \ | ? *')
				return False
		# Подготовка. #####################################################
		self.window.attributes("-topmost", True)
		value = 0
		operations_count = 4
		step = 100 / operations_count
		self.progressbar.configure(value=value)
		self.status.configure(text="Только настройка КЕГЭ", foreground="indigo")
		self.window.update()
		sleep(1)
		###################################################################
		self.status.configure(text="Создаю необходимые папки", foreground="blue")
		self.window.update()
		###################################################################
		# Проверяем существование папок и подчищаем то, что нужно, а ######
		# также создаём необходимое #######################################
		user_name = os.getlogin()
		folder_source_path = 'resources\\'
		folder_target_path = f'C:\\Users\\{user_name}\\AppData\\Roaming\\'
		desktop_path = f'C:\\Users\\{user_name}\\Desktop'
		if os.path.exists(r"C:\Exam"):
			os.system(r"rmdir /S /Q C:\Exam")
		if os.path.exists(f"{desktop_path}\\Exam"):
			os.system(f"rmdir /S /Q {desktop_path}\\Exam")
		if os.path.exists(f"{desktop_path}\\Exam.lnk"):
			os.system(f"del {desktop_path}\\Exam.lnk")
		if os.path.exists(f"{desktop_path}\\Станция КЕГЭ.lnk"):
			os.system(f"del {desktop_path}\\Станция КЕГЭ.lnk")
		os.system(f"mkdir C:\\Exam\\{self.exam_date}")
		if os.path.exists(f"{folder_target_path}{self.entry.get()}") and self.entry.get() != "":
			os.system(f"rmdir /S /Q {folder_target_path}{self.entry.get()}")
		###################################################################
		self.status.configure(text="Папки созданы", foreground="blue")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		sleep(1)
		self.status.configure(text="Устанавливаю программу КЕГЭ", foreground="blue")
		self.window.update()
		# Установка программы "Станция КЕГЭ". #############################
		for command in self.ege_kege_commands:
			os.system(command)
			sleep(1)
		install_prog = Thread(target=os.system(self.install_kege))
		install_prog.start()
		dot = ""
		while install_prog.is_alive():
			self.status.configure(text=f"Устанавливаю программу КЕГЭ{dot}")
			dot += "."
			if dot == "....":
				dot = ""
			self.window.update()
			self.window.after(1000)
		###################################################################
		self.status.configure(text="Программа КЕГЭ установлена", foreground="blue")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		sleep(1)
		self.status.configure(text="Создаю ярлык для Exam", foreground="blue")
		self.window.update()
		###################################################################
		# Создаём ярлык новой папки Exam. #################################
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Exam.lnk",
						target_path=f"C:\\Exam\\{self.exam_date}",
						description="Папка для загрузки файлов"
					)
		self.status.configure(text="Ярлык создан.", foreground="blue")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		sleep(1)
		###################################################################
		if self.entry.get() != "":
			self.status.configure(text=f"Копирую папку {self.entry.get()}...", foreground="blue")
			self.window.update()
			###################################################################
			# Копируем папку EGE_KEGE с заранее подготовленными настройками ###
			copy = copy_folder_or_file(
										folder_file_name=self.entry.get(),
										folder_file_source_path=folder_source_path,
										folder_file_target_path=folder_target_path,
										log_file=self.log_file
									)
			if copy:
				self.status.configure(text="Готово!", foreground="green")
				value += step
				self.progressbar.configure(value=value)
				self.window.update()
			else:
				self.status.configure(text="Ошибка! Смотри логи.", foreground="red")
				self.window.update()
			self.window.attributes("-topmost", False)
		else:
			self.status.configure(text="Готово!", foreground="green")
			value += step
			self.progressbar.configure(value=value)
			self.window.update()

	def start_auto(self, params: list):
		"""
		Метод - полный автомат (запустил и пошел пить чай/кофе). Cам проверяет по списку программы, какие установлены и достаточно
		ли новая версия, что необходимо ставит/обновляет, чистит все необходимые папки, создает папку Exam
		и очищает весь рабочий стол от всего, а также создаёт все ярлыки на рабочем столе.
		"""
		# Проверка имени папки в поле главного окна #######################
		for char in self.entry.get():
			if char in r'<>:"/\|?*':
				showerror("Ошибка в имени папки",
						message='Имя папки не должно содержать\n' + \
								r'следующих знаков - < > : " / \ | ? *')
				return False
		###################################################################
		self.window.attributes("-topmost", True)
		value = 0
		operations_count = 54
		step = 100 / operations_count
		self.progressbar.configure(value=value)
		self.status.configure(text="Автоматическая установка", foreground="indigo")
		self.window.update()
		sleep(1)
		self.status.configure(text="Готовлю список программ...", foreground="blue")
		self.window.update()
		# Генерируем список программ ######################################
		soft_list = [params[x].split(sep="=")[0] for x in range(
													params.index("[Program names/paths]") + 1,
													params.index("[End paths]")
																)]
		CONSTANTS = [params[x].split(sep="=")[1] for x in range(
													params.index("[Constants]\n"[:-1]) + 1,
													params.index("[End constants]\n"[:-1])
																)]
		soft_paths = [params[x].split(sep="=")[1] for x in range(
													params.index("[Program names/paths]") + 1,
													params.index("[End paths]")
																)]
		###################################################################
		sleep(1)
		self.status.configure(text="Список составлен", foreground="green")
		self.window.update()
		value += step
		self.progressbar.configure(value=value)
		sleep(1)
		self.status.configure(text="Проверяю проги...", foreground="blue")
		self.window.update()
		###################################################################
		# Проверяем состояние каждой программы: стоит или нет, та версия ##
		# или нет. Формируем словарь с данными. ###########################
		install_dict = self.checklist_soft_ver(soft_list, soft_paths, CONSTANTS)
		###################################################################
		sleep(1)
		self.status.configure(text="Проверено!", foreground="green")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		sleep(1)
		self.status.configure(text="Начинаю ставить программы...", foreground="blue")
		self.window.update()
		sleep(1)
		###################################################################
		# Производим установку/обновление необходимых программ. ###########
		for library in self.vcpp_dict:
			library_installs = library.replace('_', ' ')
			self.status.configure(text=f"Установка {library_installs}")
			self.window.update()
			install_lib = Thread(target=lambda: os.system(self.vcpp_dict.get(library)))
			install_lib.start()
			dot = ""
			while install_lib.is_alive():
				self.status.configure(text=f"Установка {library_installs}{dot}")
				dot += "."
				if dot == "....":
					dot = ""
				self.window.update()
				self.window.after(1000)
			value += step
			self.progressbar.configure(value=value)
		for soft_name in install_dict:
			dot = ""
			if soft_name == "Microsoft_Excel":
				soft_installs = "Microsoft Office"
			elif soft_name == "Libre_Calc":
				soft_installs = "Libre Office"
			else:
				soft_installs = soft_name.replace('_', ' ')
			self.status.configure(text=f"Установка {soft_installs}", foreground="blue")
			self.window.update()
			if install_dict.get(soft_name):
				self.progressbar.configure(value=value)
				self.window.update()
			else:
				if soft_name == "Станция_КЕГЭ":
					for command in self.ege_kege_commands:
						os.system(command)
				install_prog = Thread(target= lambda: os.system(self.install_strings.get(soft_name)))
				install_prog.start()
				while install_prog.is_alive():
					self.status.configure(text=f"Установка {soft_installs}{dot}")
					dot += "."
					if dot == "....":
						dot = ""
					self.window.update()
					self.window.after(1000)
				self.progressbar.configure(value=value)
				self.window.update()
			value += step
		###################################################################
		self.status.configure(text="Все проги поставлены!", foreground="green")
		self.window.update()
		sleep(1)
		self.status.configure(text="Настройка папок...", foreground="blue")
		self.window.update()
		###################################################################
		# Проверяем существование папок и подчищаем то, что нужно, а ######
		# также создаём необходимое #######################################
		user_name = os.getlogin()
		folder_source_path = 'resources\\'
		folder_target_path = f'C:\\Users\\{user_name}\\AppData\\Roaming\\'
		desktop_path = f'C:\\Users\\{user_name}\\Desktop'
		desktop_path_public = f'C:\\Users\\Public\\Desktop'
		if os.path.exists(r"C:\Exam"):
			os.system(r"rmdir /S /Q C:\Exam")
		if os.path.exists(f"C:\\Users\\{user_name}\\Desktop\\Exam"):
			os.system(f"rmdir /S /Q C:\\Users\\{user_name}\\Desktop\\Exam")
		os.system(f"mkdir C:\\Exam\\{self.exam_date}")
		if os.path.exists(f"{folder_target_path}{self.entry.get()}") and self.entry.get() != "":
			os.system(f"rmdir /S /Q {folder_target_path}{self.entry.get()}")
		os.system(f"del /F /S /Q {desktop_path}\\*")
		os.system(f"del /F /S /Q {desktop_path_public}\\*")
		for del_folder in os.listdir(desktop_path):
			os.system(f"rd /S /Q {desktop_path}\\{del_folder}")
		for del_folder_pub in os.listdir(desktop_path_public):
			os.system(f"rd /S /Q {desktop_path_public}\\{del_folder_pub}")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		###################################################################
		self.status.configure(text="Создаю ярлыки...", foreground="blue")
		self.window.update()
		###################################################################
		# Генерим ярлыки на программы и в том числе ярлык для папки #######
		# экзамена. #######################################################
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Exam.lnk",
						target_path=f"C:\\Exam\\{self.exam_date}",
						description="Папка для загрузки файлов"
					)
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Microsoft Edge.lnk",
						target_path=f"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
						description="Папка для загрузки файлов"
					)
		for prog_name in soft_list:
			if prog_name == "Python_IDE":
				target_path = self.prog_icons_paths.get("Python_IDE")
			else:
				target_path = soft_paths[soft_list.index(prog_name)][1:-1]
			if prog_name == "Free_Pascal" or prog_name == "Кумир":
				shortcut_icon = self.prog_icons_paths.get(prog_name)
			else:
				shortcut_icon = target_path
			create_shortcut(
							shortcut_path=f'{desktop_path}\\{prog_name.replace("_", " ")}.lnk',
							target_path=target_path,
							description=f'{prog_name.replace("_", " ")}',
							shortcut_icon=shortcut_icon
						)
			value += step
			self.progressbar.configure(value=value)
			self.window.update()
		###################################################################
		if self.entry.get() != "":
			self.status.configure(text=f"Копирую папку {self.entry.get()}...", foreground="blue")
			self.window.update()
			###################################################################
			# Копируем папку EGE_KEGE с заранее подготовленными настройками ###
			copy = copy_folder_or_file(
										folder_file_name=self.entry.get(),
										folder_file_source_path=folder_source_path,
										folder_file_target_path=folder_target_path,
										log_file=self.log_file
									)
			if copy:
				self.status.configure(text="Готово!", foreground="green")
				value += step
				self.progressbar.configure(value=100)
				self.window.update()
			else:
				self.status.configure(text="Ошибка! Смотри логи.", foreground="red")
				self.window.update()
			self.window.attributes("-topmost", False)
		else:
			self.status.configure(text="Готово!", foreground="green")
			value += step
			self.progressbar.configure(value=100)
			self.window.update()

	def start_manual(self, params: list):
		"""
		Метод-полуавтомат. Он подразумевает, что все программы были проверены и установлены заранее через
		соответствующее меню программы. В задачи входят: подчищение всех необходимых папок,
		очистка рабочего стола, создание новых ярлыков на рабочем столе, копирование папки EGE_KEGE с настройками.
		"""

		# Проверка имени папки в поле главного окна #######################
		for char in self.entry.get():
			if char in r'<>:"/\|?*':
				showerror("Ошибка в имени папки",
						message='Имя папки не должно содержать\n' + \
								r'следующих знаков - < > : " / \ | ? *')
				return False
		###########################################################################################################
		self.status.configure(text="Начинаем...",  foreground="blue")
		self.window.update()
		# Генерируем список программ ##############################################################################
		soft_list = [params[x].split(sep="=")[0] for x in range(
													params.index("[Program names/paths]") + 1,
													params.index("[End paths]")
																)]
		soft_paths = [params[x].split(sep="=")[1] for x in range(
													params.index("[Program names/paths]") + 1,
													params.index("[End paths]")
																)]
		###########################################################################################################
		value = 0
		operations_count = 27
		step = 100 / operations_count
		self.progressbar.configure(value=value) # Значение прогресса равен нулю
		user_name = os.getlogin() # Получаем имя пользователя
		folder_source_path = 'resources\\'
		folder_target_path = f'C:\\Users\\{user_name}\\AppData\\Roaming\\' # Получаем адрес папки "Roaming" с именем пользователя
		desktop_path = f'C:\\Users\\{user_name}\\Desktop'
		desktop_path_public = f'C:\\Users\\Public\\Desktop'
		###########################################################################################################
		self.status.configure(text="Подготавливаю папки...", foreground="blue")
		self.window.update()
		###########################################################################################################
		# Проверяем существование папок и подчищаем то, что нужно, а также создаём необходимое ####################
		if os.path.exists(r"C:\Exam"):
			os.system(r"rmdir /S /Q C:\Exam")
		if os.path.exists(f"C:\\Users\\{user_name}\\Desktop\\Exam"):
			os.system(f"rmdir /S /Q C:\\Users\\{user_name}\\Desktop\\Exam")
		os.system(f"mkdir C:\\Exam\\{self.exam_date}")
		if os.path.exists(f"{folder_target_path}{self.entry.get()}") and self.entry.get() != "":
			os.system(f"rmdir /S /Q {folder_target_path}{self.entry.get()}")
		os.system(f"del /F /S /Q {desktop_path}\\*")
		os.system(f"del /F /S /Q {desktop_path_public}\\*")
		for del_folder in os.listdir(desktop_path):
			os.system(f"rd /S /Q {desktop_path}\\{del_folder}")
		for del_folder_pub in os.listdir(desktop_path_public):
			os.system(f"rd /S /Q {desktop_path_public}\\{del_folder_pub}")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		###########################################################################################################
		self.status.configure(text="Создаю ярлыки...", foreground="blue")
		self.window.update()
		###########################################################################################################
		# Создаём ярлыки на рабочем столе #########################################################################
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Exam.lnk",
						target_path=f"C:\\Exam\\{self.exam_date}",
						description="Папка для загрузки файлов"
					)
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Microsoft Edge.lnk",
						target_path=f"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
						description="Папка для загрузки файлов"
					)
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		for prog_name in soft_list:
			if prog_name == "Python_IDE":
				target_path = self.prog_icons_paths.get("Python_IDE")
			else:
				target_path = soft_paths[soft_list.index(prog_name)][1:-1]
			if prog_name == "Free_Pascal" or prog_name == "Кумир":
				shortcut_icon = self.prog_icons_paths.get(prog_name)
			else:
				shortcut_icon = target_path
			create_shortcut(
							shortcut_path=f'{desktop_path}\\{prog_name.replace("_", " ")}.lnk',
							target_path=target_path,
							description=f'{prog_name.replace("_", " ")}',
							shortcut_icon=shortcut_icon
						)
			value += step
			self.progressbar.configure(value=value)
			self.window.update()
		###########################################################################################################
		if self.entry.get() != "":
			self.status.configure(text=f"Копирую папку {self.entry.get()}...", foreground="blue")
			self.window.update()
			###########################################################################################################
			copy = copy_folder_or_file(
										folder_file_name=self.entry.get(),
										folder_file_source_path=folder_source_path,
										folder_file_target_path=folder_target_path,
										log_file=self.log_file
									)
			if copy:
				self.status.configure(text="Готово!", foreground="green")
				value += step
				self.progressbar.configure(value=value)
				self.window.update()
			else:
				self.status.configure(text="Ошибка! Смотри логи.", foreground="red")
				self.window.update()
		else:
			self.status.configure(text="Готово!", foreground="green")
			value += step
			self.progressbar.configure(value=value)
			self.window.update()

	def checklist_soft_ver(self, soft_list: list, soft_paths: list, CONSTANTS: list):
		"""
		Метод составляет словарь с названиями программ и булевым значением,
		которое говорит о необходимости установки программы.
		soft_list - список с именами программ.
		soft_paths - список с путями к exe-файлам проверяемых программ.
		CONSTANTS - список со значениями констант.
		"""
		install_progs_list = []
		soft_number = 0 # Задаём индекс названия программы в списке soft_list
		for program in soft_list:
			if self.soft_check_ver(soft_paths[soft_list.index(program)][1:-1], CONSTANTS[soft_list.index(program)]):
				install_progs_list.append(True)
			else:
				install_progs_list.append(False)
			soft_number += 1
		return dict(zip(soft_list, install_progs_list))

	def soft_check_ver(self, soft_path: str, CONSTANT_: str):
		"""
		Метод проверяет наличие исполняемого файла пути и, если он есть, то сравнивает дату
		его последнего изменения с датой, записанной в константах. Если всё хорошо,
		то возвращает True, если всё плохо, то возвращает False.
		soft_path - путь к исполняемому файлу конкретной программы.
		CONSTANT_ - значение константы
		"""

		if os.path.exists(soft_path):
			mtime = os.stat(soft_path).st_mtime
			change_date = int(datetime.fromtimestamp(mtime).strftime("%Y%m%d"))
			if change_date >= int(CONSTANT_):
				return True
		return False

	def update_desktop_shortcuts(self, height: int, width: int, params: list):
		"""
		Метод создает маленькое окно с индикатором выполнения для анимации процесса.
		Он очищает рабочий стол от всего, что есть на нем (в том числе и в папке ...\\Public\\Desktop)
		и создает там ярлыки программ по списку.
		height - разрешение экрана по вертикали.
		width - разрешение экрана по горизонтали.
		params - основной список со всеми данными программы
		"""
		desktop_shortcuts = Toplevel()
		desktop_shortcuts.title("Ярлыки")
		desktop_shortcuts.geometry(f"120x40+{(width // 2) - 60}+{(height // 2)}")
		desktop_shortcuts.attributes("-topmost", True)
		if os.name == "posix":
			desktop_shortcuts.attributes("-type", "dock")
		else:
			desktop_shortcuts.overrideredirect(True)
		desktop_shortcuts.resizable(False, False)
		progressbar = Progressbar(desktop_shortcuts, orient="horizontal", length=100, value=0)
		progressbar.pack(side="top", padx=10, pady=10)

		value = 0
		step = 100 / 25
		desktop_path = f'C:\\Users\\{os.getlogin()}\\Desktop'
		desktop_path_public = f'C:\\Users\\Public\\Desktop'
		os.system(f"del /F /S /Q {desktop_path}\\*")
		os.system(f"del /F /S /Q {desktop_path_public}\\*")
		for del_folder in os.listdir(desktop_path):
			os.system(f'rd /S /Q "{desktop_path}\\{del_folder}"')
		for del_folder_pub in os.listdir(desktop_path_public):
			os.system(f'rd /S /Q "{desktop_path_public}\\{del_folder_pub}"')
		value += step
		progressbar.configure(value=value)
		desktop_shortcuts.update()
		sleep(0.5)
		soft_list = [params[x].split(sep="=")[0] for x in range(
																params.index("[Program names/paths]") + 1,
																params.index("[End paths]")
																)
					]
		soft_paths = [params[x].split(sep="=")[1] for x in range(
																params.index("[Program names/paths]") + 1,
																params.index("[End paths]")
																)
					]
		for prog_name in soft_list:
			if prog_name == "Python_IDE":
				target_path = self.prog_icons_paths.get("Python_IDE")
			else:
				target_path = soft_paths[soft_list.index(prog_name)][1:-1]
			if prog_name == "Free_Pascal" or prog_name == "Кумир":
				shortcut_icon = self.prog_icons_paths.get(prog_name)
			else:
				shortcut_icon = target_path
			create_shortcut(
							shortcut_path=f'{desktop_path}\\{prog_name.replace("_", " ")}.lnk',
							target_path=target_path,
							description=f'{prog_name.replace("_", " ")}',
							shortcut_icon=shortcut_icon
						)
			value += step
			progressbar.configure(value=value)
			desktop_shortcuts.update()
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Exam.lnk",
						target_path=f"C:\\Exam\\{self.exam_date}",
						description="Папка для загрузки файлов"
					)
		value += step
		progressbar.configure(value=value)
		desktop_shortcuts.update()
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Microsoft Edge.lnk",
						target_path=f"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
						description="Папка для загрузки файлов"
					)
		value += step
		progressbar.configure(value=value)
		desktop_shortcuts.update()
		sleep(1)
		desktop_shortcuts.destroy()

	def update_exam_folder(self):
		"""
		Метод только обновляет папку Exam, удаляет ярлык старый
		и создает ярлык на рабочем столе для новой папки.
		"""
		value = 0
		operations_count = 2
		step = 100 / operations_count
		desktop_path = f'C:\\Users\\{os.getlogin()}\\Desktop'
		self.status.configure(text="Только обновление папки Exam", foreground="indigo")
		self.progressbar.configure(value=value)
		self.window.update()
		sleep(1)
		self.status.configure(text="Подготавливаю папки...", foreground="blue")
		self.window.update()
		if os.path.exists(r"C:\Exam"):
			os.system(r"rmdir /S /Q C:\Exam")
		if os.path.exists(f"{desktop_path}\\Exam"):
			os.system(f"rmdir /S /Q {desktop_path}\\Exam")
		if os.path.exists(f"{desktop_path}\\Exam.lnk"):
			os.system(f"del /F /S /Q {desktop_path}\\Exam.lnk")
		os.system(f"mkdir C:\\Exam\\{self.exam_date}")
		self.status.configure(text="Папки готовы", foreground="green")
		value += step
		self.progressbar.configure(value=value)
		self.window.update()
		sleep(1)
		self.status.configure(text="Создаю ярлык...", foreground="blue")
		self.window.update()
		create_shortcut(
						shortcut_path=f"{desktop_path}\\Exam.lnk",
						target_path=f"C:\\Exam\\{self.exam_date}",
						description="Папка для загрузки файлов"
					)
		sleep(1)
		value += step
		self.progressbar.configure(value=value)
		self.status.configure(text="Готово!", foreground="green")
		self.window.update()
