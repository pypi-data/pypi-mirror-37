
# -*- coding: utf-8 -*-

u'''Utility, geodetic/geometric functions and constants.

After I{(C) Chris Veness 2011-2015} published under the same MIT Licence**, see
U{Latitude/Longitude<http://www.Movable-Type.co.UK/scripts/latlong.html>} and
U{Vector-based geodesy<http://www.Movable-Type.co.UK/scripts/latlong-vectors.html>}.

@newfield example: Example, Examples
'''

# make sure int division yields float quotient
from __future__ import division

from fmath import _Seqs, EPS, fStr, fsum_, hypot, len2, map2

from math import acos, atan2, cos, degrees, pi as PI, \
                 radians, sin, sqrt, tan  # pow

# all public contants, classes and functions
__all__ = ('PI', 'PI2', 'PI_2', 'R_M',  # constants
           'LimitError',  # classes
           'acos1', 'anStr', 'antipode',
           'degrees', 'degrees90', 'degrees180', 'degrees360',
           'enStr2',
           'equirectangular', 'equirectangular_',
           'false2f', 'ft2m',
           'halfs',
           'haversine', 'haversine_',  # XXX removed 'hsin', 'hsin3',
           'heightOf', 'horizon',
           'isantipode', 'issequence',
           'isNumpy2', 'isPoints2', 'isTuple2',
           'iterNumpy2', 'iterNumpy2over',
           'limiterrors',
           'm2degrees', 'm2ft', 'm2km', 'm2NM', 'm2SM',
           'points2', 'polygon', 'property_RO',  # DEPRECATED
           'radians', 'radiansPI_2', 'radiansPI', 'radiansPI2',
           'tan_2', 'tanPI_2_2',
           'unroll180', 'unrollPI', 'unStr',
           'wrap90', 'wrap180', 'wrap360',
           'wrapPI_2', 'wrapPI', 'wrapPI2')
__version__ = '18.10.06'

division = 1 / 2  # double check int division, see .datum.py
if not division:
    raise ImportError('%s 1/2 == %d' % ('division', division))
del division

try:
    _Strs = basestring, str  # PYCHOK .datum.py, .geohash.py
except NameError:
    _Strs = str,

PI2  = PI * 2  #: Two PI, M{PI * 2} (C{float})  # PYCHOK expected
PI_2 = PI / 2  #: Half PI, M{PI / 2} (C{float})

# R_M moved here to avoid circular import for bases and datum
R_M = 6371008.771415  #: Mean, spherical earth radius (C{meter}).

_iterNumpy2len = 1  # adjustable for testing purposes
_limiterrors   = True


class LimitError(ValueError):
    '''Error raised for lat- and/or longitudinal deltas exceeding
       the I{limit} in functions L{equirectangular} and
       L{equirectangular_}.
    '''
    pass


def acos1(x):
    '''Return M{math.acos(max(-1, min(1, x)))}.
    '''
    return acos(max(-1.0, min(1.0, x)))


def anStr(name, OKd='._-', sub='_'):
    '''Make string a valid name of alphanumeric and OKd characters.

       @param name: The original name (str).
       @keyword OKd: Other acceptable characters (str).
       @keyword sub: Substitute for invalid charactes (str).

       @return: The modified name (str).

       @note: Leading and trailing whitespace characters are removed
              and intermediate whitespace characters are coalesced
              and substituted.
    '''
    s = n = str(name).strip()
    for c in n:
        if not (c.isalnum() or c in OKd or c in sub):
            s = s.replace(c, ' ')
    return sub.join(s.strip().split())


def antipode(lat, lon):
    '''Return the antipode, the point diametrically opposite to the
       given lat- and longitude.

       @param lat: Latitude (C{degrees}).
       @param lon: Longitude (C{degrees}).

       @return: 2-Tuple (lat, lon) of the antipodal point
                (C{degrees}, C{degrees180}).

       @see: U{Geosphere<http://CRAN.R-Project.org/web/packages/geosphere/geosphere.pdf>}.
    '''
    return -lat, _wrap(lon + 180, 180, 360)


