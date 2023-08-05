# -*- coding: utf-8 -*-

from .moduli import youngs, bulk, pr
from .moduli import mu, lam, pmod
from .moduli import vp, vs, moduli_dict

from .fluidsub import avseth_gassmann, smith_gassmann
from .fluidsub import vrh, rhogas, rhosat
from .fluidsub import avseth_fluidsub, smith_fluidsub

from .anisotropy import backus_parameters, backus
from .anisotropy import backus_quality_factor, thomsen_parameters
from .anisotropy import dispersion_parameter, blangy
from .anisotropy import crack_density
from .anisotropy import hudson_delta_M, hudson_delta_G
from .anisotropy import hudson_quality_factor, hudson_inverse_Q_ratio

from .elastic import elastic_impedance
