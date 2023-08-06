# -*- coding: utf-8 -*-

import sys
import os
import re
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from rdftransformer import Annotation


"""
UMT/WGS-84 Conversion based on (c) Chris Veness 2014-2017 [MIT Licence]
GitHub: https://github.com/chrisveness/geodesy
"""
class UTM:
	def __init__(self, zone, hemisphere, easting, northing, convergence = None, scale = None):
		default_datum = {
			"a": 6378137,
			"b": 6356752.314245,
			"f": 1/298.257223563
		}
		if not (1<=zone and zone<=60):
			raise Exception("Invalid UTM zone: " + str(zone))

		if not re.match("(?i)[NS]", hemisphere):
			raise Exception("Invalid UTM hemisphere: " + hemisphere)

		self.zone = zone
		self.hemisphere = hemisphere.upper()
		self.easting = easting
		self.northing = northing
		self.datum = default_datum
		self.convergence = convergence
		self.scale = scale

	def toLatLon(self):
		z = self.zone
		h = self.hemisphere
		x = self.easting
		y = self.northing

		falseEasting = 500e3
		falseNorthing = 10000e3

		a = self.datum["a"]
		f = self.datum["f"]

		k0 = 0.9996

		x = x - falseEasting
		y = y - falseNorthing if h == "S" else y

		
		e = math.sqrt(f*(2-f))
		n = f/(2-f)
		n2 = math.pow(n, 2)
		n3 = math.pow(n, 3)
		n4 = math.pow(n, 4)
		n5 = math.pow(n, 5)
		n6 = math.pow(n, 6)

		A = (float(a)/(1+n)) * (1 + float(1)/4*n2 + float(1)/64*n4 + float(1)/256*n6)

		eta = x / (k0*A)
		xi = y / (k0*A)

		beta = [
			None,
			float(1)/2*n - float(2)/3*n2 + float(37)/96*n3 - float(1)/360*n4 - float(81)/512*n5 + float(96199)/604800*n6,
			float(1)/48*n2 +  float(1)/15*n3 - float(437)/1440*n4 + float(46)/105*n5 - float(1118711)/3870720*n6,
			float(17)/480*n3 - float(37)/840*n4 - float(209)/4480*n5 + float(5569)/90720*n6,
			float(4397)/161280*n4 - float(11)/504*n5 - float(830251)/7257600*n6,
			float(4583)/161280*n5 -  float(108847)/3991680*n6,
			float(20648693)/638668800*n6
		]

		eta1 = eta
		xi1 = xi
		for j, value in enumerate(beta[1:]):
			j = j+1
			eta1 -= value * math.cos(2*j*xi) * math.sinh(2*j*eta)
			xi1 -= value * math.sin(2*j*xi) * math.cosh(2*j*eta)

		sinh_eta1 = math.sinh(eta1)
		sin_xi1 = math.sin(xi1)
		cos_xi1 = math.cos(xi1)

		tau1 = sin_xi1/math.sqrt(sinh_eta1*sinh_eta1 + cos_xi1*cos_xi1)

		tau_i = tau1
		while True:
			sigma_i = math.sinh(e*math.atanh(e*tau_i/math.sqrt(1+tau_i*tau_i)))
			tau_i1 = tau_i * math.sqrt(1+sigma_i*sigma_i) - sigma_i * math.sqrt(1+tau_i*tau_i)
			delta_tau_i = (tau1 - tau_i1)/math.sqrt(1+tau_i1*tau_i1)*(1 + (1-e*e)*tau_i*tau_i)/((1-e*e)*math.sqrt(1+tau_i*tau_i))
			tau_i += delta_tau_i

			if math.fabs(delta_tau_i) <= 1e-12:
				break

		tau = tau_i

		phi = math.atan(tau)

		lamb = math.atan2(sinh_eta1, cos_xi1)

		p = 1
		q = 0
		for j, value in enumerate(beta[1:]):
			j = j+1
			p -= 2*j*value*math.cos(2*j*xi)*math.cosh(2*j*eta)
			q += 2*j*value*math.sin(2*j*xi)*math.sinh(2*j*eta)

		gamma1 = math.atan(math.tan(xi1) * math.tanh(eta1))
		gamma2 = math.atan2(q, p)

		gamma = gamma1 + gamma2

		sin_phi = math.sin(phi)
		k1 = math.sqrt(1-e*e*sin_phi*sin_phi) * math.sqrt(1+tau*tau)*math.sqrt(sinh_eta1*sinh_eta1+cos_xi1*cos_xi1)
		k2 = A / a / math.sqrt(p*p + q*q)

		k = k0 * k1 * k2

		lamb0 = math.radians((z-1)*6-180+3)
		lamb += lamb0

		lat = math.degrees(phi)
		lon = math.degrees(lamb)
		convergence = math.degrees(gamma)
		scale = k

		return lat, lon