def degrees90(rad):
    '''Convert and wrap radians to degrees M{(-270..+90]}.

       @param rad: Angle (C{radians}).

       @return: Angle in degrees, wrapped (C{degrees90}).
    '''
    return _wrap(degrees(rad), 90, 360)


def degrees180(rad):
    '''Convert and wrap radians to degrees M{(-180..+180]}.

       @param rad: Angle (C{radians}).

       @return: Angle in degrees, wrapped (C{degrees180}).
    '''
    return _wrap(degrees(rad), 180, 360)


def degrees360(rad):
    '''Convert and wrap radians to degrees M{(0..+360]}.

       @param rad: Angle (C{radians}).

       @return: Angle in degrees, wrapped (C{degrees360}).
    '''
    return _wrap(degrees(rad), 360, 360)


def enStr2(easting, northing, prec, *extras):
    '''Return easting, northing string representations.

       @param easting: Easting from false easting (C{meter}).
       @param northing: Northing from from false northing (C{meter}).
       @param prec: Precision in number of digits (C{int}).
       @param extras: Optional leading items (strings).

       @return: I{extras} + 2-Tuple (eastingStr, northingStr).

       @raise ValueError: Invalid I{prec}.
    '''
    w = prec // 2
    try:
        p10 = (1e-4, 1e-3, 1e-2, 1e-1, 1)[w - 1]  # 10**(5 - w)
    except IndexError:
        raise ValueError('%s invalid: %r' % ('prec', prec))
    return extras + ('%0*d' % (w, int(easting * p10)),
                     '%0*d' % (w, int(northing * p10)))


def equirectangular(lat1, lon1, lat2, lon2, radius=R_M, **options):
    '''Compute the distance between two points using
       the U{Equirectangular Approximation / Projection
       <http://www.Movable-Type.co.UK/scripts/latlong.html>}.

       See function L{equirectangular_} for more details, the
       available I{options} and errors raised.

       @param lat1: Start latitude (C{degrees}).
       @param lon1: Start longitude (C{degrees}).
       @param lat2: End latitude (C{degrees}).
       @param lon2: End longitude (C{degrees}).
       @keyword radius: Optional, mean earth radius (C{meter}).
       @keyword options: Optional keyword arguments for function
                         L{equirectangular_}.

       @return: Distance (C{meter}, same units as I{radius}).

       @see: U{Local, flat earth approximation
             <http://www.EdWilliams.org/avform.htm#flat>}, function
             L{haversine}, method L{Ellipsoid.distance2} and C{LatLon}
             methods C{distanceTo*} for more accurate and/or larger
             distances.
    '''
    _, dy, dx, _ = equirectangular_(lat1, lon1, lat2, lon2, **options)
    return radians(hypot(dx, dy)) * radius


