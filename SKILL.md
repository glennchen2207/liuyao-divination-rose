---
name: liuyao-divination
version: 4.3.0
description: 六爻占卜（納甲筮法）。銅錢搖卦、蓍草法、納甲裝卦、六親六神、旺衰分析、深度斷卦。觸發詞：六爻、六爻占卜、銅錢卦、金錢卦、納甲、銅錢搖卦、起卦（六爻）。Use when user asks for liuyao divination, coin divination, najia analysis, or hexagram casting with full najia setup.
triggers:
  - 六爻、六爻占卜、銅錢卦、金錢卦、納甲、銅錢搖卦
  - 之卦、以爻變解爻辭、古筮解經
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
3. 納甲 (assign stem/branch, 六親, 六神)
4. Determine 世應 position
5. Judge 旺衰 by month
6. Select 用神 based on question type
7. Deliver structured reading

## 解卦輸出風格（Brian 偏好）

固定節奏：**日常比喻建立直覺**（車、電梯、健身房等生活物件）→ **爻象與盤面重點用表格＋emoji** → 整體寓意 → **一句話總結收尾**。先比喻後術語、逐層疊加，不一次堆滿術語；全篇繁體。無具體問題念頭時明說「泛解供驗證、真占須先有問題」，不硬抓用神。

- **術語大表不可單獨出場**：復盤對帳、翻案表、旺衰全表這類行話密集的表格，每個術語行都要配一列白話直譯（如「旬空＝這件事目前是空的」），或先寫白話劇情線、把術語表放到深讀附錄——行話堆疊的解說他讀不懂，只會回頭要求「簡單直白說明」。

## 兩條解卦路線：納甲線 vs 古筮解經線（v4.3.0）

- **納甲線**（主線，上方各節）：真問占——走六親用神、旺衰、應期。
- **古筮解經線**：Brian 引用爻辭、問某句爻辭何義、或想以《易經》文本解卦時走這條。核心方法＝**之卦對照法**（古筮線第四法，管「單爻」）：原卦第 k 爻陰陽反轉得「之卦」，借之卦的卦名卦象卦義回解原爻辭；整卦層級另有卦義／拆卦／對卦三法。

之卦對照三步：①定位爻位讀爻辭 → ②查 64 卦爻變表第 k 欄得之卦（例：乾初九→天風姤）→ ③用之卦之義印證或照亮原爻辭。過度解讀是此法最大風險——之卦義與原爻辭連不上時不可硬凹。

⚠️ 兩線邊界：同一卦的納甲斷語（吉凶應期）與古筮解讀（爻辭意涵）可能不同，回報時標明依哪條線。

Wiki 權威頁（掛載路徑讀取；384 爻→之卦對照表已全程式驗證，**勿憑記憶手查**）：
- `易學/02_六爻斷卦/以爻變解爻辭——之卦對照法.md` — 第四法＋程式驗證版對照表
- `易學/02_六爻斷卦/易經古法解卦——卦義拆卦與對卦.md` — 整卦層級三法

臨場快速換算：本卦第 k 爻翻轉得新上下卦即之卦，卦名用 `get_hexagram_name(lower, upper)` 查 `HEXAGRAMS` 表（key＝(外卦,內卦)）；結果建議與 wiki 驗證表抽對核對。

## Coin Results Reference

⚠️ 此表為**方法 A（文墨龍：正面字面＝陰、反面＝陽）**的語意；方法 B（台幣：正面＝陽）的記錄不可直接查此表（每爻會判反）。通用規則看「陽面個數」：0＝老陰×、1＝少陽、2＝少陰、3＝老陽○（金錢卦不計三枚順序；陽面多≠陽爻——少者定性，口訣「選少的那個」，勿用多數決直覺）。
| Result | 正/反（方法A語意） | Name | Symbol | Type |
|:------:|:-----:|:----:|:------:|:----:|
| 兩正一反 | 2:1 | 少陽 | — | Static Yang |
| 一正兩反 | 1:2 | 少陰 | -- | Static Yin |
| 三反 | 0:3 | 老陽 | ○ | Moving Yang → Yin |
| 三正 | 3:0 | 老陰 | × | Moving Yin → Yang |

**方法 B 換算表（台幣：正面＝陽）**：數「正」的個數——1正＝少陽、2正＝少陰、3正＝老陽○（動）、0正（三反）＝老陰×（動）。與上表每爻恰好相反（同一記錄兩法互為錯卦，例：同一搖卦記錄 A 得水山蹇→風地觀、B 得火澤睽→雷天大壯）。

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
4. 確認的最小單位是**陰陽映射本身**（哪一面算陽面），幣種只是載體——自訂約定有無限多組，起卦前講明並全程一致即合法
5. 例外免問：使用者直接以每枚硬幣的『陰/陽』回報結果時（如「陰陰陽，陰陽陰…」），映射已自含，免問流派——直接以陽面個數定性（0＝老陰×、1＝少陽、2＝少陰、3＝老陽○）

