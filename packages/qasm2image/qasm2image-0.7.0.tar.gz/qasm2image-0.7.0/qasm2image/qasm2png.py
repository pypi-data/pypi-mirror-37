# ======================================================================
# Copyright CERFACS (February 2018)
# Contributor: Adrien Suau (suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

"""This module provide the qasm2png function."""

from math import sqrt

from cairocffi import CairoError
from cairosvg import svg2png

from qasm2image import qasm2svg
from qasm2image.svg import _constants as constants


def qasm2png(qasm_str: str,
             basis: str = ('id,u0,u1,u2,u3,x,y,z,h,s,sdg,t,tdg,rx,ry,rz,'
                           'cx,cy,cz,ch,crz,cu1,cu3,swap,ccx'),
             show_clbits: bool = True, scale: float = 1.0) -> bytes:
    """Transform a QASM code to a PNG file.

    This method output the PNG representation of the quantum circuit
    provided as a QASM program.

    Remark: not all gates are implemented. If a gate is not implemented
            then a message will be printed to warn the user and the gate
            will not be drawn in the PNG.
            If you want to implement more gates see the _draw_gate method
            in ./svg/drawing.py.

    Args:
        qasm_str    (str)  : The QASM quantum circuit to draw in PNG.
        basis       (list) : The gate basis used to represent the circuit.
        show_clbits (bool) : Flag that control the drawing of classical bit
                             lines.
        scale       (float): The scaling imposed to the produced PNG file.

    Returns:
        bytes: The PNG representation of the given QASM circuit.

    Raises:
        CairoError: if cairo (the backend used to transform SVG to PNG)
                    failed at one step. The error resulting of an
                    invalid size (typically raised because the output
                    PNG file is too large) is catched an will never be
                    thrown by this function.
    """

    # Generate the SVG first.
    svg, (width, height) = qasm2svg.qasm2svg(qasm_str, basis=basis,
                                             show_clbits=show_clbits,
                                             output_dimensions=True)
    # Adapt scaling if needed
    # Here scale is a square root because the scaling coefficient will be
    # applied
    # to width *and* to height, and not only to the pixel number.
    scale = min(scale, sqrt(constants.MAX_PNG_SIZE_PX / (width * height)))

    # And generate PNG
    succeed = False
    while not succeed:
        try:
            png_bytes = svg2png(bytestring=svg.encode('utf-8'), scale=scale)
        except CairoError as cairo_error:
            # If the error is caused by a too huge size then reduce the scaling
            if 'CAIRO_STATUS_INVALID_SIZE' in str(cairo_error):
                scale /= 2
            # Else, raise again the exception to warn the calling context
            else:
                raise cairo_error
        else:
            # If no exception occurred, then we can exit our loop.
            succeed = True

    return png_bytes
