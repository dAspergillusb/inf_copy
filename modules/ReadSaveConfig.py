from tkinter import filedialog
from tkinter import messagebox as mb
try:
	from FilesOperations import *
except ModuleNotFoundError:
	from modules.FilesOperations import *


def read_settings_from_file(from_file=True, other_conf_path=""):
	"""
	Функция считывает данные из файла, который указывается соответствующим диалоговым окном
	или из стандартного файла конфигурации, если он был изменён (например через сохранение новой
	конфигурации в стандартный файл или при переопределении основных переменных).
	from_file - флаг, который нужен для понимания, откуда берутся настроки новые: из файла или при изменении
				настроек через программу (булево значение).
	other_conf_path - путь к файлу настроек (строка).
	"""
	if from_file:
		other_conf_path = filedialog.askopenfilename(filetypes=[("EGE configurator файлы", "*.ege"), ("Все файлы", "*.*")])
		if other_conf_path == () or other_conf_path == "":
			return None
		elif os.path.getsize(other_conf_path) == 0:
			return mb.showerror("Ошибка", message="Файл пустой!")

	params = []
	with open(other_conf_path, "r", encoding="utf-8") as conf_current:
		for param in conf_current.readlines():
			params.append(param[:-1])
	return params


def save_settings_to_file(params: list, log_file: str):
	"""
	Функция сохраняет настройки в файл, создавая его и прописывая внутрь по структуре все необходимые переменные
	из памяти.
	Обрабатывет ошибку доступа к записи файла. Результат пишет в log-файл. Если всё хорошо, то возвращает сообщение
	об успешном сохранении настроек в файл.
	Нет аргументов.
	"""
	save_conf_to_file = filedialog.asksaveasfilename(filetypes=[("EGE configurator файлы", "*.ege")])
	if save_conf_to_file == () or save_conf_to_file == "":
		return save_conf_to_file # заглушка при нажатии кнопки "отмена" в диалоговом окне
	try:
		with open(save_conf_to_file, "w", encoding="utf-8") as new_conf:
			new_conf.write('[Conf path]\n')
			new_conf.write(f'{params.index("[Conf path]") + 1}\n')
			new_conf.write('[End confpath]\n')
			new_conf.write('\n')
			new_conf.write('[Exam config]\n')
			new_conf.write(f'{params[params.index("[Exam config]") + 1]}\n')
			new_conf.write('[End config]\n')
			new_conf.write('\n')
			new_conf.write('[Program names/paths]\n')
			for param in range(params.index("[Program names/paths]") + 1, params.index("[End paths]")):
				new_conf.write(f'{params[param]}\n')
			new_conf.write('[End paths]\n')
			new_conf.write('\n')
			new_conf.write('[Constants]\n')
			for CONSTANT in range(params.index("[Constants]") + 1, params.index("[End constants]")):
				new_conf.write(f'{params[CONSTANT]}\n')
			new_conf.write('[End constants]\n')
			new_conf.write('\n')
	except PermissionError:
		write_log_file("Ошибка записи файла. Нет прав доступа к записи файла.", log_file)
		return mb.showerror("Ошибка", message="Ошибка доступа к файлу! Смотри логи.")
	except FileNotFoundError:
		write_log_file("Ошибка записи файла. Нет найден файл.", log_file)
		return mb.showerror("Ошибка", message="Ошибка доступа к файлу! Смотри логи.")
	return mb.showinfo("Успех", message=f'Конфигурация программы успешно сохранена в файл {save_conf_to_file.split(sep=sep)[-1]}')
