import os

#constants
sheet_name = "Source"
p_input = "./input"
p_output = "./output"
os.makedirs(p_input, exist_ok=True)
os.makedirs(p_output, exist_ok=True)

p_file_output_total = "TOTAL.xls"

p_final_report = "report.docx"
p_final_report = os.path.join(p_output, p_final_report)

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