### 方法 A：文墨龍傳統古銅錢法
- 有年號的面（乾隆通寶、康熙通寶等）= 字面 = 正面 = **陰面**
- 背面（筆畫較少的面，滿文局名等）= 背 = **陽面**
- ⚠️ 直覺容易搞反：有字≠陽，在文墨龍系統中有年號=陰

### 方法 B：中華民國硬幣法（Brian 自定義）
- 正面（國父孫中山頭像＋中華民國年號面）= **陽面**
- 反面／背面（面額面：壹圓、伍圓等）= **陰面**
- ⚠️ 與文墨龍法正面陰陽定義**剛好相反**
- 詳見 Wiki：易學/01_六爻裝卦/硬幣起卦法.md

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
- 陰陽陰(☵) = 坎卦（初陰+中陽+上陰）
- 陽陰陽(☲) = 離卦
- 陰陰陽(☶) = 艮卦

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
| 五爻 | 3反面 | 老陽 | 變陰爻 |
| 上爻 | 3正面 | 老陰 | 變陽爻 |

- **本卦**：下卦=坤(地) + 上卦=兌(澤) = **澤地萃**（第45卦）
- **變卦**：五爻老陽變陰→上卦由兌變離(火)，下卦不變= **火地晉**（第35卦）

## Pitfalls

- 六爻 interpretation is complex; always do full 納甲 setup before concluding
- Ensure all 簡體 → 繁體 conversion when storing results in wiki
- 網路排盤軟體有兩種排列方向（由上往下 vs 由下往上），輸入時需留意
- scripts/liuyao_divine.py 三類裝卦 bug 已修復：①TRIGRAMS lines 曾誤用上→下序，非對稱卦會排成爻位顛倒的反卦；②get_xunwang 曾不管日干支永回甲子旬空戌亥；③najia 外卦曾誤取列表前3支，四五上爻地支六親全錯。已驗證：萃→晉、蹇→觀兩案例與傳統排盤一致
- 爻位式輸入的陽靜爻寫**單一 `-`**：解析是 `'--' in part` 子字串判定，`---` 會被靜默解析成陰靜爻（正反式輸入不受此坑影響）
- script 排出的納甲盤，引用前抽查二至三爻手推核對（TRIGRAM_DIZHI 列表＝內卦三支在前、外卦三支在後；六親以卦宮五行起）——排盤程式的靜默裝卦錯誤會讓動爻六親反掉、斷卦方向整體反轉
- 腳本只排**本卦**納甲，不輸出變卦爻支——動爻『化出』之支須自推：按**變卦卦象**取納甲同爻位地支（納甲依八卦不依宮：乾甲壬／坤乙癸／震庚／巽辛／坎戊／離己／艮丙／兌丁），再判進神/退神/化墓/回頭生剋（例：睽之大壯＝內乾外震，三爻丑化辰＝進神、上爻巳化戌＝火墓）
- 對照已驗證案例重跑腳本時，--coins 的每爻正/反個數照 Coin Results 表逐爻推導後再轉寫；輸出與預期不符先核對自己的輸入轉寫再懷疑程式——錯一爻會排出一個看似合理的完全不同卦，甚至動爻位置也對得上
- `--coins` 正反式的語意是『正』＝陰面、『反』＝陽面（方法A語意）。把使用者直接回報的『陰/陽』結果轉寫進腳本時必須**陰→正、陽→反**——照直覺『陽→正』會排出同一記錄的鏡像錯卦（兩法互錯例：蹇→觀 vs 睽→大壯）
- **起卦日／月建自動化（v4.2.0）**：不傳 `--day/--month` 時自動取今日干支＋節氣月建（cnlunar 八字月柱地支，節氣交界也正確）；自動失敗印 ⚠️ 警告並退回寫死預設「乙巳日/巳月」——**帶警告的盤六神/旬空/旺衰不可直接引用**。納甲六親／世應不受日辰影響，抽查時別被「六神看起來正確」的假象騙過
- **Brian 報的卦若不是當日卜的**（「上次卜的」「5月卜的」等），必須先確認**卜卦當天日期**再用 lunar_converter 取當日日柱＋月建重排——不可拿今天的日辰頂替：六神、旬空、旺衰、應期整組全錯、結論可完全反轉（連是否旬空都會反掉）；日辰不影響的只有卦象結構——六親、世應、動爻與本變卦卦義
- `lunar_converter.py` 在 **import 時**就會對缺 cnlunar 環境印訊息＋`sys.exit`（SystemExit 不被 `except Exception` 接住，呼叫方會被拖崩）——要 import 它的程式必須先 `import cnlunar` 驗存在。cnlunar 裝在 python-3.14.9 直譯器（`/home/glenn/.hermes/tools/python-3.14.9+20261021-linux-x64/bin/python3`）；多個 python-* 並存不可用 `head -1` 挑（3.14.7 沒裝）

