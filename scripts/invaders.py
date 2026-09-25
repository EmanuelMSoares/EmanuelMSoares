#!/usr/bin/env python3
"""
Contribution Invaders
Transforma o gráfico de contribuições do GitHub numa fase de Space Invaders em SVG animado:
cada dia com contribuições vira um invasor, a nave atravessa o ano abatendo semana por semana
e o placar sobe até o total real de contribuições.

Uso:
  python3 scripts/invaders.py --user EmanuelMSoares --out dist/invaders.svg
  python3 scripts/invaders.py --demo --out preview.svg      # dados de exemplo

Com a variável GITHUB_TOKEN (caso do GitHub Actions) usa a API GraphQL.
Sem token, lê a página pública de contribuições.
Não precisa de nenhuma biblioteca externa.
"""
import argparse
import datetime as dt
import json
import os
import random
import re
import urllib.request

FONT_WOFF_B64 = "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"  # subset da fonte Tiny5 (SIL Open Font License)

MESES = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]

# ---------------------------------------------------------------- paleta
BG = "#140F24"
INK = "#F0E9FF"
MUTED = "#8B7FA8"
LILAC = "#D2A8FF"
GREEN = "#39D353"
FLOOR = "#2E2350"
EMPTY = "#261D42"
LEVEL_COLORS = {1: "#3D2C6B", 2: "#6242B5", 3: "#9A6BF2", 4: "#D8B9FF"}

# ---------------------------------------------------------------- sprites
INV_A = ["..X.....X..", "...X...X...", "..XXXXXXX..", ".XX.XXX.XX.",
         "XXXXXXXXXXX", "X.XXXXXXX.X", "X.X.....X.X", "...XX.XX..."]
INV_B = ["..X.....X..", "X..X...X..X", "X.XXXXXXX.X", "XXX.XXX.XXX",
         "XXXXXXXXXXX", ".XXXXXXXXX.", "..X.....X..", ".X.......X."]
CANNON = ["......X......", ".....XXX.....", ".....XXX.....", ".XXXXXXXXXXX.",
          "XXXXXXXXXXXXX", "XXXXXXXXXXXXX", "XXXXXXXXXXXXX", "XXXXXXXXXXXXX"]

# ---------------------------------------------------------------- geometria
W = 900
PITCH_X, PITCH_Y = 16, 15
INV_PX = 1.25
CANNON_PX = 2.5
GRID_TOP = 82
SHIP_TOP = 232
H = 282

# ---------------------------------------------------------------- tempo (segundos)
INTRO = 0.8        # nave parada antes de começar
STEP = 0.17        # tempo para passar de uma semana à outra
POP = 0.18         # duração da explosão
MSG_DELAY = 0.6    # pausa entre o último tiro e a mensagem
MSG_TIME = 3.0     # tempo da mensagem de fase concluída
WAVE = 0.015       # atraso entre colunas no renascimento
SHIP_BACK = 1.2    # tempo da nave voltando ao começo
TAIL = 0.6


