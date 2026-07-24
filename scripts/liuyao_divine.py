#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六爻占卜計算腳本
支援銅錢搖卦法，自動裝卦、定世應、配六親六神

使用方式：
    python liuyao_divine.py --coins "正正反 正反正 反反反 正正正 正反反 反正正"
    python liuyao_divine.py --coins "--- --- --X --O -- -- ---" 
"""

import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Windows 編碼處理
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ==================== 基礎資料 ====================

# 八卦符號與名稱
TRIGRAMS = {
    '乾': {'symbol': '☰', 'lines': [1, 1, 1], 'element': '金', 'nature': '天'},
    '坤': {'symbol': '☷', 'lines': [0, 0, 0], 'element': '土', 'nature': '地'},
    '震': {'symbol': '☳', 'lines': [0, 0, 1], 'element': '木', 'nature': '雷'},
    '巽': {'symbol': '☴', 'lines': [1, 1, 0], 'element': '木', 'nature': '風'},
    '坎': {'symbol': '☵', 'lines': [0, 1, 0], 'element': '水', 'nature': '水'},
    '離': {'symbol': '☲', 'lines': [1, 0, 1], 'element': '火', 'nature': '火'},
    '艮': {'symbol': '☶', 'lines': [1, 0, 0], 'element': '土', 'nature': '山'},
    '兌': {'symbol': '☱', 'lines': [0, 1, 1], 'element': '金', 'nature': '澤'},
}

# 八卦序數（用於計算）
TRIGRAM_ORDER = ['乾', '兌', '離', '震', '巽', '坎', '艮', '坤']

# 六十四卦資料
HEXAGRAMS = {
    ('乾', '乾'): {'name': '乾為天', 'serial': 1, 'palace': '乾', 'meaning': '元亨利貞。剛健中正，大吉大利。'},
    ('坤', '坤'): {'name': '坤為地', 'serial': 2, 'palace': '坤', 'meaning': '元亨，利牝馬之貞。柔順承載，厚德載物。'},
    ('坎', '坎'): {'name': '坎為水', 'serial': 29, 'palace': '坎', 'meaning': '習坎，有孚，維心亨。險難重重，需守正待時。'},
    ('離', '離'): {'name': '離為火', 'serial': 30, 'palace': '離', 'meaning': '利貞，亨。畜牝牛，吉。光明附麗，依附正道。'},
    ('震', '震'): {'name': '震為雷', 'serial': 51, 'palace': '震', 'meaning': '亨，震來虩虩，笑言啞啞。震動驚懼，動而有得。'},
    ('巽', '巽'): {'name': '巽為風', 'serial': 57, 'palace': '巽', 'meaning': '小亨，利有攸往，利見大人。隨風潛入，柔順得利。'},
    ('艮', '艮'): {'name': '艮為山', 'serial': 52, 'palace': '艮', 'meaning': '艮其背，不獲其身。止而不動，靜待時機。'},
    ('兌', '兌'): {'name': '兌為澤', 'serial': 58, 'palace': '兌', 'meaning': '亨，利貞。喜悅和悅，口舌悅人。'},
    
    ('乾', '坤'): {'name': '天地否', 'serial': 12, 'palace': '乾', 'meaning': '否之匪人，不利君子貞。天地不交，閉塞不通。'},
    ('坤', '乾'): {'name': '地天泰', 'serial': 11, 'palace': '坤', 'meaning': '泰，小往大來，吉亨。天地交合，通泰吉祥。'},
    ('乾', '震'): {'name': '天雷無妄', 'serial': 25, 'palace': '巽', 'meaning': '元亨利貞。無妄之往，不可疾也。意外之變，守正為上。'},
    ('震', '乾'): {'name': '雷天大壯', 'serial': 34, 'palace': '坤', 'meaning': '利貞。剛健有為，壯盛進取。'},
    ('乾', '坎'): {'name': '天水訟', 'serial': 6, 'palace': '離', 'meaning': '有孚窒惕，中吉，終凶。爭訟不吉，宜和解。'},
    ('坎', '乾'): {'name': '水天需', 'serial': 5, 'palace': '坤', 'meaning': '有孚，光亨，貞吉。利涉大川。等待時機。'},
    ('乾', '離'): {'name': '天火同人', 'serial': 13, 'palace': '離', 'meaning': '同人於野，亨。利涉大川，利君子貞。和同共濟。'},
    ('離', '乾'): {'name': '火天大有', 'serial': 14, 'palace': '乾', 'meaning': '元亨。富有天下，盛大亨通。'},
    
    ('坤', '震'): {'name': '地雷復', 'serial': 24, 'palace': '坤', 'meaning': '亨，出入無疾，朋來無咎。陽氣復返，否極泰來。'},
    ('震', '坤'): {'name': '雷地豫', 'serial': 16, 'palace': '震', 'meaning': '利建侯行師。和樂愉快，順勢而動。'},
    ('坤', '坎'): {'name': '地水師', 'serial': 7, 'palace': '坎', 'meaning': '貞，丈人吉，無咎。領軍出征，宜正道。'},
    ('坎', '坤'): {'name': '水地比', 'serial': 8, 'palace': '坤', 'meaning': '吉，原筮元永貞，無咎。親比輔助，和諧相處。'},
    ('坤', '離'): {'name': '地火明夷', 'serial': 36, 'palace': '坎', 'meaning': '利艱貞。光明受損，韜光養晦。'},
    ('離', '坤'): {'name': '火地晉', 'serial': 35, 'palace': '乾', 'meaning': '康侯用錫馬蕃庶，晝日三接。進升吉祥。'},
    
    ('震', '坎'): {'name': '雷水解', 'serial': 40, 'palace': '震', 'meaning': '利西南，無所往，其來復吉。困難解除。'},
    ('坎', '震'): {'name': '水雷屯', 'serial': 3, 'palace': '坎', 'meaning': '元亨利貞，勿用有攸往。創業艱難，宜守不宜進。'},
    ('震', '離'): {'name': '雷火豐', 'serial': 55, 'palace': '坎', 'meaning': '亨，王假之，勿憂，宜日中。盛大豐收。'},
    ('離', '震'): {'name': '火雷噬嗑', 'serial': 21, 'palace': '巽', 'meaning': '亨，利用獄。去除障礙，依法行事。'},
    ('坎', '離'): {'name': '水火既濟', 'serial': 63, 'palace': '坎', 'meaning': '亨小，利貞，初吉終亂。功成事畢，需防衰落。'},
    ('離', '坎'): {'name': '火水未濟', 'serial': 64, 'palace': '離', 'meaning': '亨，小狐汔濟，濡其尾，無攸利。尚未成功。'},
    
    ('巽', '乾'): {'name': '風天小畜', 'serial': 9, 'palace': '巽', 'meaning': '亨，密雲不雨，自我西郊。積蓄待發。'},
    ('乾', '巽'): {'name': '天風姤', 'serial': 44, 'palace': '乾', 'meaning': '女壯，勿用取女。不期而遇，需謹慎。'},
    ('巽', '坤'): {'name': '風地觀', 'serial': 20, 'palace': '乾', 'meaning': '盥而不薦，有孚顒若。觀察審視。'},
    ('坤', '巽'): {'name': '地風升', 'serial': 46, 'palace': '震', 'meaning': '元亨，用見大人，勿恤，南征吉。步步高升。'},
    ('巽', '坎'): {'name': '風水渙', 'serial': 59, 'palace': '離', 'meaning': '亨，王假有廟，利涉大川，利，利貞。渙散流佈。'},
    ('坎', '巽'): {'name': '水風井', 'serial': 48, 'palace': '震', 'meaning': '改邑不改井，無喪無得，往來井井。養民濟世。'},
    ('巽', '離'): {'name': '風火家人', 'serial': 37, 'palace': '巽', 'meaning': '利女貞。家庭和睦，女主內。'},
    ('離', '巽'): {'name': '火風鼎', 'serial': 50, 'palace': '離', 'meaning': '元吉，亨。鼎新革新，大吉大利。'},
    
    ('艮', '乾'): {'name': '山天大畜', 'serial': 26, 'palace': '艮', 'meaning': '利貞，不家食吉，利涉大川。積德蓄德。'},
    ('乾', '艮'): {'name': '天山遁', 'serial': 33, 'palace': '乾', 'meaning': '亨，小利貞。退避隱遁，明哲保身。'},
    ('艮', '坤'): {'name': '山地剝', 'serial': 23, 'palace': '乾', 'meaning': '不利有攸往。剝落衰敗，宜守不宜進。'},
    ('坤', '艮'): {'name': '地山謙', 'serial': 15, 'palace': '兌', 'meaning': '亨，君子有終。謙虛謹慎，終有善果。'},
    ('艮', '坎'): {'name': '山水蒙', 'serial': 4, 'palace': '離', 'meaning': '亨。匪我求童蒙，童蒙求我。啟蒙教育。'},
    ('坎', '艮'): {'name': '水山蹇', 'serial': 39, 'palace': '兌', 'meaning': '利西南，不利東北，利見大人，貞吉。險阻困難。'},
    ('艮', '離'): {'name': '山火賁', 'serial': 22, 'palace': '艮', 'meaning': '亨，小利有攸往。文飾美化，表面功夫。'},
    ('離', '艮'): {'name': '火山旅', 'serial': 56, 'palace': '離', 'meaning': '小亨，旅貞吉。旅途漂泊，小心謹慎。'},
    
    ('兌', '乾'): {'name': '澤天夬', 'serial': 43, 'palace': '坤', 'meaning': '揚于王庭，孚號，有厲，告自邑，不利即戎。決斷果斷。'},
    ('乾', '兌'): {'name': '天澤履', 'serial': 10, 'palace': '艮', 'meaning': '履虎尾，不咥人，亨。小心謹慎，履行禮法。'},
    ('兌', '坤'): {'name': '澤地萃', 'serial': 45, 'palace': '兌', 'meaning': '亨，王假有廟，利見大人，亨，利貞。聚集會合。'},
    ('坤', '兌'): {'name': '地澤臨', 'serial': 19, 'palace': '坤', 'meaning': '元亨利貞，至于八月有凶。君臨天下，盛大亨通。'},
    ('兌', '坎'): {'name': '澤水困', 'serial': 47, 'palace': '兌', 'meaning': '亨，貞，大人吉，無咎，有言不信。困頓艱難。'},
    ('坎', '兌'): {'name': '水澤節', 'serial': 60, 'palace': '坎', 'meaning': '亨，苦節不可貞。節制適度，中道而行。'},
    ('兌', '離'): {'name': '澤火革', 'serial': 49, 'palace': '坎', 'meaning': '己日乃孚，元亨利貞，悔亡。變革改新。'},
    ('離', '兌'): {'name': '火澤睽', 'serial': 38, 'palace': '艮', 'meaning': '小事吉。乖違背離，小事可成。'},
    
    ('震', '巽'): {'name': '雷風恆', 'serial': 32, 'palace': '震', 'meaning': '亨，無咎，利貞，利有攸往。恆久不變。'},
    ('巽', '震'): {'name': '風雷益', 'serial': 42, 'palace': '巽', 'meaning': '利有攸往，利涉大川。增益進取。'},
    ('震', '艮'): {'name': '雷山小過', 'serial': 62, 'palace': '兌', 'meaning': '亨，利貞，可小事，不可大事。稍有過度。'},
    ('艮', '震'): {'name': '山雷頤', 'serial': 27, 'palace': '巽', 'meaning': '貞吉，觀頤，自求口實。養生颐養。'},
    ('震', '兌'): {'name': '雷澤歸妹', 'serial': 54, 'palace': '兌', 'meaning': '征凶，無攸利。少女出嫁，未必順利。'},
    ('兌', '震'): {'name': '澤雷隨', 'serial': 17, 'palace': '震', 'meaning': '元亨利貞，無咎。隨順和樂，隨機應變。'},
    ('巽', '艮'): {'name': '風山漸', 'serial': 53, 'palace': '艮', 'meaning': '女歸吉，利貞。循序漸進。'},
    ('艮', '巽'): {'name': '山風蠱', 'serial': 18, 'palace': '巽', 'meaning': '元亨，利涉大川。甲蠱敗壞，需整治改革。'},
    ('巽', '兌'): {'name': '風澤中孚', 'serial': 61, 'palace': '艮', 'meaning': '豚魚吉，利涉大川，利貞。誠信感通。'},
    ('兌', '巽'): {'name': '澤風大過', 'serial': 28, 'palace': '坎', 'meaning': '棟橈，利有攸往，亨。過度負荷。'},
    ('艮', '兌'): {'name': '山澤損', 'serial': 41, 'palace': '艮', 'meaning': '有孚，元吉，無咎，可貞，利有攸往。損己利人。'},
    ('兌', '艮'): {'name': '澤山咸', 'serial': 31, 'palace': '兌', 'meaning': '亨，利貞，取女吉。感應相通。'},
}

# 八卦天干配置
TRIGRAM_TIANGAN = {
    '乾': {'inner': '甲', 'outer': '壬'},
    '坤': {'inner': '乙', 'outer': '癸'},
    '震': {'inner': '庚', 'outer': '庚'},
    '巽': {'inner': '辛', 'outer': '辛'},
    '坎': {'inner': '戊', 'outer': '戊'},
    '離': {'inner': '己', 'outer': '己'},
    '艮': {'inner': '丙', 'outer': '丙'},
    '兌': {'inner': '丁', 'outer': '丁'},
}

# 八卦地支序列（從初爻到上爻）
TRIGRAM_DIZHI = {
    '乾': ['子', '寅', '辰', '午', '申', '戌'],
    '坤': ['未', '巳', '卯', '丑', '亥', '酉'],
    '震': ['子', '寅', '辰', '午', '申', '戌'],
    '巽': ['丑', '亥', '酉', '未', '巳', '卯'],
    '坎': ['寅', '辰', '午', '申', '戌', '子'],
    '離': ['卯', '丑', '亥', '酉', '未', '巳'],
    '艮': ['辰', '午', '申', '戌', '子', '寅'],
    '兌': ['巳', '卯', '丑', '亥', '酉', '未'],
}

# 地支五行
DIZHI_ELEMENT = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}

# 五行相生相剋
ELEMENTS_RELATION = {
    '生': {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'},
    '剋': {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'},
}

# 六親定義（以我為中心）
LIUQIN = {
    '父母': '生我',
    '子孫': '我生',
    '官鬼': '剋我',
    '妻財': '我剋',
    '兄弟': '同我',
}

# 六神排列（依日干）
LIUSHEN_ORDER = {
    '甲': ['青龍', '朱雀', '勾陳', '螣蛇', '白虎', '玄武'],
    '乙': ['青龍', '朱雀', '勾陳', '螣蛇', '白虎', '玄武'],
    '丙': ['朱雀', '勾陳', '螣蛇', '白虎', '玄武', '青龍'],
    '丁': ['朱雀', '勾陳', '螣蛇', '白虎', '玄武', '青龍'],
    '戊': ['勾陳', '螣蛇', '白虎', '玄武', '青龍', '朱雀'],
    '己': ['螣蛇', '白虎', '玄武', '青龍', '朱雀', '勾陳'],
    '庚': ['白虎', '玄武', '青龍', '朱雀', '勾陳', '螣蛇'],
    '辛': ['白虎', '玄武', '青龍', '朱雀', '勾陳', '螣蛇'],
    '壬': ['玄武', '青龍', '朱雀', '勾陳', '螣蛇', '白虎'],
    '癸': ['玄武', '青龍', '朱雀', '勾陳', '螣蛇', '白虎'],
}

# 六神含義
LIUSHEN_MEANING = {
    '青龍': {'element': '木', 'meaning': '喜慶、酒色、貴人、文書'},
    '朱雀': {'element': '火', 'meaning': '口舌、文書、消息、爭吵'},
    '勾陳': {'element': '土', 'meaning': '田土、牢獄、遲鈍、阻礙'},
    '螣蛇': {'element': '土', 'meaning': '虛驚、怪異、纏繞、變化'},
    '白虎': {'element': '金', 'meaning': '凶傷、孝服、血光、手術'},
    '玄武': {'element': '水', 'meaning': '盜賊、陰私、曖昧、欺騙'},
}

# 八宮卦世應位置（世爻/應爻位置，從初爻=1開始）
PALACE_POSITIONS = {
    '乾': {
        '乾為天': (6, 3), '天風姤': (1, 4), '天山遁': (2, 5), '天地否': (3, 6),
        '風地觀': (4, 1), '山地剝': (5, 2), '火地晉': (4, 1), '火天大有': (3, 6),
    },
    '兌': {
        '兌為澤': (6, 3), '澤水困': (1, 4), '澤地萃': (2, 5), '澤山咸': (3, 6),
        '水山蹇': (4, 1), '地山謙': (5, 2), '雷山小過': (4, 1), '雷澤歸妹': (3, 6),
    },
    '離': {
        '離為火': (6, 3), '火山旅': (1, 4), '火風鼎': (2, 5), '火水未濟': (3, 6),
        '山水蒙': (4, 1), '風水渙': (5, 2), '天水訟': (4, 1), '天火同人': (3, 6),
    },
    '震': {
        '震為雷': (6, 3), '雷地豫': (1, 4), '雷水解': (2, 5), '雷風恆': (3, 6),
        '地風升': (4, 1), '水風井': (5, 2), '澤風大過': (4, 1), '澤雷隨': (3, 6),
    },
    '巽': {
        '巽為風': (6, 3), '風天小畜': (1, 4), '風火家人': (2, 5), '風雷益': (3, 6),
        '天雷無妄': (4, 1), '火雷噬嗑': (5, 2), '山雷頤': (4, 1), '山風蠱': (3, 6),
    },
    '坎': {
        '坎為水': (6, 3), '水澤節': (1, 4), '水雷屯': (2, 5), '水火既濟': (3, 6),
        '澤火革': (4, 1), '雷火豐': (5, 2), '地火明夷': (4, 1), '地水師': (3, 6),
    },
    '艮': {
        '艮為山': (6, 3), '山火賁': (1, 4), '山天大畜': (2, 5), '山澤損': (3, 6),
        '火澤睽': (4, 1), '天澤履': (5, 2), '風澤中孚': (4, 1), '風山漸': (3, 6),
    },
    '坤': {
        '坤為地': (6, 3), '地雷復': (1, 4), '地澤臨': (2, 5), '地天泰': (3, 6),
        '雷天大壯': (4, 1), '澤天夬': (5, 2), '水天需': (4, 1), '水地比': (3, 6),
    },
}

# 空亡表
XUNWANG = {
    '甲子': ['戌', '亥'],
    '甲戌': ['申', '酉'],
    '甲申': ['午', '未'],
    '甲午': ['辰', '巳'],
    '甲辰': ['寅', '卯'],
    '甲寅': ['子', '丑'],
}

# 天干序數
TIANGAN_LIST = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支序數
DIZHI_LIST = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']


# ==================== 計算函數 ====================

def get_trigram_from_lines(lines: List[int]) -> str:
    """根據三爻判斷卦象"""
    # lines: [初爻, 二爻, 三爻] 或 [四爻, 五爻, 上爻]
    # 1 = 陽, 0 = 陰
    for name, data in TRIGRAMS.items():
        if data['lines'] == lines:
            return name
    return '乾'  # 預設


def get_trigram_symbol(trigram: str) -> str:
    """取得卦象符號（上下排列）"""
    return TRIGRAMS.get(trigram, {}).get('symbol', '☰')


def get_hexagram_name(lower: str, upper: str) -> str:
    """取得六十四卦名稱"""
    key = (upper, lower)  # 外卦在上，內卦在下
    return HEXAGRAMS.get(key, {}).get('name', f'{upper}{lower}')


def get_hexagram_info(lower: str, upper: str) -> dict:
    """取得六十四卦完整資訊"""
    key = (upper, lower)
    return HEXAGRAMS.get(key, {
        'name': f'{upper}{lower}',
        'serial': 0,
        'palace': upper,
        'meaning': '卦義待查。'
    })


def get_liuqin(palace_element: str, element: str) -> str:
    """根據卦宮五行和爻五行計算六親"""
    # 以卦宮為「我」
    relations = {
        '生': None,
        '被生': None,
        '剋': None,
        '被剋': None,
        '同': None,
    }
    
    # 同我（兄弟）
    if palace_element == element:
        return '兄弟'
    
    # 我生（子孫）
    if ELEMENTS_RELATION['生'].get(palace_element) == element:
        return '子孫'
    
    # 生我（父母）
    if ELEMENTS_RELATION['生'].get(element) == palace_element:
        return '父母'
    
    # 我剋（妻財）
    if ELEMENTS_RELATION['剋'].get(palace_element) == element:
        return '妻財'
    
    # 剋我（官鬼）
    if ELEMENTS_RELATION['剋'].get(element) == palace_element:
        return '官鬼'
    
    return '兄弟'


def get_shi_ying(hexagram_name: str, palace: str) -> Tuple[int, int]:
    """取得世應位置"""
    palace_data = PALACE_POSITIONS.get(palace, {})
    return palace_data.get(hexagram_name, (6, 3))


def get_xunwang(year_ganzhi: str) -> List[str]:
    """取得當旬空亡"""
    # 取得旬首
    ganzhi_idx = TIANGAN_LIST.index(year_ganzhi[0]) if year_ganzhi[0] in TIANGAN_LIST else 0
    dizhi_idx = DIZHI_LIST.index(year_ganzhi[1]) if year_ganzhi[1] in DIZHI_LIST else 0
    
    # 計算旬首（甲子、甲戌...）
    # 甲子旬：甲子到癸酉
    # 甲戌旬：甲戌到癸未
    # 以此類推
    xun_start_idx = (ganzhi_idx - dizhi_idx) % 10
    if xun_start_idx < 0:
        xun_start_idx += 10
    
    # 確定屬於哪一旬
    xun_ganzhi_idx = dizhi_idx % 6  # 0=甲子, 1=甲戌, ...
    xun_heads = ['甲子', '甲戌', '甲申', '甲午', '甲辰', '甲寅']
    
    # 計算當日干支所属旬
    day_offset = (TIANGAN_LIST.index(year_ganzhi[0]) - dizhi_idx) % 60
    for xun_head in xun_heads:
        if xun_head in XUNWANG:
            return XUNWANG[xun_head]
    
    return ['戌', '亥']  # 預設


def parse_coins(coins_str: str) -> List[dict]:
    """
    解析銅錢搖卦結果
    
    輸入格式：
    - "正正反 正反正 反反反 正正正 正反反 反正正"（六次搖卦，空格分隔）
    - 或 "--- --- --X --O -- -- ---"（爻位表示）
    
    回傳：六爻資料（初爻到上爻）
    """
    coins_str = coins_str.strip()
    
    # 方式一：正反表示
    if '正' in coins_str or '反' in coins_str:
        parts = coins_str.split()
        results = []
        
        for part in parts:
            zheng_count = part.count('正')
            fan_count = part.count('反')
            
            if zheng_count == 3:  # 三正 = 老陰
                results.append({'yao': '陰', 'moving': True, 'name': '老陰', 'symbol': '×'})
            elif fan_count == 3:  # 三反 = 老陽
                results.append({'yao': '陽', 'moving': True, 'name': '老陽', 'symbol': '○'})
            elif zheng_count == 2:  # 兩正一反 = 少陽
                results.append({'yao': '陽', 'moving': False, 'name': '少陽', 'symbol': '—'})
            elif fan_count == 2:  # 一正兩反 = 少陰
                results.append({'yao': '陰', 'moving': False, 'name': '少陰', 'symbol': '--'})
            else:
                results.append({'yao': '陽', 'moving': False, 'name': '少陽', 'symbol': '—'})
        
        return results
    
    # 方式二：爻位表示
    else:
        parts = coins_str.split()
        results = []
        
        for part in parts:
            part = part.strip()
            if 'X' in part or 'x' in part:  # 老陰（動爻）
                results.append({'yao': '陰', 'moving': True, 'name': '老陰', 'symbol': '×'})
            elif 'O' in part or 'o' in part:  # 老陽（動爻）
                results.append({'yao': '陽', 'moving': True, 'name': '老陽', 'symbol': '○'})
            elif '--' in part:  # 陰爻
                results.append({'yao': '陰', 'moving': False, 'name': '少陰', 'symbol': '--'})
            else:  # 陽爻
                results.append({'yao': '陽', 'moving': False, 'name': '少陽', 'symbol': '—'})
        
        return results


def build_hexagram(yao_data: List[dict]) -> dict:
    """
    根據六爻資料建卦
    
    回傳：本卦和變卦資訊
    """
    # 確保有六爻
    if len(yao_data) < 6:
        # 補足（預設為少陽）
        while len(yao_data) < 6:
            yao_data.append({'yao': '陽', 'moving': False, 'name': '少陽', 'symbol': '—'})
    
    yao_data = yao_data[:6]  # 只取六爻
    
    # 本卦（只看陰陽）
    ben_lines = [1 if y['yao'] == '陽' else 0 for y in yao_data]
    
    # 內卦（初二三爻）
    inner_lines = ben_lines[:3]
    inner_trigram = get_trigram_from_lines(inner_lines)
    
    # 外卦（四五上爻）
    outer_lines = ben_lines[3:]
    outer_trigram = get_trigram_from_line(outer_lines)
    
    # 本卦名稱
    ben_name = get_hexagram_name(inner_trigram, outer_trigram)
    ben_info = get_hexagram_info(inner_trigram, outer_trigram)
    
    # 變卦（動爻變化）
    bian_lines = ben_lines.copy()
    for i, y in enumerate(yao_data):
        if y['moving']:
            bian_lines[i] = 1 - bian_lines[i]  # 陽變陰，陰變陽
    
    bian_inner_lines = bian_lines[:3]
    bian_inner_trigram = get_trigram_from_lines(bian_inner_lines)
    
    bian_outer_lines = bian_lines[3:]
    bian_outer_trigram = get_trigram_from_lines(bian_outer_lines)
    
    bian_name = get_hexagram_name(bian_inner_trigram, bian_outer_trigram)
    bian_info = get_hexagram_info(bian_inner_trigram, bian_outer_trigram)
    
    return {
        'ben': {
            'name': ben_name,
            'inner': inner_trigram,
            'outer': outer_trigram,
            'palace': ben_info.get('palace', outer_trigram),
            'serial': ben_info.get('serial', 0),
            'meaning': ben_info.get('meaning', ''),
            'lines': ben_lines,
        },
        'bian': {
            'name': bian_name,
            'inner': bian_inner_trigram,
            'outer': bian_outer_trigram,
            'palace': bian_info.get('palace', bian_outer_trigram),
            'serial': bian_info.get('serial', 0),
            'meaning': bian_info.get('meaning', ''),
            'lines': bian_lines,
        },
        'yao_data': yao_data,
    }


def get_trigram_from_line(lines: List[int]) -> str:
    """根據三爻判斷卦象（別名）"""
    return get_trigram_from_lines(lines)


def najia(hexagram_data: dict, day_ganzhi: str) -> dict:
    """
    裝卦（納甲）：為六爻配上天干地支、六親、六神
    
    Args:
        hexagram_data: 建卦結果
        day_ganzhi: 占卜日的干支（例：乙巳）
    
    Returns:
        完整的納甲排盤資料
    """
    ben = hexagram_data['ben']
    inner = ben['inner']
    outer = ben['outer']
    palace = ben['palace']
    yao_data = hexagram_data['yao_data']
    
    # 卦宮五行
    palace_element = TRIGRAMS.get(palace, {}).get('element', '金')
    
    # 日干（用於六神）
    day_gan = day_ganzhi[0] if day_ganzhi else '甲'
    
    # 六神順序
    liushen_order = LIUSHEN_ORDER.get(day_gan, LIUSHEN_ORDER['甲'])
    
    # 內外卦地支
    inner_dizhi = TRIGRAM_DIZHI.get(inner, ['子', '寅', '辰', '午', '申', '戌'])
    outer_dizhi = TRIGRAM_DIZHI.get(outer, ['子', '寅', '辰', '午', '申', '戌'])
    
    # 內外卦天干
    inner_tiangan = TRIGRAM_TIANGAN.get(inner, {}).get('inner', '甲')
    outer_tiangan = TRIGRAM_TIANGAN.get(outer, {}).get('outer', '壬')
    
    # 世應位置
    shi, ying = get_shi_ying(ben['name'], palace)
    
    # 空亡
    kongwang = get_xunwang(day_ganzhi)
    
    # 組裝六爻
    lines_detail = []
    
    for i in range(6):
        yao_num = i + 1  # 爻位（初爻=1）
        
        # 內卦（初二三）或外卦（四五上）
        if yao_num <= 3:
            dizhi = inner_dizhi[yao_num - 1]
            tiangan = inner_tiangan
        else:
            dizhi = outer_dizhi[yao_num - 4]
            tiangan = outer_tiangan
        
        # 爻五行
        element = DIZHI_ELEMENT.get(dizhi, '土')
        
        # 六親
        liuqin = get_liuqin(palace_element, element)
        
        # 六神（從初爻到上爻對應）
        liushen = liushen_order[i]
        
        # 世應
        is_shi = (yao_num == shi)
        is_ying = (yao_num == ying)
        
        # 空亡
        is_kong = dizhi in kongwang
        
        # 動爻
        is_moving = yao_data[i]['moving']
        
        lines_detail.append({
            'yao_num': yao_num,
            'yao_name': f'{"初" if yao_num == 1 else "上" if yao_num == 6 else ["二","三","四","五"][yao_num-2]}爻',
            'yao_type': yao_data[i]['name'],
            'yao_symbol': yao_data[i]['symbol'],
            'yao_yinyang': yao_data[i]['yao'],
            'is_moving': is_moving,
            'tiangan': tiangan,
            'dizhi': dizhi,
            'element': element,
            'liuqin': liuqin,
            'liushen': liushen,
            'is_shi': is_shi,
            'is_ying': is_ying,
            'is_kong': is_kong,
        })
    
    return {
        'lines': lines_detail,
        'palace': palace,
        'palace_element': palace_element,
        'shi': shi,
        'ying': ying,
        'kongwang': kongwang,
        'day_ganzhi': day_ganzhi,
    }


def analyze_wangshuai(element: str, month: str) -> str:
    """
    判斷五行旺衰
    
    Args:
        element: 五行
        month: 月份地支
    
    Returns:
        旺相休囚死
    """
    # 月份對應季節
    month_season = {
        '寅': '春', '卯': '春', '辰': '春',
        '巳': '夏', '午': '夏', '未': '夏',
        '申': '秋', '酉': '秋', '戌': '秋',
        '亥': '冬', '子': '冬', '丑': '冬',
    }
    
    # 五行旺相表
    wang_table = {
        '春': {'木': '旺', '火': '相', '水': '休', '金': '囚', '土': '死'},
        '夏': {'火': '旺', '土': '相', '木': '休', '水': '囚', '金': '死'},
        '秋': {'金': '旺', '水': '相', '土': '休', '火': '囚', '木': '死'},
        '冬': {'水': '旺', '木': '相', '金': '休', '土': '囚', '火': '死'},
    }
    
    season = month_season.get(month, '春')
    return wang_table.get(season, {}).get(element, '休')


def divine_coins(coins_str: str, day_ganzhi: str = '乙巳', month_dizhi: str = '巳') -> dict:
    """
    銅錢搖卦占卜
    
    Args:
        coins_str: 銅錢搖卦結果
        day_ganzhi: 占卜日干支
        month_dizhi: 占卜月地支
    
    Returns:
        完整占卜結果
    """
    # 解析銅錢
    yao_data = parse_coins(coins_str)
    
    # 建卦
    hexagram = build_hexagram(yao_data)
    
    # 裝卦
    najia_data = najia(hexagram, day_ganzhi)
    
    # 判旺衰
    for line in najia_data['lines']:
        line['wangshuai'] = analyze_wangshuai(line['element'], month_dizhi)
    
    return {
        'hexagram': hexagram,
        'najia': najia_data,
    }


def format_output(result: dict, question_type: str = None) -> str:
    """格式化輸出"""
    lines = []
    
    hexagram = result['hexagram']
    najia = result['najia']
    ben = hexagram['ben']
    bian = hexagram['bian']
    
    lines.append("## 🔮 六爻占卜")
    lines.append("")
    lines.append(f"**起卦方式**：銅錢搖卦法")
    lines.append(f"**占卜日**：{najia['day_ganzhi']}日")
    lines.append("")
    
    # 本卦與變卦
    lines.append("### 本卦與變卦")
    lines.append("")
    
    inner_sym = TRIGRAMS.get(ben['inner'], {}).get('symbol', '☰')
    outer_sym = TRIGRAMS.get(ben['outer'], {}).get('symbol', '☰')
    ben_sym = f"{outer_sym}\n{inner_sym}"
    
    bian_inner_sym = TRIGRAMS.get(bian['inner'], {}).get('symbol', '☰')
    bian_outer_sym = TRIGRAMS.get(bian['outer'], {}).get('symbol', '☀')
    bian_sym = f"{bian_outer_sym}\n{bian_inner_sym}"
    
    lines.append("| 項目 | 卦名 | 卦象 |")
    lines.append("|:----:|:----:|:----:|")
    lines.append(f"| **本卦** | {ben['name']} | {outer_sym}{inner_sym} |")
    lines.append(f"| **變卦** | {bian['name']} | {bian_outer_sym}{bian_inner_sym} |")
    lines.append("")
    
    # 卦義
    lines.append("### 卦義")
    lines.append("")
    lines.append(f"**本卦《{ben['name']}》**：{ben['meaning']}")
    if ben['name'] != bian['name']:
        lines.append(f"**變卦《{bian['name']}》**：{bian['meaning']}")
    lines.append("")
    
    # 納甲排盤
    lines.append("### 納甲排盤")
    lines.append("")
    lines.append("| 爻位 | 卦象 | 天干 | 地支 | 五行 | 六親 | 六神 | 旺衰 | 動爻 |")
    lines.append("|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|")
    
    for line in reversed(najia['lines']):  # 從上爻到初爻
        yao_sym = line['yao_symbol']
        shi_ying = ''
        if line['is_shi']:
            shi_ying = '世'
        if line['is_ying']:
            shi_ying += '應'
        
        kong_str = '旬空' if line['is_kong'] else ''
        moving_str = '○' if line['is_moving'] and line['yao_yinyang'] == '陽' else ('×' if line['is_moving'] else '')
        
        lines.append(
            f"| {line['yao_name']} | {yao_sym} {shi_ying} | {line['tiangan']} | "
            f"{line['dizhi']} | {line['element']} | {line['liuqin']} | {line['liushen']} | "
            f"{line['wangshuai']} | {kong_str}{moving_str} |"
        )
    
    lines.append("")
    
    # 斷卦要點
    lines.append("### 斷卦分析")
    lines.append("")
    
    # 用神分析
    lines.append(f"**卦宮**：{najia['palace']}宮（{najia['palace_element']}）")
    lines.append(f"**世爻**：{najia['shi']}爻")
    lines.append(f"**應爻**：{najia['ying']}爻")
    lines.append(f"**旬空**：{najia['kongwang'][0]}、{najia['kongwang'][1]}")
    lines.append("")
    
    # 動爻分析
    moving_lines = [l for l in najia['lines'] if l['is_moving']]
    if moving_lines:
        lines.append("**動爻分析**：")
        for ml in moving_lines:
            lines.append(f"- {ml['yao_name']}（{ml['tiangan']}{ml['dizhi']}）：{ml['liuqin']}爻動，五行{ml['element']}，{ml['wangshuai']}")
    else:
        lines.append("**動爻**：無動爻，為靜卦")
    lines.append("")
    
    # 世應關係
    shi_line = next((l for l in najia['lines'] if l['is_shi']), None)
    ying_line = next((l for l in najia['lines'] if l['is_ying']), None)
    
    if shi_line and ying_line:
        lines.append("**世應關係**：")
        shi_elem = shi_line['element']
        ying_elem = ying_line['element']
        
        if shi_elem == ying_elem:
            lines.append(f"- 世應同屬{shi_elem}，比和之象")
        elif ELEMENTS_RELATION['生'].get(shi_elem) == ying_elem:
            lines.append(f"- 世({shi_elem})生應({ying_elem})，我有意於彼")
        elif ELEMENTS_RELATION['生'].get(ying_elem) == shi_elem:
            lines.append(f"- 應({ying_elem})生世({shi_elem})，彼有意於我")
        elif ELEMENTS_RELATION['剋'].get(shi_elem) == ying_elem:
            lines.append(f"- 世({shi_elem})剋應({ying_elem})，我制彼")
        elif ELEMENTS_RELATION['剋'].get(ying_elem) == shi_elem:
            lines.append(f"- 應({ying_elem})剋世({shi_elem})，彼制我，不利")
    
    lines.append("")
    
    # 問題類型解讀
    if question_type:
        lines.append("### 📝 針對問題解讀")
        lines.append("")
        lines.append(interpret_question(question_type, najia))
    
    return "\n".join(lines)


def interpret_question(question_type: str, najia: dict) -> str:
    """根據問題類型解讀"""
    
    # 用神對照
    yongshen_map = {
        '事業工作': '官鬼',
        '財運投資': '妻財',
        '感情婚姻': '妻財（男測）/ 官鬼（女測）',
        '健康疾病': '官鬼（病）/ 子孫（藥）',
        '考試學業': '父母',
        '出行旅行': '父母（文書）/ 兄弟（阻礙）',
        '尋人尋物': '妻財（財物）/ 兄弟（朋友）',
        '官非訴訟': '官鬼',
    }
    
    yongshen = yongshen_map.get(question_type, '官鬼')
    
    lines = []
    lines.append(f"**問{question_type}**，用神為：{yongshen}")
    lines.append("")
    
    # 找用神爻
    yongshen_liuqin = yongshen.split('（')[0].strip()
    yongshen_lines = [l for l in najia['lines'] if l['liuqin'] == yongshen_liuqin]
    
    if yongshen_lines:
        for yl in yongshen_lines:
            status = []
            if yl['is_kong']:
                status.append('旬空')
            if yl['wangshuai'] in ['旺', '相']:
                status.append(f"{yl['wangshuai']}（有力）")
            elif yl['wangshuai'] in ['囚', '死']:
                status.append(f"{yl['wangshuai']}（無力）")
            
            status_str = '、'.join(status) if status else '休（平）'
            lines.append(f"- 用神在{yl['yao_name']}（{yl['tiangan']}{yl['dizhi']}），五行{yl['element']}，{yl['wangshuai']}，{status_str}")
    else:
        lines.append("- 卦中無用神，需看原神")
    
    return "\n".join(lines)


# ==================== 主程式 ====================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='六爻占卜')
    parser.add_argument('--coins', '-c', type=str, help='銅錢搖卦結果')
    parser.add_argument('--day', '-d', type=str, default='乙巳', help='占卜日干支')
    parser.add_argument('--month', '-m', type=str, default='巳', help='占卜月地支')
    parser.add_argument('--question', '-q', type=str, help='問題類型')
    parser.add_argument('--json', '-j', action='store_true', help='輸出 JSON 格式')
    
    args = parser.parse_args()
    
    if not args.coins:
        print("請提供銅錢搖卦結果")
        print("格式：python liuyao_divine.py --coins \"正正反 正反正 反反反 正正正 正反反 反正正\"")
        sys.exit(1)
    
    try:
        result = divine_coins(args.coins, args.day, args.month)
        
        if args.json:
            # 移除無法序列化的資料
            output = {
                'ben': result['hexagram']['ben'],
                'bian': result['hexagram']['bian'],
                'najia': result['najia'],
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(format_output(result, args.question))
    
    except Exception as e:
        print(f"錯誤：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)