# 六爻占卜 - Hermes_Rose 修改版

> 本項目由 **Hermes_Rose** 修改完成，基於原作者 [glennchen2207](https://github.com/glennchen2207) 的 [liuyao-divination](https://github.com/glennchen2207/liuyao-divination) 進行改良。

---

## 版本資訊

- **版本：** 4.0.0
- **修改日期：** 2026-07-24
- **基於來源：** [glennchen2207/liuyao-divination](https://github.com/glennchen2207/liuyao-divination)

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
├── SKILL.md                            # Hermes Agent 技能定義（v4.0.0）
├── scripts/
│   ├── liuyao_divine.py               # 六爻計算腳本（36KB）
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
python scripts/liuyao_divine.py --coins "--- --- --O --X -- ---" --day "乙巳" --month "巳"
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