def equirectangular_(lat1, lon1, lat2, lon2,
                     adjust=True, limit=45, wrap=False):
    '''Compute the distance between two points using
       the U{Equirectangular Approximation / Projection
       <http://www.Movable-Type.co.UK/scripts/latlong.html>}.

       This approximation is valid for smaller distance of several
       hundred Km or Miles, see the I{limit} keyword argument and
       the L{LimitError}.

       @param lat1: Start latitude (C{degrees}).
       @param lon1: Start longitude (C{degrees}).
       @param lat2: End latitude (C{degrees}).
       @param lon2: End longitude (C{degrees}).
       @keyword adjust: Adjust the wrapped, unrolled longitudinal
                        delta by the cosine of the mean latitude (C{bool}).
       @keyword limit: Optional limit for the lat- and longitudinal
                       deltas (C{degrees}) or C{None} or 0 for unlimited.
       @keyword wrap: Wrap and L{unroll180} longitudes and longitudinal
                      delta (C{bool}).

       @return: 4-Tuple (distance2, delta_lat, delta_lon, lon2_unroll)
                with the distance in degrees squared, the latitudinal
                delta I{lat2}-I{lat1}, the wrapped, unrolled, and
                adjusted longitudinal delta I{lon2}-I{lon1} and the
                unrollment for I{lon2}.  To convert I{distance2} to
                meter, use M{radians(sqrt(distance2)) * radius} where
                I{radius} is the mean earth radius in the desired units,
                for example L{R_M} meter.

       @raise LimitError: If the lat- and/or longitudinal delta exceeds
                          the I{-limit..+limit} range and I{limiterrors}
                          set to C{True}.

       @see: U{Local, flat earth approximation
             <http://www.EdWilliams.org/avform.htm#flat>}, functions
             L{equirectangular} and L{haversine}, method
             L{Ellipsoid.distance2} and C{LatLon} methods C{distanceTo*}
             for more accurate and/or larger distances.
    '''
    d_lat = lat2 - lat1
    d_lon, ulon2 = unroll180(lon1, lon2, wrap=wrap)

    if limit and _limiterrors \
             and max(abs(d_lat), abs(d_lon)) > limit > 0:
        t = fStr((lat1, lon1, lat2, lon2), prec=4)
        raise LimitError('%s(%s, limit=%s) delta exceeds limit' %
                        ('equirectangular_', t, fStr(limit, prec=2)))

    if adjust:  # scale delta lon
        d_lon *= cos(radians(lat1 + lat2) * 0.5)

    d2 = d_lat**2 + d_lon**2  # degrees squared!
    return d2, d_lat, d_lon, ulon2 - lon2


def false2f(value, name='value', false=True):
    '''Convert a false east-/northing to non-negative float.

       @param value: Value to convert (C{scalar}).
       @keyword name: Optional name of the value (C{str}).
       @keyword false: Optionally, value includes false origin (C{bool}).

       @return: The value (C{float}).

       @raise ValueError: Invalid or negative I{value}.
    '''
    try:
        f = float(value)
        if f < 0 and false:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError('%s invalid: %r' % (name, value))
    return f


def ft2m(feet):
    '''Convert I{International} feet to meter (m).

       @param feet: Value in feet (C{scalar}).

       @return: Value in m (C{float}).
    '''
    return feet * 0.3048  # US Survey 1200./3937. == 0.3048006096012192


def halfs(str2):
    '''Split a string in 2 halfs.

       @param str2: String to split (C{str}).

       @return: 2-Tuple (1st, 2nd) half (C{str}s).

       @raise ValueError: Zero or odd C{len}(I{str2}).
    '''
    h, r = divmod(len(str2), 2)
    if r or not h:
        raise ValueError('%s invalid: %r' % ('str2', str2))
    return str2[:h], str2[h:]


def haversine(lat1, lon1, lat2, lon2, radius=R_M, wrap=False):
    '''Compute the distance between two points using the U{Haversine
       <http://www.Movable-Type.co.UK/scripts/latlong.html>} formula.

       @param lat1: Start latitude (C{degrees}).
       @param lon1: Start longitude (C{degrees}).
       @param lat2: End latitude (C{degrees}).
       @param lon2: End longitude (C{degrees}).
       @keyword radius: Optional, mean earth radius (C{meter}).
       @keyword wrap: Wrap and L{unrollPI} longitudes (C{bool}).

       @return: Distance (C{meter}, same units as I{radius}).

       @see: U{Distance between two (spherical) points
             <http://www.EdWilliams.org/avform.htm#Dist>}, functions
             L{equirectangular}, L{Ellipsoid.distance2} or I{LatLon}
             methods I{distanceTo*} and I{equirectangularTo}.
    '''
    d, lon2 = unroll180(lon1, lon2, wrap=wrap)
    r = haversine_(radians(lat2), radians(lat1), radians(d))
    return r * float(radius)


