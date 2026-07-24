#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小六壬卜卦計算腳本"""

import sys
import os
from datetime import datetime, timezone, timedelta

# Windows 編碼處理
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    from lunar_python import Lunar, Solar
except ImportError:
    print("錯誤：請先安裝 lunar_python")
    sys.exit(1)

# 六卦定義
HEXAGRAMS = ["大安", "留連", "速喜", "赤口", "小吉", "空亡"]

# 時辰對應
SHICHEN = {
    "子": {"hours": "23:00-01:00", "num": 1},
    "丑": {"hours": "01:00-03:00", "num": 2},
    "寅": {"hours": "03:00-05:00", "num": 3},
    "卯": {"hours": "05:00-07:00", "num": 4},
    "辰": {"hours": "07:00-09:00", "num": 5},
    "巳": {"hours": "09:00-11:00", "num": 6},
    "午": {"hours": "11:00-13:00", "num": 7},
    "未": {"hours": "13:00-15:00", "num": 8},
    "申": {"hours": "15:00-17:00", "num": 9},
    "酉": {"hours": "17:00-19:00", "num": 10},
    "戌": {"hours": "19:00-21:00", "num": 11},
    "亥": {"hours": "21:00-23:00", "num": 12},
}

SHICHEN_ORDER = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 月份卦象對照（正月=1）
MONTH_HEXAGRAMS = {
    1: 0, 7: 0,   # 大安
    2: 1, 8: 1,   # 留連
    3: 2, 9: 2,   # 速喜
    4: 3, 10: 3,  # 赤口
    5: 4, 11: 4,  # 小吉
    6: 5, 12: 5,  # 空亡
}

# 吉凶等級
AUSPICIOUSNESS = {
    "大安": "吉",
    "留連": "平",
    "速喜": "吉",
    "赤口": "凶",
    "小吉": "吉",
    "空亡": "凶",
}

# 五行
FIVE_ELEMENTS = {
    "大安": "木",
    "留連": "水",
    "速喜": "火",
    "赤口": "金",
    "小吉": "水",
    "空亡": "土",
}

# 神獸
SPIRIT_BEASTS = {
    "大安": "青龍",
    "留連": "玄武",
    "速喜": "朱雀",
    "赤口": "白虎",
    "小吉": "六合",
    "空亡": "勾陳",
}


def get_shichen(hour: int) -> tuple:
    """根據小時取得時辰名稱和數字"""
    if hour == 23 or hour == 0:
        return "子", 1
    elif 1 <= hour <= 2:
        return "丑", 2
    elif 3 <= hour <= 4:
        return "寅", 3
    elif 5 <= hour <= 6:
        return "卯", 4
    elif 7 <= hour <= 8:
        return "辰", 5
    elif 9 <= hour <= 10:
        return "巳", 6
    elif 11 <= hour <= 12:
        return "午", 7
    elif 13 <= hour <= 14:
        return "未", 8
    elif 15 <= hour <= 16:
        return "申", 9
    elif 17 <= hour <= 18:
        return "酉", 10
    elif 19 <= hour <= 20:
        return "戌", 11
    else:  # 21-22
        return "亥", 12


def count_hexagram(start_idx: int, count: int) -> int:
    """從起始卦象開始，數 count 步後的卦象索引"""
    return (start_idx + count - 1) % 6


