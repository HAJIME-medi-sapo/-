# -*- coding: utf-8 -*-
"""
スルガ銀行35年案件（木造準耐火）収支・出口モデル
使い方: 下の【入力】を実数値に差し替えて `python3 不動産投資_収支モデル.py`
"""

# ========== 【入力】ここだけ差し替える ==========
TOCHI        = 59_000_000    # 土地価格（推定。契約書の按分に差し替え）
KENMONO      = 99_900_000    # 建物価格（LINE記載）
JIKO_RITSU   = 0.10          # 自己資金割合
RATE         = 0.0255        # 借入金利
YEARS        = 35            # 借入期間
HYOMEN       = 0.080         # 満室想定表面利回り（未入手のため仮）
SHOHIYO      = 9_530_000     # 諸費用（登免税・司法書士・仲手・保険・印紙等）
KUSHITSU     = 0.05          # 空室・滞納損
KANRI        = 0.05          # 管理委託料
SHURIN       = 0.03          # 修繕・原状回復・共用費
HOKEN        = 150_000       # 火災・地震保険（年）
KOTEI_RITSU  = 0.007         # 固都税（物件価格に対する概算率）
ZEIRITSU     = 0.43          # 個人の限界税率（所得税＋住民税）
JOTO_ZEI     = 0.20315       # 長期譲渡所得税率（5年超）
RENT_DECAY   = 0.010         # 賃料下落率（年）
SETSUBI_RATIO= 0.00          # 建物附属設備の分離割合（内訳書入手後に0.15等へ）
KOSU         = 15            # 戸数（15戸計画）
KOUJI_UP     = 0.00          # 工事費の増額率（請負金額の上振れ想定）
TOCHI_SENKO_M= 0             # 土地先行融資の月数（0なら土地建物一括実行）
# ===============================================

KAKAKU = TOCHI + KENMONO
JIKO   = round(KAKAKU * JIKO_RITSU)
LOAN   = KAKAKU - JIKO
N      = YEARS * 12
KOTEI  = KAKAKU * KOTEI_RITSU
TOUKA  = JIKO + SHOHIYO      # 投下自己資金


def pmt(p, annual, n):
    r = annual / 12
    return p * r / (1 - (1 + r) ** (-n))


def schedule(p, annual, n):
    r = annual / 12
    mm = pmt(p, annual, n)
    bal, out = p, []
    for _ in range(n):
        it = bal * r
        pr = mm - it
        bal -= pr
        out.append((it, pr, max(bal, 0.0)))
    return mm, out


def year_sum(rows, y):
    s = rows[(y - 1) * 12:y * 12]
    return sum(x[0] for x in s), sum(x[1] for x in s), s[-1][2]


def dep_of(year):
    """年次の減価償却費。木造住宅用22年(0.046)、附属設備15年(0.067)。"""
    if year > 22:
        return 0.0
    setsubi = KENMONO * SETSUBI_RATIO
    honta = KENMONO - setsubi
    d = honta * 0.046
    if SETSUBI_RATIO > 0 and year <= 15:
        d += setsubi * 0.067
    return d


def noi_of(gross):
    opex = gross * (KANRI + SHURIN) + KOTEI + HOKEN
    return gross * (1 - KUSHITSU) - opex


def taxable_income(noi, interest, dep):
    """不動産所得。赤字時は土地取得に係る負債利子を損益通算対象から除外(措法41の4)。"""
    sho = noi - interest - dep
    if sho >= 0:
        return sho
    land_int = interest * TOCHI / KAKAKU
    return -max(-sho - min(-sho, land_int), 0.0)


def bisect(f, lo, hi, it=200):
    for _ in range(it):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


M, ROWS = schedule(LOAN, RATE, N)
ANN = M * 12


def section(t):
    print("\n" + "=" * 74 + f"\n{t}\n" + "=" * 74)


