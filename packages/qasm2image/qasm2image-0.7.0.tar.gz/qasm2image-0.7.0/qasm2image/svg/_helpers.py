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

"""This module groups useful functions for qasm2svg.

The functions here are used in many places in the code of qasm2svg
and needed to be in a separate module.
"""
import os
from typing import Tuple, Sequence, Union

from qasm2image.svg import _constants, _types

QubitType = Tuple[str, int]


def get_x_from_index(index: int) -> int:
    """Compute the x-coordinate with the provided x index.

    This method compute the x coordinate associated with the
    given x index. The returned value has the same dimension as
    the constants provided in _constants.py.

    Parameters:
        index (int): The circuit representation is divided in
                     columns. In each column fits a gate and some
                     additional space for gate separation. The
                     provided index represent the column in which
                     we want to plot.

    Returns:
      int: The *center* of the column that corresponds to the given
           index.
              ___________
             |           |
             |           |
             |           |
             |           |
              ‾‾‾‾‾‾‾‾‾‾‾
             ^     ^
             |     returned value
             not returned value

    """
    x_coord = _constants.REGISTER_NAME_WIDTH
    x_coord += _constants.GATE_LEFT_BORDER
    x_coord += index * (
        _constants.GATE_SIZE + _constants.GATE_HORIZONTAL_SPACING)
    x_coord += _constants.GATE_SIZE / 2
    return x_coord


def get_y_from_quantum_register(qreg_index_in_json: int,
                                bit_mapping: dict) -> int:
    """Compute the y-coordinate associated to the given quantum register.

    This method assumes that all the quantum registers are drawn *before* the
    classical ones.

    Parameter:
        quantum_register_index_in_JSON (int): identifier of the quantum
               register from the JSON circuit representation.
        bit_mapping (dict): the map that stores the correspondances between
               bits indices in the JSON circuit and the desired output
               indices.
               Structure:
                  {'qubits': {index_in_JSON : index_in_drawing},
                   'clbits': {index_in_JSON : index_in_drawing}}
    Returns:
      int: The y-coordinate of the line representing the quantum register
           number quantum_register_index.
    """
    y_coord = _constants.VERTICAL_BORDER
    index_to_draw = bit_mapping['qubits'][qreg_index_in_json]
    y_coord += index_to_draw * _constants.REGISTER_LINES_VERTICAL_SPACING
    return y_coord


def get_y_from_classical_register(clreg_index_in_json: int,
                                  quantum_registers_number: int,
                                  bit_mapping: dict) -> int:
    """Compute the y-coordinate associated to the given classical register.

    This method assumes that all the quantum registers are drawn *before* the
    classical ones.

    Parameters:
        clreg_index_in_json (int): identifier of the classical
                                from the JSON circuit representation.
        quantum_registers_number (int): Number of quantum registers in the
                                        circuit.
        bit_mapping (dict): the map that stores the correspondances between
               bits indices in the JSON circuit and the desired output
               indices.
               Structure:
                  {'qubits': {index_in_JSON : index_in_drawing},
                   'clbits': {index_in_JSON : index_in_drawing}}
    Returns:
      int: The y-coordinate of the line representing the classical register
           number classical_register_index.
    """
    y_coord = _constants.VERTICAL_BORDER
    cl_index_to_draw = bit_mapping['clbits'][clreg_index_in_json]
    index_to_draw = quantum_registers_number + cl_index_to_draw
    y_coord += index_to_draw * _constants.REGISTER_LINES_VERTICAL_SPACING
    return y_coord


def get_dimensions(json_circuit, show_clbits: bool) -> Tuple[int, int]:
    """Compute the width and height of the given circuit.

    Parameter:
        json_circuit (dict): JSON representation of the circuit. Can be obtained
                             from the QASM representation by the following
                             lines of code:

          # qasm_str is the string containing the QASM code.
          ast = qiskit.qasm.Qasm(data = qasm_str).parse()
          u = qiskit.unroll.Unroller(ast, qiskit.unroll.JsonBackend(basis))
          u.execute()
          json_circuit = u.backend.circuit

        show_clbits   (bool): Flag set to True if the method should also draw
                              classical bits.
    Returns:
        tuple: The computed width and height of the given circuit.
    """

    circuit_gates_number = _get_circuit_width(json_circuit)
    register_number = json_circuit['header'].get('number_of_qubits', 0)
    if show_clbits:
        register_number += json_circuit['header'].get('number_of_clbits', 0)

    width = _constants.REGISTER_NAME_WIDTH
    width += _constants.GATE_LEFT_BORDER
    width += circuit_gates_number * (
        _constants.GATE_SIZE + _constants.GATE_HORIZONTAL_SPACING)
    width -= _constants.GATE_HORIZONTAL_SPACING
    width += _constants.GATE_RIGHT_BORDER

    height = _constants.VERTICAL_BORDER
    height += (register_number - 1) * _constants.REGISTER_LINES_VERTICAL_SPACING
    height += _constants.VERTICAL_BORDER
    return width, height


