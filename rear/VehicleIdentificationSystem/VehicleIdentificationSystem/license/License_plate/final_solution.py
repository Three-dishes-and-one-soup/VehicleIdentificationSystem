# -*- coding: utf-8 -*-
"""
author: 周行健
create time: 2020.7.09
update time: 2020.7.19
"""
import os
from . import img_pretreatment as ip
from . import string_cut as sc
from . import predict_province as pp
from . import predict_digits as pd
from . import predict_letters as pl


def get_result(image_path):
    PROVINCES = (
    "京", "闽", "粤", "苏", "沪", "浙", "津", "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新", "赣", "鄂", "桂", "甘", "晋", "蒙",
    "陕", "吉", "贵", "青", "藏", "川", "宁", "琼")

    LETTERS = (
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "I", "O")

    pretreatment = ip.run(image_path)  # 改一下这里的路径就行
    sc.cut(pretreatment)
    cache_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'License_plate/cache/')
    if len(os.listdir(cache_path)) != 7:
        return False
    else:
        pro_max1_index, pro_max1, pro_max2_index, pro_max2, pro_max3_index, pro_max3 = pp.predict()
        let_max1_index, let_max1, let_max2_index, let_max2, let_max3_index, let_max3 = pl.predict()
        result_digits = pd.predict()
        province_result = {'first': {'result': PROVINCES[pro_max1_index], 'probability': pro_max1},
                           'second': {'result': PROVINCES[pro_max2_index], 'probability': pro_max2},
                           'third': {'result': PROVINCES[pro_max3_index], 'probability': pro_max3}}
        letter_result = {'first': {'result': LETTERS[let_max1_index], 'probability': let_max1},
                         'second': {'result': LETTERS[let_max2_index], 'probability': let_max2},
                         'third': {'result': LETTERS[let_max3_index], 'probability': let_max3}}
        digit_result = {'first': {'result': result_digits[0][0], 'probability': result_digits[0][2:]},
                        'second': {'result': result_digits[1][0], 'probability': result_digits[1][2:]},
                        'third': {'result': result_digits[2][0], 'probability': result_digits[2][2:]},
                        'forth': {'result': result_digits[3][0], 'probability': result_digits[3][2:]},
                        'fifth': {'result': result_digits[4][0], 'probability': result_digits[4][2:]}}
        result = {'pro': province_result, 'let': letter_result, 'dig': digit_result}
        return result
