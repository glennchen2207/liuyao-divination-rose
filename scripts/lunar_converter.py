#!/usr/bin/env python3
"""
農曆轉換腳本
使用 cnlunar 套件進行西曆轉農曆轉換

使用方式：
    python lunar_converter.py --date "2026-01-25 13:03"
    python lunar_converter.py --date "2026-04-17 08:30"

輸出：
    JSON 格式的農曆資訊，包含年月日時的干支與序數
"""

import argparse
import datetime
import json
import sys

try:
    import cnlunar
except ImportError:
    print("請先安裝 cnlunar 套件：pip install cnlunar")
    sys.exit(1)


# 地支對應序數
DIZHI_MAP = {
    '子': 1, '丑': 2, '寅': 3, '卯': 4,
    '辰': 5, '巳': 6, '午': 7, '未': 8,
    '申': 9, '酉': 10, '戌': 11, '亥': 12
}

# 時辰對應時間範圍
SHICHEN_MAP = {
    (23, 1): ('子時', '子'),
    (1, 3): ('丑時', '丑'),
    (3, 5): ('寅時', '寅'),
    (5, 7): ('卯時', '卯'),
    (7, 9): ('辰時', '辰'),
    (9, 11): ('巳時', '巳'),
    (11, 13): ('午時', '午'),
    (13, 15): ('未時', '未'),
    (15, 17): ('申時', '申'),
    (17, 19): ('酉時', '酉'),
    (19, 21): ('戌時', '戌'),
    (21, 23): ('亥時', '亥'),
}


def get_shichen(hour: int) -> tuple:
    """根據小時取得時辰"""
    if hour == 23 or hour == 0:
        return ('子時', '子')
    for (start, end), (name, zhi) in SHICHEN_MAP.items():
        if start <= hour < end:
            return (name, zhi)
    return ('子時', '子')  # 預設


def convert_to_lunar(date_str: str) -> dict:
    """
    將西曆日期時間轉換為農曆資訊
    
    Args:
        date_str: 西曆日期時間字串，格式 "YYYY-MM-DD HH:MM"
    
    Returns:
        dict: 農曆資訊
    """
    # 解析日期時間
    try:
        if ' ' in date_str:
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        else:
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError as e:
        return {'error': f'日期格式錯誤：{e}'}
    
    # 使用 cnlunar 轉換
    lunar = cnlunar.Lunar(dt, godType='8char')
    
    # 取得時辰
    shichen_name, shichen_zhi = get_shichen(dt.hour)
    
    # 從年干支取得年支
    year_8char = lunar.year8Char  # 例: '乙巳'
    year_zhi = year_8char[1]  # 取地支 '巳'
    year_zhi_num = DIZHI_MAP.get(year_zhi, 0)
    
    # 時辰序數
    shichen_num = DIZHI_MAP.get(shichen_zhi, 0)
    
    # 組合結果
    result = {
        'western_date': dt.strftime('%Y-%m-%d %H:%M'),
        'lunar_year': lunar.lunarYear,
        'lunar_month': lunar.lunarMonth,
        'lunar_day': lunar.lunarDay,
        'lunar_month_cn': lunar.lunarMonthCn,  # 例: '臘月'
        'lunar_day_cn': lunar.lunarDayCn,  # 例: '初七'
        'year_ganzhi': lunar.year8Char,  # 例: '乙巳'
        'year_zhi': year_zhi,  # 例: '巳'
        'year_zhi_num': year_zhi_num,  # 例: 6
        'month_ganzhi': lunar.month8Char,
        'day_ganzhi': lunar.day8Char,
        'shichen': shichen_name,  # 例: '未時'
        'shichen_zhi': shichen_zhi,  # 例: '未'
        'shichen_num': shichen_num,  # 例: 8
        'full_cn': f'{lunar.lunarYearCn}年{lunar.lunarMonthCn}{lunar.lunarDayCn}',
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='西曆轉農曆工具')
    parser.add_argument('--date', '-d', required=True, help='西曆日期時間（格式：YYYY-MM-DD HH:MM）')
    parser.add_argument('--json', '-j', action='store_true', help='輸出 JSON 格式')
    
    args = parser.parse_args()
    
    result = convert_to_lunar(args.date)
    
    if 'error' in result:
        print(f"錯誤: {result['error']}")
        sys.exit(1)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"西曆：{result['western_date']}")
        print(f"農曆：{result['full_cn']}")
        print(f"年干支：{result['year_ganzhi']}（年支序數：{result['year_zhi_num']}）")
        print(f"月：{result['lunar_month']}（{result['lunar_month_cn']}）")
        print(f"日：{result['lunar_day']}（{result['lunar_day_cn']}）")
        print(f"時辰：{result['shichen']}（序數：{result['shichen_num']}）")


if __name__ == '__main__':
    main()