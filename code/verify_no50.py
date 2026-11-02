#!/usr/bin/env python3
"""No.50 v0.2 reproducibility audit. Python 3.10+; standard library only.

Runs exhaustive exact checks for binary-deletion channel at n=4,5,7,8.
Source independent cross-check: DP vs direct subset enumeration.
No unbounded-switch theorem is asserted or tested.
"""
from __future__ import annotations
import argparse, json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path


def offsets(n):
    return [(1 << k) - 1 for k in range(n + 1)]


def binary_words(n):
    return [format(i, f'0{n}b') for i in range(1 << n)]


def counts_dp(word: str):
    n = len(word); ofs = offsets(n)
    c = [0] * ((1 << (n + 1)) - 1)
    c[0] = 1
    for j, bit_char in enumerate(word):
        bit = int(bit_char)
        for k in range(j, -1, -1):
            start, next_start = ofs[k], ofs[k + 1]
            for v in range(1 << k):
                t = c[start + v]
                if t:
                    c[next_start + (v << 1) + bit] += t
    return c


def counts_direct(word: str):
    n = len(word); ofs = offsets(n)
    c = [0] * ((1 << (n + 1)) - 1)
    for mask in range(1 << n):
        k = mask.bit_count(); v = 0
        for j in range(n):
            if mask & (1 << j):
                v = (v << 1) + int(word[j])
        c[ofs[k] + v] += 1
    return c


def row_table(n):
    return [counts_dp(word) for word in binary_words(n)]


