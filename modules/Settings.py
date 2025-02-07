from tkinter import Tk, Toplevel, PhotoImage
from tkinter import ttk
from tkinter import messagebox as mb
from time import sleep
try:
	from FilesOperations import write_log_file
except ModuleNotFoundError:
	from modules.FilesOperations import write_log_file


class Settings():
	"""
	Класс занимается созданием окна с основными настройками и записью этих настроек в файл конфигурации.
	"""
	def __init__(self, params: list, icon: Toplevel.wm_iconphoto):
		self.params = params
		self.icon = icon
		self.conf_path = params[params.index("[Conf path]\n"[:-1]) + 1].split(sep="=")[1]
		self.exam_date = params[params.index("[Exam config]\n"[:-1]) + 1].split(sep="=")[1]
		self.soft_paths = [params[x].split(sep="=")[1] for x in range(
																		params.index("[Program names/paths]") + 1,
																		params.index("[End paths]")
																	)
					]
		self.CONSTANTS = [params[x].split(sep="=")[1] for x in range(
																	params.index("[Constants]\n"[:-1]) + 1,
																	params.index("[End constants]\n"[:-1])
																		)]
		self.settings = Toplevel()
		width = self.settings.winfo_screenwidth()
		height = self.settings.winfo_screenheight()
		self.settings.title("Основные настройки")
		self.settings.geometry(f"780x680+{(width // 2) - 390}+{(height // 2) - 340}")
		#settings.attributes("-topmost", True)
		self.settings.resizable(False, False)
		self.settings.wm_iconphoto(False, self.icon)

	def program_settings(self):
		"""
		Метод создаёт окно с переменными (имя папки, которая будет создаваться в папке Exam;
		путь к файлу конфигурации; переменные с именами программ; константы), которые там можно менять.
		После нажатия на кнопку "Сохранить", происходит вызов метода set_save_exam_constants_paths.
		"""
		soft_list = [self.params[x].split(sep="=")[0] for x in range(
																		self.params.index("[Program names/paths]") + 1,
																		self.params.index("[End paths]")
																	)
					]

		CONSTANT_LIST = [self.params[x].split(sep="=")[0] for x in range(
																	self.params.index("[Constants]\n"[:-1]) + 1,
																	self.params.index("[End constants]\n"[:-1])
																		)
						]
	###################################################################
		set_frame_exam_conf = ttk.Frame(self.settings)	#, padding=[10, 10])
		set_frame_exam_conf.pack(side="top")
		set_frame_exam = ttk.Frame(set_frame_exam_conf, padding=[10,10])
		set_frame_exam.pack(side="left")
		set_frame_conf = ttk.Frame(set_frame_exam_conf, padding=[10,10])
		set_frame_conf.pack(side="right")
		set_frame_confs = ttk.Frame(self.settings)
		set_frame_confs.pack(side="top")
		set_frame_paths = ttk.Frame(set_frame_confs, borderwidth=1, relief="solid", padding=[10, 10])
		set_frame_paths.pack(side="left", padx=10)
		set_frame_paths_text = ttk.Frame(set_frame_paths)
		set_frame_paths_text.pack(side="top")
		set_frame_paths_left = ttk.Frame(set_frame_paths)
		set_frame_paths_left.pack(side="left")
		set_frame_paths_right = ttk.Frame(set_frame_paths)
		set_frame_paths_right.pack(side="right")
		set_frame_constants = ttk.Frame(set_frame_confs, borderwidth=1, relief="solid", padding=[10, 10])
		set_frame_constants.pack(side="right", padx=10)
		set_frame_constants_text = ttk.Frame(set_frame_constants)
		set_frame_constants_text.pack(side="top")
		set_frame_constants_left = ttk.Frame(set_frame_constants)
		set_frame_constants_left.pack(side="left")
		set_frame_constants_right = ttk.Frame(set_frame_constants)
		set_frame_constants_right.pack(side="right")
		set_frame_buttons = ttk.Frame(self.settings, padding=[10, 10])
		set_frame_buttons.pack(side="top", pady=10)
		# То, что касается папки для папки Exam и файла настроек conf.ege #
		ttk.Label(set_frame_exam, text="Папка в папке Exam").pack(side="top", padx=10, pady=5)
		set_date_exam_entry = ttk.Entry(set_frame_exam, width=10)
		set_date_exam_entry.pack(side="top", padx=10, pady=0)
		set_date_exam_entry.insert(0, self.exam_date)
		ttk.Label(set_frame_conf, text="Путь до файла конфига").pack(side="top", padx=10, pady=5)
		set_conf_entry = ttk.Entry(set_frame_conf, width=20)
		set_conf_entry.pack(side="top", padx=10, pady=0)
		set_conf_entry.insert(0, self.conf_path)
		###################################################################
		# То, что касается переменных для путей к exe файлам программ #####
		entry_obj_list_paths = []
		ttk.Label(set_frame_paths_text, text="Путь к exe файлам").pack(side="top", pady=10)
		for item in soft_list:
			ttk.Label(set_frame_paths_left, text=item.replace("_", " ")).pack(side="top",padx=15, pady=1)
			locals()[item] = ttk.Entry(set_frame_paths_right, width=35)
			locals()[item].pack(side="top")
			locals()[item].insert(0, self.soft_paths[soft_list.index(item)])
			entry_obj_list_paths.append(locals()[item])
		###################################################################
		# То, что касается переменных констант ############################
		entry_obj_list_CONSTANT = []
		ttk.Label(set_frame_constants_text, text="Даты последнего изменения").pack(side="top", pady=10)
		for item in CONSTANT_LIST:
			ttk.Label(set_frame_constants_left, text=item).pack(side="top", padx=15, pady=1)
			locals()[item] = ttk.Entry(set_frame_constants_right, width=10)
			locals()[item].pack(side="top")
			locals()[item].insert(0, self.CONSTANTS[CONSTANT_LIST.index(item)])
			entry_obj_list_CONSTANT.append(locals()[item])
		###################################################################
		ttk.Button(set_frame_buttons, text="Сохранить", command=lambda: self.program_settings_save(
																										set_conf_entry.get(),
																										set_date_exam_entry.get(),
																										entry_obj_list_CONSTANT,
																										entry_obj_list_paths,
																											)
					).pack(side="left", padx=10, pady=0)
		ttk.Button(set_frame_buttons, text="Выход", command=lambda: self.exit()).pack(side="right", padx=10, pady=0)

	def program_settings_save(self, set_conf_entry: str, set_date_exam_entry: str, entry_obj_list_CONSTANT: list, entry_obj_list_paths: list):
		"""
		Функция формирует строку с параметрами "до изменения" (берет данные из существующих переменных)
		и согласно полученным данным (берет из ячеек  с записями). Далее формируется строка с новыми данными
		и записывается в файл конфигурации. Потом вызывается функция read_settings_from_file.
		set_conf_entry - строка с данными о пути файла конфигурации.
		set_date_exam_entry - строка с данными о названии папки, которая будет создавать в папке Exam.
		entry_obj_list_CONSTANT - список объектов типа ttk.Entry с записями занчений констант.
		soft_list - список названий программ.
		entry_obj_list_paths - список объектов типа ttk.Entry с записями путей к исполняемым файлам программ.
		"""
		try:
			with open(self.conf_path, "r", encoding="utf-8") as conf_old:
				configuration_new = conf_old.read()
			configuration_new = configuration_new.replace(self.conf_path, set_conf_entry)
			configuration_new = configuration_new.replace(self.exam_date, set_date_exam_entry)
			step_for_ = 0
			for entry in entry_obj_list_CONSTANT:
				configuration_new = configuration_new.replace(self.CONSTANTS[step_for_], entry.get())
				step_for_ += 1
			step_for_ = 0
			for entry in entry_obj_list_paths:
				configuration_new = configuration_new.replace(self.soft_paths[step_for_], entry.get())
				step_for_ += 1
			with open(self.conf_path, "w", encoding="utf-8") as conf_new:
				conf_new.write(configuration_new)
		except FileNotFoundError:
			write_log_file(error_text="Ошибка! Файл конфигурации не найден. Проверьте наличие файла конфигурации.")
			return mb.showerror("Ошибка", message="Ошибка доступа к файлу! Файл не найден!")
		# Убиваем окно настроек. ####################################################################################
		self.exit()

	def get_status(self):
		"""
		Метод проверяет существование окна "Основные настройки".
		"""
		return True if self.settings.winfo_exists() else False

	def exit(self):
		self.settings.destroy()