# ================================================================ dados
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2,
          "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def fetch_graphql(user, token):
    query = """query($login: String!) { user(login: $login) { contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays {
        date weekday contributionCount contributionLevel } } } } } }"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "contribution-invaders"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[{"date": dt.date.fromisoformat(d["date"]), "weekday": d["weekday"],
               "count": d["contributionCount"], "level": LEVELS[d["contributionLevel"]]}
              for d in w["contributionDays"]] for w in cal["weeks"]]
    return weeks, cal["totalContributions"]


def fetch_html(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode()
    cells = re.findall(r'data-date="([^"]+)" id="contribution-day-component-(\d+)-(\d+)" '
                       r'data-level="(\d)"', html)
    tips = dict(re.findall(r'for="contribution-day-component-(\d+-\d+)"[^>]*>([^<]*)</tool-tip>', html))
    if not cells:
        raise RuntimeError("não encontrei o calendário na página pública")
    by_week, total = {}, 0
    for date, wd, wk, lv in cells:
        m = re.match(r"(\d[\d,]*) contribution", tips.get(f"{wd}-{wk}", ""))
        count = int(m.group(1).replace(",", "")) if m else 0
        total += count
        by_week.setdefault(int(wk), []).append({"date": dt.date.fromisoformat(date),
                                                "weekday": int(wd), "count": count, "level": int(lv)})
    weeks = [sorted(by_week[k], key=lambda d: d["weekday"]) for k in sorted(by_week)]
    return weeks, total


def demo_data(seed=7, target=1374):
    """Um ano fictício que vai ficando mais ativo com o tempo."""
    rnd = random.Random(seed)
    today = dt.date.today()
    start = today - dt.timedelta(days=(today.weekday() + 1) % 7 + 52 * 7)
    days, d = [], start
    while d <= today:
        progress = (d - start).days / (today - start).days
        weekend = d.weekday() >= 5
        p_active = (0.25 + 0.65 * progress) * (0.35 if weekend else 1)
        count = 0
        if rnd.random() < p_active:
            count = max(1, int(rnd.expovariate(1 / (2 + 9 * progress))))
        days.append([d, count])
        d += dt.timedelta(days=1)
    raw = sum(c for _, c in days) or 1
    for day in days:
        if day[1]:
            day[1] = max(1, round(day[1] * target / raw))
    nonzero = sorted(c for _, c in days if c)
    q = [nonzero[int(len(nonzero) * f)] for f in (0.25, 0.5, 0.75)]
    weeks = []
    for date, count in days:
        level = 0 if not count else 1 + sum(count > t for t in q)
        wd = (date.weekday() + 1) % 7
        if wd == 0 or not weeks:
            weeks.append([])
        weeks[-1].append({"date": date, "weekday": wd, "count": count, "level": level})
    return weeks, sum(c for _, c in days)


# ================================================================ helpers de SVG
def pixel_path(rows, px, ox=0.0, oy=0.0):
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == "X":
                s = c
                while c < len(row) and row[c] == "X":
                    c += 1
                w = (c - s) * px
                out.append(f"M{ox + s * px:g} {oy + r * px:g}h{w:g}v{px:g}h{-w:g}z")
            else:
                c += 1
    return "".join(out)


def pct(t, total):
    return f"{max(0.0, min(100.0, t / total * 100)):.3f}%"


def windows_keyframes(name, windows, total, eps=0.01):
    """Keyframes de opacidade com cortes secos: visível apenas dentro das janelas (seg)."""
    stops = [(0.0, 0)]
    for a, b in windows:
        stops += [(max(a - eps, 0.0), 0), (a, 1), (b - eps, 1), (b, 0)]
    stops.append((total, 0))
    stops.sort()
    body = "".join(f"{pct(t, total)}{{opacity:{v}}}" for t, v in stops)
    return f"@keyframes {name}{{{body}}}"


def fmt_br(n):
    return f"{n:,}".replace(",", ".")


# ================================================================ render
def render(weeks, total):
    n = len(weeks)
    grid_w = n * PITCH_X
    left = (W - grid_w) / 2
    inv_w, inv_h = 11 * INV_PX, 8 * INV_PX
    off_x, off_y = (PITCH_X - inv_w) / 2, (PITCH_Y - inv_h) / 2
    col_center = [left + i * PITCH_X + PITCH_X / 2 for i in range(n)]

    fire = [INTRO + i * STEP for i in range(n)]
    last_fire = fire[-1]
    msg_start = last_fire + MSG_DELAY
    msg_end = msg_start + MSG_TIME
    respawn = msg_end
    T = respawn + SHIP_BACK + TAIL

    active_cols = [i for i, w in enumerate(weeks) if any(d["count"] > 0 for d in w)]
    col_sum = [sum(d["count"] for d in w) for w in weeks]

    css, body = [], []

    # --- estilos fixos
    css.append(f'@font-face{{font-family:"Pixel";src:url(data:font/woff;base64,{FONT_WOFF_B64}) format("woff")}}')
    css.append('text{font-family:"Pixel",monospace}')
    css.append(".fa{animation:fa 1s linear infinite}.fb{opacity:0;animation:fb 1s linear infinite}")
    css.append("@keyframes fa{0%,49.9%{opacity:1}50%,100%{opacity:0}}@keyframes fb{0%,49.9%{opacity:0}50%,100%{opacity:1}}")
    css.append(f".cell{{fill:var(--c);transform-box:fill-box;transform-origin:center;"
               f"animation-duration:{T:.2f}s;animation-iteration-count:infinite;animation-timing-function:linear}}")
    for lv, color in LEVEL_COLORS.items():
        css.append(f".l{lv}{{--c:{color}}}")
    for r in range(7):
        css.append(f".r{r}{{animation-delay:{r * 0.02:.2f}s}}")

    # --- invasores: uma animação por coluna (explode no tiro, renasce em onda)
    for i in active_cols:
        f, r = fire[i], respawn + i * WAVE
        css.append(
            f"@keyframes c{i}{{"
            f"0%,{pct(f, T)}{{opacity:1;transform:scale(1);fill:var(--c)}}"
            f"{pct(f + 0.05, T)}{{opacity:1;transform:scale(1.4);fill:#FFFFFF}}"
            f"{pct(f + POP, T)}{{opacity:0;transform:scale(2.2);fill:#FFFFFF}}"
            f"{pct(r, T)}{{opacity:0;transform:scale(.2);fill:var(--c)}}"
            f"{pct(r + 0.35, T)},100%{{opacity:1;transform:scale(1);fill:var(--c)}}}}"
            f".k{i}{{animation-name:c{i}}}")

    # --- laser: mesma animação para todos, deslocada no tempo
    beam_on = 0.12
    css.append(f".beam{{opacity:0;animation:beam {T:.2f}s linear infinite}}"
               f"@keyframes beam{{0%,{pct(beam_on, T)}{{opacity:1}}{pct(beam_on + 0.01, T)},100%{{opacity:0}}}}")

    # --- nave
    dx = col_center[-1] - col_center[0]
    css.append(f".ship{{animation:ship {T:.2f}s linear infinite}}"
               f"@keyframes ship{{0%,{pct(INTRO, T)}{{transform:translateX(0)}}"
               f"{pct(last_fire, T)},{pct(respawn, T)}{{transform:translateX({dx:g}px)}}"
               f"{pct(respawn + SHIP_BACK, T)},100%{{transform:translateX(0)}}}}")

    # --- mensagem de fase concluída
    css.append(windows_keyframes("msg", [(msg_start, msg_end)], T))
    css.append(f".msg{{opacity:0;animation:msg {T:.2f}s linear infinite}}")

    # --- placar: um texto por valor, cada um visível na sua janela
    score_steps = [(0, [(0.0, fire[active_cols[0]] if active_cols else respawn), (respawn, T)])]
    running = 0
    for idx, i in enumerate(active_cols):
        running += col_sum[i]
        end = fire[active_cols[idx + 1]] if idx + 1 < len(active_cols) else respawn
        score_steps.append((running, [(fire[i], end)]))
    for k, (_, win) in enumerate(score_steps):
        css.append(windows_keyframes(f"s{k}", win, T))
        css.append(f".s{k}{{opacity:0;animation:s{k} {T:.2f}s linear infinite}}")

    css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}.rm{opacity:1!important}}")

    # ================= corpo
    body.append(f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>')

    # HUD
    body.append(f'<text x="{left:g}" y="42" font-size="16" fill="{MUTED}">SCORE</text>')
    last_k = len(score_steps) - 1
    for k, (value, _) in enumerate(score_steps):
        extra = " rm" if k == last_k else ""
        body.append(f'<text class="s{k}{extra}" x="{left + 62:g}" y="42" font-size="16" fill="{INK}">{value:05d}</text>')
    body.append(f'<text x="{left + grid_w:g}" y="42" font-size="16" fill="{MUTED}" text-anchor="end">ÚLTIMOS 12 MESES</text>')

    # meses
    last_label, prev_month = -3, None
    for i, w in enumerate(weeks):
        month = w[0]["date"].month
        if month != prev_month and i > 0 and i - last_label >= 3 and i < n - 2:
            body.append(f'<text x="{left + i * PITCH_X:g}" y="{GRID_TOP - 9}" font-size="11" fill="{MUTED}">'
                        f'{MESES[month - 1]}</text>')
            last_label = i
        prev_month = month

    # sprite reutilizável
    body.append(f'<defs><g id="inv"><path class="fa" d="{pixel_path(INV_A, INV_PX)}"/>'
                f'<path class="fb" d="{pixel_path(INV_B, INV_PX)}"/></g></defs>')

    # grade
    empty_d = []
    for i, w in enumerate(weeks):
        for d in w:
            x = left + i * PITCH_X
            y = GRID_TOP + d["weekday"] * PITCH_Y
            cx, cy = x + PITCH_X / 2 - 2, y + PITCH_Y / 2 - 2
            empty_d.append(f"M{cx:g} {cy:g}h4v4h-4z")  # fica visível quando o invasor é abatido
            if d["count"] > 0:
                body.append(f'<g transform="translate({x + off_x:g} {y + off_y:g})">'
                            f'<use href="#inv" class="cell k{i} l{d["level"]} r{d["weekday"]}"/></g>')
    body.insert(1, f'<path d="{"".join(empty_d)}" fill="{EMPTY}"/>')

    # lasers
    for i in active_cols:
        top_wd = min(d["weekday"] for d in weeks[i] if d["count"] > 0)
        y_top = GRID_TOP + top_wd * PITCH_Y + off_y
        h = SHIP_TOP - y_top
        cx = col_center[i]
        body.append(f'<g class="beam" style="animation-delay:{fire[i]:.3f}s">'
                    f'<rect x="{cx - 3.5:g}" y="{y_top:g}" width="7" height="{h:g}" fill="{GREEN}" opacity=".25"/>'
                    f'<rect x="{cx - 1.5:g}" y="{y_top:g}" width="3" height="{h:g}" fill="{GREEN}"/></g>')

    # nave e chão
    ship_x = col_center[0] - 13 * CANNON_PX / 2
    body.append(f'<g class="ship"><path d="{pixel_path(CANNON, CANNON_PX, ship_x, SHIP_TOP)}" fill="{GREEN}"/></g>')
    body.append(f'<rect x="{left:g}" y="{H - 22}" width="{grid_w:g}" height="2" fill="{FLOOR}"/>')

    # mensagem
    mid_y = GRID_TOP + 7 * PITCH_Y / 2
    msg_sub = (f"{fmt_br(total)} CONTRIBUIÇÕES NO ÚLTIMO ANO" if total
               else "NENHUMA CONTRIBUIÇÃO AINDA")
    box_w, box_h = 520, 92
    body.append(f'<g class="msg"><rect x="{(W - box_w) / 2:g}" y="{mid_y - box_h / 2 - 8:g}" width="{box_w}" '
                f'height="{box_h}" rx="6" fill="{BG}" stroke="{FLOOR}" stroke-width="2"/>'
                f'<text x="{W / 2:g}" y="{mid_y - 4:g}" font-size="30" fill="{LILAC}" '
                f'text-anchor="middle">FASE CONCLUÍDA</text>'
                f'<text x="{W / 2:g}" y="{mid_y + 24:g}" font-size="15" fill="{INK}" '
                f'text-anchor="middle">{msg_sub}</text></g>')

    desc = (f"Gráfico de contribuições do GitHub como uma fase de Space Invaders: "
            f"{fmt_br(total)} contribuições no último ano.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-labelledby="t d"><title id="t">Contribution Invaders</title>'
            f'<desc id="d">{desc}</desc><style>{"".join(css)}</style>{"".join(body)}</svg>')


def main():
    ap = argparse.ArgumentParser(description="Gera o SVG do Contribution Invaders")
    ap.add_argument("--user", help="usuário do GitHub")
    ap.add_argument("--out", default="dist/invaders.svg")
    ap.add_argument("--demo", action="store_true", help="usa dados de exemplo")
    args = ap.parse_args()

    if args.demo:
        weeks, total = demo_data()
    elif not args.user:
        ap.error("informe --user ou --demo")
    else:
        weeks = None
        if os.environ.get("GITHUB_TOKEN"):
            try:
                weeks, total = fetch_graphql(args.user, os.environ["GITHUB_TOKEN"])
            except Exception as err:  # cai para a página pública
                print(f"GraphQL falhou ({err}); usando a página pública")
        if weeks is None:
            weeks, total = fetch_html(args.user)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(render(weeks, total))
    print(f"{args.out}: {len(weeks)} semanas, {total} contribuições")


if __name__ == "__main__":
    main()