def haversine_(a2, a1, b21):
    '''Compute the I{angular} distance between two points using the
       U{Haversine<http://www.Movable-Type.co.UK/scripts/latlong.html>}
       formula.

       @param a2: End latitude (C{radians}).
       @param a1: Start latitude (C{radians}).
       @param b21: Longitudinal delta, M{end-start} (C{radians}).

       @return: Angular distance (C{radians}).

       @see: Function L{haversine}.
    '''
    def _hsin(rad):
        return sin(rad * 0.5)**2

    h = _hsin(a2 - a1) + cos(a1) * cos(a2) * _hsin(b21)  # haversine
    try:
        r = atan2(sqrt(h), sqrt(1 - h)) * 2  # == asin(sqrt(h)) * 2
    except ValueError:
        r = 0 if h < 0.5 else PI
    return r


def heightOf(angle, distance, radius=R_M):
    '''Determine the height above the (spherical) earth after
       traveling along a straight line at a given tilt.

       @param angle: Tilt angle above horizontal (C{degrees}).
       @param distance: Distance along the line (C{meter} or same units
                        as I{radius}).
       @keyword radius: Optional mean earth radius (C{meter}).

       @return: Height (C{meter}, same units as I{distance} and I{radius}).

       @raise ValueError: Invalid I{angle}, I{distance} or I{radius}.

       @see: U{MultiDop GeogBeamHt<http://GitHub.com/NASA/MultiDop>}
             (U{Shapiro et al. 2009, JTECH
             <http://journals.AMetSoc.org/doi/abs/10.1175/2009JTECHA1256.1>}
             and U{Potvin et al. 2012, JTECH
             <http://journals.AMetSoc.org/doi/abs/10.1175/JTECH-D-11-00019.1>}).
    '''
    d, r = distance, radius
    if d > r:
        d, r = r, d

    if d > EPS:
        d = d / float(r)
        s = sin(radians(angle))
        s = fsum_(1, 2 * s * d, d**2)
        if s > 0:
            return r * sqrt(s) - float(radius)

    raise ValueError('%s%r' % ('heightOf', (angle, distance, radius)))


def horizon(height, radius=R_M, refraction=False):
    '''Determine the distance to the horizon from a given altitude
       above the (spherical) earth.

       @param height: Altitude (C{meter} or same units as I{radius}).
       @keyword radius: Optional mean earth radius (C{meter}).
       @keyword refraction: Consider atmospheric refraction (C{bool}).

       @return: Distance (C{meter}, same units as I{height} and I{radius}).

       @raise ValueError: Invalid I{height} or I{radius}.

       @see: U{Distance to horizon<http://www.EdWilliams.org/avform.htm#Horizon>}.
    '''
    if min(height, radius) < 0:
        raise ValueError('%s%r' % ('horizon', (height, radius)))

    if refraction:
        d2 = 2.415750694528 * height * radius  # 2.0 / 0.8279
    else:
        d2 = height * fsum_(radius, radius, height)
    return sqrt(d2)


def isantipode(lat1, lon1, lat2, lon2, eps=EPS):
    '''Check whether two points are anitpodal, on diametrically
       opposite sides of the earth.

       @param lat1: Latitude of one point (C{degrees}).
       @param lon1: Longitude of one point (C{degrees}).
       @param lat2: Latitude of the other point (C{degrees}).
       @param lon2: Longitude of the other point (C{degrees}).
       @keyword eps: Tolerance for near-equality (C{degrees}).

       @return: C{True} if points are antipodal within the
                I{eps} tolerance, C{False} otherwise.

       @see: U{Geosphere<http://CRAN.R-Project.org/web/packages/geosphere/geosphere.pdf>}.
    '''
    return abs( lat1 + lat2) < eps and \
           abs((lon1 - lon2) % 360 - 180) < eps


