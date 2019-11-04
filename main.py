

import os
import datetime
import copy
import time
from pprint import pprint

import params as p
import helpers as h
import analysis as a


date_trial = datetime.date(2019, 11, 30)
if datetime.date.today() > date_trial:
    quit()

# =============

def process_input(dir_input:str):
    dirs = os.listdir(dir_input)
    dirs = list(filter(lambda x: os.path.isdir(os.path.join(dir_input, x)), dirs))

    print("Проверка структуры выборок\n=====")
    flag_compare_ok = True
    for d1 in dirs:
        print(f"Проверка структуры выборки {d1}")
        not_found = []
        for d2 in dirs:
            if d1 == d2:
                continue
            check_dir1 = os.path.join(dir_input, d1)
            check_dir2 = os.path.join(dir_input, d2)
            comp = h.compare_dirs_structure(check_dir1, check_dir2)
            not_found.extend(comp)

        if len(not_found):
            flag_compare_ok = False
            for d, not_found_in in not_found:
                print(f"не найдена выборка \"{d}\" в папке \"{not_found_in}\"")

    if(flag_compare_ok):
        print("\nСтруктура выборок одинакова!\n")
    else:
        print("\nОШИБКА! Структура некоторых выборок неоднородна!")
        print("Продолжение анализа невозможно!")
        return {'status':'error'}

    rc = {'status':'ok'}
    # проверка на нормальность
    print("=====\n\nПроверка на нормальность\n=====")
    rd = []
    for d in dirs:
        check_dir = os.path.join(dir_input, d)
        data = process_samples(check_dir, a.analyze_data_normality)
        print("\n")
        rd.append({
            'sample': d,
            'path': os.path.normpath(check_dir),
            'data': data
        })
    rc['normality'] = rd

    #генерируем хинт какие выборки нормальны
    normal_samples_paths = {o: [] for o in p.n_objects_to_analysis}
    for s in rd:
        for subs in s['data']:
            path = os.path.normpath(subs['path'])
            for obj in subs['results']:
                flag_normal = False
                for _, test in obj['normal'].items():
                    #если хотя бы один тест пройден - выборку признаём нормальной
                    flag_normal = flag_normal | test['status']

                if flag_normal:
                    if obj['object'] not in normal_samples_paths.keys():
                        normal_samples_paths[obj['object']] = []
                    normal_samples_paths[obj['object']].append(path)

    print("Выборки признаные нормальными:")
    pprint(normal_samples_paths)

    # сравнение пар выборок
    print("=====\n\nСравнение пар выборок\n=====")
    rd = []
    for i, d1 in enumerate(dirs[:-1]):
        for d2 in dirs[i+1:]:
            check_dir1 = os.path.join(dir_input, d1)
            check_dir2 = os.path.join(dir_input, d2)
            data = process_samples_pair(check_dir1, check_dir2,
                                        a.analyze_data_compare,
                                        normal_samples_paths=normal_samples_paths,
                                        sample1=d1, sample2=d2)
            rd.append({
                'sample1': d1,
                'sample2': d2,
                'data': data
            })

    rc['comparisons'] = rd
    return rc

def process_samples_pair(dir_input_1:str, dir_input_2:str, func, **kwargs):
    rc = []
    indirname = os.path.split(dir_input_1)[-1]
    print(f"Обработка папки {indirname} => [{dir_input_1}] [{dir_input_2}]")

    data1 = h.load_dataframe_from_folder(dir_input_1)
    data2 = h.load_dataframe_from_folder(dir_input_2)

    if data1 is not None and data2 is not None and \
            len(data1) > 0 and len(data2) > 0:
        # TODO  анализ данных
        results = func(data1, data2, path1 = dir_input_1, path2 = dir_input_1, **kwargs)

        doc = {
            'title': indirname,
            'path1': os.path.normpath(dir_input_1),
            'path2': os.path.normpath(dir_input_2),
            'results': results
        }
        rc.append(doc)
    else:
        if len(list(filter( lambda x: os.path.isdir(os.path.join(dir_input_1, x)), os.listdir(dir_input_1)))) == 0 and \
                len(list(filter( lambda x: os.path.isdir(os.path.join(dir_input_2, x)), os.listdir(dir_input_2)))) == 0:
            print(f"Нет данных в папке {dir_input_1}")

    # ==========
    #обработка подпапок

    for in_dir in os.listdir(dir_input_1):
        inpath1 = os.path.join(dir_input_1, in_dir)
        inpath2 = os.path.join(dir_input_2, in_dir)

        if os.path.exists(inpath1) and os.path.exists(inpath2) and \
                os.path.isdir(inpath1) and os.path.isdir(inpath2):
            rc_s = process_samples_pair(inpath1,inpath2, func, **kwargs)
            rc.extend(rc_s)

    return rc

def process_samples(dir_input:str, func, **kwargs):
    rc = []
    indirname = os.path.split(dir_input)[-1]
    print(f"Обработка папки {indirname} => [{dir_input}]")

    data1 = h.load_dataframe_from_folder(dir_input)

    if data1 is not None and len(data1) > 0 :
        # TODO  анализ данных
        results = func(data1, **kwargs)

        doc = {
            'title': indirname,
            'path': os.path.normpath(dir_input),
            'results': results
        }
        rc.append(doc)
    else:
        if len(list(filter( lambda x: os.path.isdir(os.path.join(dir_input, x)), os.listdir(dir_input)))) == 0:
            print(f"Нет данных в папке {dir_input}")

    # ==========
    #обработка подпапок

    for in_dir in os.listdir(dir_input):
        inpath1 = os.path.join(dir_input, in_dir)

        if os.path.exists(inpath1) and os.path.exists(inpath1) and \
                os.path.isdir(inpath1) and os.path.isdir(inpath1):
            rc_s = process_samples(inpath1, func, **kwargs)
            rc.extend(rc_s)

    return rc

if __name__ == '__main__':
    import pyfiglet
    import warnings
    warnings.filterwarnings("ignore")

    ascii_banner = pyfiglet.figlet_format("   MAGIC\nanalysis")
    # ascii___
    # custom_fig = pyfiglet.Figlet(font='basic')
    # ascii_banner = custom_fig.renderText("   MAGIC")
    # ascii_banner += custom_fig.renderText("analysis")
    # ascii_banner += custom_fig.renderText("ANALYSIS")
    print(ascii_banner)
    print("Cравнение выборок данных от опытов.\n\n=====================================\n")
    # quit()
    time.sleep(2)
    report = process_input(p.p_input)
    print("\n====\n")

    if report['status'] == 'ok':
        h.print_report(report, p.p_final_report)

    input("Нажмите ENTER чтоб закрыть окно...")