def divine(solar_year: int, solar_month: int, solar_day: int, hour: int, minute: int) -> dict:
    """
    執行小六壬卜卦
    
    參數:
        solar_year: 西曆年
        solar_month: 西曆月
        solar_day: 西曆日
        hour: 小時 (0-23)
        minute: 分鐘 (0-59)
    
    回傳:
        包含完整卜卦結果的字典
    """
    # 轉換為農曆
    solar = Solar.fromDate(datetime(solar_year, solar_month, solar_day, hour, minute))
    lunar = solar.getLunar()
    
    lunar_month = lunar.getMonth()
    lunar_day = lunar.getDay()
    
    # 處理跨日子時
    actual_hour = hour
    if hour == 23:
        # 23:00-23:59 屬當日子時，日期不變
        pass
    
    # 取得時辰
    shichen_name, shichen_num = get_shichen(actual_hour)
    
    # 第一步：月份卦象
    month_hex_idx = MONTH_HEXAGRAMS[lunar_month]
    month_hex = HEXAGRAMS[month_hex_idx]
    
    # 第二步：日期卦象（從月份卦象開始數）
    day_hex_idx = count_hexagram(month_hex_idx, lunar_day)
    day_hex = HEXAGRAMS[day_hex_idx]
    
    # 第三步：時辰卦象（從日期卦象開始數）
    shichen_hex_idx = count_hexagram(day_hex_idx, shichen_num)
    shichen_hex = HEXAGRAMS[shichen_hex_idx]
    
    # 組合判斷
    combination = get_combination_interpretation(month_hex, day_hex, shichen_hex)
    
    return {
        "solar": {
            "year": solar_year,
            "month": solar_month,
            "day": solar_day,
            "hour": hour,
            "minute": minute,
            "datetime_str": f"{solar_year}年{solar_month}月{solar_day}日 {hour:02d}:{minute:02d}",
        },
        "lunar": {
            "month": lunar_month,
            "day": lunar_day,
            "month_chinese": lunar.getMonthInChinese(),
            "day_chinese": lunar.getDayInChinese(),
        },
        "shichen": {
            "name": shichen_name,
            "num": shichen_num,
            "hours": SHICHEN[shichen_name]["hours"],
        },
        "hexagrams": {
            "month": {
                "name": month_hex,
                "stage": "開始",
                "auspicious": AUSPICIOUSNESS[month_hex],
                "element": FIVE_ELEMENTS[month_hex],
                "beast": SPIRIT_BEASTS[month_hex],
            },
            "day": {
                "name": day_hex,
                "stage": "過程",
                "auspicious": AUSPICIOUSNESS[day_hex],
                "element": FIVE_ELEMENTS[day_hex],
                "beast": SPIRIT_BEASTS[day_hex],
            },
            "shichen": {
                "name": shichen_hex,
                "stage": "結果",
                "auspicious": AUSPICIOUSNESS[shichen_hex],
                "element": FIVE_ELEMENTS[shichen_hex],
                "beast": SPIRIT_BEASTS[shichen_hex],
            },
        },
        "combination": combination,
    }


def get_combination_interpretation(month_hex: str, day_hex: str, shichen_hex: str) -> dict:
    """取得三卦組合的整體解讀"""
    
    # 統計吉凶
    auspicious_count = sum(1 for h in [month_hex, day_hex, shichen_hex] if AUSPICIOUSNESS[h] == "吉")
    neutral_count = sum(1 for h in [month_hex, day_hex, shichen_hex] if AUSPICIOUSNESS[h] == "平")
    inauspicious_count = sum(1 for h in [month_hex, day_hex, shichen_hex] if AUSPICIOUSNESS[h] == "凶")
    
    # 整體評分 (0-100)
    score = auspicious_count * 30 + neutral_count * 10
    
    # 決定整體評語
    if auspicious_count == 3:
        overall = "極佳"
        advice = "運勢極佳，諸事順利，把握時機行動。"
    elif auspicious_count == 2 and neutral_count == 1:
        overall = "佳"
        advice = "大致順利，中間有些波折，最終結果良好。"
    elif auspicious_count == 2 and inauspicious_count == 1:
        overall = "尚可"
        advice = "開始順利，但某個階段會有阻礙，需多加注意。"
    elif auspicious_count == 1 and neutral_count == 2:
        overall = "平穩"
        advice = "平穩中帶有轉機，需要耐心等待時機。"
    elif auspicious_count == 1 and neutral_count == 1 and inauspicious_count == 1:
        overall = "普通"
        advice = "起頭不錯，中間有阻礙，結果需謹慎應對。"
    elif inauspicious_count == 3:
        overall = "較差"
        advice = "運勢較差，建議暫緩重要決定，多加觀察。"
    elif inauspicious_count == 2:
        overall = "不佳"
        advice = "阻礙較多，宜保守行事，避免衝動。"
    elif neutral_count >= 2:
        overall = "平"
        advice = "運勢普通，保持平常心即可。"
    else:
        overall = "一般"
        advice = "依實際情況謹慎判斷。"
    
    return {
        "overall": overall,
        "score": score,
        "auspicious_count": auspicious_count,
        "neutral_count": neutral_count,
        "inauspicious_count": inauspicious_count,
        "advice": advice,
        "start_end_relation": get_relation_reading(month_hex, shichen_hex),
    }


