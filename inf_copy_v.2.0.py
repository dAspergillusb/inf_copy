from threading import Thread
from sys import exit as crash_exit
import os
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import Tk, Menu, BooleanVar, PhotoImage

from modules.InstallMethod import InstallMethod
from modules.FilesOperations import write_log_file
from modules.ChecklistSoftWindow import ChecklistSoftWindow
from modules.ReadSaveConfig import read_settings_from_file, save_settings_to_file
from modules.HelpAbout import about_program, help_instructions
from modules.Settings import Settings
# Импорт переменных путей к файлам проверяемых программ, а также к файлу конфига и log-файлу
from InitPaths import InitPaths


###########################################################################################################
def read_settings(other_conf_path="", from_menu=False):
	"""
	Функция считывает данные из файла, который указывается соответствующим диалоговым окном
	или из стандартного файла конфигурации, если он был изменён (например через сохранение новой
	конфигурации в стандартный файл или при переопределении основных переменных).
	from_menu - флаг, который нужен для понимания программой, откуда вызывается функция: из строки-меню
				или из какой-то функции просто для обновления переменных прграммы.
	other_conf_path - путь к файлу настроек (строка).
	"""
	global params
	old_params = params.copy()
	if from_menu:
		params = read_settings_from_file(other_conf_path=other_conf_path)
	else:
		params = read_settings_from_file(from_file=False, other_conf_path=other_conf_path)
	if params == None:
		params = old_params.copy()
		return old_params
	try:
		for index in range(params.index("[Conf path]") + 1, params.index("[End confpath]")):
			globals()[params[index].split(sep="=")[0]] = params[index].split(sep="=")[1]
		for index in range(params.index("[Exam config]") + 1, params.index("[End config]")):
			globals()[params[index].split(sep="=")[0]] = params[index].split(sep="=")[1]
		for index in range(params.index("[Program names/paths]") + 1, params.index("[End paths]")):
			globals()[params[index].split(sep="=")[0]] = params[index].split(sep="=")[1]
		for index in range(params.index("[Constants]") + 1, params.index("[End constants]")):
			globals()[params[index].split(sep="=")[0]] = params[index].split(sep="=")[1]
	except ValueError:
		write_log_file("Ошибка с данными в одном из блоков файла конфигурации: [Conf path], [Exam config], [Program names/paths], [Constants].", log_file)
		return mb.showerror("Ошибка", message="Неправильный или битый файл конфигурации!")
		#crash_exit("ValueError code - Смотри лог-файл программы.")
	except PermissionError:
		write_log_file("Ошибка с чтением файла. Нет прав доступа к чтению файла.", log_file)
		return mb.showerror("Ошибка", message="Ошибка доступа к файлу!")
		#crash_exit("PermissionError code - Смотри лог-файл программы.")
	except IndexError:
		write_log_file("Ошибка с данными в одном из общего числа параметров файла конфигурации: отсутствует знак '=' в одной из строчек параметров.", log_file)
		return mb.showerror("Ошибка", message="Ошибка с данными в одном из общего числа параметров файла конфигурации.")
		#crash_exit("IndexError code - Смотри лог-файл программы.")


###########################################################################################################
def start(only_update_shortcuts=False, only_update_exam=False):
	"""
	Функция, исходя из переменных only_update_shortcuts и only_update_exam определяет то, какой метод
	установки будет применяться. Или будет просто обновление ярлыков на рабочем столе.
	only_update_shortcuts - если True, то функция только обновляет ярлыки.
	only_update_exam - если True, то функция только обновляет папку Exam.
	Если обе переменные False, то, исходя из чекбоксов в меню "Параметры", функция запускает
	автоматическую, полуавтоматическую установку или просто перустановку Станции КЕГЭ.
	"""
	installmethod = InstallMethod(exam_date, window, progressbar, status, entry, init_paths)
	if only_update_exam:
		installmethod.update_exam_folder()
	elif not only_update_shortcuts:
		if only_kege.get():
			installmethod.install_only_kege()
		elif auto_install_var.get():
			installmethod.start_auto(params)
		else:
			installmethod.start_manual(params)
	else:
		installmethod.update_desktop_shortcuts(height, width, params)


###########################################################################################################
def create_checklist_soft():
	"""
	Функция создает окно "Чек-лист программ" как параллельный поток, а основной поток контроллирует
	то, существует ли еще это окно. После закрытия окна происходит обновление переменных программы.
	"""
	checklist_soft_window = ChecklistSoftWindow(
												width,
												height,
												icon,
												params,
												init_paths
											)
	checklist_soft_window.create_soft_checklist()
	checklist_thread = Thread(target=lambda: wait_until_window_alive(checklist_soft_window))
	checklist_thread.start()
	#read_settings(other_conf_path=conf_path)