def isNumpy2(obj):
    '''Check for an I{Numpy2LatLon} points wrapper.

       @param obj: The object (any C{type}).

       @return: C{True} if I{obj} is an I{Numpy2LatLon}
                instance, C{False} otherwise.
    '''
    # isinstance(self, (Numpy2LatLon, ...))
    return getattr(obj, 'isNumpy2', False)


def isPoints2(obj):
    '''Check for an I{LatLon2psxy} points wrapper.

       @param obj: The object (any C{type}).

       @return: C{True} if I{obj} is an I{LatLon2psxy}
                instance, C{False} otherwise.
    '''
    # isinstance(self, (LatLon2psxy, ...))
    return getattr(obj, 'isPoints2', False)


def issequence(obj, *excluded):
    '''Check for sequence types.

       @param obj: The object (any C{type}).
       @param excluded: Optional, exclusions (C{type}s).

       @note: Excluding C{tuple} implies excluding C{namedtuple}.

       @return: C{True} if I{obj} is a sequence, C{False} otherwise.
    '''
    if excluded:
        return isinstance(obj, _Seqs) and not \
               isinstance(obj, excluded)
    else:
        return isinstance(obj, _Seqs)


def isTuple2(obj):
    '''Check for an I{Tuple2LatLon} points wrapper.

       @param obj: The object (any).

       @return: C{True} if I{obj} is an I{Tuple2LatLon}
                instance, C{False} otherwise.
    '''
    # isinstance(self, (Tuple2LatLon, ...))
    return getattr(obj, 'isTuple2', False)


def iterNumpy2(obj):
    '''Iterate over Numpy2 wrappers or other sequences exceeding
       the threshold.

       @param obj: Points array, list, sequence, set, etc. (any).

       @return: C{True} do, C{False} don't iterate.
    '''
    try:
        return isNumpy2(obj) or len(obj) > _iterNumpy2len
    except TypeError:
        return False


def iterNumpy2over(n=None):
    '''Get or set the L{iterNumpy2} threshold.

       @keyword n: Optional, new threshold (C{int}).

       @return: Previous threshold (C{int}).

       @raise ValueError: Invalid I{n}.
    '''
    global _iterNumpy2len
    p = _iterNumpy2len
    if n is not None:
        try:
            i = int(n)
            if i > 0:
                _iterNumpy2len = i
            else:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError('%s invalid: %r' % ('n', n))
    return p


def limiterrors(raiser=None):
    '''Get/set the raising of limit errors.

       @keyword raiser: Choose C{True} to raise or C{False} to
                        ignore L{LimitError} exceptions.  Use
                        C{None} to leave the setting unchanged.

       @return: Previous setting (C{bool}).
    '''
    global _limiterrors
    t = _limiterrors
    if raiser in (True, False):
        _limiterrors = raiser
    return t


def m2degrees(meter, radius=R_M):
    '''Convert distance to angle along equator.

       @param meter: Value in meter (C{scalar}).

       @return: Equatorial angle in degrees (C{float}).

       @raise ValueError: Invalid I{radius}.
    '''
    if radius < EPS:
        raise ValueError('%s invalid: %r' % ('radius', radius))
    return degrees(meter / radius)


def m2ft(meter):
    '''Convert meter to I{International} feet (ft).

       @param meter: Value in meter (C{scalar}).

       @return: Value in ft (C{float}).
    '''
    return meter * 3.2808399  # US Survey == 3937./1200. = 3.2808333333333333


def m2km(meter):
    '''Convert meter to kilo meter (km).

       @param meter: Value in meter (C{scalar}).

       @return: Value in km (C{float}).
    '''
    return meter * 1.0e-3


def m2NM(meter):
    '''Convert meter to nautical miles (NM).

       @param meter: Value in meter (C{scalar}).

       @return: Value in NM (C{float}).
    '''
    return meter * 5.39956804e-4  # == * 1.0 / 1852.0


