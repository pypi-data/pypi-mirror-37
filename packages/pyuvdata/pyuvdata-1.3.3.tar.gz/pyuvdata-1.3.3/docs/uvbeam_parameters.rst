UVBeam Parameters
======================================
These are the standard attributes of UVBeam objects.

Under the hood they are actually properties based on UVParameter objects.

Required
----------------
These parameters are required to have a sensible UVBeam object and 
are required for most kinds of beam files.

**Naxes_vec**
     Number of basis vectors specified at each pixel, options are 2 or 3 (or 1 if beam_type is "power")

**Nfreqs**
     Number of frequency channels

**Nspws**
     Number of spectral windows (ie non-contiguous spectral chunks). More than one spectral window is not currently supported.

**antenna_type**
     String indicating antenna type. Allowed values are "simple", and "phased_array"

**bandpass_array**
     Frequency dependence of the beam. Depending on the data_normalization, this may contain only the frequency dependence of the receiving chain ("physical" normalization) or all the frequency dependence ("peak" normalization).

**beam_type**
     String indicating beam type. Allowed values are "efield", and "power".

**data_array**
     Depending on beam type, either complex E-field values ("efield" beam type) or power values ("power" beam type) for beam model. units are linear normalized to either peak or solid angle as given by data_normalization. The shape depends on the beam_type and pixel_coordinate_system, if it is "healpix", the shape is: (Naxes_vec, Nspws, Nfeeds or Npols, Nfreqs, Npixels), otherwise it is (Naxes_vec, Nspws, Nfeeds or Npols, Nfreqs, Naxes2, Naxes1)

**data_normalization**
     Normalization standard of data_array, options are: "physical", "peak" or "solid_angle". Physical normalization means that the frequency dependence of the antenna sensitivity is included in the data_array while the frequency dependence of the receiving chain is included in the bandpass_array. Peak normalized means that for each frequency the data_arrayis separately normalized such that the peak is 1 (so the beam is dimensionless) and all direction-independent frequency dependence is moved to the bandpass_array (if the beam_type is "efield", then peak normalized means that the absolute value of the peak is 1). Solid angle normalized means the peak normalized beam is divided by the integral of the beam over the sphere, so the beam has dimensions of 1/stradian.

**feed_name**
     Name of physical feed (string)

**feed_version**
     Version of physical feed (string)

**freq_array**
     Array of frequencies, shape (Nspws, Nfreqs), units Hz

**history**
     String of history, units English

**model_name**
     Name of beam model (string)

**model_version**
     Version of beam model (string)

**pixel_coordinate_system**
     Pixel coordinate system, options are: "az_za", "orthoslant_zenith", "healpix". "az_za" is a uniformly gridded azimuth, zenith angle coordinate system, where az runs from East to North in radians. It has axes [azimuth, zen_angle]. "orthoslant_zenith" is a orthoslant projection at zenith where y points North, x point East. It has axes [zenorth_x, zenorth_y]. "healpix" is a HEALPix map with zenith at the north pole and az, za coordinate axes (for the basis_vector_array) where az runs from East to North. It has axes [hpx_inds].

**spw_array**
     Array of spectral window Numbers, shape (Nspws)

**telescope_name**
     Name of telescope (string)

Optional
----------------
These parameters are defined by one or more file standard but are not always required.
Some of them are required depending on the beam_type, antenna_type and pixel_coordinate_systems (as noted below).

**Naxes1**
     Number of elements along the first pixel axis. Not required if pixel_coordinate_system is "healpix".

**Naxes2**
     Number of elements along the second pixel axis. Not required if pixel_coordinate_system is "healpix".

**Ncomponents_vec**
     Number of basis vectors components specified at each pixel, options are 2 or 3.  Only required for E-field beams.

**Nelements**
     Required if antenna_type = "phased_array". Number of elements in phased array

**Nfeeds**
     Number of feeds. Not required if beam_type is "power".

**Npixels**
     Number of healpix pixels. Only required if pixel_coordinate_system is "healpix".

**Npols**
     Number of polarizations. Only required if beam_type is "power".

**axis1_array**
     Coordinates along first pixel axis. Not required if pixel_coordinate_system is "healpix".

**axis2_array**
     Coordinates along second pixel axis. Not required if pixel_coordinate_system is "healpix".

**basis_vector_array**
     Beam basis vector components -- directions for which the electric field values are recorded in the pixel coordinate system. Not required if beam_type is "power". The shape depends on the pixel_coordinate_system, if it is "healpix", the shape is: (Naxes_vec, Ncomponents_vec, Npixels), otherwise it is (Naxes_vec, Ncomponents_vec, Naxes2, Naxes1)

**coupling_matrix**
     Required if antenna_type = "phased_array". Matrix of complex element couplings, units: dB, shape: (Nelements, Nelements, Nfeed, Nfeed, Nspws, Nfreqs)

**delay_array**
     Required if antenna_type = "phased_array". Array of element delays, units: seconds, shape: (Nelements)

**element_coordinate_system**
     Required if antenna_type = "phased_array". Element coordinate system, options are: N-E or x-y

**element_location_array**
     Required if antenna_type = "phased_array". Array of element locations in element coordinate system,  shape: (2, Nelements)

**extra_keywords**
     Any user supplied extra keywords, type=dict. Keys should be 8 character or less strings if writing to beam fits files. Use the special key "comment" for long multi-line string comments.

**feed_array**
     Array of feed orientations. shape (Nfeeds). options are: N/E or x/y or R/L. Not required if beam_type is "power".

**gain_array**
     Required if antenna_type = "phased_array". Array of element gains, units: dB, shape: (Nelements)

**interpolation_function**
     String indicating interpolation function. Must be set to use the interp_* methods. Allowed values are : "az_za_simple".

**loss_array**
     Array of antenna losses, shape (Nspws, Nfreqs), units dB?

**mismatch_array**
     Array of antenna-amplifier mismatches, shape (Nspws, Nfreqs), units ?

**nside**
     Healpix nside parameter. Only required if pixel_coordinate_system is "healpix".

**ordering**
     Healpix ordering parameter, allowed values are "ring" and "nested". Only required if pixel_coordinate_system is "healpix".

**pixel_array**
     Healpix pixel numbers. Only required if pixel_coordinate_system is "healpix".

**polarization_array**
     Array of polarization integers, shape (Npols). Uses the same convention as UVData: pseudo-stokes 1:4 (pI, pQ, pU, pV);  circular -1:-4 (RR, LL, RL, LR); linear -5:-8 (XX, YY, XY, YX). Only required if beam_type is "power".

**receiver_temperature_array**
     Array of receiver temperatures, shape (Nspws, Nfreqs), units K

**reference_input_impedance**
     Reference input impedance of the receiving chain (sets the reference for the S parameters), units: Ohms

**reference_output_impedance**
     Reference output impedance of the receiving chain (sets the reference for the S parameters), units: Ohms

**s_parameters**
     S parameters of receiving chain, shape (4, Nspws, Nfreqs), ordering: s11, s12, s21, s22. see https://en.wikipedia.org/wiki/Scattering_parameters#Two-Port_S-Parameters

last updated: 2018-08-23