####################################################################################################
# neuropythy/vision/optimize.py
# Code for optimizing retinotopic maps on the cortical surface.
# By Noah C. Benson

import os, gzip, types, six, abc, pimms
import numpy                 as np
import numpy.linalg          as npla
import scipy                 as sp
import scipy.sparse          as sps
import scipy.optimize        as spopt
import pyrsistent            as pyr
from   ..                import geometry as geo
from   ..                import mri      as mri
from   ..util            import (times, zdivide, zinv)
from   ..geometry        import (triangle_area)

# Helper Functions #################################################################################
def numel(x):
    '''
    numel(x) yields the number of elements in x: the product of the shape of x.
    '''
    return int(np.prod(np.shape(x)))
def rows(x):
    '''
    rows(x) yields the number of rows in x; if x is a scalar, this is still 1.
    '''
    s = np.shape(x)
    return s[0] if len(s) > 0 else 1
def ftimes(a,b):
    '''
    ftimes(mtx1,mtx2) yields mtx1 * mtx2.
    ftimes(mtx,vec) yields mtx.dot(scipy.sparse.diags(vec)).
    ftimes(vec1,vec2) yields vec1 * vec2
    ftimes(vec,scl) yields vec * scl.
    '''
    sa = len(np.shape(a))
    sb = len(np.shape(b))
    if sa == sb or sa == 0 or sb == 0: return a * b
    elif sa == 2: return a.dot(sps.diags(b))
    else: return sps.diags(a).dot(b)
def finv(x):
    '''
    finv(x) yields the inverse of x, 1/x, if x is a normal array or value; if x is a sparse array,
      then yields a new sparse array with only the specified values inverted.
    '''
    if sps.issparse(x):
        x = x.copy()
        x.data = 1.0/x.data
        return x
    else: return 1.0/x
def fzinv(x):
    '''
    fzinv(x) yields the inverse of x, zinv(x), if x is a normal array or value; if x is a sparse
      array, then yields a new sparse array with only the specified values inverted.
    '''
    if sps.issparse(x):
        x = x.copy()
        x.data = zinv(x.data)
        return x
    else: return zinv(x)
def fapply(f,x):
    '''
    fapply(f,x) yields the result of applying f either to x, if x is a normal value or array, or to
      x.data if x is a sparse matrix. Does not modify x (unless f modifiex x).
    '''
    if sps.issparse(x):
        y = x.copy()
        y.data = f(x.data)
        return y
    else: return f(x)
def finto(x,ii,n):
    '''
    finto(x,ii,n) yields a vector u of length n such that u[ii] = x if x is a vector or matrix and
      is not sparse; if x is sparse, then yields the equivalent sparse matrix.
    '''
    ii = np.asarray(ii)
    if sp.issparse(x):
        (rows,cols) = x.nonzero()
        cls = type(x)
        return cls((x.data, (ii[rows], cols)), shape=x.shape)
    else: return x[ii]
def fdot(a,b,s=None):
    '''
    fdot(a,b) yields the dot product of a and b, doing so in a fashion that respects sparse matrices
      when encountered. This does not error check for bad dimensionality.
    fdot(a,b,shape) yields the dot product of a and b, interpreting vectors as either rows or
      columns in such a way that the shape of the resulting output is equal to shape. If this cannot
      be done, an exception is raised. 
    '''
    if s is None:
        if sps.issparse(a): return a.dot(b)
        elif sps.issparse(b): return b.T.dot(a.T).T
        else: return np.dot(a,b)
    else:
        a = a if sps.issparse(a) else np.squeeze(a)
        b = b if sps.issparse(b) else np.squeeze(b)
        sa = a.shape
        sb = b.shape
        (la,lb,ls) = [len(x) for x in (sa,sb,s)]
        if la == 0 or lb == 0:   z = fdot(a,b,None)
        elif la == 2 or lb == 2: z = fdot(a,b,None)
        elif la != 1 or lb != 1: raise ValueError('fdot only works with tensor rank <= 2')
        elif ls == 0:            return np.dot(a,b)
        elif ls == 2:            z = fdot(np.expand_dims(a,-1), np.expand_dims(a,0))
        else: raise ValueError('fdot: cannot turn %s * %s into %s' % (sa,sb,s))
        if z.shape == s: return z
        elif ls == 0 and z.shape == (1,1): return z[0,0]
        elif ls == 1 and s[0] == numel(z): return (z.toarray() if sps.issparse(z) else z).reshape(s)
        else: raise ValueError('fdot: cannot turn %s * %s into %s' % (sa,sb,s))

