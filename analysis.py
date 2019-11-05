
import os
import datetime
import copy
import time
from pandas_ods_reader import read_ods
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import seaborn as sns;

sns.set()
import scipy.stats as stats
import statsmodels.api as sm

from scipy.special import erfc
import numpy as np

import params as p
import helpers as h


def chauvenet(array: np.ndarray):
    mean = array.mean()
    stdv = array.std()
    N = len(array)
    criterion = 1.0/(2*N)
    d = abs(array-mean)/stdv
    prob = erfc(d)
    return prob < criterion


def analyze_data_normality(df, **kwargs):

    all_obj_reports = []
    for n_obj in p.n_objects_to_analysis:
        report_object = {}
        dfo1 = df[df[p.n_objtype] == n_obj]

        report_object['object'] = n_obj
        report_object['count'] = len(dfo1)
        # f_threshold_value
        # p_img_dir

        data1 = pd.to_numeric(dfo1[p.n_value], errors='raise')

        # визуализация данных
        vis_file = h.get_new_filename(p.p_img_dir)
        plt.hist(data1, 50)
        plt.savefig(vis_file, dpi=200)
        report_object['grafic'] = vis_file
        plt.clf()

        # проверка на нормальность
        normal = {'shapiro': {}, 'anderson': {}}

        statistic, pval = stats.shapiro(data1)
        normal['shapiro']['pvalue'] = pval
        normal['shapiro']['statistic'] = statistic
        normal['shapiro']['status'] = bool(pval > p.f_threshold_value)

        statistic, pval = sm.stats.normal_ad(data1)
        normal['anderson']['pvalue'] = pval
        normal['anderson']['statistic'] = statistic
        normal['anderson']['status'] = bool(pval > p.f_threshold_value)

        report_object['normal'] = normal

        all_obj_reports.append(report_object)

    return all_obj_reports

def analyze_data_compare(df1, df2, **kwargs):
    #print(kwargs['normal_samples_paths'])

    all_obj_reports = []
    for n_obj in p.n_objects_to_analysis:

        report_object = {}
        dfo1 = df1[df1[p.n_objtype] == n_obj]
        dfo2 = df2[df2[p.n_objtype] == n_obj]

        report_object['object'] = n_obj
        report_object['count1'] = len(dfo1)
        report_object['count2'] = len(dfo2)
        # f_threshold_value
        # p_img_dir

        data1 = pd.to_numeric(dfo1[p.n_value], errors='raise')
        data2 = pd.to_numeric(dfo2[p.n_value], errors='raise')

        # визуализация данных
        vis_file = h.get_new_filename(p.p_img_dir)
        plt.style.use('classic')
        plt.style.use('seaborn-whitegrid')
        sns.distplot(data1, label=kwargs['sample1'])
        sns.distplot(data2, label=kwargs['sample2'])
        plt.legend()
        plt.savefig(vis_file, dpi=200)
        report_object['grafic'] = vis_file
        plt.clf()

        if os.path.normpath(kwargs['path1']) not in kwargs['normal_samples_paths'][n_obj] or \
                os.path.normpath(kwargs['path2']) not in kwargs['normal_samples_paths'][n_obj]:
            print("Сравнение выборок не являющихся нормальными! Тест отклонён.")
            all_obj_reports.append(report_object)
            continue

        #сравнение выборок по среднему
        report_object['meantest'] = {'student': {}, 'mannweatney':{}}

        statistic, pvalue = stats.ttest_ind(data1, data2)
        report_object['meantest']['student']['pvalue'] = pvalue
        report_object['meantest']['student']['statistic'] = statistic
        report_object['meantest']['student']['status'] = bool(pvalue > p.f_threshold_value)

        statistic, pvalue = stats.mannwhitneyu(data1, data2)
        report_object['meantest']['mannweatney']['pvalue'] = pvalue
        report_object['meantest']['mannweatney']['statistic'] = statistic
        report_object['meantest']['mannweatney']['status'] = bool(pvalue > p.f_threshold_value)


        all_obj_reports.append(report_object)

    return all_obj_reports
