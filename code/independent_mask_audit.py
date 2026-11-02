#!/usr/bin/env python3
"""Independent TV spot audits using deletion-mask enumeration + dicts.

Does not import the main verification modules; verifies complete pairwise
minimum for specified rational deletion probabilities at n=6,7,8 and
compares claimed winner vectors against this separate counting implementation.
Python 3.10+, standard library only.
"""
import argparse
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

RATIONAL_POINTS={
  6:[(1,4),(3,5),(4,5)],
  7:[(1,4),(3,5),(3,4),(4,5)],
  8:[(1,4),(3,5),(3,4),(4,5),(9,10)],
}


def direct_counts(word):
    ans=[{} for _ in range(len(word)+1)]
    for mask in range(1<<len(word)):
        bits=''.join(word[i] for i in range(len(word)) if mask&(1<<i))
        d=ans[len(bits)]
        d[bits]=d.get(bits,0)+1
    return ans


def pair_coeffs(first,second):
    return tuple(sum(abs(first[k].get(w,0)-second[k].get(w,0))
                     for w in first[k].keys()|second[k].keys())//2
                 for k in range(len(first)))


def weight_num(v,a,b):
    n=len(v)-1
    return sum(t*(b-a)**k*a**(n-k) for k,t in enumerate(v))


def exhaustive_q(n,table,a,b):
    best=None; winners=[]; polys=set()
    for i,j in combinations(range(1<<n),2):
        co=pair_coeffs(table[i],table[j])
        val=weight_num(co,a,b)
        if best is None or val<best:
            best=val;winners=[co]
        elif val==best:winners.append(co)
    winning_polys=set(winners)
    return best,winning_polys


def run(envelope_path):
    recorded=json.loads(Path(envelope_path).read_text('utf-8'))
    out={'version':'v0.2','independent_method':'direct mask enumeration in dicts + integer rational TV',
         'comparisons':[]}
    for item in recorded['lengths']:
        n=item['n']
        words=[format(i,f'0{n}b') for i in range(1<<n)]
        table=[direct_counts(word) for word in words]
        candidates=[]
        for (x,y), expected in zip(item['winner_pairs'],item['winner_a_coefficients']):
            actual=pair_coeffs(table[int(x,2)],table[int(y,2)])
            assert tuple(expected)==actual,(n,x,y)
            candidates.append(actual)
        for a,b in RATIONAL_POINTS[n]:
            smallest,winner_polys=exhaustive_q(n,table,a,b)
            expected_num=min(weight_num(w,a,b) for w in candidates)
            assert smallest==expected_num,(n,a,b,smallest,expected_num)
            assert winner_polys.issubset(set(candidates)),(n,a,b,winner_polys)
            out['comparisons'].append({'n':n,'q':f'{a}/{b}',
                  'minimum_TV':str(Fraction(smallest,b**n)),
                  'distinct_winning_polynomial_count':len(winner_polys),
                  'all_winning_polynomials_in_envelope_candidates':True})
        print('INDEPENDENT MASK PASS: n=%d, %d words, %d rational parameters'
              %(n,len(words),len(RATIONAL_POINTS[n])))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--envelope',required=True)
    ap.add_argument('--out')
    arg=ap.parse_args()
    result=run(arg.envelope)
    data=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if arg.out:Path(arg.out).write_bytes(data.encode('utf-8'))
    print('INDEPENDENT MASK AUDIT PASS: all 12 rational checkpoints')
