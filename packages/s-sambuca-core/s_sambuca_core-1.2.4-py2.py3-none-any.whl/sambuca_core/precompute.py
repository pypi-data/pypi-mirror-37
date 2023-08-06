import math
import numpy as np

def precompute_vals(bb_lambda_ref,
               wavelengths,
               a_cdom_lambda0cdom,
               a_cdom_slope,
               lambda0cdom,
               a_nap_lambda0nap,
               a_nap_slope,
               lambda0nap,
               lambda0x,
               bb_ph_slope,
               x_ph_lambda0x,
               bb_nap_slope,
               x_nap_lambda0x,
               water_refractive_index,
               theta_air,
               off_nadir):

    # Sub-surface solar zenith angle in radians
    inv_refractive_index = 1.0 / water_refractive_index
    theta_w = \
        math.asin(inv_refractive_index * math.sin(math.radians(theta_air)))

    # Sub-surface viewing angle in radians
    theta_o = \
        math.asin(inv_refractive_index * math.sin(math.radians(off_nadir)))

    inv_cos_theta_w = 1.0 / math.cos(theta_w)
    inv_cos_theta_0 = 1.0 / math.cos(theta_o)

    # Calculate derived SIOPS, based on
    # Mobley, Curtis D., 1994: Radiative Transfer in natural waters.
    bb_water = (0.00194 / 2.0) * np.power(bb_lambda_ref / wavelengths, 4.32)
    a_cdom_star = a_cdom_lambda0cdom * \
        np.exp(-a_cdom_slope * (wavelengths - lambda0cdom))
    a_nap_star = a_nap_lambda0nap * \
        np.exp(-a_nap_slope * (wavelengths - lambda0nap))

    # Calculate backscatter
    backscatter = np.power(lambda0x / wavelengths, bb_ph_slope)
    # specific backscatter due to phytoplankton
    bb_ph_star = x_ph_lambda0x * backscatter
    # specific backscatter due to NAP
     # If a bb_nap_slope value has been supplied, use it.
     # Otherwise, reuse bb_ph_slope.
    if bb_nap_slope:
        backscatter = np.power(lambda0x / wavelengths, bb_nap_slope)
    bb_nap_star = x_nap_lambda0x * backscatter

    return (bb_water, a_cdom_star, a_nap_star,
            bb_ph_star, bb_nap_star, inv_cos_theta_w, inv_cos_theta_0)
