import os
from datetime import datetime
from time import sleep


###########################################################################################################
def create_shortcut(shortcut_path="C:\\Users\\Public\\Desktop", target_path="C:\\pagefile.sys", arguments="", description="Файл подкачки", shortcut_icon=""):
	"""
	Функция создаёт файл с vbs-скриптом, который в свою очередь создаёт ярлык файла по заданному пути.
	shortcut_path - путь вместе и именем ярлыка до места создания ярлыка (по умолчанию - C:\\Users\\Public\\Desktop).
	target_path - путь до файла, ярлык которого будет создаваться (по умолчанию - C:\\pagefile.sys)
	arguments - строка с аргументами, которые можно добавить к программе перед запуском (по умолчанию - пустая строка).
	description - описание, которое выводится при наведении курсора мыши на ярлык (по умолчанию - Файл подкачки).
	shortcut_icon - иконка для ярлыка Файл (по умолчанию - пустая строка).
	"""
	working_dir = target_path[:-len(target_path.split(sep="\\")[-1])] # Создаёт строку пути рабочей папки, обрезая имя файла.
	with open("shortcut.vbs", "w", encoding="windows-1251") as shortcut:
		shortcut.writelines(['set WshShell = WScript.CreateObject("WScript.Shell")\n',
			f'set oShellLink = WshShell.CreateShortcut("{shortcut_path}")\n',
			f'oShellLink.TargetPath = "{target_path}"\n',
			f'oShellLink.Arguments = "{arguments}"\n',
			'oShellLink.WindowStyle = 1\n',
			f'oShellLink.IconLocation = "{shortcut_icon if shortcut_icon != "" else target_path}"\n'
			f'oShellLink.Description = "{description}"\n',
			f'oShellLink.WorkingDirectory = "{working_dir}"\n',
			'oShellLink.Save'])
	os.system('start /wait shortcut.vbs')
	os.system('del /F /Q shortcut.vbs')

###########################################################################################################


###########################################################################################################
def copy_folder_or_file(folder_file_name: str, folder_file_source_path: str, folder_file_target_path: str, log_file: str):
	"""
	Функция копирует папку или файл по заданному пути.
	folder_file_name - имя папки или файла (строка).
	folder_file_source_path - путь до папки или файла (без указания имени папки или файла; строка).
	folder_file_target_path - путь, куда папка или файл будут копироваться (строка).
	Обрабатывает ошибки типа "Отсутствует папка, куда копировать", стандартные ошибки команды "xcopy".
	"""
	error_list = []
	if os.path.isdir(f"{folder_file_source_path}\\{folder_file_name}"):
		for fold_file in os.listdir(f"{folder_file_source_path}\\{folder_file_name}"):
			if os.path.isfile(f"{folder_file_source_path}\\{folder_file_name}\\{fold_file}"):
				error_list.append(os.system(f'xcopy /E /Y "{folder_file_source_path}\\{folder_file_name}\\{fold_file}" "{folder_file_target_path}\\{folder_file_name}\\"'))
			elif os.path.isdir(f"{folder_file_source_path}\\{folder_file_name}\\{fold_file}"):
				error_list.append(os.system(f'xcopy /E /Y "{folder_file_source_path}\\{folder_file_name}\\{fold_file}" "{folder_file_target_path}\\{folder_file_name}\\{fold_file}\\"'))
	elif os.path.isfile(f"{folder_file_source_path}\\{folder_file_name}"):
		error_list.append(os.system(f'xcopy /E /Y "{folder_file_source_path}\\{folder_file_name}" "{folder_file_target_path}\\"'))
	else:
		write_log_file(f"Ошибка копирования {folder_file_name}. Такой папки или файла не существует.", log_file)
		return False
	if sum(error_list) == 0:
		return True
	else:
		if os.path.isdir(f"{folder_file_source_path}\\{folder_file_name}"):
			name = os.listdir(f"{folder_file_source_path}\\{folder_file_name}")
		else:
			name = [folder_file_name]
		for i in range(len(error_list)):
			if error_list[i] == 1:
				write_log_file(f"Ошибка копирования {name[i]}. Не найдены файлы для копирования.", log_file)
			elif error_list[i] == 4:
				write_log_file(f"Ошибка инициализации копирования {name[i]}. Недостаточно памяти или места на диске. Или файл (файл внутри папки) занят другим процессом.", log_file)
			elif error_list[i] == 5:
				write_log_file(f"Ошибка записи на диск файла или папки {name[i]}.", log_file)
		return False
		#mb.showerror("Ошибка копирования", message=f"Следующие папки/файлы скопированы с ошибкой\n{error_text}")


###########################################################################################################
def write_log_file(error_text: str, log_file: str):
	"""
	Функция пишет ошибки в log-файл.
	error_text - сообщение, которое будет вписано в строку расшифровки ошибки в log-файле.
	log_file - путь до log-файла.
	"""
	if not os.path.exists(log_file):
		os.system("mkdir log")
	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	with open(log_file, "a", encoding="utf-8") as log:
		log.write(f"{now} >> {error_text}\n")