# Potential Functions ##############################################################################
@six.add_metaclass(abc.ABCMeta)
class PotentialFunction(object):
    '''
    The PotentialFunction class is intended as the base-class for all potential functions that can
    be minimized by neuropythy. PotentialFunction is effectively an abstract class that requires its
    subclasses to implement the method __call__(), which must take one argument: a numpy vector of
    parameters. The method must return a tuple of (z,dz) where z is  the potential value for the
    given paramters and dz is the Jacobian of the function at the parameters. Note that if the
    potential z returned is a scalar, then dz must be a vector of length len(params); if z is a
    vector, then dz must be a matrix of size (len(z) x len(params))
    '''
    # the __call__ function is how one generally calls a potential function
    @abc.abstractmethod
    def __call__(params):
        '''
        pf(params) yields the tuple (z, dz) where z is the potential value at the given parameters
          vector, params, and dz is the vector of the potential gradient.
        '''
        raise RuntimeError('The __call__() method was not overloaded for object %s' % self)
    # Arithmetic Operators #########################################################################
    def __getitem__(self, ii):
        return PotentialSubselection(self, ii)
    def __neg__(self):
        return PotentialTimesConstant(self, -1)
    def __add__(self, x):
        if isinstance(x, PotentialFunction): return PotentialPlusPotential(self, x)
        elif np.isclose(x, 0).all():         return self
        else:                                return PotentialPlusConstant(self, x)
    def __radd__(self, x):
        if np.isclose(x, 0): return self
        else:                return PotentialPlusConstant(self, x)
    def __sub__(self, x):
        return self.__add__(-x)
    def __rsub__(self, x):
        return PotentialPlusConstant(PotentialTimesConstant(self, -1), x)
    def __mul__(self, x):
        if isinstance(x, PotentialFunction): return PotentialTimesPotential(self, x)
        elif np.isclose(x, 1).all():         return self
        else:                                return PotentialTimesConstant(self, x)
    def __rmul__(self, x):
        if np.isclose(x, 1): return self
        else:                return PotentialTimesConstant(self, x)
    def __div__(self, x):
        return self.__mul__(1/x)
    def __rdiv__(self, x):
        return PotentialPowerConstant(self, -1) * x
    def __truediv__(self, x):
        return self.__mul__(1/x)
    def __rtruediv__(self, x):
        return PotentialPowerConstant(self, -1) * x
    def __pow__(self, x):
        if isinstance(x, PotentialFunction): return PotentialPowerPotential(self, x)
        else:                                return PotentialPowerConstant(self, x)
    def __rpow__(self, x):
        return ConstantPowerPotential(x, self)
    def log(self, base=None):
        if base is None:
            return PotentialLog(self)
        elif isinstance(base, PotentialFunction):
            return PotentialTimesPotential(PotentialLog(self), 1.0/PotentialLog(base))
        else:
            return PotentialTimesConstant(PotentialLog(self), 1.0/np.log(base))
    def sqrt(self):
        return PotentialPowerConstant(self, 0.5)
    def compose(self, f):
        return PotentialComposition(self, f)
@pimms.immutable
class PotentialSubselection(PotentialFunction):
    def __init__(self, f, ii):
        self.f = f
        self.indices = ii
    @pimms.param
    def f(f0): return f0
    @pimms.param
    def indices(ii):
        ii = np.asarray(ii)
        if (np.issubdtype(ii.dtype, np.dtype('bool').type) or
            (len(ii) > 2 and np.logical_or(ii == True, ii == False).all())):
            ii = np.where(ii)[0]
        return pimms.imm_array(ii)
    def __call__(self, params):
        params = np.asarray(params)
        ii = self.indices
        (z,dz) = self.f(params[ii])
        grad = finto(dz, ii, len(params))
        return (z,grad)
