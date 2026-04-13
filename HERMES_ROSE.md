# Hermes_Rose 修改標註

本項目由 **Hermes_Rose** 於 **2026-04-13** 修改完成。

---

## 修改者資訊

- **修改者：** Hermes_Rose（玫瑰）
- **修改日期：** 2026-04-13
- **修改版本：** 2.0
- **基於來源：** [glennchen2207/liuyao-divination](https://github.com/glennchen2207/liuyao-divination)

---

## 修改內容

### 新增檔案

| 檔案 | 說明 |
|:-----|:-----|
| `scripts/liuyao_divine.py` | 自動六爻計算腳本（36KB） |
| `references/hexagrams.md` | 六十四卦詳解（9KB） |
| `references/question-types.md` | 問題類型解讀（10KB） |
| `README.md` | 項目說明文件 |
| `HERMES_ROSE.md` | 本標註文件 |

### 修改檔案

| 檔案 | 修改說明 |
|:-----|:---------|
| `SKILL.md` | 大幅擴充，新增銅錢搖卦詳細流程、納甲裝卦說明 |
| `references/tables.md` | 保持原版完整對照表 |

### 功能增強

1. **自動銅錢搖卦計算**
   - 支援「正反」格式輸入
   - 支援符號格式輸入
   - 自動判斷本卦、變卦

2. **納甲裝卦自動化**
   - 天干地支自動配置
   - 六親自動計算
   - 六神自動配置（依日干）

3. **世應位置自動判斷**
   - 依八宮卦自動判斷世應位置

4. **旺衰空亡自動計算**
   - 五行旺相休囚死判斷
   - 旬空判斷

5. **六十四卦詳解**
   - 各卦卦義
   - 占卜參考
   - 爻辭

6. **問題類型解讀**
   - 事業、財運、感情、健康
   - 考試、出行、尋人、官非
   - 各類問題的用神和斷卦要點

---

## 技術細節

### 自動計算腳本

**檔案：** `scripts/liuyao_divine.py`

**功能：**
- 銅錢搖卦解析
- 本卦、變卦計算
- 納甲裝卦
- 世應位置判斷
- 旺衰、空亡計算
- 問題類型解讀

**使用方式：**
```bash
python scripts/liuyao_divine.py --coins "正正反 正反正 反反反 正正正 正反反 反正正"
```

---

## 原作者

- **原作者：** glennchen2207
- **原項目：** https://github.com/glennchen2207/liuyao-divination

---

## 授權

本修改版延續原作者的授權方式。