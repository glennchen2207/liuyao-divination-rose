---
name: liuyao-divination
version: 4.0.0
description: 六爻占卜（納甲筮法）。銅錢搖卦、蓍草法、納甲裝卦、六親六神、旺衰分析、深度斷卦。觸發詞：六爻、六爻占卜、銅錢卦、金錢卦、納甲、銅錢搖卦、起卦（六爻）。Use when user asks for liuyao divination, coin divination, najia analysis, or hexagram casting with full najia setup.
triggers:
  - 六爻、六爻占卜、銅錢卦、金錢卦、納甲、銅錢搖卦
  - 龜卦、文王卦、六爻卦
  - liuyao, najia divination, coin divination, hexagram casting
---

# 六爻占卜（納甲筮法）

六爻占卜是源於《易經》的傳統占卜方法，透過銅錢搖卦，得到六十四卦之一，結合天干地支、五行生剋、六親六神進行深度斷卦分析。

## When to Use

- User asks to 六爻占卜、銅錢搖卦、納甲起卦
- User provides coin results (正/反) and wants detailed hexagram analysis
- User asks about career, wealth, love, health via 六爻 divination
- **NOT for 小六壬** — 小六壬 uses separate skill `xiaoliuren-divination`

## Quick Start (Coin Method)

1. User shakes 6 coins and reports 正/反 for each throw
2. Build 本卦 and 變卦 from results
3. 納甲 (assign stem/branch, 六亲, 六神)
4. Determine 世應 position
5. Judge 旺衰 by month
6. Select 用神 based on question type
7. Deliver structured reading

## Coin Results Reference

| Result | 正/反 | Name | Symbol | Type |
|:------:|:-----:|:----:|:------:|:----:|
| 兩正一反 | 2:1 | 少陽 | — | Static Yang |
| 一正兩反 | 1:2 | 少陰 | -- | Static Yin |
| 三反 | 0:3 | 老陽 | ○ | Moving Yang → Yin |
| 三正 | 3:0 | 老陰 | × | Moving Yin → Yang |

## Casting Order & Structure

- 6 throws from bottom to top: 1st throw = 初爻, 6th = 上爻
- Throws 1-3 form 下卦 (lower trigram), throws 4-6 form 上卦 (upper trigram)
- Any throw with 3正 or 3反 = 動爻 (moving line), which flips in the 變卦
- All 7/8 = 靜爻 (static), no change in 變卦

**Synonyms**: 龜卦 = 文王卦 = 六爻卦 = 金錢卦 = 銅錢卦 (same system, different names)

## ⚠️ CRITICAL: Confirm Coin Method Before Casting

**Different coin methods define yin/yang faces differently — sometimes OPPOSITE — producing entirely different hexagrams from the same coin results.**

**Mandatory step before every 六爻 casting:**
1. Ask the user which coin method they are using: 文墨龍古銅錢法 or 中華民國硬幣法 or custom definition
2. Apply the corresponding yin/yang mapping consistently for all 6 throws
3. Only after confirming the method, proceed to `parse_coins()` and full najia

### 方法 A：文墨龍傳統古銅錢法
- 有年號的面（乾隆通寶、康熙通寶等）= 字面 = 正面 = **陰面**
- 背面（筆畫較少的面，滿文局名等）= 背 = **陽面**
- ⚠️ 直覺容易搞反：有字≠陽，在文墨龍系統中有年號=陰

### 方法 B：中華民國硬幣法（Brian 自定義）
- 正面（國父孫中山頭像＋中華民國年號面）= **陽面**
- 反面／背面（面額面：壹圓、伍圓等）= **陰面**
- ⚠️ 與文墨龍法正面陰陽定義**剛好相反**
- 詳見 Wiki：易學/概念/補充/中華民國硬幣起卦法.md

### 方法 C：現代硬幣自定義（FB 教學 method）
- 硬幣正反面可自行定義
- **只需全程保持一致即可**
- 自定義後：3正面=老陽（變陰爻）、3反面=老陰（變陽爻）

**Key difference:**
- 文墨龍法: 正面(字面)=陰, 三正面=老陰×, 三反面=老陽○
- 中華民國法: 正面(孫中山面)=陽, 三正面=老陽○, 三反面=老陰×

## 蓍草法（大衍之數，曾仕強教學）

Classic method from 繫辭上傳 Ch.9 — 大衍之數五十，其用四十有九. Three rounds per line (三變得一爻), yielding 6/7/8/9. See `references/liuyao-video-sources.md` for full steps.