def get_relation_reading(start_hex: str, end_hex: str) -> str:
    """解讀開始卦與結果卦的關係"""
    
    # 五行相生相剋
    elements = {"木": {"生": "火", "剋": "土", "被生": "水", "被剋": "金"},
                "火": {"生": "土", "剋": "金", "被生": "木", "被剋": "水"},
                "土": {"生": "金", "剋": "水", "被生": "火", "被剋": "木"},
                "金": {"生": "水", "剋": "木", "被生": "土", "被剋": "火"},
                "水": {"生": "木", "剋": "火", "被生": "金", "被剋": "土"}}
    
    start_element = FIVE_ELEMENTS[start_hex]
    end_element = FIVE_ELEMENTS[end_hex]
    
    if start_element == end_element:
        return f"開始與結果同屬{start_element}，事態穩定發展。"
    
    if end_element == elements[start_element]["生"]:
        return f"{start_element}生{end_element}，過程順暢，結果比預期更好。"
    
    if end_element == elements[start_element]["剋"]:
        return f"{start_element}剋{end_element}，過程有阻礙但可克服。"
    
    if end_element == elements[start_element]["被生"]:
        return f"{end_element}生{start_element}，外在資源有助於事態發展。"
    
    if end_element == elements[start_element]["被剋"]:
        return f"{end_element}剋{start_element}，可能有外在阻力，需謹慎應對。"
    
    return f"開始{start_element}，結果{end_element}，看具體問題而定。"


def format_output(result: dict) -> str:
    """格式化輸出"""
    lines = []
    
    lines.append("## 🔮 小六壬卜卦")
    lines.append("")
    lines.append(f"**西曆：** {result['solar']['datetime_str']}")
    lines.append(f"**農曆：** {result['lunar']['month_chinese']}{result['lunar']['day_chinese']} {result['shichen']['name']}時")
    lines.append("")
    
    # 三卦表格
    lines.append("### 卦象結果")
    lines.append("")
    lines.append("| 階段 | 卦象 | 吉凶 | 五行 | 神獸 |")
    lines.append("|:----:|:----:|:----:|:----:|:----:|")
    
    for stage in ["month", "day", "shichen"]:
        h = result["hexagrams"][stage]
        auspicious_icon = "✅" if h["auspicious"] == "吉" else ("⚠️" if h["auspicious"] == "凶" else "➖")
        lines.append(f"| **{h['stage']}** | {h['name']} | {auspicious_icon} {h['auspicious']} | {h['element']} | {h['beast']} |")
    
    lines.append("")
    
    # 組合解讀
    combo = result["combination"]
    lines.append("### 📊 綜合分析")
    lines.append("")
    lines.append(f"**整體運勢：** {combo['overall']} ({combo['score']}/90)")
    lines.append(f"**吉平凶分布：** 吉 {combo['auspicious_count']} / 平 {combo['neutral_count']} / 凶 {combo['inauspicious_count']}")
    lines.append("")
    lines.append(f"**建議：** {combo['advice']}")
    lines.append("")
    lines.append(f"**開始與結果關係：** {combo['start_end_relation']}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("用法：python divine.py <年> <月> <日> <時> [分]")
        print("範例：python divine.py 2024 4 13 14")
        print("範例：python divine.py 2024 4 13 14 30")
        sys.exit(1)
    
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    
    result = divine(year, month, day, hour, minute)
    print(format_output(result))