def m2SM(meter):
    '''Convert meter to statute miles (SM).

       @param meter: Value in meter (C{scalar}).

       @return: Value in SM (C{float}).
    '''
    return meter * 6.21369949e-4  # XXX 6.213712e-4 == 1.0 / 1609.344


def points2(points, closed=True, base=None):
    '''Check a polygon or path represented as an array, generator,
       iterable, list, set, tuple or other sequence of points.

       @param points: The points (I{LatLon}[])
       @keyword closed: Optionally, treat the I{points} as a closed
                        polygon or path and remove any duplicate or
                        closing final I{points} (C{bool}).
       @keyword base: Optionally, check I{points} against this
                      base class C{None}.

       @return: 2-Tuple (number, ...) of points (C{int}, C{list} or
                C{tuple}).

       @raise TypeError: Some I{points} are not I{LatLon}.

       @raise ValueError: Insufficient number of I{points}.
    '''
    n, points = len2(points)

    if closed:
        # remove duplicate or closing final points
        while n > 1 and (points[n-1] == points[0] or
                         points[n-1] == points[n-2]):
            n -= 1
        # XXX following line is unneeded if points
        # are always indexed as ... i in range(n)
        points = points[:n]  # XXX numpy.array slice is a view!

    if n < (3 if closed else 1):
        raise ValueError('too few points: %s' % (n,))

    if base and not (isNumpy2(points) or isTuple2(points)):
        for i in range(n):
            base.others(points[i], name='points[%s]' % (i,))

    return n, points


def polygon(points, closed=True, base=None):
    '''DEPRECATED, use function L{points2}.
    '''
    return points2(points, closed=closed, base=base)


def property_RO(method):
    '''Decorator for C{Read_Only} property.

       @param method: The callable to be decorated as C{property.getter}.

       @note: Like standard Python C{property} without a C{property.setter}
              with a more descriptive error message when set.
    '''
    def Read_Only(self, ignored):
        '''Throws an C{AttributeError}, always.
        '''
        raise AttributeError('Read_Only property: %r.%s = %r' %
                             (self, method.__name__, ignored))

    return property(method, Read_Only, None, method.__doc__ or 'N/A')


def radiansPI(deg):
    '''Convert and wrap degrees to radians M{(-PI..+PI]}.

       @param deg: Angle (C{degrees}).

       @return: Radians, wrapped (C{radiansPI})
    '''
    return _wrap(radians(deg), PI, PI2)


def radiansPI2(deg):
    '''Convert and wrap degrees to radians M{(0..+2PI]}.

       @param deg: Angle (C{degrees}).

       @return: Radians, wrapped (C{radiansPI2})
    '''
    return _wrap(radians(deg), PI2, PI2)


def radiansPI_2(deg):
    '''Convert and wrap degrees to radians M{(-3PI/2..+PI/2]}.

       @param deg: Angle (C{degrees}).

       @return: Radians, wrapped (C{radiansPI_2})
    '''
    return _wrap(radians(deg), PI_2, PI2)


def tan_2(rad):
    '''Compute the tangent of half angle.

       @param rad: Angle (C{radians}).

       @return: M{tan(rad / 2)} (C{float}).
    '''
    return tan(rad * 0.5)


def tanPI_2_2(rad):
    '''Compute the tangent of half angle, 90 degrees rotated.

       @param rad: Angle (C{radians}).

       @return: M{tan((rad + PI/2) / 2)} (C{float}).
    '''
    return tan((rad + PI_2) * 0.5)


def unroll180(lon1, lon2, wrap=True):
    '''Unroll longitudinal delta and wrap longitude in degrees.

       @param lon1: Start longitude (C{degrees}).
       @param lon2: End longitude (C{degrees}).
       @keyword wrap: Wrap and unroll to the M{(-180..+180]} range (C{bool}).

       @return: 2-Tuple (delta I{lon2}-I{lon1}, I{lon2}) unrolled
                (C{degrees}, C{degrees}).

       @see: Capability I{LONG_UNROLL} in U{GeographicLib
       <http://GeographicLib.SourceForge.io/html/python/interface.html#outmask>}.
    '''
    d = lon2 - lon1
    if wrap and abs(d) > 180:
        u = _wrap(d, 180, 360)
        if u != d:
            return u, lon1 + u
    return d, lon2