def a_coeffs(c1, c2, n):
    ofs = offsets(n)
    a = []
    for k in range(n + 1):
        start = ofs[k]; end = start + (1 << k)
        t = sum(abs(c1[j] - c2[j]) for j in range(start, end))
        assert t % 2 == 0
        a.append(t // 2)
    return tuple(a)


def distance_numerator(coeffs, a, b):
    # D(q=a/b) = numerator / b^n
    n = len(coeffs) - 1
    return sum(v * (b-a)**k * a**(n-k) for k, v in enumerate(coeffs))


def power_coeffs(coeffs):
    # D(q) as sum_j c_j q^j, each c_j integer
    n = len(coeffs) - 1
    out = [0] * (n+1)
    for k, v in enumerate(coeffs):
        for j in range(k+1):
            out[n-k+j] += v * (-1)**j * comb(k, j)
    return tuple(out)


def bernstein_on_interval(power, lo, hi):
    # Transform q=lo+(hi-lo)t, then convert power basis to Bernstein degree n
    n = len(power)-1
    span = hi-lo
    changed = []
    for j in range(n+1):
        changed.append(sum(Fraction(power[i]*comb(i,j)) * lo**(i-j) * span**j
                           for i in range(j,n+1)))
    return [sum(changed[j] * Fraction(comb(i,j),comb(n,j))
                for j in range(i+1)) for i in range(n+1)]


def full_interval_certificate():
    certs = []
    for n, x1, y1, x2, y2 in [
        (4, '0010','0100','0110','1001'),
        (5, '00010','00100','00110','01001')]:
        rows = row_table(n)
        target1 = a_coeffs(rows[int(x1,2)],rows[int(y1,2)],n)
        target2 = a_coeffs(rows[int(x2,2)],rows[int(y2,2)],n)
        target_powers = [power_coeffs(target1),power_coeffs(target2)]
        bounds = [(Fraction(0),Fraction(3,4)),(Fraction(3,4),Fraction(1))]
        lowest = None
        for i in range(1<<n):
            for j in range(i+1,1<<n):
                p = power_coeffs(a_coeffs(rows[i],rows[j],n))
                for t,(lo,hi) in enumerate(bounds):
                    diff = tuple(p[k]-target_powers[t][k] for k in range(n+1))
                    bern = bernstein_on_interval(diff,lo,hi)
                    assert min(bern)>=0, (n,i,j,t,bern)
                    if lowest is None or min(bern)<lowest:lowest=min(bern)
        # Check target polynomials match the stated closed form:
        # A(q)=(1-q)^2(q^2-q+1), B(q)=(1-q)^3(3q+1)
        assert tuple(target_powers[0][:5]) == (1,-3,4,-3,1)
        assert tuple(target_powers[1][:5]) == (1,0,-6,8,-3)
        certs.append({'n':n,'pairs':comb(1<<n,2),'intervals':2,
                      'all_Bernstein_coefficients_nonnegative':True,
                      'min_coefficient':str(lowest),
                      'witnesses':[(x1,y1),(x2,y2)],
                      'distance_a_coeffs':[list(target1),list(target2)],
                      'target_power_coeffs':[list(target_powers[0]),list(target_powers[1])]})
    return certs


def exact_point_audit(n,a,b,table=None):
    rows = table if table is not None else row_table(n)
    best = None; bestpairs = []
    distinct_vals = {}
    distinct_polys = set()
    for i in range(1<<n):
        for j in range(i+1,1<<n):
            coeff = a_coeffs(rows[i],rows[j],n)
            distinct_polys.add(coeff)
            val = distance_numerator(coeff,a,b)
            distinct_vals[val] = 1
            if best is None or val<best:
                best=val;bestpairs=[(i,j)]
            elif val==best:bestpairs.append((i,j))
    vals=sorted(distinct_vals)
    assert vals[0]==best and len(vals)>1
    return {'n':n,'q':f'{a}/{b}','pairs':comb(1<<n,2),'unique_coefficient_vectors':len(distinct_polys),
            'min_TV':str(Fraction(best,b**n)),
            'runner_up_distinct_value':str(Fraction(vals[1],b**n)),
            'gap':str(Fraction(vals[1]-best,b**n)),
            'optimal_pairs':[list(format(i,f'0{n}b') for i in xy) for xy in bestpairs]}


def insert(word,bit,pos):return word[:pos]+bit+word[pos:]


def insertion_counterexample(table8, result8):
    parents=[('0110001','1000110'),('0111001','1001110')]
    bestnum=int(Fraction(result8['min_TV'])*5**8)
    min_num=None; num_ops=0; beats=0; min_case=None
    for x,y in parents:
        for bit in ('0','1'):
            for px in range(8):
                for py in range(8):
                    xx=insert(x,bit,px); yy=insert(y,bit,py)
                    coeff=a_coeffs(table8[int(xx,2)],table8[int(yy,2)],8)
                    num=distance_numerator(coeff,4,5)
                    num_ops+=1
                    if min_num is None or num<min_num:
                        min_num=num;min_case=[xx,yy]
                    if num==bestnum:beats+=1
    assert num_ops==256 and min_num>bestnum and beats==0
    return {'q':'4/5','parent_optimal_pairs':parents,'operation_count':num_ops,
            'minimum_insertion_distance':str(Fraction(min_num,5**8)),
            'global_minimum_n8':result8['min_TV'],
            'optimal_extensions':beats,'best_extension_example':min_case}


def run():
    out={'version':'v0.2','status':'AUDIT_HOLD','arithmetic':'exact integer/Fraction; standard library only',
         'assertions':{'finite_interval_n4_n5':True,'finite_witnesses_n7':True,
                       'simple_insertion_fails_n7_to_n8':True,
                       'unbounded_switching':'NOT PROVED'}}
    out['full_interval_certificates']=full_interval_certificate()
    rows7=row_table(7)
    out['n7_rational_witnesses']=[exact_point_audit(7,a,b,rows7)
      for a,b in [(1,4),(3,5),(3,4),(4,5)]]
    actual=[[r['optimal_pairs'][0][0],r['optimal_pairs'][0][1]] for r in out['n7_rational_witnesses']]
    expected=[['0000100','0001000'],['0010110','0011010'],['0011001','0100101'],['0110001','1000110']]
    assert actual==expected
    # Audit repair v0.2: the winning *polynomial sets* at all four q must
    # be singleton and pairwise disjoint; checking one representative alone
    # is insufficient to infer three polynomial transitions.
    winning_poly_sets=[]
    for entry in out['n7_rational_witnesses']:
        present={a_coeffs(rows7[int(x,2)],rows7[int(y,2)],7)
                 for x,y in entry['optimal_pairs']}
        assert len(present)==1, (entry['q'],present)
        winning_poly_sets.append(present)
    assert len(set.union(*winning_poly_sets))==4
    out['n7_unique_optimal_distance_polynomial_count_per_witness']=[len(v) for v in winning_poly_sets]
    out['n7_winning_polynomial_sets_pairwise_disjoint']=True
    representative_vectors=[next(iter(v)) for v in winning_poly_sets]
    out['n7_witness_coefficient_vectors']=[list(v) for v in representative_vectors]
    expected_gaps=['81/2048','48/15625','9/8192','16/15625']
    assert [r['gap'] for r in out['n7_rational_witnesses']]==expected_gaps
    rows8=row_table(8)
    out['n8_point']=exact_point_audit(8,4,5,rows8)
    assert out['n8_point']['min_TV']=='7233/390625'
    out['insertion_failure']=insertion_counterexample(rows8,out['n8_point'])
    # Independent path for specific pair subsequence counts: DP versus mask enumeration.
    cases=['0010','0100','0110','1001','00010','00100','00110','01001',
           '0110001','1000110','0111001','1001110','01011001','01100101']
    for word in cases:assert counts_dp(word)==counts_direct(word),word
    out['independent_counting_crosscheck']={'method_a':'dynamic programming',
         'method_b':'direct enumeration of deletion masks',
         'words_tested':cases,'all_match':True}
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default=None,help='write report JSON to path')
    args=parser.parse_args()
    result=run()
    resultstr=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.out:Path(args.out).write_bytes(resultstr.encode('utf-8'))
    print('PASS: 616 pairs x 2 intervals = 1,232 exact Bernstein certificates (n=4,5).')
    print('PASS: n=7 all 8,128 pairs at four q; singleton, pairwise-disjoint winning polynomial sets.')
    print('PASS: n=8 all 32,640 pairs at q=4/5; 256 insertion operations fail.')
    print('PASS: selected DP coefficients agree with direct deletion-mask enumeration.')
    print('NOT PROVED: unbounded number of switches or general recursive optimizer.')
    print('STATUS: AUDIT_HOLD, novelty INCONCLUSIVE, no independent AI audit.')