@pimms.immutable
class PotentialPlusPotential(PotentialFunction):
    def __init__(self, g, h):
        self.g = g
        self.h = h
    @pimms.param
    def g(g0): return g0
    @pimms.param
    def h(h0): return h0
    def __call__(self, params):
        return tuple([a + b for (a,b) in zip(self.g(params), self.h(params))])
@pimms.immutable
class PotentialPlusConstant(PotentialFunction):
    def __init__(self, f, c):
        self.f = f
        self.c = c
    @pimms.param
    def f(f0): return f0
    @pimms.param
    def c(c0): return c0
    def __call__(self, params):
        (z,dz) = self.f(params)
        return (z + self.c, dz)
@pimms.immutable
class PotentialTimesPotential(PotentialFunction):
    def __init__(self, g, h):
        self.g = g
        self.h = h
    @pimms.param
    def g(g0): return g0
    @pimms.param
    def h(h0): return h0
    def __call__(self, params):
        (zg, dzg) = self.g(params)
        (zh, dzh) = self.h(params)
        return (zg*zh, ftimes(zh, dzg) + ftimes(zg, dzh))
@pimms.immutable
class PotentialTimesConstant(PotentialFunction):
    def __init__(self, f, c):
        self.f = f
        self.c = c
    @pimms.param
    def f(f0): return f0
    @pimms.param
    def c(c0): return c0
    def __call__(self, params):
        (z,dz) = self.f(params)
        return (z * self.c, ftimes(self.c, dz))
@pimms.immutable
class PotentialPowerConstant(PotentialFunction):
    def __init__(self, f, c):
        self.f = f
        self.c = c
    @pimms.param
    def f(f0): return f0
    @pimms.param
    def c(c0): return c0
    def __call__(self, params):
        c = self.c
        (z,dz) = self.f(params)
        return (z**c, ftimes(c * z**(c-1), dz))
@pimms.immutable
class ConstantPowerPotential(PotentialFunction):
    def __init__(self, c, f):
        self.f = f
        self.c = c
    @pimms.param
    def f(f0): return f0
    @pimms.param
    def c(c0): return c0
    @pimms.value
    def log_c(c): return np.log(c)
    def __call__(self, params):
        (z,dz) = self.f(params)
        z = self.c ** z
        return (z, self.log_c * ftimes(z, dz))
def exp(x):
    if isinstance(x, PotentialFunction): return ConstantPowerPotential(np.e, x)
    else: return np.exp(x)
def exp2(x):
    if isinstance(x, PotentialFunction): return ConstantPowerPotential(2, x)
    else: return np.exp2(x)
@pimms.immutable
class PotentialPowerPotential(PotentialFunction):
    def __init__(self, g, h):
        self.g = g
        self.h = h
    @pimms.param
    def g(g0): return g0
    @pimms.param
    def h(h0): return h0
    def __call__(self, params):
        (zg,dzg) = self.g(params)
        (zh,dzh) = self.h(params)
        return (zg**zh, zg**(zh - 1) * (ftimes(zg, dzh) + ftimes(zg*np.log(zg), dzh)))
def pow(x,y):
    if isinstance(x, PotentialFunction):
        if isinstance(y, PotentialFunction): return PotentialPowerPotential(x, y)
        else: return PotentialPowerConstant(x, y)
    elif isinstance(y, PotentialFunction): ConstantPowerPotential(x, y)
    else: return np.pow(x,y)
@pimms.immutable
class PotentialLog(PotentialFunction):
    def __init__(self, f):
        self.f = f
    @pimms.param
    def f(f0): return f0
    def __call__(self, params):
        (z,dz) = self.f(params)
        return (np.log(z), finv(dz))
