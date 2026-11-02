#!/usr/bin/env python3
"""No.50 v0.2: exact all-parameter lower envelopes for n=6,7,8.

Proof certificate: coefficientwise domination for all but six n=8
polynomials; for those six, Bernstein certificates on [0,1/2]
and [1/2,1]. Candidate lower envelope is certified by exact
Bernstein signs plus unique root isolations using a derivative-sign
certificate. Pure Python >=3.10 standard library; no floating point.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from math import comb

# Explicit path addition is required with python -I (isolated mode).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_no50 import (row_table, a_coeffs, power_coeffs, distance_numerator,
                         bernstein_on_interval)

WINNERS = {
    6: [('000100','001000'), ('010110','011010'), ('001101','010011')],
    7: [('0000100','0001000'), ('0010110','0011010'),
        ('0011001','0100101'), ('0110001','1000110')],
    8: [('00001000','00010000'), ('00101100','00110100'),
        ('01011001','01100101'), ('00110001','01000110')],
}
# Certified 1e-6-wide rational brackets, excluding the exact 1/2 root.
BRACKETS = {
    6: [(F(1,2),F(1,2)),(F(763072,1000000),F(763073,1000000))],
    7: [(F(1,2),F(1,2)),(F(742622,1000000),F(742623,1000000)),
        (F(788152,1000000),F(788153,1000000))],
    8: [(F(544922,1000000),F(544923,1000000)),
        (F(717875,1000000),F(717876,1000000)),
        (F(826005,1000000),F(826006,1000000))],
}
# Constant-first coefficients for each polynomial equation printed in Table 2.
ROOT_FACTORS = {
    6:[(-1,2),(-3,6,-5,3)],
    7:[(-1,2),(-3,6,-3,-1,2),(-7,1,10)],
    8:[(-2,6,-7,5),(-3,6,0,-6,2,2),(-4,1,3,2)],
}
EXPECTED_UNIQUE_POLYS = {6:260,7:1190,8:5835}
EXPECTED_EXCEPTIONS = {6:0,7:0,8:6}


def ev(poly, x):
    return sum(F(c)*x**k for k,c in enumerate(poly))


def diff_poly(p,q):
    return tuple(a-b for a,b in zip(p,q))


def cert_bern(poly, lo, hi):
    """All Bernstein coefficients >=0 => polynomial >=0 on [lo,hi]."""
    assert lo <= hi
    b=bernstein_on_interval(poly,lo,hi)
    assert min(b)>=0, ('BERNSTEIN FAIL',lo,hi,poly,b)
    return min(b)


def assert_polynomial_divisible(num, den):
    # Ascending-power, exact rational polynomial long division.
    q=[F(v) for v in num]
    d=[F(v) for v in den]
    while q and q[-1]==0:q.pop()
    while d and d[-1]==0:d.pop()
    assert d and d[-1]
    while len(q)>=len(d):
        ratio=q[-1]/d[-1]
        ofs=len(q)-len(d)
        for i in range(len(d)):
            q[ofs+i]-=ratio*d[i]
        while q and q[-1]==0:q.pop()
    assert not q, ('displayed root polynomial does not divide candidate difference',num,den)


def certify_length(n):
    words=1<<n
    rows=row_table(n)
    polys={}
    for i in range(words):
        for j in range(i+1,words):
            a=a_coeffs(rows[i],rows[j],n)
            if a not in polys:polys[a]=(i,j)
    assert len(polys)==EXPECTED_UNIQUE_POLYS[n],(n,len(polys))
    coeff_w=[a_coeffs(rows[int(x,2)],rows[int(y,2)],n) for x,y in WINNERS[n]]
    power_w=[power_coeffs(a) for a in coeff_w]
    assert len(set(coeff_w))==len(coeff_w)

    # Every polynomial is >= one displayed candidate for the entire q range,
    # except some exceptional n=8 polynomials dealt with below.
    exceptions=[]
    dominated=0
    for a in polys:
        if any(all(x<=y for x,y in zip(w,a)) for w in coeff_w):
            dominated+=1
        else:
            exceptions.append(a)
    assert len(exceptions)==EXPECTED_EXCEPTIONS[n],(n,len(exceptions))

    exception_certs=[]
    for a in exceptions:
        p=power_coeffs(a)
        halves=[]
        for lo,hi in ((F(0),F(1,2)),(F(1,2),F(1))):
            found=None
            for i,w in enumerate(power_w):
                d=diff_poly(p,w)
                b=bernstein_on_interval(d,lo,hi)
                if min(b)>=0:
                    found=i
                    break
            assert found is not None,(n,a,lo,hi)
            halves.append(found)
        exception_certs.append({'coefficient_vector':list(a),
                                'representative_pair':[format(t,f'0{n}b') for t in polys[a]],
                                'witness_index_0_based_for_[0,1/2]_[1/2,1]':halves})

    # Brackets for all successive candidate crossings, with a strictly
    # monotone difference on the enclosing rational subinterval.
    brackets=BRACKETS[n]
    assert len(brackets)==len(coeff_w)-1
    transition_certs=[]
    for i,(lo,hi) in enumerate(brackets):
        assert F(0)<lo<=hi<F(1)
        d=diff_poly(power_w[i],power_w[i+1])
        f=ROOT_FACTORS[n][i]
        assert_polynomial_divisible(d,f)
        if lo==hi:
            assert ev(d,lo)==0
            # point root; adjacent open regions are separately certified below.
            cert={'index':i,'lower':str(lo),'upper':str(hi),'exact_rational_root':True}
        else:
            assert ev(f,lo)*ev(f,hi)<0, (n,i,'root factor lacks sign change')
            left,right=ev(d,lo),ev(d,hi)
            assert left<0 and right>0,(n,i,lo,hi,left,right)
            derivative=tuple(j*d[j] for j in range(1,n+1))
            der_b=bernstein_on_interval(derivative,lo,hi)
            assert min(der_b)>0,(n,i,'not strictly increasing',der_b)
            # At most one root by derivative sign, at least one by IVT.
            cert={'index':i,'lower':str(lo),'upper':str(hi),
                  'exact_rational_root':False,
                  'unique_root_certified_by_positive_derivative_Bernstein':True}
            # Neither any third winning polynomial nor an exception can
            # beat the two adjacent contenders over this transition window.
            for j,p in enumerate(power_w):
                if j in (i,i+1): continue
                ok=any(min(bernstein_on_interval(diff_poly(p,power_w[idx]),lo,hi))>=0
                       for idx in (i,i+1))
                assert ok,(n,i,j,'third candidate enters transition')
        cert['defining_root_polynomial_ascending_coefficients']=list(f)
        transition_certs.append(cert)

    # Between crossing brackets, the corresponding winner beats all
    # other candidates on the complete interval (Bernstein proof).
    regular=[];start=F(0)
    for i,(lo,hi) in enumerate(brackets):
        regular.append((start,lo,i))
        start=hi
    regular.append((start,F(1),len(coeff_w)-1))
    regular_certs=[]
    for lo,hi,i in regular:
        assert lo<hi,(n,lo,hi)
        for j,p in enumerate(power_w):
            if j==i:continue
            cert_bern(diff_poly(p,power_w[i]),lo,hi)
            assert ev(p,(lo+hi)/2)>ev(power_w[i],(lo+hi)/2), (n,i,j)
        regular_certs.append({'winner_index_0_based':i,'lower':str(lo),'upper':str(hi)})

    # The actual ordered candidates each occupy a nonempty open region.
    # In crossing windows the same two competitors are the only possibilities,
    # and the signed unique root makes exactly one switch.
    return {
        'n':n, 'word_pairs':comb(words,2), 'unique_distance_polynomials':len(polys),
        'coefficientwise_dominated_poly_count':dominated,
        'exception_poly_count':len(exceptions), 'exception_certificates':exception_certs,
        'winner_pairs':[[x,y] for x,y in WINNERS[n]],
        'winner_a_coefficients':[list(a) for a in coeff_w],
        'winner_power_coefficients':[list(a) for a in power_w],
        'regular_intervals':regular_certs,'transition_certificates':transition_certs,
        'exact_interior_switch_count':len(brackets),
        'proof_method':'exact coefficient dominance + exact Bernstein + unique-root interval isolation',
    }


def run():
    ret={'version':'v0.2','status':'AUDIT_HOLD','novelty':'INCONCLUSIVE',
         'mathematical_claim':'EXACT finite envelopes n=6,7,8; NOT unbounded switching',
         'lengths':[certify_length(n) for n in (6,7,8)]}
    assert [r['exact_interior_switch_count'] for r in ret['lengths']]==[2,3,3]
    return ret

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out')
    args=parser.parse_args()
    result=run()
    data=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.out:Path(args.out).write_bytes(data.encode('utf-8'))
    for d in result['lengths']:
        print('PASS n=%d: %d pair comparisons / %d polynomials / %d exceptions / %d exact switches'
              %(d['n'],d['word_pairs'],d['unique_distance_polynomials'],
                d['exception_poly_count'],d['exact_interior_switch_count']))
    print('UNPROVED: unbounded switching or a recursive optimizer for all lengths.')