section("1. 前提")
print(f"  物件価格 {KAKAKU:>13,} 円 (土地 {TOCHI:,} / 建物 {KENMONO:,} = {KENMONO/KAKAKU*100:.1f}%)")
print(f"  自己資金 {JIKO:>13,} 円 + 諸費用 {SHOHIYO:,} 円 → 投下自己資金 {TOUKA:,} 円")
print(f"  借入     {LOAN:>13,} 円 / {YEARS}年 / {RATE*100:.2f}%")
print(f"  月返済   {M:>13,.0f} 円   年返済 {ANN:,.0f} 円")
print(f"  総返済   {M*N:>13,.0f} 円   うち利息 {M*N-LOAN:,.0f} 円 (借入の{(M*N-LOAN)/LOAN*100:.1f}%)")
print(f"  初年度償却 {dep_of(1):>11,.0f} 円")

section("1b. 新築15戸企画としての追加論点")
print(f"  戸数 {KOSU} 戸 / 工事費増額率 {KOUJI_UP*100:.1f}% / 土地先行融資 {TOCHI_SENKO_M} ヶ月")
print(f"\n  【戸あたり必要賃料】")
print(f"{'水準':<14}{'満室年収':>13}{'月/戸':>11}")
_be = bisect(lambda g: noi_of(KAKAKU*g)-ANN, 0.01, 0.30)
_d13 = bisect(lambda g: noi_of(KAKAKU*g)-ANN*1.3, 0.01, 0.30)
for lab, g in [("税引前CF=0", _be), ("DSCR1.3", _d13), ("表面7.0%", 0.070),
               ("表面8.0%", 0.080), ("表面9.0%", 0.090)]:
    gross = KAKAKU * g
    print(f"{lab:<12}{gross:>13,.0f}{gross/KOSU/12:>11,.0f}")
if KOUJI_UP > 0:
    _up = KENMONO * KOUJI_UP
    print(f"\n  工事費増額 +{KOUJI_UP*100:.1f}% = +{_up:,.0f} 円 → 投下自己資金 {TOUKA:,} 円に対し {_up/TOUKA*100:.1f}%")
if TOCHI_SENKO_M > 0:
    print(f"  土地先行 {TOCHI_SENKO_M}ヶ月の金利負担（収入ゼロ期間）: {TOCHI*RATE*TOCHI_SENKO_M/12:,.0f} 円")

section("2. 表面利回り別 保有中キャッシュフロー（1年目・税引前）")
print(f"{'表面':>6}{'満室年収':>13}{'NOI':>13}{'返済':>13}{'税引前CF':>13}{'DSCR':>7}{'CCR':>8}")
for g in [0.065, 0.070, 0.075, 0.080, 0.085, 0.090]:
    gross = KAKAKU * g
    noi = noi_of(gross)
    print(f"{g*100:>5.1f}%{gross:>13,.0f}{noi:>13,.0f}{ANN:>13,.0f}{noi-ANN:>13,.0f}"
          f"{noi/ANN:>7.2f}{(noi-ANN)/TOUKA*100:>7.1f}%")
print(f"\n  税引前CF=0 → 表面 {bisect(lambda g: noi_of(KAKAKU*g)-ANN, 0.01, 0.30)*100:.2f}%")
print(f"  DSCR1.3   → 表面 {bisect(lambda g: noi_of(KAKAKU*g)-ANN*1.3, 0.01, 0.30)*100:.2f}%")

section(f"3. 税引後キャッシュフロー（1年目・限界税率{ZEIRITSU*100:.0f}%）")
it1 = year_sum(ROWS, 1)[0]
print(f"{'表面':>6}{'不動産所得':>14}{'税額':>13}{'税引前CF':>13}{'税引後CF':>13}{'月平均':>11}")
for g in [0.070, 0.075, 0.080, 0.085]:
    noi = noi_of(KAKAKU * g)
    tax = taxable_income(noi, it1, dep_of(1)) * ZEIRITSU
    print(f"{g*100:>5.1f}%{noi-it1-dep_of(1):>14,.0f}{-tax:>13,.0f}{noi-ANN:>13,.0f}"
          f"{noi-ANN-tax:>13,.0f}{(noi-ANN-tax)/12:>11,.0f}")

section("4. 金利感応度（NOI固定・変動金利の場合）")
noi_base = noi_of(KAKAKU * HYOMEN)
for r2 in [RATE, RATE + 0.005, RATE + 0.010, RATE + 0.015, RATE + 0.020]:
    m2 = pmt(LOAN, r2, N)
    print(f"  金利 {r2*100:>5.2f}%  月返済 {m2:>10,.0f} (+{m2-M:>8,.0f})  税引前CF {noi_base-m2*12:>12,.0f}  DSCR {noi_base/(m2*12):.2f}")