def log(x, base=None):
    if isinstance(x, PotentialFunction): return PotentialLog(x, base=base)
    else: return np.log(x, base)
def log2(x): return log(x,2)
def log10(x): return log(x,10)
@pimms.immutable
class PotentialComposition(PotentialFunction):
    def __init__(self, g, h):
        self.g = g
        self.h = h
    @pimms.param
    def g(g0): return g0
    @pimms.param
    def h(h0): return h0
    def __call__(self, params):
        (zh, dzh)  = self.h(params)
        (zgh,dzgh) = self.g(zh)
        return (zgh, fdot(dzgh, dzh, np.shape(zgh) + np.shape(params)))
@pimms.immutable
class PotentialSum(PotentialFunction):
    def __init__(self, f, weights=None):
        self.f = f
        self.weights = None
    @pimms.param
    def f(f0): return f0
    @pimms.param
    def weights(w): return None if w is None else pimms.imm_array(w)
    def __call__(self, params):
        (z,dz) = self.f(params)
        w = self.weights
        if w is None: return (np.sum(z),    np.squeeze(np.asarray(dz.sum(axis=0))))
        else:         return (np.dot(z, w), np.squeeze(np.asarray(ftimes(w, dz).sum(axis=0))))
def sum(x, weights=None):
    if isinstance(x, PotentialFunction): return PotentialSum(x, weights=weights)
    elif weights is None: return np.sum(x)
    else: return np.dot(x, weights) / np.sum(weights)
@pimms.immutable
class SimplexPotential(PotentialFunction):
    '''
    SimplexPotential is the base-class for potentials that use simplices (i.e., subsets of the
    parameter space) to define themselves and don't want to have to deal with monitoring the
    specifics of the indexing.

    To create a SimplexPotential, the constructor must be given a matrix of simplex indices; each
    row corresponds to one simplex. Note that while the first dimension must correspond to simplex,
    the remaining dimensions may be any shape. When the new potential function object is called, it
    internally sorts the parameters into a matrix the same shape as the simplex index and then calls
    the simplex_potential() function. This function should return an array of potential values, one
    per simplex, and a gradient array the same shape as the simplex index. This gradient array is
    then sorted into a sparse Jacobian matrix, which is returned along with the vector potential
    values. To create a scalar potential, one generally uses PotentialSum() on such an object.
    '''
    def __init__(self, simplices):
        self.simplices = simplices
    @pimms.param
    def simplices(s): return pimms.imm_array(s)
    @pimms.value
    def simplex_dimensions(simplices):
        return np.prod(simplices.shape[1:], dtype=np.int)
    @pimms.value
    def flat_simplices(simplices):
        fs = simplices.flatten()
        fs.setflags(write=False)
        return fs
    @pimms.value
    def jacobian_indices(flat_simplices, simplex_dimensions):
        (s,d) = (int(len(flat_simplices)/simplex_dimensions), simplex_dimensions)
        ii = np.tile(np.reshape(np.arange(s), (s,1)), (1,d)).flatten()
        ii.setflags(write=False)
        return (ii, flat_simplices)
    def simplex_potential(self, params):
        raise RuntimeError('simplex_potential not overloaded in object %s' % self)
    def __call__(self, params):
        params = np.asarray(params)
        s = np.reshape(params[self.flat_simplices.flatten()], self.simplices.shape)
        (z,dz) = self.simplex_potential(s)
        dz = sps.csr_matrix((dz.flatten(), self.jacobian_indices), shape=(len(dz), len(params)))
        return (z, dz)
