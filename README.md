# 六爻占卜 - Hermes_Rose 修改版

> 本項目由 **Hermes_Rose** 修改完成，基於原作者 [glennchen2207](https://github.com/glennchen2207) 的 [liuyao-divination](https://github.com/glennchen2207/liuyao-divination) 進行改良。

---

## 版本資訊

- **版本：** 4.3.0
- **修改日期：** 2026-11-27
- **基於來源：** [glennchen2207/liuyao-divination](https://github.com/glennchen2207/liuyao-divination)

---

## v4.3.0 更新內容（2026-11-27：古筮解經路線接入）

- SKILL.md 新增「兩條解卦路線」節：納甲線之外接入**之卦對照法**（古筮線第四法——單爻陰陽反轉得之卦，借之卦卦義回解原爻辭）
- 觸發詞新增「之卦、以爻變解爻辭、古筮解經」
- 指向 wiki 權威頁：`以爻變解爻辭——之卦對照法.md`（384 爻全程式驗證對照表）＋`易經古法解卦——卦義拆卦與對卦.md`（整卦三法）；臨場換算可呼叫腳本 `get_hexagram_name` 查 `HEXAGRAMS` 表
- SKILL.md 與本地 skill 主本完全同步（repo 舊版殘留簡體字一併清除）；裝卦引擎腳本本次無改動

---

## v4.2.0 更新內容（2026-11-26：起卦日/月建自動化）

- `--day/--month` 不傳時**自動取今日干支＋節氣月建**（cnlunar；月建取八字月柱地支，節氣交界也正確），消除忘傳參數排錯盤的隱患
- 自動取得失敗時印 ⚠️ 警告並退回寫死預設「乙巳日/巳月」——**帶警告的盤不可直接引用**
- 輸出新增「月建」顯示（`占卜日：甲辰日｜月建：亥月`）
- 修復：匯入 `lunar_converter` 前先驗 `cnlunar` 存在（該模組 import 時對缺套件會印訊息＋`sys.exit`，原本會把呼叫方拖崩）

---

## v4.1.0 更新內容（2026-11-26：裝卦引擎修正）

| 修正項 | 說明 |
|:----:|:----|
| 爻序 | 震/巽/艮/兌 TRIGRAMS 爻序曾誤用上→下序，非對稱卦會排成爻位顛倒的反卦 |
| 旬空 | get_xunwang 曾不管日干支，永遠回傳甲子旬空「戌亥」；改為依當日干支所屬旬計算 |
| 外卦納甲 | 四五上爻地支曾誤取列表前3支（內卦那組）；改取索引 3,4,5（TRIGRAM_DIZHI＝內卦三支在前、外卦三支在後） |
| 爻位輸入 | 陽靜爻改用單一 `-`（`---` 含 `--` 子字串會被靜默解析為陰靜爻） |
| SKILL.md | 新增方法B（台幣）換算表、動爻誤判陷阱、抽查核對建議；修正萃→晉範例的動爻正反 |

✅ 驗證案例：澤地萃→火地晉（本卦、變卦、納甲六親、世應、六神、旬空均與傳統排盤一致）

---

## v4.0.0 更新內容（從 chinese-divination 拆分）

**重大架構變更**：從合併版 `chinese-divination`（v3.2.0）拆回獨立 Skill，觸發詞各自明確，不再混淆。

| 項目 | v3.2.0（合併版） | v4.0.0（獨立版） |
|:----:|:----:|:------:|
| Skill 名稱 | chinese-divination | liuyao-divination（獨立） |
| 觸發詞 | 六爻+小六壬混合 | 僅六爻相關 |
| 銅錢陰陽面 | CRITICAL 警告 | 同（保留） |
| 小六壬 | 包含 | 已移除（獨立為 xiaoliuren-divination） |

---

## 完整功能列表

| 項目 | 原版 | 修改版 |
|:----:|:----:|:------:|
| 自動計算腳本 | ❌ 無 | ✅ 完整六爻計算 |
| 銅錢搖卦支援 | ⚠️ 說明 | ✅ 完整解析+輸出+流派確認 |
| 納甲裝卦 | ❌ 手動 | ✅ 自動配天干地支 |
| 六親六神 | ⚠️ 需查表 | ✅ 自動配置 |
| 世應位置 | ⚠️ 需查表 | ✅ 自動判斷 |
| 六十四卦資料 | ❌ 無 | ✅ 完整64卦詳解 |
| 問題類型解讀 | ⚠️ 簡略 | ✅ 8種問題詳細解讀 |
| 輸出格式 | ⚠️ 範例 | ✅ 完整排盤輸出 |
| 影片知識整合 | ❌ 無 | ✅ 文墨龍/易谷/曾仕強 |

---

## 檔案結構

```
liuyao-divination-rose/
├── README.md                           # 本說明文件
├── HERMES_ROSE.md                      # 修改標註文件
├── SKILL.md                            # Hermes Agent 技能定義（v4.3.0）
├── scripts/
│   ├── liuyao_divine.py               # 六爻計算腳本（35KB）
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

### 銅錢搖卦

```bash
python scripts/liuyao_divine.py --coins "正正反 正反正 反反反 正正正 正反反 反正正"
python scripts/liuyao_divine.py --coins "正正反 正反正 反反反 正正正 正反反 反正正" --question "感情"
python scripts/liuyao_divine.py --coins "- - --X - -- --O" --day "甲辰" --month "亥"   # 陽靜爻=單一 '-'；'---' 會被解析為陰靜；--day/--month 不傳＝自動取今日（v4.2.0）
```

---

## ⚠️ 銅錢陰陽面定義

不同流派對銅錢正反面的陰陽定義不同，**每次起卦前必須確認**：

| 流派 | 正面（字面/年號） | 背面（滿文/面額） |
|:----:|:----:|:----:|
| 文墨龍（古銅錢法） | 陰 | 陽 |
| 中華民國硬幣法 | 陽 | 陰 |

> 兩種流派的正面陰陽剛好相反，三正/三反判定完全不同。每次起卦前必須先確認使用哪種定義。

---

## 相關項目

- **xiaoliuren-divination-rose** — 小六壬卜卦 Skill（獨立 repo）

---

## 授權

本修改版延續原作者的授權方式。