###########################################################################################################
def create_settings_window():
	"""
	Функция создаёт окно "Основные настройки" как параллельный поток. Основной поток контроллирует
	существование этого окна. После его закрытия обновляются паременные программы.
	"""
	settings = Settings(params, PhotoImage(file="inf_copy.png"))
	settings.program_settings()
	settings_thread = Thread(target=lambda: wait_until_window_alive(settings))
	settings_thread.start()

###########################################################################################################
def wait_until_window_alive(toplevel_window):
	"""
	Функция-контроллер. Отслеживает состояние окна, вызывая соответствующий метод у объекта. Обновление
	происходит раз в одну секунду. После получения статуса False, вызывает функцию read_settings.
	"""
	if toplevel_window.get_status():
		#print("Window status:", "Alive")
		window.after(1000, lambda: wait_until_window_alive(toplevel_window))
	else:
		#print("Window status:", "Dead")
		read_settings(other_conf_path=conf_path)

###########################################################################################################
def exit(window):
	"""
	Функция закрывает главное окно программы.
	"""
	window.destroy()


# Создаем объект InitPaths для инициализации основных путей к файлам ######################################
init_paths = InitPaths()
init_paths.init_programs_paths()
conf_path_default = init_paths.get_conf_path_default()
log_file = init_paths.get_log_file_path()
###########################################################################################################


# Создаем основной пустой список параметров params и список будущих переменных configuration_items. #######
# configuration_items нужен только тогда, когда не существует файла конфигурации. #########################
params = []
configuration_items = [
		'[Conf path]\n',
		f'conf_path={conf_path_default}\n',
		'[End confpath]\n',
		'\n',
		'[Exam config]\n',
		'exam_date=2023.12.16\n',
		'[End config]\n',
		'\n',
		'[Program names/paths]\n',
		'Станция_КЕГЭ="C:\\Program Files\\Станция КЕГЭ\\KEGE.exe"\n',
		'Microsoft_Excel="C:\\Program Files\\Microsoft Office\\Office16\\EXCEL.exe"\n',
		'Libre_Calc="C:\\Program Files\\LibreOffice\\program\\scalc.exe"\n',
		'Microsoft_Word="C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.exe"\n',
		'Libre_Writer="C:\\Program Files\\LibreOffice\\program\\swriter.exe"\n',
		'Microsoft_PowerPoint="C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT.exe"\n',
		'Libre_Impress="C:\\Program Files\\LibreOffice\\program\\simpress.exe"\n',
		f'Sublime_Text="C:\\Program Files\\{init_paths.get_sublime_path()}\\sublime_text.exe"\n',
		'Кумир_Стандарт="C:\\Program Files (x86)\\Kumir-2.1.0-rc11\\bin\\kumir2-classic.exe"\n',
		'Кумир="C:\\Program Files (x86)\\Kumir\\kumir.exe"\n',
		f'Visual_Studio="C:\\{init_paths.get_vs_20xx()[0]}\\Microsoft Visual Studio\\{init_paths.get_vs_20xx()[1]}\\Community\\Common7\\IDE\\devenv.exe"\n',
		'CodeBlocks="C:\\Program Files\\CodeBlocks\\codeblocks.exe"\n',
		'Free_Pascal="C:\\FPC\\3.2.0\\bin\\i386-win32\\fp.exe"\n',
		'Pascal_ABC="C:\\Program Files (x86)\\PascalABC.NET\\PascalABCNET.exe"\n',
		f'Java_JDK="C:\\Program Files\\Java\\{init_paths.get_jdk_path()}\\bin\\java.exe"\n',
		f'Intellij_Idea="C:\\{init_paths.get_intellij_path()[0]}\\{init_paths.get_intellij_path()[1]}\\bin\\idea64.exe"\n',
		f'Eclipse_IDE="C:\\Users\\{os.getlogin()}\\eclipse\\java-2021-09\\eclipse\\eclipse.exe"\n',
		f'Python_IDE="C:\\Program Files\\{init_paths.get_python_path()}\\pythonw.exe"\n',
		f'Wing_IDE="C:\\{init_paths.get_wing_path()[0]}\\{init_paths.get_wing_path()[1]}\\bin\\wing-101.exe"\n',
		f'PyCharm="C:\\{init_paths.get_pycharm_path()[0]}\\{init_paths.get_pycharm_path()[1]}\\bin\\pycharm64.exe"\n',
		'Far_Manager="C:\\Program Files\\Far Manager\\Far.exe"\n',
		'Total_Commander="C:\\Program Files\\totalcmd\\TOTALCMD64.exe"\n',
		f'Google_Chrome="C:\\{init_paths.get_chrome_path()}\\Google\\Chrome\\Application\\chrome.exe"\n',
		'[End paths]\n',
		'\n',
		'[Constants]\n',
		'KEGE_VER=20231113\n',
		'EXCEL_VER=20150731\n',
		'CALC_VER=20211205\n',
		'WORD_VER=20150731\n',
		'WRITER_VER=20211205\n',
		'POWERPOINT_VER=20150731\n',
		'IMPRESS_VER=20211205\n',
		'SUBLIME_VER=20211221\n',
		'KUMIR_STD_VER=20200414\n',
		'KUMIR_VER=20120309\n',
		'VIS_STUD_VER=20210513\n',
		'CODEBLOCKS_VER=20200314\n',
		'FREE_PASCAL_VER=20200604\n',
		'PASCAL_ABC_VER=20210502\n',
		'JAVA_VER=20210511\n',
		'INT_IDEA_VER=20201006\n',
		'ECLIPSE_VER=20210906\n',
		'PYTHON_VER=20200923\n',
		'WING_VER=20211211\n',
		'PYCHARM_VER=20201006\n',
		'FAR_VER=20220202\n',
		'TOT_COMM_VER=20210610\n',
		'GOOG_CHR_VER=20231220\n',
		'[End constants]\n',
		'\n'
		]