- `references/hexagrams.md` 僅收錄**部分**卦（各宮本宮＋少數重卦）——解卦前先確認該卦條目存在；缺條目時以卦辭＋大象傳為主，輔以腳本 `get_hexagram_info` 的卦義，勿當成全部六十四卦都已收錄

### ⚠️ Common Misread Patterns

| Mistake | What happened | Why dangerous |
|---------|--------------|-------------|
| 正反正 ↔ 反正反 | Swapped two characters, 2:1 vs 1:2 | Changes yin↔yang for that line |
| 正反反 ↔ 反正正 | Swapped start/end, same 1:2 but different order | Less dangerous (same type) but still verify |

### ⚠️ Script Bug: `get_trigram_from_line`

The `build_hexagram()` function in `scripts/liuyao_divine.py` calls `get_trigram_from_line()` which is only defined as an alias for `get_trigram_from_lines()`. If the alias ever breaks or the function is removed, the outer trigram lookup will fail silently.

## Video Sources (影片學習來源)

三部 YouTube 教學影片的完整知識摘要見 `references/liuyao-video-sources.md`：
1. **文墨龍** — 銅錢起卦正確方法 (v1FBl9Unrds, 46K views)
2. **易谷** — 六爻知識架構篇：本卦、變卦和爻 (KeTv6CIRfzE, 34K views)
3. **曾仕強** — 如何卜卦？如何解卦？ (R7SCFbdpePc, 336K views)

Wiki 知識庫頁面：
- `易學/01_六爻裝卦/銅錢起卦法.md`
- `易學/02_六爻斷卦/易谷六爻知識架構.md`
- `易學/02_六爻斷卦/曾仕強卜卦解卦.md`
- `易學/02_六爻斷卦/易經古法解卦——卦義拆卦與對卦.md`
- `易學/02_六爻斷卦/以爻變解爻辭——之卦對照法.md`

## Related Skills

- `xiaoliuren-divination` — 小六壬卜卦（不同系統，觸發詞不同）
- `chinese-divination` — 已合併為本 skill，不再使用

## 案例歸檔與隱私（Brian 拍板）

- 個人事件卦例（轉職、財務、健康等真實人生決策）**主場＝Brian 的 wiki**：`易學/查詢/案例/`，frontmatter type=query＋`case-record` 標籤，建頁走建庫 SOP（區規範→索引/紀錄回寫→lint 0E0W→git）；references 只收去個人化骨架版（問者匿名、事件泛稱，範本 `liuyao-case-verified-job-change.md`）
- wiki 卦例命名慣例（2026-11-27 井之需案確立）：已實證對帳＝`六爻實證案例-<卦>問<主題>`、新卜未驗證＝`六爻卦例-<卦>問<主題>`（檔名忌括號等特殊字元；驗證後不改檔名，回頁補對帳表＋待驗證項勾選）。索引易學區總頁數口徑＝排除 admin 三頁＋原始資料 7 頁＋學習路徑，僅算核心＋查詢
- 本鏡像 repo 為公開——個人素材收進 skill/repo 前必須去個人化；有隱私疑慮的完整版留 wiki（解卦時掛載路徑讀得到，不因「我要參考」而收進 skill）
- 錯誤舊資料＝**勘誤公告保留原文**：頂部 Banner 標明錯在哪＋指向正確版，不刪原文；新舊案例檔以檔內交叉引用接起

GitHub mirror repo: `glennchen2207/liuyao-divination-rose`（公開）：
- 升版同步三處：SKILL.md frontmatter `version`、README（版本區＋`vX.Y.Z 更新內容`節）、HERMES_ROSE.md（歷程節）；`gh repo edit --description` 同步 repo 描述
- `.py` 以 LF 推送；commit 作者＝`glennchen2207 <glennchen2207@users.noreply.github.com>`（repo 既有慣例）
- push 後以 `gh api repos/glennchen2207/liuyao-divination-rose/contents/<path>` 讀回驗證版本號／新函式在位才算完成