@pimms.immutable
class FixedDistancePotential(SimplexPotential):
    '''
    FixedDistancePotential(ii, x0) represents the potential function that is the displacement of the
    parameter(s) from the reference value(s) x0. If x0 is a vector, then the call is equivalent to
    DistancePotential([x0]) (i.e., a 1 x n matrix). If x0 is a single value, then [[x0]] is used.
    For a matrix x0 with dimensions (n x m), then x0 is assumed to represent a set of n vectors with
    m dimensions each. The simplex index ii must match the vector/matrix arrangement in x0.

    For parameter matrix x, reference matrix x0, and axis parameter a, the potential is:
      np.sqrt(np.sum((x - x0)**2, axis=1))
    And the gradient is is the direction of greatest increase (i.e. the vector away from x0).
    '''
    def __init__(self, simplices, x0):
        self.reference = x0
        SimplexPotential.__init__(self, simplices)
    @pimms.param
    def simplices(s):
        s = np.array(s)
        if   len(s.shape) == 0: s = np.asarray([[s]])
        elif len(s.shape) == 1: s = np.reshape(s, (s.shape[0], 1))
        else:                   s = np.reshape(s, (s.shape[0], np.prod(s.shape[1:])))
        s.setflags(write=False)
        return s
    @pimms.param
    def reference(x0):
        x0 = np.array(x0)
        if   len(x0.shape) == 0: x0 = np.asarray([[sx0]])
        elif len(x0.shape) == 1: x0 = np.reshape(s, (x0.shape[0], 1))
        else:                    x0 = np.reshape(x0, (x0.shape[0], np.prod(x0.shape[1:])))
        x0.setflags(write=False)
        return x0
    def simplex_potential(self, params):
        delta = params - self.reference
        dist = np.sqrt(np.sum(delta**2, axis=1))
        return (dist, zdivide(delta, dist))
@pimms.immutable
class PairedMeanDifferencePotential(SimplexPotential):
    '''
    PairedMeanDifferencePotential(ii, jj) represents the potential function that is the difference
    between the means of the parameter comprising the paired simplces in matrices ii and jj.

    For parameter matrix x and flattened simplex matrices ii and jj, the potential is like:
      (ii,jj) = [np.reshape(ij, (len(ij), -1)) for ij in (ii,jj)]
      np.sqrt(np.sum((np.mean(x[ii], axis=1) - np.mean(x0[jj], axis=1))**2, axis=1))
    And the gradient is is the direction of greatest increase of the distance between the points.
    '''
    def __init__(self, ii, jj):
        SimplexPotential.__init__(self, (ii,jj))
    @pimms.param
    def simplices(s):
        (ii,jj) = map(np.asarray, s)
        if len(ii.shape) == 0:
            ii = np.reshape(ii, (1,1))
            jj = np.reshape(jj, (1,1))
        elif len(ii.shape) == 1:
            ii = np.reshape(ii, (ii.shape[0], 1))
            jj = np.reshape(jj, (jj.shape[0], 1))
        else:
            ii = np.reshape(ii, (ii.shape[0], -1))
            jj = np.reshape(jj, (jj.shape[0], -1))
        s = np.reshape(np.hstack([ii,jj]), (ii.shape[0], 2, ii.shape[1]))
        s.setflags(write=False)
        return s
    def simplex_potential(self, params):
        mu0 = np.mean(params[:,0], axis=1)
        mu1 = np.mean(params[:,1], axis=1)
        z = mu0 - mu1
        dz = np.ones(params.shape) * (np.reshape([1, -1], (1,2,1)) / params.shape[2])
        return (z, dz)
@pimms.immutable
class PairedDistancePotential(SimplexPotential):
    '''
    PairedDistancePotential(ii, jj) represents the potential function that is the displacement of
    the parameter(s) ii from the parameter(s) jj. Both ii and jj should be identically-shaped
    matrices of simplices.

    For parameter matrix x and flattened simplex matrices ii and jj, the potential is like:
      np.sqrt(np.sum((x[ii] - x0[jj])**2, axis=1))
    And the gradient is is the direction of greatest increase of the distance between the points.
    '''
    def __init__(self, ii, jj):
        SimplexPotential.__init__(self, (ii,jj))
    @pimms.param
    def simplices(s):
        (ii,jj) = map(np.asarray, s)
        if len(ii.shape) == 0:
            ii = np.reshape([ii], (1,1))
            jj = np.reshape([jj], (1,1))
        elif len(ii.shape) == 1:
            ii = np.reshape(ii, (ii.shape[0], 1))
            jj = np.reshape(jj, (jj.shape[0], 1))
        else:
            ii = np.reshape(ii, (ii.shape[0], -1))
            jj = np.reshape(jj, (jj.shape[0], -1))
        s = np.reshape(np.hstack([ii,jj]), (ii.shape[0], 2, ii.shape[1]))
        s.setflags(write=False)
        return s
    def simplex_potential(self, params):
        delta = params[:,0] - params[:,1]
        dist = np.sqrt(np.sum(delta**2, axis=1))
        dz = zdivide(delta, dist)
        dz = np.reshape(np.hstack([dz, -dz]), params.shape)
        return (dist, dz)