1. 50根蓍草，取1根置前 → 代表「不變」（堅定意志）
2. 49根隨機分兩堆 → 分而為二以象兩（天地/陰陽）
3. 從右堆取1根夾左手指間 → 掛一以象三（天地人三才）
4. 每4根一束數 → 揲之以四以象四時
5. 餘數放指間 → 歸奇於扐以象閏
6. 第一變餘數：不是5就是9
7. 第二變餘數：不是4就是8
8. 第三變餘數：不是4就是8
9. 數剩餘束數 → 得6/7/8/9
10. 每爻需三變，六爻共18變成一卦

**Probability:** 八(最常見) > 七 > 九 > 六(最少)
- 哲學含義：大多數事情是不變的（七、八），真正變的是少數（六、九）

## Trigram Lookup（八卦組合查表）

- 三個陽爻(☰) = 乾卦
- 三個陰爻(☷) = 坤卦
- 陽陽陰(☱) = 兌卦
- 陰陽陽(☴) = 巽卦
- 陽陰陰(☳) = 震卦
- 陰陽陽(☵) = 坎卦（初陰+中陽+上陰）
- 陽陰陽(☲) = 離卦
- 陰陽陰(☶) = 艮卦

## 六神 (Six Spirits)

| Spirit | Animal | Element |
|:------:|:------:|:-------:|
| 青龍 | Dragon  | Wood    |
| 朱雀 | Sparrow | Fire    |
| 勾陳 | Gouchen | Earth   |
| 螣蛇 | Snake   | Earth   |
| 白虎 | Tiger   | Metal   |
| 玄武 | Tortoise| Water   |

## 爻的術語對照

| Common Name | 符號 | 術語名 | 性質 |
|:-----------:|:----:|:------:|:----:|
| 陽爻 | — | 單 | 陽（靜） |
| 陰爻 | -- | 拆 | 陰（靜） |
| 老陽/陽爻動爻 | ○ | 重 | 陽（動）→ 變陰 |
| 老陰/陰爻動爻 | × | 交 | 陰（動）→ 變陽 |

## Worked Example: 澤地萃 → 火地晉

| 爻位 | 擲卦結果 | 判定 | 變化 |
|------|---------|------|------|
| 初爻 | 1陰2陽 | 陰爻（少陰） | 不變 |
| 二爻 | 2陽1陰 | 陰爻（少陰） | 不變 |
| 三爻 | 2陽1陰 | 陰爻（少陰） | 不變 |
| 四爻 | 2陰1陽 | 陽爻（少陽） | 不變 |
| 五爻 | 3正面 | 老陽 | 變陰爻 |
| 上爻 | 3反面 | 老陰 | 變陽爻 |

- **本卦**：下卦=坤(地) + 上卦=兌(澤) = **澤地萃**（第45卦）
- **變卦**：五爻老陽變陰→上卦由兌變離(火)，下卦不變= **火地晉**（第35卦）

## Pitfalls

- 六爻 interpretation is complex; always do full 納甲 setup before concluding
- Ensure all 簡體 → 繁體 conversion when storing results in wiki
- 網路排盤軟體有兩種排列方向（由上往下 vs 由下往上），輸入時需留意

### ⚠️ Common Misread Patterns

| Mistake | What happened | Why dangerous |
|---------|--------------|-------------|
| 正反正 ↔ 反正反 | Swapped two characters, 2:1 vs 1:2 | Changes yin↔yang for that line |
| 正反反 ↔ 反正正 | Swapped start/end, same 1:2 but different order | Less dangerous (same type) but still verify |

### ⚠️ Script Bug: `get_trigram_from_line`

The `build_hexagram()` function in `scripts/liuyao_divine.py` calls `get_trigram_from_line()` (line ~275) which is only defined as an alias for `get_trigram_from_lines()`. If the alias ever breaks or the function is removed, the outer trigram lookup will fail silently.

## Video Sources (影片學習來源)

三部 YouTube 教學影片的完整知識摘要見 `references/liuyao-video-sources.md`：
1. **文墨龍** — 銅錢起卦正確方法 (v1FBl9Unrds, 46K views)
2. **易谷** — 六爻知識架構篇：本卦、變卦和爻 (KeTv6CIRfzE, 34K views)
3. **曾仕強** — 如何卜卦？如何解卦？ (R7SCFbdpePc, 336K views)

Wiki 知識庫頁面：
- `易學/概念/補充/文墨龍銅錢起卦.md`
- `易學/概念/補充/易谷六爻知識架構.md`
- `易學/概念/補充/曾仕強卜卦解卦.md`

## Related Skills

- `xiaoliuren-divination` — 小六壬卜卦（不同系統，觸發詞不同）
- `chinese-divination` — 已合併為本 skill，不再使用