print(f"  税引前CF=0 になる金利: {bisect(lambda r2: noi_base-pmt(LOAN,r2,N)*12, 0.001, 0.15)*100:.2f}%")

section("5. デッドクロスと年次推移")
print(f"{'年':>4}{'支払利息':>14}{'元金返済':>14}{'年末残債':>16}{'償却費':>14}")
for y in [1, 5, 10, 15, 20, 22, 23, 25, 30, 35]:
    i, p, b = year_sum(ROWS, y)
    print(f"{y:>4}{i:>14,.0f}{p:>14,.0f}{b:>16,.0f}{dep_of(y):>14,.0f}")
for y in range(1, YEARS + 1):
    if year_sum(ROWS, y)[1] > dep_of(y):
        print(f"  → デッドクロス: {y}年目")
        break

section("6. 出口シミュレーション")
print(f"  新築時表面 {HYOMEN*100:.1f}% / 賃料下落 年{RENT_DECAY*100:.1f}% / 譲渡費用3% / 譲渡税 {JOTO_ZEI*100:.3f}%")
for hold in [7, 10, 15]:
    bal = ROWS[hold * 12 - 1][2]
    boka = TOCHI + max(KENMONO - sum(dep_of(y) for y in range(1, hold + 1)), 0)
    cum = 0.0
    for y in range(1, hold + 1):
        i = year_sum(ROWS, y)[0]
        noi = noi_of(KAKAKU * HYOMEN * (1 - RENT_DECAY) ** (y - 1))
        cum += (noi - ANN) - taxable_income(noi, i, dep_of(y)) * ZEIRITSU
    gross = KAKAKU * HYOMEN * (1 - RENT_DECAY) ** hold
    print(f"\n── 保有{hold}年 ── 残債 {bal:,.0f} / 簿価 {boka:,.0f} / 累積税引後CF {cum:,.0f}")
    print(f"{'売却表面':>9}{'売却価格':>14}{'譲渡税':>12}{'売却手取り':>14}{'通算総利益':>14}{'年平均':>12}")
    for cap in [0.080, 0.085, 0.090, 0.095, 0.100]:
        price = gross / cap
        fee = price * 0.03
        tax = max(price - fee - boka, 0) * JOTO_ZEI
        net = price - fee - bal - tax
        total = net + cum - TOUKA
        print(f"{cap*100:>8.1f}%{price:>14,.0f}{tax:>12,.0f}{net:>14,.0f}{total:>14,.0f}{total/hold:>12,.0f}")

section("7. 建物価格按分・附属設備分離の比較（保有10年）")
print(f"{'ケース':<30}{'建物':>13}{'比率':>7}{'10年償却':>13}{'節税累計':>12}{'譲渡税増':>11}{'正味':>12}")


def alloc(ken, ratio, label, hold=10):
    setsubi, honta = ken * ratio, ken * (1 - ratio)
    cum = sum(honta * 0.046 + (setsubi * 0.067 if y <= 15 else 0) for y in range(1, hold + 1))
    saved, gtax = cum * ZEIRITSU, cum * JOTO_ZEI
    print(f"{label:<28}{ken:>13,}{ken/KAKAKU*100:>6.1f}%{cum:>13,.0f}{saved:>12,.0f}{gtax:>11,.0f}{saved-gtax:>12,.0f}")
    return saved - gtax


base = alloc(KENMONO, 0.00, "A 現状")
for ken, ratio, lab in [(KENMONO, 0.15, "B 現状＋附属設備15%分離"),
                        (120_000_000, 0.00, "C 建物1.2億へ交渉"),
                        (120_000_000, 0.15, "D C＋附属設備15%分離")]:
    print(f"   ↑ Aとの差 {alloc(ken, ratio, lab)-base:+,.0f} 円")

print("\n  ※減価償却の増加は簿価を下げ売却時の譲渡益を同額増やす。実質の利得は")
print(f"    限界税率{ZEIRITSU*100:.0f}%と譲渡税{JOTO_ZEI*100:.3f}%の差分のみ（税率アービトラージ）。")
print("  ※売主が課税事業者の場合、建物価格の引き上げは売主の納税消費税を増やす＝実質値引き要求。")