@pimms.immutable
class TriangleSignedArea2DPotential(SimplexPotential):
    '''
    TriangleSignedArea2DPotential(faces) yields a potential function that tracks the signed area of
    the given list of faces. The faces array should be an n x 3 x 2 where n is the number of faces.
    The signed area is positive if the triangle is counter-clockwise and negative if the triangle is
    clockwise.
    '''
    def __init__(self, faces):
        SimplexPotential.__init__(self, faces)
    def simplex_potential(self, params):
        # transpose to be 3 x 2 x n
        p = np.transpose(params, (1,2,0))
        # First, get the two legs...
        (dx_ab, dy_ab) = p[1] - p[0]
        (dx_ac, dy_ac) = p[2] - p[0]
        (dx_bc, dx_bc) = p[2] - p[1]
        # now, the area is half the z-value of the cross-product...
        sarea = 0.5 * (dx_ab*dy_ac - dx_ac*dy_ab)
        sdiff = 0.5 * np.transpose([[-dy_bc,dx_bc], [dy_ac,-dx_ac], [-dy_ab,dx_ab]], (2,0,1))
        return (sarea, sdiff)
@pimms.immutable
class TriangleArea2DPotential(SimplexPotential):
    '''
    TriangleArea2DPotential(faces) yields a potential function that tracks the unsigned area of the
    given list of faces. The faces array should be an n x 3 x 2 where n is the number of faces.
    '''
    def __init__(self, faces):
        SimplexPotential.__init__(self, faces)
    def simplex_potential(self, params):
        # transpose to be 3 x 2 x n
        p = np.transpose(params, (1,2,0))
        # First, get the two legs...
        (dx_ab, dy_ab) = p[1] - p[0]
        (dx_ac, dy_ac) = p[2] - p[0]
        (dx_bc, dy_bc) = p[2] - p[1]
        # now, the area is half the z-value of the cross-product...
        sarea0 = 0.5 * (dx_ab*dy_ac - dx_ac*dy_ab)
        # but we want to abs it
        sarea = np.abs(sarea0)
        dsarea0 = np.sign(sarea0)
        sdiff = times(0.5*dsarea0,
                      np.transpose([[-dy_bc,dx_bc], [dy_ac,-dx_ac], [-dy_ab,dx_ab]], (2,0,1)))
        return (sarea, sdiff)
@pimms.immutable
class SimplexCentroidNorm(SimplexPotential):
    '''
    SimplexCentroidNorm(simplices) is a potential function that represents the norm of the centroid
    of each of the given simplces. In this calculation, simplices must be an (n x m x d) array where
    n is the number of simplices, m is the number of points in each simplex, and d is the number of
    dimensions of the embedding space.
    '''
    def __init__(self, faces):
        SimplexPotential.__init__(self, faces)
    def simplex_potential(self, params):
        # first get the mean of the vertices
        mu = np.mean(params, axis=1)
        # then get the norm
        norm = np.sqrt(np.sum(mu**2, axis=1))
        # for the gradient, start with the gradient at the centroid:
        gradc = mu / np.expand_dims(norm, 1)
        # then extend to the vertices
        grad = np.expand_dims(gradc / 9.0, 1) * np.ones((1, params.shape[1], 1))
        return (mu, grad)
