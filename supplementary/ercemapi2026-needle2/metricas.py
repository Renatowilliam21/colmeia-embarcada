import json, re, csv, statistics as st, math
from pathlib import Path

RAW = Path("resultados_esp32/20261025T164514Z_ESP32S3/raw_results.jsonl")
rx_pre = re.compile(r"EVT prefill tokens=(\d+) ms=(\d+) tps=([\d.]+)")
rx_done = re.compile(r"EVT done tokens=(\d+) ms=(\d+) tps=([\d.]+)")
rx_conf = re.compile(r"CONF ([\d.]+)")
rx_mem = re.compile(r"EVT memory phase=(\w+) psram_free=(\d+) internal_free=(\d+) "
                    r"psram_min_free=(\d+) internal_min_free=(\d+)")

def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)

rows, bad_name = [], []
for line in RAW.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    s = "\n".join(r["serial_lines"])
    pre, done, conf = rx_pre.search(s), rx_done.search(s), rx_conf.search(s)
    mem = {m.group(1): m.groups()[1:] for m in rx_mem.finditer(s)}
    if '"name"' not in r.get("model_output", ""):
        bad_name.append(r["case_id"])
    pre_ms = int(pre.group(2)) if pre else None
    gen_ms = int(done.group(2)) if done else None
    rows.append(dict(
        case_id=r["case_id"], categoria=r["category"], prompt=r["prompt"],
        conf=float(conf.group(1)) if conf else None,
        prefill_ms=pre_ms, gen_ms=gen_ms,
        tokens=int(done.group(1)) if done else None,
        tps=float(done.group(3)) if done else None,
        wall_ms=r["elapsed_wall_ms"],
        overhead_ms=(r["elapsed_wall_ms"] - pre_ms - gen_ms) if pre and done else None,
        psram_before=mem.get("before", [None])[0], psram_after=mem.get("after", [None])[0],
        psram_min_after=mem.get("after", [None] * 4)[2],
        internal_min_after=mem.get("after", [None] * 4)[3],
        chamadas=json.dumps(r.get("parsed_calls"), ensure_ascii=False)))

with open("metricas_por_caso.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

def resumo(nome, k):
    v = [x[k] for x in rows if x[k] is not None]
    print(f"{nome}: n={len(v)} media={st.mean(v):.2f} dp={st.pstdev(v):.2f} "
          f"mediana={st.median(v):.2f} min={min(v):.2f} max={max(v):.2f}")

for nome, k in [("wall_ms", "wall_ms"), ("prefill_ms", "prefill_ms"), ("gen_ms", "gen_ms"),
                ("overhead_ms", "overhead_ms"), ("tokens", "tokens"), ("tps", "tps"), ("conf", "conf")]:
    resumo(nome, k)
pm = [int(x["psram_min_after"]) for x in rows if x["psram_min_after"]]
im = [int(x["internal_min_after"]) for x in rows if x["internal_min_after"]]
print("PSRAM min livre (bytes):", min(pm), "| interna min livre:", min(im))
dif = [int(x["psram_after"]) - int(x["psram_before"]) for x in rows if x["psram_before"] and x["psram_after"]]
print("variacao PSRAM antes/depois: min", min(dif), "max", max(dif))
print("casos com model_output sem a chave name:", bad_name)
for k, n in [(13, 36), (14, 36), (13, 33), (14, 33)]:
    lo, hi = wilson(k, n); print(f"Wilson {k}/{n}: {lo:.1f}% a {hi:.1f}%")