def _get_circuit_width(json_circuit) -> int:
    """Compute the width of the given circuit.

    The returned width is not:
        1) A number of pixel (or cm, mm, ...)
        2) The *minimum* number of time steps needed to complete the
           circuit.

    Here the "width" is the number of columns needed to *represent clearly*
    the circuit.
    One situation where the returned integer does not correspond to the
    definition given in 2) above could be

        cx q[0], q[5];
        cx q[1], q[6];

    The 2 instructions above are completely independent and could be performed
    in parallel (in one time step). But the graphic representations of these 2
    instructions overlap: the CNOT lines will overlap between the qubits 1 and 5.
    This situation will then output a "width" of 2, even if the width of the
    circuit in the sense of quantum computing is 1.

    Parameters:
        json_circuit (dict): JSON representation of the circuit. Can be obtained
                             from the QASM representation by the following
                             lines of code:

          # qasm_str is the string containing the QASM code.
          ast = qiskit.qasm.Qasm(data = qasm_str).parse()
          u = qiskit.unroll.Unroller(ast, qiskit.unroll.JsonBackend(basis))
          u.execute()
          json_circuit = u.backend.circuit

    Returns:
        int: The computed width of the given circuit.
    """

    clbits_number = json_circuit['header'].get('number_of_clbits', 0)
    qubits_number = json_circuit['header'].get('number_of_qubits', 0)
    index_last_gate_on_reg = {
        'clbits': [0] * max(clbits_number, 1),
        'qubits': [0] * max(qubits_number, 1)}
    # For each instruction
    for instruction in json_circuit['instructions']:
        _update_data_structure(index_last_gate_on_reg, instruction)

    return max(max(index_last_gate_on_reg['clbits']),
               max(index_last_gate_on_reg['qubits']))


def get_max_index(bit_gate_rank: _types.BitRankType, instruction=None,
                  qubits=None, clbits=None) -> \
        Tuple[int, Tuple[int, int, int, int]]:
    """Compute the maximum x index with an overlap.

    The maximum x index with an overlap is the maximum column index
    where the representation of the 'instruction' (see below) would
    overlap with an already drawn gate representation.

    The algorithm to determine the 'instruction' is:
    1) If the instruction parameter is not None, then data is extracted
       from it.
    2) If the instruction parameter is None and at least one of the qubits
       and clbits parameters is set, then data is extracted from the
       qubits and clbits parameters.
    3) Else, an exception is raised.

    Parameters:
        bit_gate_rank (dict): Dictionnary representing the column index
                              of the last drawn gate for each bit.
           Structure: {'qubits' : [ 3,    # last drawn gate on the first qubit
                                          # is in the third column.
                                    2,
                                    ...,
                                    10 ], # last drawn gate on the last qubit
                                          # is in the tenth column.
                       'clbits' : [ 1,    # last drawn gate on the first
                       classical
                                          # bit is on the first column.
                                    ...,
                                    0 ]
                      }
        instruction (dict): Dictionnary representing the current instruction.
           Structure: see qiskit data structures.
        qubits (list): A list of quantum bits.
        clbits (list): A list of classical bits.
    Returns:
        tuple: (max_index, (minq, maxq, minc, maxc)):
                 - max_index (int): the maximum x index with an overlap.
                 - minq      (int): smallest qubit index used.
                 - maxq      (int): greatest qubit index used.
                 - minc      (int): smallest classical bit index used.
                 - maxc      (int): greatest classical bit index used.
               You can iterate on all the register indexes where something will
               be drawn with
                 for qreg_index in range(minq, maxq+1):
                     # code
                 for creg_index in range(minq, maxq+1):
                     # code
               The ranges can be empty, i.e. it is possible that minq = 0 and
               maxq = -1 or minc = 0 and maxc = -1.
    Raises:
        RuntimeError: when no instruction, no qubits and no clbits are given to
        the function.
    """

    if instruction is None and qubits is None and clbits is None:
        raise RuntimeError("You should provide either an instruction or a bit "
                           "(quantum or classical) to get_max_index.")

    # By default, [minq,maxq] and [minc,maxc] are set to None.
    # Same for the index we are searching.
    minq, maxq, minc, maxc = None, None, None, None
    max_index_q, max_index_c = -1, -1

    # Default values for qubits and clbits
    if qubits is None:
        qubits = []
    if clbits is None:
        clbits = []

    # We compute the qubits and clbits involved in the instruction
    if instruction is not None:
        qubits, clbits = get_involved_bits(instruction)

    # We update with the given sequences of qubits and clbits.
    if qubits:
        minq = min(qubits)
        maxq = max(qubits) if not clbits else len(bit_gate_rank['qubits']) - 1
        max_index_q = max(
            [bit_gate_rank['qubits'][qubit] for qubit in range(minq, maxq + 1)])
    if clbits:
        minc = min(clbits) if not qubits else 0
        maxc = max(clbits)
        max_index_c = max(
            [bit_gate_rank['clbits'][clbit] for clbit in range(minc, maxc + 1)])

    if minq is None:
        minq, maxq = 0, -1
    if minc is None:
        minc, maxc = 0, -1

    return max(max_index_c, max_index_q), (minq, maxq, minc, maxc)


