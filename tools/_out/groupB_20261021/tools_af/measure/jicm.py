# male 37deg JIC end extractor (SIZE-40, 2026-10-01): plane section through the part axis, the JIC end expressed in the generator's
# JIC chain (gen_straight2.JIC: TM thread major, SL seat length, CD cone dia, LL land length, TZ thread zone incl. the 45deg thread
# chamfer, RL relief length; 60deg ramp between thread major and relief).
# Validated on the Brennan 2404-32-16 STEP: returns the 2403 -32 chain (templates/DesignTable_2403_SW2.xlsx) exactly; used for the
# -40 chain (JIC_MEAS_40) on the Brennan 2404-40-32 STEP.
#   python tools/measure/jicm.py <step> [axis 0|1|2] [sign +1|-1] [plane normal 0|1|2]
# The JIC tip must lie on the positive leg coordinate a = sign * <axis coordinate>, the body (hex face) at a ~ 0.
import sys, math, json
from prof import leg_edges

TOL = 2e-4


def lines(p, axis=0, sign=-1, pn=2):
    out = []
    for kind, P in leg_edges(p, axis, sign, pn):
        if kind != 'L':
            continue
        (a1, r1), (a2, r2) = P[0], P[-1]
        if a1 > a2:
            a1, r1, a2, r2 = a2, r2, a1, r1
        out.append(dict(a1=a1, r1=r1, a2=a2, r2=r2, ang=math.degrees(math.atan2(abs(r2 - r1), abs(a2 - a1)))))
    return out


def chain(p, axis=0, sign=-1, pn=2):
    L = [l for l in lines(p, axis, sign, pn) if l['a2'] > 1e-6 and min(l['r1'], l['r2']) > 0.05]
    tip = max(l['a2'] for l in L)
    seat = [l for l in L if abs(l['ang'] - 37) < 0.2 and abs(l['a2'] - tip) < TOL]
    assert len(seat) == 1, ('37deg seat at the tip', seat)
    s = seat[0]; rT, rC = min(s['r1'], s['r2']), max(s['r1'], s['r2']); a_seat = s['a1']
    land = [l for l in L if abs(l['ang']) < 0.05 and abs(l['r1'] - rC) < TOL and abs(l['a2'] - a_seat) < TOL]
    assert len(land) == 1, ('land at the cone dia', land)
    a_land = land[0]['a1']
    flats = [l for l in L if abs(l['ang']) < 0.05 and l['a1'] > -TOL and l['a2'] < a_land + TOL]
    rM = max(l['r1'] for l in flats)
    ramp = [l for l in L if abs(l['ang'] - 60) < 0.2 and abs(max(l['r1'], l['r2']) - rM) < TOL]
    assert len(ramp) == 1, ('60deg ramp from the thread major', ramp)
    a_out, a_in = ramp[0]['a2'], ramp[0]['a1']
    relief = [l for l in L if abs(l['ang']) < 0.05 and abs(l['r1'] - rC) < 2e-3 and abs(l['a2'] - a_in) < TOL]
    assert len(relief) == 1, ('relief at the cone dia', relief)
    return dict(end_length=round(tip, 4), tip_dia=round(2 * rT, 4), TM=round(2 * rM, 4), SL=round(tip - a_seat, 4), CD=round(2 * rC, 4),
                LL=round(a_seat - a_land, 4), TZ=round(a_land - a_out, 4), ramp=round(a_out - a_in, 4), RL=round(a_in - relief[0]['a1'], 4))


if __name__ == '__main__':
    a = sys.argv[1:]
    print(json.dumps(chain(a[0], *(int(x) for x in a[1:4]))))