############################################################################################################
# Первоначальные настройки переменных программы. ###########################################################
try:
	# Определяем путь к файлу конфига из файла конфига, вытаскивая его из всей строки ######################
	if os.path.exists(conf_path_default) and os.path.getsize(conf_path_default) != 0:
		with open(conf_path_default, "r", encoding="utf-8") as config_for_confpath:
			conf_path = config_for_confpath.read().split(sep="\n")[1].split(sep="=")[1]
		if not os.path.exists(conf_path):
			write_log_file("Файла конфигурации по заданному пути не существует! Проверте блок [Conf path] в файле конфигурации.", log_file)
			mb.showerror("Ошибка", message="Неправильный или битый файл конфигурации! Смотри логи.")
			crash_exit("ValueError code - Смотри лог-файл программы.")
	else:
		conf_path = conf_path_default
	if os.path.exists(conf_path) and conf_path != conf_path_default:
		with open(conf_path, "r", encoding="utf-8") as config:
			for param in config.readlines():
				params.append(param[:-1])
		read_settings(other_conf_path=conf_path)
	else:
		if not os.path.exists("config"):
			os.system("mkdir config")
	# Если нет файла конфигурации, то он создаётся из списка configuration_items ###########################
		if not os.path.exists(conf_path_default) or os.path.getsize(conf_path_default) == 0:
			with open(conf_path_default, "w", encoding="utf-8") as config:
				for conf_item in configuration_items:
					config.write(conf_item)
	# Если файл конфигурации есть, то переписываются значения путей к исполняемым файлам ###################
	# из списка configuration_items (работает только для файла, который по умолчанию) #######################
		else:
			with open(conf_path_default, "r", encoding="utf-8") as config:
				current_paths = config.read()
			with open(conf_path_default, "w", encoding="utf-8") as config:
				for item in range(configuration_items.index("[Program names/paths]\n") + 1, configuration_items.index('[End paths]\n')):
					#							  замена	разбиваем строку в список по "\n"	заменяем старую строку на новую
					#										и получаем значение строки старой	из списка с новыми значениями переменных
					current_paths = current_paths.replace(current_paths.split(sep="\n")[item], configuration_items[item][:-1])
				config.write(current_paths)
		read_settings(other_conf_path=conf_path)
except ValueError:
	write_log_file("Ошибка с данными в одном из блоков файла конфигурации: [Conf path], [Exam config], [Program names/paths], [Constants].", log_file)
	mb.showerror("Ошибка", message="Неправильный или битый файл конфигурации! Смотри логи.")
	crash_exit("ValueError code - Смотри лог-файл программы.")
