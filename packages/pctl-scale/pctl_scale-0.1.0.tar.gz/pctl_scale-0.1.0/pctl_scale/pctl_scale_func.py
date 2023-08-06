import numpy as np


def saturate_upper_to_one(x, u):
    t = x - u
    k = 1 / (1 - u)
    return u / (u + (1 - u) * np.exp(-t * k))


def saturate_lower_to_zero(x, d):
    t = d - x
    k = 1 / d
    return d / np.exp(t * k)


def percentile_scale_clean(x, d=.05, u=.95):
    # compute upper and lower pctl values
    vd, vu = np.percentile(x, q=(d * 100, u * 100))

    # scale x=[vd,vu] to y=[d,u]
    to1 = (x - vd) / (vu - vd)
    y = d + u * to1

    # saturate upper values to [u,1]
    y[y > u] = saturate_upper_to_one(y[y > u], u)

    # fit lower values to [0,d]
    y[y < d] = saturate_lower_to_zero(y[y < d], d)

    # done
    return y, vd, vu


def check_ignore(e, naignore=[]):
    """True if the element is nan, inf, None, or
    from a specified list with excluded values
    """
    if e:   # Check None
        if np.isnan(e):
            return True
        if np.isinf(e):
            return True
        if naignore:
            if e in naignore:
                return True
    else:
        return True
    return False


def percentile_scale(x, d=.05, u=.95, naignore=[0], naimpute=0):
    # ensure numpy array
    x_ = np.array(x)
    # memorize ineligible values
    idxmiss = np.array([check_ignore(e, naignore) for e in x_])
    idxexist = np.logical_not(idxmiss)

    y, vd, vu = percentile_scale_clean(x_[idxexist], d=d, u=u)

    z = np.empty(shape=x_.shape)
    z[idxexist] = y
    z[idxmiss] = naimpute

    return z, vd, vu