def unrollPI(rad1, rad2, wrap=True):
    '''Unroll longitudinal delta and wrap longitude in radians.

       @param rad1: Start longitude (C{radians}).
       @param rad2: End longitude (C{radians}).
       @keyword wrap: Wrap and unroll to the M{(-PI..+PI]} range (C{bool}).

       @return: 2-Tuple (delta I{rad2}-I{rad1}, I{rad2}) unrolled
                (C{radians}, C{radians}).

       @see: Capability I{LONG_UNROLL} in U{GeographicLib
       <http://GeographicLib.SourceForge.io/html/python/interface.html#outmask>}.
    '''
    r = rad2 - rad1
    if wrap and abs(r) > PI:
        u = _wrap(r, PI, PI2)
        if u != r:
            return u, rad1 + u
    return r, rad2


def unStr(name, *args, **kwds):
    '''Return the string representation of an invokation.

       @param name: Function, method or class name (C{str}).
       @param args: Optional positional arguments.
       @keyword kwds: Optional keyword arguments.

       @return: Representation (C{str}).
    '''
    t = tuple('%s=%s' % t for t in sorted(kwds.items()))
    if args:
        t = map2(str, args) + t
    return '%s(%s)' % (name, ', '.join(t))


def _wrap(angle, wrap, limit):
    '''(INTERNAL) Angle wrapper M{((wrap-limit)..+wrap]}.

       @param angle: Angle (C{radians} or C{degrees}).
       @param wrap: Range (C{radians} or C{degrees}).
       @param limit: Upper limit (PI2 C{radians} or 360 C{degrees}).

       @return: The I{angle}, wrapped (C{radians} or C{degrees}).
    '''
    if not wrap >= angle > (wrap - limit):
        # math.fmod(-1.5, 3.14) == -1.5, but -1.5 % 3.14 == 1.64
        # math.fmod(-1.5, 360) == -1.5, but -1.5 % 360 == 358.5
        angle %= limit
        if angle > wrap:
            angle -= limit
    return angle


def wrap90(deg):
    '''Wrap degrees to M{(-270..+90]}.

       @param deg: Angle (C{degrees}).

       @return: Degrees, wrapped (C{degrees90}).
    '''
    return _wrap(deg, 90, 360)


def wrap180(deg):
    '''Wrap degrees to M{(-180..+180]}.

       @param deg: Angle (C{degrees}).

       @return: Degrees, wrapped (C{degrees180}).
    '''
    return _wrap(deg, 180, 360)


def wrap360(deg):
    '''Wrap degrees to M{(0..+360]}.

       @param deg: Angle (C{degrees}).

       @return: Degrees, wrapped (C{degrees360}).
    '''
    return _wrap(deg, 360, 360)


def wrapPI(rad):
    '''Wrap radians to M{(-PI..+PI]}.

       @param rad: Angle (C{radians}).

       @return: Radians, wrapped (C{radiansPI}).
    '''
    return _wrap(rad, PI, PI2)


def wrapPI2(rad):
    '''Wrap radians to M{(0..+2PI]}.

       @param rad: Angle (C{radians}).

       @return: Radians, wrapped (C{radiansPI2}).
    '''
    return _wrap(rad, PI2, PI2)


def wrapPI_2(rad):
    '''Wrap radians to M{(-3PI/2..+PI/2]}.

       @param rad: Angle (C{radians}).

       @return: Radians, wrapped (C{radiansPI_2}).
    '''
    return _wrap(rad, PI_2, PI2)

# **) MIT License
#
# Copyright (C) 2016-2018 -- mrJean1 at Gmail dot com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
