import numpy as np
import oapackage
from oapackage.oahelper import choose


def graph2arrayTransformation(pp, arrayclass, verbose=0):
    """ From a relabeling of the graph return the corresponding array transformation

    Args:
        pp (array): relabeling of graph vertices
        arrayclass (arraydata_t): class of arrays
        verbose (int): verbosity level
    Returns:
        tt (obj): array transformation
    """
    ppi = np.zeros(len(pp), )
    ppi[pp] = range(len(pp))
    ppi = np.array(ppi).astype(int)
    pp = np.array(pp).astype(int)

    # extract colperms and rowperm and levelperms from this...
    rowperm = np.array((pp[0:arrayclass.N]))
    rowperm = rowperm - rowperm.min()
    colperm = np.array((pp[arrayclass.N:(arrayclass.N + arrayclass.ncols)]))
    colperm = np.argsort(colperm)  # colperm-colperm.min()
    ns = np.sum(arrayclass.getS())
    lvlperm = np.array(
        (pp[(arrayclass.N + arrayclass.ncols):(arrayclass.N + arrayclass.ncols + ns)]))
    lvlperm = lvlperm - lvlperm.min()

    ttr = oapackage.array_transformation_t(arrayclass)
    ttr.setrowperm(rowperm)
    ttr = ttr.inverse()
    ttc = oapackage.array_transformation_t(arrayclass)
    ttc.setcolperm(colperm)

    ttl = oapackage.array_transformation_t(arrayclass)

    ncols = arrayclass.ncols
    cs = np.hstack(([0], np.cumsum(arrayclass.getS())))
    lp = []
    for ii in range(ncols):
        ww = lvlperm[cs[ii]:cs[ii + 1]]
        ww = ww - ww.min()
        ww = np.argsort(ww)
        lp.append(ww)
        ttl.setlevelperm(ii, ww)

    ttl = ttl.inverse()

    tt = ttr * ttc * ttl
    return tt


@oapackage.oahelper.deprecated
def showtriangles(jresults, showindex=1):
    """ Show triangle of j-values """
    raise Exception('function was removed')
#    import oalib
#    if isinstance(jresults, oalib.jstruct_t):
#        showindex = 0
#        jresults = (jresults,)
#
#    js = jresults[0]
#    i = 0
#    idx = [i]
#    for j in range(4, js.k + 1):
#        nn = choose(j - 1, 3)
#        i = i + nn
#        idx.append(i)
#    for jj, js in enumerate(jresults):
#        vals = oalib.intArray.frompointer(js.vals)
#        if showindex:
#            print('i: %d' % jj)
#        for kk in range(0, js.k - 3):
#            xx = [vals[v] for v in range(idx[kk], idx[kk + 1])]
#            s = ','.join(map(str, xx))
#            print('%s' % s)


def xtest_showtriangles():
    al = oapackage.exampleArray(11, 1)
    js = oapackage.jstruct_t(al)
    showtriangles(js)
