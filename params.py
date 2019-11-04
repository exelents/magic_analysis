import os
import logging

#constants
sheet_name = "Source"
p_input = "./input"
p_output = "./output"
os.makedirs(p_input, exist_ok=True)
os.makedirs(p_output, exist_ok=True)

p_file_output_total = "TOTAL.xls"

p_final_report = "report.docx"
p_errors_log = "errors.txt"
p_data_highlights = "DATA_HIGHLIGHTS"
p_final_report = os.path.join(p_output, p_final_report)
p_data_highlights = os.path.join(p_output, p_data_highlights)
os.makedirs(p_data_highlights, exist_ok=True)

p_img_dir = "img"
p_img_dir = os.path.join(p_output, p_img_dir)
os.makedirs(p_img_dir, exist_ok=True)

n_cytoplasm = "Цитоплазма"
n_nucleos = "Ядро"
n_nucleori = "Ядрышко"

n_objects_to_analysis = [n_cytoplasm, n_nucleos, n_nucleori]

n_objtype = "Object type"
n_value = "Значение"

i_rounddig = 4
f_threshold_value = 0.05  # порог проверки на нормальность и для теста стьюдента

# эвристика для детекта возможных ядрышек записаных в ядра
f_nucleori_max_size = 14.7


#еггог logger
__logfile = os.path.join(p_output, p_errors_log)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# file log
fl = logging.FileHandler(__logfile, encoding='utf-8')
fl.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
fl.setFormatter(formatter)
logger.addHandler(fl)
