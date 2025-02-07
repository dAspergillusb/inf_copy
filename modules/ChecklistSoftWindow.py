import os
from tkinter import Toplevel
from tkinter import ttk
from tkinter.messagebox import showinfo
from datetime import datetime
from time import sleep
from threading import Thread


class ChecklistSoftWindow:
	"""
	Класс занимается созданием окна "Чек-листа приложений", Проверкой, установкой программ.
	"""
	def __init__(self, width: int, height: int, icon, params: list, init_paths):
		self.width = width
		self.height = height
		self.height_checklist_after = "690"
		self.icon = icon
		self.params = params
		self.install_all_but = False
		self.conf_path_default = init_paths.get_conf_path_default()
		self.ege_kege_commands = init_paths.get_ege_kege_commands()
		self.install_strings = init_paths.get_install_strings()
		self.sublime_text_commands = init_paths.get_sublime_text_commands()
		self.sublime_path = init_paths.get_sublime_path()
		self.vcpp_dict = init_paths.get_vcpp_dict()
		self.checklist = Toplevel()
		self.checklist.title("Чек-лист программ")
		self.checklist.geometry(f"460x660+{(self.width // 2) - 230}+{(self.height // 2) - 330}")
		#self.checklist.attributes("-topmost", True)
		self.checklist.resizable(False, False)
		self.checklist.wm_iconphoto(False, self.icon)

	###########################################################################################################
	def create_soft_checklist(self):
		"""
		Метод создаёт окно со списком программ и статусом "Не проверено" напротив каждой позиции программы.
		После нажатия на кнопку "Проверить" функция передаёт список программ, список надписей (именно объектов)
		функции checklist_soft_ver на проверку программ на предмет существования её в системе или актуальности
		её версии.
		"""

		soft_list = [self.params[x].split(sep="=")[0] for x in range(
													self.params.index("[Program names/paths]\n"[:-1]) + 1,
													self.params.index("[End paths]\n"[:-1])
																	)
					]
		soft_paths = [self.params[x].split(sep="=")[1] for x in range(
													self.params.index("[Program names/paths]\n"[:-1]) + 1,
													self.params.index("[End paths]\n"[:-1])
																	)
					]
		CONSTANTS = [self.params[x].split(sep="=")[1] for x in range(
													self.params.index("[Constants]\n"[:-1]) + 1,
													self.params.index("[End constants]\n"[:-1])
																	)
					]

		check_frame_bottom = ttk.Frame(self.checklist)
		check_frame_bottom.pack(side="top")
		check_frame_one_two = ttk.Frame(self.checklist, borderwidth=1, relief="solid", padding=[10, 10])
		check_frame_one_two.pack(side="top")
		check_frame_one = ttk.Frame(check_frame_one_two, width=20)
		check_frame_one.pack(side="left")
		check_frame_two = ttk.Frame(check_frame_one_two)
		check_frame_two.pack(side="right", padx=20)
		check_frame_button = ttk.Frame(self.checklist)
		check_frame_button.pack(side="top")
		check_frame_install_nes = ttk.Frame(self.checklist, padding=[5, 5])
		check_frame_install_nes.pack(side="bottom")
		ttk.Label(check_frame_bottom, text="Список проверяемых программ", font=("Arial", 12)).pack(side="top", pady = 10, expand=1)
		list_labels_check = []
		for soft_name in soft_list:
			ttk.Label(check_frame_one, text=soft_name.replace("_", " "), font=("Arial", 12)).pack(side="top", padx=0, pady=1)
			locals()[soft_name] = ttk.Label(check_frame_two, text="Не проверено", foreground="black", font=("Arial", 12))
			locals()[soft_name].pack(side="top", padx=0, pady=1)
			list_labels_check.append(locals()[soft_name])
		ttk.Button(
					check_frame_button,
					text="Проверить",
					command=lambda: self.checklist_soft_ver(
														soft_list=soft_list,
														soft_paths=soft_paths,
														CONSTANTS=CONSTANTS,
														obj_checklist=self.checklist,
														obj_frame=check_frame_install_nes,
														list_labels_check=list_labels_check
													)
				).pack(side="left", padx=15, pady=7)
		ttk.Button(check_frame_button, text="Выход", command=lambda: self.exit()).pack(side="left", padx=15, pady=7)

	###########################################################################################################
	def checklist_soft_ver(self, soft_list: list, soft_paths: list, CONSTANTS: list, obj_checklist: Toplevel, obj_frame: ttk.Frame, list_labels_check: list):
		"""
		Метод проверяет по заданному пути наличие исполняемого файла программы и, если он есть, то сравнивает
		дату последнего изменения этого файла с заданным в константах.
		Если исполняемый файл существует, и версия актуальная, то функция в список установок добавляет "True".
		Во всех  остальных случаях она добавляет "False".
		Кроме того, функция меняет в окне со списком статус каждой программы на "Установить", "Обновить"
		или "Проверено" (если всё хорошо) после проверки.
		soft_list - список с именами программ.
		soft_paths - список путей к exe-файлам проверяемых программ.
		obj_checklist - объект типа Toplevel() (окно со списком программ).
		obj_frame - объект типа ttk.Frame для добавления кнопки в окно со списком программ.
		list_labels_check - список объектов типа ttk.Label для изменения их надписей.
		"""

		install_progs_list = []
		soft_number = 0 # Задаём индекс названия программы в списке soft_list
		for label in list_labels_check:
			soft_path_ver = self.soft_check_ver(
											soft_list[soft_number],
											soft_paths[soft_number][1:-1],
											CONSTANTS[soft_number]
										)
			if soft_path_ver == (True, True): 
				label.configure(text="Проверено", foreground="green")
				install_progs_list.append(True)
			elif soft_path_ver == (True, False):
				label.configure(text="Обновить", foreground="red")
				install_progs_list.append(False)
			else:
				label.configure(text="Установить", foreground="red")
				install_progs_list.append(False)
			soft_number += 1
		if not self.install_all_but:
			obj_checklist.geometry(f"460x{self.height_checklist_after}+{(self.width // 2) - 230}+{(self.height // 2) - int(self.height_checklist_after) // 2}")
			install_all = ttk.Button(
										obj_frame,
										text="Установить необходимое",
										command=lambda: self.install_soft(
																			dict(zip(soft_list, install_progs_list)),
																			list_labels_check,
																			obj_checklist
																		)
									)
			install_all.pack(side="top", expand=1, pady=0)
			self.install_all_but = True
		elif not (False in install_progs_list):
			obj_checklist.geometry(f"460x660+{(self.width // 2) - 230}+{(self.height // 2) - 330}")

	###########################################################################################################
	def soft_check_ver(self, soft_name: str, soft_path: str, CONSTANT_: str):
		"""
		Метод проверяет наличие исполняемого файла пути и, если он есть, то сравнивает дату
		его последнего изменения с датой, записанной в константах. Если всё хорошо,
		то возвращает кортеж (True, True), если дата более старая, чем записанная в константах,
		то возвращает кортеж (True, False), если всё плохо, то возвращает кортеж (False, False).
		soft_name - строка с названием программы.
		soft_path - строка-путь к исполняемому файлу конкретной программы.
		CONSTANT_ - значение константы
		"""

		if os.path.exists(soft_path):
			mtime = os.stat(soft_path).st_mtime
			change_date = int(datetime.fromtimestamp(mtime).strftime("%Y%m%d"))
			if change_date >= int(CONSTANT_):
				return True, True
			else:
				return True, False
		return False, False

	###########################################################################################################
	def install_soft(self, soft_dict: dict, list_labels_check: list, obj_checklist: Toplevel):
		"""
		Метод устанавливает программы согласно словарю soft_dict, который передаётся ей.
		Словарь вида: {"Название программы": True/False}, где True - ставить программу не нужно. False - функция
		передает сгенерерованную строку "Устанавливается {ИМЯ_ПРОГРАММЫ} и строку с командой "тихой"" установки
		программы в метод active_install_window.
		soft_dict - словарь вида {"Название программы": True или False}.
		list_labels_check - список надписей из окна с перечнем программ.
		obj_checklist - объект типа Toplevel окна "Чек-листо программ".
		"""

		soft_list = list(soft_dict.keys())
		for library in self.vcpp_dict:
			self.active_install_window(f'Устанавливается\n{library.replace("_", " ")}', self.vcpp_dict.get(library))
		for soft_name in soft_dict:
			if soft_name == "Microsoft_Excel":
				soft_installs = "Microsoft Office"
			elif soft_name == "Libre_Calc":
				soft_installs = "Libre Office"
			else:
				soft_installs = soft_name.replace('_', ' ')
			if not soft_dict.get(soft_name):
				if soft_name == "Станция_КЕГЭ":
					for command in self.ege_kege_commands:
						os.system(command)
						sleep(1)
				if soft_name == "Sublime_Text" and list_labels_check[soft_list.index(soft_name)].cget("text") == "Обновить":
					self.sublite_text_uninst_update(uninstall_sublime=True, update_variable_sublime_path=True)
				self.active_install_window(f'Устанавливается\n{soft_installs}', self.install_strings.get(soft_name))
				list_labels_check[soft_list.index(soft_name)].configure(text="Установлено", foreground="green")
				obj_checklist.update()
				obj_checklist.after(500)
		return showinfo(title="Успех", message="Все программы установлены или обновлены.\nПроверьте ещё раз статусы.")

	###########################################################################################################
	def active_install_window(self, text: str, command: str):
		"""
		Метод создает объект типа Toplevel с информацией об устанавливаемой программе. Некоторые программы устанавливаются
		достаточно долго, поэтому создается впечатление, что настоящая программа зависла. Чтобы этого не было в окне
		присутствует анимация в виде таймера, который отсчитывает время в секундах с момента начала установки конкретной
		программы из списка.
		text - строка с названием устанавливаемой программы.
		command - строка с командой "тихой" установки.
		"""

		self.checklist.attributes("-topmost", True)
		active_inst = Toplevel()
		active_inst.geometry(f"180x110+{(self.width // 2) - 60}+{(self.height // 2)}")
		active_inst.overrideredirect(True)
		active_inst.resizable(False, False)
		active_inst.attributes("-topmost", True)
		main_frame = ttk.Frame(active_inst, borderwidth=20, relief="ridge")
		main_frame.pack(side="top")
		ttk.Label(
					main_frame,
					text=text,
					font=("Arial", 12),
					foreground="blue",
					justify="center"
				).pack(side="top", ipadx=5, ipady=5)
		install_process_sec = ttk.Label(
					main_frame,
					text="",
					font=("Arial", 10),
					justify="center"
				)
		install_process_sec.pack(side="top")
		active_inst.update()
		dots = " ."
		count = 0
		install_process = Thread(target=lambda: os.system(command))
		install_process.start()
		while install_process.is_alive():
			install_process_sec.configure(text=f"Прошло {count} сек")
			count += 1
			active_inst.update()
			active_inst.after(1000)
		active_inst.destroy()
		self.checklist.attributes("-topmost", False)

	###########################################################################################################
	def sublite_text_uninst_update(self, uninstall_sublime: bool, update_variable_sublime_path: bool):
		"""
		Метод удаляет программу Sublime Text и обновляет файл конфигурации.
		Нужна эта функция потому, что разраб (_!Мать_его!_) поменял название папки,
		куда ставится программа более новой версии, чем третья! И, соответсвенно, старая версия автоматичеки не
		не удаляется при запуске установщика новой версии программы. Это просто "пять баллов!"
		uninstall_sublime - флаг для удаления программы (булево значение)
		update_variable_sublime_path - флаг для обновлнеия фалйа конфигурации
		"""

		if uninstall_sublime:
			os.system(self.sublime_text_commands[0])
			sleep(3)
			sublime_path_new = self.sublime_path.replace(self.sublime_path.split(sep="\\")[2], "Sublime Text")
		if update_variable_sublime_path:
			with open(self.conf_path_default, 'r+', encoding="utf-8") as config:
				configuration = config.read()
				configuration.replace(self.sublime_path, sublime_path_new)
				config.write(configuration)
		#	read_settings_from_file(from_file=False, other_conf_path=conf_path_default)

	def get_status(self):
		"""
		Метод проверяет существование окна "Чек-лист программ".
		"""
		return True if self.checklist.winfo_exists() else False

	def exit(self):
		"""
		Метод закрывает окно проверки софта.
		"""
		self.checklist.destroy()
