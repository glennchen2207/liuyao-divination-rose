# Hermes_Rose 修改標註

## 版本歷程

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