except PermissionError:
	write_log_file("Ошибка с чтением файла. Нет прав доступа к чтению файла.", log_file)
	mb.showerror("Ошибка", message="Ошибка доступа к файлу! Смотри логи.")
	crash_exit("PermissionError code - Смотри лог-файл программы.")
except IndexError:
	write_log_file("Ошибка с данными в одном из общего числа параметров файла конфигурации: отсутствует знак '=' в одной из строчек параметров.", log_file)
	mb.showerror("Ошибка", message="Ошибка с данными в одном из общего числа параметров файла конфигурации. Смотри логи.")
	crash_exit("IndexError code - Смотри лог-файл программы.")
###########################################################################################################

# Создается основное окно программы. ######################################################################
window = Tk()
window.title("Soft install & configure")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"300x170+{(width // 2) - 150}+{(height // 2) - 85}")
#window.attributes("-topmost", True)
window.resizable(False, False)
icon = PhotoImage(file="inf_copy.png")
window.wm_iconphoto(False, icon)

# Словарь с картинками для окна "Документация". ###########################################################
images = {
				"main": PhotoImage(file="doc_pics/main.png"),
				"settings": PhotoImage(file="doc_pics/settings.png"),
				"programm_list_before": PhotoImage(file="doc_pics/programm_list_before.png"),
				"programm_list_after": PhotoImage(file="doc_pics/programm_list_after.png"),
				"resources": PhotoImage(file="doc_pics/resources.png"),
				"menu_file": PhotoImage(file="doc_pics/menu_file.png"),
				"menu_params": PhotoImage(file="doc_pics/menu_params.png"),
				"menu_help": PhotoImage(file="doc_pics/menu_help.png")
			}

main_menu = Menu(window)
window.config(menu=main_menu)

menu_settings = Menu(main_menu, tearoff=0)
menu_settings.add_command(label="Основные настройки", command=create_settings_window)
menu_settings.add_separator()
auto_install_var = BooleanVar()
auto_install_var.set(True)
menu_settings.add_checkbutton(label="Автоустановка", onvalue=True, offvalue=False, state="active", variable=auto_install_var)
only_kege = BooleanVar()
only_kege.set(False)
menu_settings.add_checkbutton(label="Только установка и настройка КЕГЭ", onvalue=True, offvalue=False, state="active", variable=only_kege)

menu_file = Menu(main_menu, tearoff=0)
menu_file.add_command(label="Загрузить файл настроек", command=lambda: read_settings(from_menu=True))
menu_file.add_command(label="Сохранить настройки в файл", command=lambda: save_settings_to_file(params, log_file))
menu_file.add_separator()
menu_file.add_command(label="Чек-лист программ", command=create_checklist_soft)
menu_file.add_command(label="Обновить ярлыки рабочего стола", command=lambda: start(only_update_shortcuts=True))
menu_file.add_command(label="Обновить папку Exam", command=lambda: start(only_update_exam=True))
menu_file.add_separator()
menu_file.add_command(label="Выход", command=lambda: exit(window))

menu_help = Menu(main_menu, tearoff=0)
menu_help.add_command(label="Документация", command=lambda: help_instructions(width, height, icon, images))
menu_help.add_command(label="О программе", command=lambda: about_program(width, height, 480, 180, icon))

main_menu.add_cascade(label="Файл", menu=menu_file)
main_menu.add_cascade(label="Параметры", menu=menu_settings)
main_menu.add_cascade(label="Помощь", menu=menu_help)

frame_1 = ttk.Frame()
frame_1.pack(side="top", pady=10)
frame_2 = ttk.Frame()
frame_2.pack(side="top", pady=0)
frame_3 = ttk.Frame()
frame_3.pack(side="top", pady=10)
frame_4 = ttk.Frame()
frame_4.pack(side="top", pady=0)

ttk.Label(frame_1, text="Прогресс").pack(side="left", padx=10)
progressbar = ttk.Progressbar(frame_1, orient="horizontal", length=150, value=0)
progressbar.pack(side="left")

ttk.Label(frame_2, text="Имя папки").pack(side="left", padx=5)
entry = ttk.Entry(frame_2, width=12)
entry.insert(0, "EGE_KEGE")
entry.pack(side="left", padx=5)

ttk.Label(frame_3, text="Статус: ").pack(side="left", padx=1)
status = ttk.Label(frame_3, text="Не готово!", foreground="red")
status.pack(side="left")

ttk.Button(frame_4, text="Выход", command=lambda: exit(window)).pack(side="right", padx=25)

ttk.Button(frame_4, text="Старт", command=start).pack(side="right", padx=25)

window.mainloop()