def _get_text_dimensions(text: str, fontsize: int):
    try:
        import cairocffi as cairo
    except ImportError:
        return len(text) * fontsize, fontsize
    surface = cairo.SVGSurface('undefined65761354373731713.svg', 1280, 200)
    cairo_context = cairo.Context(surface)
    cairo_context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL,
                                   cairo.FONT_WEIGHT_BOLD)
    cairo_context.set_font_size(fontsize)
    _, _, width, height, _, _ = cairo_context.text_extents(text)

    # Don't forget to remove the undefined65761354373731713.svg file
    os.remove("undefined65761354373731713.svg")

    return width, height


def adapt_text_font_size(text: str, desired_width: Union[int, float],
                         desired_height: Union[int, float]) -> int:
    """

    :param text: The text whose size needs to be adapted.
    :param desired_width: The maximal width we want to obtain for the text.
    :param desired_height: The maximal height we want to obtain for the text.
    :return: The font-size that will make the text have the desired dimensions.
    """
    # Take an arbitrary initial font size, big enough to lower the errors of
    # the computations below
    initial_font_size = 100
    # Draw the text. To draw the text with the best font size (not too small
    # nor too big) we compute its width with a known font size and adapt the
    # real font size.
    text_width, text_height = _get_text_dimensions(text, initial_font_size)
    # We want to fit the full gate name to the gate box, so we compute the
    # scaling factor needed to fit the gate name.
    font_scale = max(text_width / desired_width, text_height / desired_height)
    # Finally we do the assumption that applying a scaling factor to the font
    # size is the same as applying this scaling factor to the rendered text.
    return int(initial_font_size / font_scale)


def _update_data_structure(bit_gate_rank: _types.BitRankType,
                           instruction) -> None:
    # By default we increment the current index by 1
    increment = 1
    # But not when the instruction is a 'barrier' instruction
    if instruction['name'] == 'barrier':
        increment = 0

    # Compute the values to update.
    index_to_update, (minq, maxq, minc, maxc) = get_max_index(bit_gate_rank,
                                                              instruction=instruction)
    # And perform the update.
    for qubit in range(minq, maxq + 1):
        bit_gate_rank['qubits'][qubit] = index_to_update + increment
    for clbit in range(minc, maxc + 1):
        bit_gate_rank['clbits'][clbit] = index_to_update + increment


def get_involved_bits(instruction) -> Tuple[Sequence[int], Sequence[int]]:
    """Returns the bits involved in the instruction.

    :param instruction: The instruction of interest.
    :return: The quantum and classical bits used by the considered instruction.
    """
    qubits = instruction.get('qubits', [])
    clbits = instruction.get('clbits', [])
    if 'conditional' in instruction:
        mask = int(instruction['conditional']['mask'], 0)
        number_of_clbits = len(bin(mask)[2:])
        clbits += list(range(number_of_clbits))

    return qubits, clbits
