# Hermes_Rose 修改標註

## 版本歷程

### v4.2.0 (2026-11-26)
- `--day/--month` 自動化：不傳時自動取今日干支＋節氣月建（cnlunar・八字月柱地支）；失敗印 ⚠️ 退回預設乙巳/巳
- 輸出新增月建顯示（`占卜日｜月建`）
- 修復 import 順序：lunar_converter 匯入時對缺 cnlunar 會 sys.exit（SystemExit 無法被 except Exception 捕獲），改為先驗 cnlunar 存在再匯入

### v4.1.0 (2026-11-26)
- 裝卦引擎三類 bug 修正：TRIGRAMS 爻序（震/巽/艮/兌曾上下顛倒）、get_xunwang 旬空計算（曾永回戌亥）、外卦納甲地支取支（四五上爻曾取錯）
- 爻位式輸入陽靜爻改單一 `-`（`---` 會被解析為陰靜）
- SKILL.md 新增方法B台幣換算表、動爻誤判陷阱、納甲盤抽查核對建議；萃→晉工作範例動爻正反筆誤修正
- 驗證案例：澤地萃→火地晉，與傳統排盤一致

### v4.0.0 (2026-07-24)
- **重大架構變更**：從 chinese-divination（合併版 v3.2.0）拆分回獨立 Skill
- Skill 名稱改回 `liuyao-divination`，觸發詞明確僅含六爻相關
- 移除小六壬相關內容（divine.py 已移至 xiaoliuren-divination-rose）
- 觸發詞不再包含「小六壬」「掐指一算」等小六壬專屬詞
- 保留所有六爻功能、銅錢流派確認、影片知識來源

### v3.2.0 (2026-07-24)
- 合併六爻+小六壬為 chinese-divination umbrella skill
- 新增 CRITICAL：銅錢陰陽面流派確認
- 新增小六壬卜卦功能（divine.py）
- 新增六爻案例誤讀研究、影片知識來源

### v2.0 (2026-04-13)
- 初始修改版，基於原版 liuyao-divination
- 新增自動銅錢搖卦計算
- 新增納甲裝卦自動化
- 新增六十四卦詳解
- 新增問題類型解讀