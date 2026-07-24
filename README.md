# 六爻占卜 + 小六壬 - Hermes_Rose 修改版

> 本項目由 **Hermes_Rose** 修改完成，基於原作者 [glennchen2207](https://github.com/glennchen2207) 的 [liuyao-divination](https://github.com/glennchen2207/liuyao-divination) 進行改良。

---

## 版本資訊

- **版本：** 3.2.0
- **修改日期：** 2026-07-24
- **基於來源：** [glennchen2207/liuyao-divination](https://github.com/glennchen2207/liuyao-divination)

---

## v3.2.0 更新內容

| 項目 | v2.0 | v3.2.0 |
|:----:|:----:|:------:|
| Skill 名稱 | liuyao-divination | chinese-divination（合併） |
| 涵蓋範圍 | 僅六爻 | 六爻 + 小六壬 |
| 銅錢陰陽面 | 無流派警告 | ⚠️ CRITICAL：起卦前確認流派 |
| 影片知識來源 | 無 | 文墨龍、易谷、曾仕強 |
| 小六壬卜卦 | ❌ | ✅ divine.py |
| 六爻案例研究 | ❌ | ✅ liuyao-case-study-misread.md |
| 六爻影片來源 | ❌ | ✅ liuyao-video-sources.md |

---

## 完整功能列表

| 項目 | 原版 | 修改版 |
|:----:|:----:|:------:|
| 自動計算腳本 | ❌ 無 | ✅ 完整六爻 + 小六壬計算 |
| 銅錢搖卦支援 | ⚠️ 說明 | ✅ 完整解析+輸出+流派確認 |
| 納甲裝卦 | ❌ 手動 | ✅ 自動配天干地支 |
| 六親六神 | ⚠️ 需查表 | ✅ 自動配置 |
| 世應位置 | ⚠️ 需查表 | ✅ 自動判斷 |
| 六十四卦資料 | ❌ 無 | ✅ 完整64卦詳解 |
| 問題類型解讀 | ⚠️ 簡略 | ✅ 8種問題詳細解讀 |
| 輸出格式 | ⚠️ 範例 | ✅ 完整排盤輸出 |
| 小六壬卜卦 | ❌ 無 | ✅ 大安/留連/速喜/赤口/小吉/空亡 |
| 影片知識整合 | ❌ 無 | ✅ 文墨龍/易谷/曾仕強 |

---

## 檔案結構

```
chinese-divination/
├── README.md                           # 本說明文件
├── HERMES_ROSE.md                      # 修改標註文件
├── SKILL.md                            # Hermes Agent 技能定義（v3.2.0）
├── scripts/
│   ├── liuyao_divine.py               # 六爻計算腳本（36KB）
│   ├── divine.py                       # 小六壬計算腳本
│   └── lunar_converter.py              # 農曆轉換腳本
└── references/
    ├── tables.md                       # 完整對照表
    ├── hexagrams.md                    # 六十四卦詳解
    ├── question-types.md               # 問題類型解讀
    ├── liuyao-case-study-misread.md    # 六爻案例誤讀研究
    └── liuyao-video-sources.md         # 六爻影片知識來源
```

---

## 安裝需求

```bash
pip install cnlunar
```

---

## 使用方式

### 六爻占卜

```bash
# 銅錢搖卦
python scripts/liuyao_divine.py --coins "正正反 正反正 反反反 正正正 正反反 反正正"

# 帶問題類型
python scripts/liuyao_divine.py --coins "正正反 正反正 反反反 正正正 正反反 反正正" --question "感情"

# 指定占卜日
python scripts/liuyao_divine.py --coins "--- --- --O --X -- ---" --day "乙巳" --month "巳"
```

### 小六壬卜卦

```bash
python scripts/divine.py
```

---

## ⚠️ 銅錢陰陽面定義

不同流派對銅錢正反面的陰陽定義不同，**每次起卦前必須確認**：

| 流派 | 正面（字面/年號） | 背面（滿文/面額） |
|:----:|:----:|:----:|
| 文墨龍（古銅錢法） | 陰 | 陽 |
| 中華民國硬幣法 | 陽 | 陰 |

> 兩種流派的正面陰陽剛好相反，三正/三反的判定完全不同，起卦前必須先確認使用哪種定義。

---

## 問題類型

| 類型 | 用神 | 說明 |
|:----:|:----:|:-----:|
| 事業工作 | 官鬼爻 | 工作、職位、上司 |
| 財運投資 | 妻財爻 | 財運、投資、薪水 |
| 感情婚姻 | 妻財（男）/ 官鬼（女） | 感情、對象 |
| 健康疾病 | 官鬼（病）/ 子孫（藥） | 疾病、醫藥 |
| 考試學業 | 父母爻 | 文書、成績 |
| 出行旅行 | 世爻 | 出行平安 |
| 尋人尋物 | 依關係取 | 人、物 |
| 官非訴訟 | 官鬼爻 | 訴訟、官司 |

---

## 授權

本修改版延續原作者的授權方式。