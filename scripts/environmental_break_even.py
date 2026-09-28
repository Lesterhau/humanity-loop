#!/usr/bin/env python3
"""Humanity Loop environmental break-even calculator.

Decision-support simulation. Carbon, water, and other resource dimensions remain
separate; this module does not manufacture a single "green score".
"""
from __future__ import annotations
import argparse, json, math, random, statistics
from pathlib import Path

HORIZONS = {"90d": 90, "1y": 365, "3y": 1095, "10y": 3650}

def triangular(rng, spec):
    if isinstance(spec, (int, float)):
        return float(spec)
    return rng.triangular(float(spec["low"]), float(spec["high"]), float(spec.get("mode", spec.get("mid", (spec["low"]+spec["high"])/2))))

def simulate(cfg, n=10000, seed=1, scale=1.0):
    rng=random.Random(seed)
    paybacks=[]
    carbon_costs=[]
    carbon_benefits=[]
    water_costs=[]
    for _ in range(n):
        daily_kwh=triangular(rng,cfg["daily_kwh"])*scale
        kg_per_kwh=triangular(rng,cfg["kg_co2e_per_kwh"])
        liters_per_kwh=triangular(rng,cfg["liters_water_per_kwh"])
        daily_gross=triangular(rng,cfg["daily_gross_carbon_benefit_kg"])*scale**triangular(rng,cfg.get("benefit_scale_elasticity",1.0))
        discount=1.0
        for k in ("attribution","evidence_quality","additionality","durability"):
            discount*=triangular(rng,cfg[k])
        daily_benefit=daily_gross*discount
        daily_cost=daily_kwh*kg_per_kwh
        carbon_costs.append(daily_cost*365)
        carbon_benefits.append(daily_benefit*365)
        water_costs.append(daily_kwh*liters_per_kwh*365)
        if daily_benefit > daily_cost:
            initial_debt=triangular(rng,cfg.get("initial_carbon_debt_kg",0.0))
            paybacks.append(initial_debt/(daily_benefit-daily_cost))
        else:
            paybacks.append(math.inf)
    return {
      "scale":scale,
      "annual_carbon_cost_kg":{"p10":q(carbon_costs,.1),"median":q(carbon_costs,.5),"p90":q(carbon_costs,.9)},
      "annual_attributable_carbon_benefit_kg":{"p10":q(carbon_benefits,.1),"median":q(carbon_benefits,.5),"p90":q(carbon_benefits,.9)},
      "annual_water_use_liters":{"p10":q(water_costs,.1),"median":q(water_costs,.5),"p90":q(water_costs,.9)},
      "payback_probability":{h:sum(x<=d for x in paybacks)/n for h,d in HORIZONS.items()},
      "never_payback_probability":sum(math.isinf(x) for x in paybacks)/n,
      "median_payback_days": finite_median(paybacks),
    }

def q(xs,p):
    ys=sorted(xs); return ys[min(len(ys)-1,max(0,int(p*(len(ys)-1))))]

def finite_median(xs):
    ys=[x for x in xs if math.isfinite(x)]
    return statistics.median(ys) if ys else None

def recommendation(base, expanded):
    b=base["payback_probability"]["1y"]; e=expanded["payback_probability"]["1y"]
    if e >= max(.6,b+.05): return "SCALE"
    if e < b-.05: return "REALLOCATE"
    return "HOLD"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("config",type=Path)
    ap.add_argument("--samples",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=1)
    args=ap.parse_args()
    cfg=json.loads(args.config.read_text())
    runs={str(s):simulate(cfg,args.samples,args.seed,s) for s in (1.0,1.1,1.5,2.0)}
    base=runs["1.0"]
    for s in ("1.1","1.5","2.0"):
        runs[s]["recommendation_vs_base"]=recommendation(base,runs[s])
    print(json.dumps({"model":"HL environmental break-even v0.1","runs":runs},indent=2,allow_nan=False))

if __name__=="__main__": main()
