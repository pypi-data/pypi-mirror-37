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

"""This module contain the function qasm2svg.

The function qasm2svg draw a quantum circuit as a SVG image string.
"""

from typing import Tuple, Union

import qiskit

from qasm2image.svg import _drawing

QubitType = Tuple[qiskit.QuantumRegister, int]


def qasm2svg(qasm_str: str,
             basis: str = ('id,u0,u1,u2,u3,x,y,z,h,s,sdg,t,tdg,rx,ry,rz,'
                           'cx,cy,cz,ch,crz,cu1,cu3,swap,ccx'),
             show_clbits: bool = True, output_dimensions: bool = False) -> \
    Union[str, Tuple[str, Tuple[int, int]]]:
    """Transform a QASM code to an SVG file.

    This method output the SVG representation of the quantum circuit
    provided as a QASM program.

    Remark: not all gates are implemented. If a gate is not implemented
            then a message will be printed to warn the user and the gate
            will not be drawn in the SVG.
            If you want to implement more gates see the _draw_gate method
            in ./svg/drawing.py.

    Args:
        qasm_str    (str) : The QASM quantum circuit to draw in SVG.
        basis       (list): The gate basis used to represent the circuit as a
                            comma-separated string of names.
        show_clbits (bool): Flag that control the drawing of classical bit
                            lines.
        output_dimensions (bool): Flag that control the output of the function.
                            If set to True, the return type will be (str,
                            (str, str))
                            for (SVG, (width, height)). Else, the function
                            will only
                            return the SVG representation.
    Returns:
        Union[str, Tuple[str, Tuple[int, int]]]: SVG or (SVG, (width, height))
    """

    # Uncompile the QASM code to recover the gates to draw.
    ast = qiskit.qasm.Qasm(data=qasm_str).parse()
    unroller = qiskit.unroll.Unroller(ast, qiskit.unroll.JsonBackend(
        basis.split(',')))
    unroller.execute()
    json_circuit = unroller.backend.circuit

    svg_repr, (width, height) = _drawing.draw_json_circuit(json_circuit,
                                                           show_clbits=show_clbits)
    if not output_dimensions:
        return svg_repr

    return svg_repr, (width, height)
