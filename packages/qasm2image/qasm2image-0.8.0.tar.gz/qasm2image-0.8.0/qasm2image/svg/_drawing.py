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

"""This module provide the core functions for drawing a circuit in SVG.

All the functions related to SVG drawing with svgwrite and needed by qasm2svg
are in this module. The main function is draw_json_circuit, which use all the
other functions to draw a quantum circuit in SVG.

The functions use a specific data structure for keeping track of the positions
where they can draw. The variable bit_gate_rank is this data structure and is
described below:

   Structure: {'qubits' : [ 3,    # last drawn gate on the first qubit
                                  # is in the third column.
                            2,
                            ...,
                            6,    # last drawn gate on the i-th qubit
                                  # is in the sixth column.
                            ...,
                            10 ], # last drawn gate on the last qubit
                                  # is in the tenth column.
               'clbits' : [ 1,    # last drawn gate on the first classical
                                  # bit is on the first column.
                            ...,
                            0 ]
              }
"""

import itertools
from typing import Tuple

from svgwrite import Drawing

from qasm2image.svg import _helpers, _constants, _types


def _draw_classical_double_line(drawing: Drawing, x1_coord: int, y1_coord: int,
                                x2_coord: int, y2_coord: int) -> None:
    """Draw a double line between (x1_coord, y1_coord) and (x2_coord, y2_coord).

    :param drawing: Drawing that will be used to draw.
    :param x1_coord: x-coordinate of the first point.
    :param y1_coord: y-coordinate of the first point.
    :param x2_coord: x-coordinate of the second point.
    :param y2_coord: y-coordinate of the second point.
    :raise NotImplementedError: when x1_coord != x2_coord and
    y1_coord != y2_coord (i.e. when the line is neither horizontal
    nor vertical).
    """
    x_increment, y_increment = 0, 0
    if x1_coord == x2_coord:
        x_increment = _constants.DOUBLE_LINES_SEPARATION
    elif y1_coord == y2_coord:
        y_increment = _constants.DOUBLE_LINES_SEPARATION
    else:
        raise NotImplementedError("The drawn line should be either horizontal "
                                  "or vertical.")
    drawing.add(
        drawing.line(start=(x1_coord - x_increment, y1_coord - y_increment),
                     end=(x2_coord - x_increment, y2_coord - y_increment),
                     stroke=_constants.GATE_BORDER_COLOR,
                     stroke_width=_constants.STROKE_THICKNESS))
    drawing.add(
        drawing.line(start=(x1_coord + x_increment, y1_coord + y_increment),
                     end=(x2_coord + x_increment, y2_coord + y_increment),
                     stroke=_constants.GATE_BORDER_COLOR,
                     stroke_width=_constants.STROKE_THICKNESS))


def _draw_line_between_qubits(drawing: Drawing,
                              bit_gate_rank: _types.BitRankType,
                              control_qubit: int, target_qubit: int,
                              bit_mapping: dict,
                              index_to_draw: int = None) -> None:
    """Draw a line between the two given qubits.

    :param drawing: Drawing that will be used to draw.
    :param bit_gate_rank: Structure used to keep track of the used and free
    places. See module docstring for more information.
    :param control_qubit: First qubit.
    :param target_qubit: Second qubit.
    :param bit_mapping: Unused at the moment.
    :param index_to_draw: If precised, force the line to be drawn at the given
    index. Else, the index is computed and the line drawn at the first free
    place possible.
    """
    if index_to_draw is None:
        index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                                  qubits=[control_qubit,
                                                          target_qubit])
    x_coord = _helpers.get_x_from_index(index_to_draw)
    y1_coord = _helpers.get_y_from_quantum_register(control_qubit, bit_mapping)
    y2_coord = _helpers.get_y_from_quantum_register(target_qubit, bit_mapping)
    drawing.add(drawing.line(start=(x_coord, y1_coord), end=(x_coord, y2_coord),
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))


def _draw_cnot_cross(drawing: Drawing, x_coord: float, y_coord: float) -> None:
    """Draw the cross of a CX gate with the circle around.

    :param drawing: Drawing that will be used to draw.
    :param x_coord: x-coordinate of the crossing point.
    :param y_coord: y-coordinate of the crossing point.
    """
    # Draw the circle
    _draw_gate_circle(drawing, x_coord, y_coord)

    # Draw the cross
    drawing.add(
        drawing.line(start=(x_coord - _constants.GATE_SIZE / 2, y_coord),
                     end=(x_coord + _constants.GATE_SIZE / 2, y_coord),
                     stroke=_constants.GATE_BORDER_COLOR,
                     stroke_width=_constants.STROKE_THICKNESS))

    drawing.add(
        drawing.line(start=(x_coord, y_coord - _constants.GATE_SIZE / 2),
                     end=(x_coord, y_coord + _constants.GATE_SIZE / 2),
                     stroke=_constants.GATE_BORDER_COLOR,
                     stroke_width=_constants.STROKE_THICKNESS))


def _draw_control_circle(drawing: Drawing, x_coord: float, y_coord: float,
                         desired_value: bool) -> None:
    if desired_value:
        filling_color = _constants.CONTROL_TRUE_GATE_FILL_COLOR
    else:
        filling_color = _constants.CONTROL_FALSE_GATE_FILL_COLOR

    drawing.add(drawing.circle(center=(x_coord, y_coord),
                               r=_constants.CONTROL_GATE_SIZE / 2,
                               fill=filling_color,
                               stroke=_constants.GATE_BORDER_COLOR,
                               stroke_width=_constants.STROKE_THICKNESS))


def _draw_gate_circle(drawing: Drawing, x_coord: float, y_coord: float) -> None:
    drawing.add(
        drawing.circle(center=(x_coord, y_coord), r=_constants.GATE_SIZE / 2,
                       fill=_constants.GATE_FILL_COLOR,
                       stroke=_constants.GATE_BORDER_COLOR,
                       stroke_width=_constants.STROKE_THICKNESS))


def _draw_gate_rect(drawing: Drawing, x_coord: float, y_coord: float) -> None:
    anchor = tuple((x_coord - _constants.GATE_SIZE / 2,
                    y_coord - _constants.GATE_SIZE / 2))
    drawing.add(drawing.rect(insert=anchor,
                             size=(_constants.GATE_SIZE, _constants.GATE_SIZE),
                             fill=_constants.GATE_FILL_COLOR,
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))


def _draw_swap_cross(drawing: Drawing, x_coord: float, y_coord: float) -> None:
    start_bl_tr = tuple((x_coord - _constants.GATE_SIZE / 2,
                         y_coord - _constants.GATE_SIZE / 2))
    end_bl_tr = tuple((x_coord + _constants.GATE_SIZE / 2,
                       y_coord + _constants.GATE_SIZE / 2))
    # Draw the cross
    drawing.add(drawing.line(start=start_bl_tr, end=end_bl_tr,
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))

    start_br_tl = tuple((x_coord + _constants.GATE_SIZE / 2,
                         y_coord - _constants.GATE_SIZE / 2))
    end_br_tl = tuple((x_coord - _constants.GATE_SIZE / 2,
                       y_coord + _constants.GATE_SIZE / 2))
    drawing.add(drawing.line(start=start_br_tl, end=end_br_tl,
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))


def _draw_swap_gate(drawing: Drawing, bit_gate_rank: _types.BitRankType,
                    qubit1: int, qubit2: int, bit_mapping: dict) -> None:
    index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                              qubits=[qubit1, qubit2])
    x_coord = _helpers.get_x_from_index(index_to_draw)
    yq1_coord = _helpers.get_y_from_quantum_register(qubit1, bit_mapping)
    yq2_coord = _helpers.get_y_from_quantum_register(qubit2, bit_mapping)

    _draw_swap_cross(drawing, x_coord, yq1_coord)
    _draw_swap_cross(drawing, x_coord, yq2_coord)
    _draw_line_between_qubits(drawing, bit_gate_rank, qubit1, qubit2,
                              bit_mapping, index_to_draw)


def _draw_measure_gate(drawing: Drawing, bit_gate_rank: _types.BitRankType,
                       measured_qubit: int, target_clbit: int,
                       show_clbits: bool, bit_mapping: dict) -> None:
    index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                              qubits=[measured_qubit],
                                              clbits=[target_clbit])

    x_coord = _helpers.get_x_from_index(index_to_draw)
    yq_coord = _helpers.get_y_from_quantum_register(measured_qubit, bit_mapping)
    if show_clbits:
        yc_coord = _helpers.get_y_from_classical_register(target_clbit, len(
            bit_gate_rank['qubits']), bit_mapping)
        # Draw the line between the 2 bits
        _draw_classical_double_line(drawing, x_coord, yq_coord, x_coord,
                                    yc_coord)

        # Draw the little thing that tells where we put the measure.
        anchor = tuple((x_coord - _constants.MEASURE_GATE_CLBIT_SIZE / 2,
                        yc_coord - _constants.MEASURE_GATE_CLBIT_SIZE / 2))
        sizes = tuple((_constants.MEASURE_GATE_CLBIT_SIZE,
                       _constants.MEASURE_GATE_CLBIT_SIZE))
        drawing.add(drawing.rect(insert=anchor, size=sizes,
                                 fill=_constants.MEASURE_GATE_CLBIT_FILL_COLOR,
                                 stroke=_constants.GATE_BORDER_COLOR,
                                 stroke_width=_constants.STROKE_THICKNESS))
        # Draw the "measure" gate.
        _draw_unitary_gate(drawing, bit_gate_rank, measured_qubit, "M",
                           bit_mapping, index_to_draw=index_to_draw)

    else:
        # Draw the "measure" gate.
        _draw_unitary_gate(drawing, bit_gate_rank, measured_qubit,
                           "M" + str(target_clbit), bit_mapping,
                           index_to_draw=index_to_draw)


def _draw_unitary_gate(drawing: Drawing, bit_gate_rank: _types.BitRankType,
                       qubit: int, gate_name: str, bit_mapping: dict,
                       index_to_draw: int = None,
                       is_controlled_gate: bool = False) -> None:
    if index_to_draw is None:
        index_to_draw = bit_gate_rank['qubits'][qubit]
    x_coord = _helpers.get_x_from_index(index_to_draw)
    y_coord = _helpers.get_y_from_quantum_register(qubit, bit_mapping)

    # Draw the good gate shape
    if is_controlled_gate:
        _draw_gate_circle(drawing, x_coord, y_coord)
    else:
        _draw_gate_rect(drawing, x_coord, y_coord)

    desired_width = _constants.GATE_SIZE - 2 * _constants.GATE_INSIDE_MARGIN
    desired_height = _constants.GATE_SIZE - 2 * _constants.GATE_INSIDE_MARGIN
    font_size = _helpers.adapt_text_font_size(gate_name, desired_width,
                                              desired_height)
    if is_controlled_gate:
        font_size *= _constants.FONT_SIZE_REDUCTION_FACTOR_FOR_CONTROLLED_GATES

    vertical_multiplier = _constants.FONT_SIZE_CENTER_VERTICALLY_MULTIPLIER

    drawing.add(drawing.text(gate_name, insert=(
        x_coord, y_coord + vertical_multiplier * font_size),
                             text_anchor="middle", font_size=font_size))


def _draw_classically_conditioned_part(drawing: Drawing,
                                       bit_gate_rank: _types.BitRankType,
                                       instruction, bit_mapping: dict) -> None:
    """Draw the line and the controls for classically controlled instructions.

    :param drawing: an instance of svgwrite.Drawing, used to write the SVG.
    :param bit_gate_rank: see module documentation for more information on this
    data structure.
    :param instruction: A QISKit instruction. The dict has a key 'conditional'
    associated to an other Python dict with entries:
        'type': the type of the instruction. For example 'equals'.
        'mask': the classical bits used (?)
        'val' : the value compared with 'type' comparator to the classical bit.
    :param bit_mapping:
    :raise NotImplementedError: if the given instruction affects more than 1
    qubit.
    """

    qubits = instruction['qubits']
    if len(qubits) > 1:
        raise NotImplementedError("Classically controlled multi-qubit "
                                  "instructions are not implemented for the "
                                  "moment.")
    total_qubits_number = len(bit_gate_rank['qubits'])
    total_clbits_number = len(bit_gate_rank['clbits'])

    # We take the binary little-endian representation of the value that
    # should be compared with the value stored in classical registers.
    # int(x, 0) let the 'int' function choose automatically the good basis.
    value = int(instruction['conditional']['val'], 0)
    mask = int(instruction['conditional']['mask'], 0)
    # The [2:] is to remove the "Ob" part returned by the "bin" function.
    # The [::-1] is to reverse the list order, to have a little-endian
    # representation.
    little_endian_bit_value = bin(value)[2:][::-1]
    number_of_clbits = len(bin(mask)[2:])

    assert number_of_clbits <= total_clbits_number

    # Compute the important coordinates.
    index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                              instruction=instruction)
    x_coord = _helpers.get_x_from_index(index_to_draw)
    yq_coord = _helpers.get_y_from_quantum_register(qubits[0], bit_mapping)
    yc_coord = _helpers.get_y_from_classical_register(number_of_clbits - 1,
                                                      total_qubits_number,
                                                      bit_mapping)
    # Then draw the double line representing the classical control.
    _draw_classical_double_line(drawing, x_coord, yq_coord, x_coord, yc_coord)

    # Finally draw all the controlled circles
    for classical_register_index in range(number_of_clbits):
        y_coord = _helpers.get_y_from_classical_register(
            classical_register_index, total_qubits_number, bit_mapping)
        clbit_should_be_1 = (
            classical_register_index < len(little_endian_bit_value) and
            little_endian_bit_value[classical_register_index] == '1')
        _draw_control_circle(drawing, x_coord, y_coord, clbit_should_be_1)


def _draw_gate(drawing: Drawing, bit_gate_rank: _types.BitRankType, instruction,
               show_clbits: bool, bit_mapping: dict) -> None:
    unitary_gate_names = set('xyzhst')
    supported_base_gates = unitary_gate_names | {'sdg', 'tdg'}
    supported_u_gates = {"u{}".format(i) for i in [1, 2, 3]} | {'u'}
    supported_unitary_gates = supported_base_gates | supported_u_gates
    supported_controlled_gates = (
        {"c{}".format(name) for name in supported_unitary_gates} |
        {"cc{}".format(name) for name in supported_unitary_gates})
    supported_special_gates = {'measure', 'barrier', 'reset', 'swap'}
    supported_gates = (supported_unitary_gates | supported_controlled_gates |
                       supported_special_gates)

    name = instruction['name']
    qubits = instruction['qubits']
    name_conditional_part = ""

    if 'conditional' in instruction:
        if show_clbits:
            _draw_classically_conditioned_part(drawing, bit_gate_rank,
                                               instruction, bit_mapping)
        else:
            # TODO: Change 'c' by the name of the classical register.
            name_conditional_part = "[c={}]".format(
                int(instruction['conditional']['val'], 0))

    # Tag needed later
    drawing_controlled_gate = False
    # Compute the x coordinate of the gate.
    index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                              instruction=instruction)

    # If it is a measure gate then call the specialized function to draw it.
    if name == 'measure':
        _draw_measure_gate(drawing, bit_gate_rank, qubits[0],
                           instruction['clbits'][0], show_clbits, bit_mapping)

    # If it is a barrier gate then we do not draw anything
    if name == 'barrier':
        pass

    # If it is a reset gate, then draw a unitary gate with 'reset' name.
    if name == 'reset':
        _draw_unitary_gate(drawing, bit_gate_rank, qubits[0],
                           name + name_conditional_part, bit_mapping)

    # If it is a swap gate, then draw the specific gate.
    if name == 'swap':
        _draw_swap_gate(drawing, bit_gate_rank, qubits[0], qubits[1],
                        bit_mapping)

    # If the gate is a controlled one then draw the controlled part and let the
    # code just after draw the main gate.
    if name.lower().startswith('c'):
        # Used to draw the line, we need the two qubits at the extremities.
        upper_qubit = min(qubits)
        lower_qubit = max(qubits)
        control_qubits = qubits[:-1]  # All the qubits except the last one
        target_qubit = qubits[-1]  # The last qubit is the target

        # Draw the line, then the little control circle
        _draw_line_between_qubits(drawing, bit_gate_rank, upper_qubit,
                                  lower_qubit, bit_mapping, index_to_draw)
        for control_qubit in control_qubits:
            _draw_control_circle(drawing,
                                 _helpers.get_x_from_index(index_to_draw),
                                 _helpers.get_y_from_quantum_register(
                                     control_qubit, bit_mapping), True)
        # Then if it's a (C)CX gate, draw the stylised (C)CX gate.
        if name.lower().lstrip('c') == 'x':
            _draw_cnot_cross(drawing, _helpers.get_x_from_index(index_to_draw),
                             _helpers.get_y_from_quantum_register(target_qubit,
                                                                  bit_mapping))
        # Else keep the information that we should draw a controlled gate.
        else:
            drawing_controlled_gate = True
            name = name[1:]
            qubits = qubits[1:]

    # Draw the main gate.
    # 1. Special case for gates with parameters
    if instruction.get('params', None):
        def _round_numeric_param(numeric_param: float) -> str:
            if abs(numeric_param) < 1e-10:
                # Avoid the "0.0"
                return "0"
            return str(
                round(numeric_param, _constants.PARAMETERS_ROUND_DECIMAL))

        _draw_unitary_gate(drawing, bit_gate_rank, qubits[0],
                           name + name_conditional_part + "({})".format(
                               ",".join(map(_round_numeric_param,
                                            instruction['params']))), bit_mapping,
                           is_controlled_gate=drawing_controlled_gate,
                           index_to_draw=index_to_draw)

    # 2. For all the gates without parameters, simply draw them
    elif name.lower() in supported_base_gates:
        _draw_unitary_gate(drawing, bit_gate_rank, qubits[0],
                           name.upper() + name_conditional_part, bit_mapping,
                           is_controlled_gate=drawing_controlled_gate,
                           index_to_draw=index_to_draw)

    # Warn the user we encountered a non-implemented gate.
    if instruction['name'].lower() not in supported_gates:
        print("WARNING: Gate '{}' is not implemented".format(instruction['name']))

    # And finally take care of our data structure that keeps track of the
    # position
    # where we want to draw.
    _helpers._update_data_structure(bit_gate_rank, instruction)


def _draw_registers_names_and_lines(drawing: Drawing, circuit_width: int,
                                    json_circuit, show_clbits: bool) -> None:
    # First we draw the names of each register
    qubit_labels = json_circuit['header'].get('qubit_labels', [])
    clbit_labels = (
        json_circuit['header'].get('clbit_labels', []) if show_clbits else [])

    # 1. Compute the font size that will be used to keep good dimensions
    font_size = _constants.REGISTER_NAME_FONT_SIZE
    for qubit_label in itertools.chain(qubit_labels, clbit_labels):
        qubit_text_name = "{}[{}]".format(*qubit_label)
        desired_width = (
            _constants.REGISTER_NAME_WIDTH -
            _constants.REGISTER_NAME_LEFT_BORDER -
            _constants.REGISTER_NAME_RIGHT_BORDER)
        adapted_font_size = _helpers.adapt_text_font_size(qubit_text_name,
                                                          desired_width,
                                                          _constants.MAX_REGISTER_NAME_HEIGHT)
        font_size = min(font_size, adapted_font_size)

    # 2. Draw the bit names
    y_coord = _constants.VERTICAL_BORDER
    for bit_label in itertools.chain(qubit_labels, clbit_labels):
        qubit_text_name = "{}[{}]".format(*bit_label)
        drawing.add(drawing.text(qubit_text_name, insert=(
            _constants.REGISTER_NAME_WIDTH -
            _constants.REGISTER_NAME_RIGHT_BORDER,
            y_coord + _constants.FONT_SIZE_CENTER_VERTICALLY_MULTIPLIER *
            font_size),
                                 text_anchor="end", font_size=font_size))
        y_coord += _constants.REGISTER_LINES_VERTICAL_SPACING

    # Then we draw the register lines
    y_coord = _constants.VERTICAL_BORDER

    # Start with quantum registers
    quantum_register_number = json_circuit['header'].get('number_of_qubits', 0)
    for _ in range(quantum_register_number):
        drawing.add(
            drawing.line(start=(_constants.REGISTER_NAME_WIDTH, y_coord),
                         end=(circuit_width, y_coord),
                         stroke=_constants.GATE_BORDER_COLOR,
                         stroke_width=_constants.STROKE_THICKNESS))
        y_coord += _constants.REGISTER_LINES_VERTICAL_SPACING

    # And see if we want to plot classical registers.
    if show_clbits:
        classical_register_number = json_circuit['header'].get(
            'number_of_clbits', 0)
        for _ in range(classical_register_number):
            _draw_classical_double_line(drawing, _constants.REGISTER_NAME_WIDTH,
                                        y_coord, circuit_width, y_coord)
            y_coord += _constants.REGISTER_LINES_VERTICAL_SPACING


def draw_json_circuit(json_circuit, unit: str = 'px', round_index: int = 0,
                      show_clbits: bool = True, bit_order: dict = None) -> \
    Tuple[str, Tuple[int, int]]:
    """Draw a circuit represented as a JSON string.

    Args:
        json_circuit (dict): A quantum circuit in JSON format. This can be
        obtained with
                             the QISKit object qiskit.unroll.JsonBackend.
        unit         (str) : Unit used to draw the circuit. This parameter is
        not really
                             tested at the moment and values different from
                             "px" could
                             cause the function to fail.
        round_index  (int) : Number of digits after the decimal point to keep
        in the SVG.
                             A value different from "0" could cause the
                             function to fail,
                             this parameter need to be tested.
        show_clbits  (bool): True if the function should draw the classical
        bits, False
                             otherwise.
        bit_order    (dict): A Python dictionary storing the bit ordering.
    Returns:
        Tuple[str, Tuple[int, int]]: (SVG, (width, height))
            - SVG: string representing the given circuit in SVG format.
            - width: computed width in pixels.
            - height: computed height in pixels.
    """

    json_header = json_circuit["header"]

    # TEMPORARY FIX FOR THE QOBJ STRUCTURE
    # "issue": the json_circuit['header']['clbit_labels'] and
    # json_circuit['header']['qubit_labels'] don't have the same meaning and it
    # seems unintuitive. I fix that here. This part should be removed if the
    # qobj structure change to fix this behaviour.
    new_clbit_labels = list()
    for clbit_label in json_circuit['header']['clbit_labels']:
        for i in range(clbit_label[1] + 1):
            new_clbit_labels.append([clbit_label[0], i])
    json_header['clbit_labels'] = new_clbit_labels

    # Take the appropriate default value for bit_order if not provided by the
    # user.
    if bit_order is None:
        bit_order = dict()
        for qubit_index, qubit_label in enumerate(json_header['qubit_labels']):
            bit_key = "".join(map(str, qubit_label))
            bit_order[bit_key] = qubit_index
        for clbit_index, clbit_label in enumerate(json_header['clbit_labels']):
            bit_key = "".join(map(str, clbit_label))
            bit_order[bit_key] = clbit_index

    # Transform the bit_order structure in a more useful one: the bit_order
    # structure associates bit labels to their index, but in the json circuit
    # we don't have bit labels but rather bit indices. So we want to have a
    # dictionary mapping indices in the json circuit to indices on the drawn
    # circuit.
    bit_mapping = {'clbits': dict(), 'qubits': dict()}
    for qubit_index, qubit_label in enumerate(json_header['qubit_labels']):
        bit_key = "".join(map(str, qubit_label))
        bit_mapping['qubits'][qubit_index] = bit_order[bit_key]
    for clbit_index, clbit_label in enumerate(json_header['clbit_labels']):
        bit_key = "".join(map(str, clbit_label))
        bit_mapping['clbits'][clbit_index] = bit_order[bit_key]

    # Compute the width and height
    width, height = _helpers.get_dimensions(json_circuit, show_clbits)
    width, height = round(width, round_index), round(height, round_index)
    width_str, height_str = str(width) + unit, str(height) + unit

    # Create the drawing
    drawing = Drawing(size=(width_str, height_str))

    # Create the internal structure used by the drawing functions
    index_last_gate_on_reg = {
        'clbits': [0] * json_circuit['header'].get('number_of_clbits', 0),
        'qubits': [0] * json_circuit['header'].get('number_of_qubits', 0)}

    # And draw!
    # First the registers names and lines
    _draw_registers_names_and_lines(drawing, width, json_circuit, show_clbits)
    # And then each gate
    for instruction in json_circuit['instructions']:
        _draw_gate(drawing, index_last_gate_on_reg, instruction, show_clbits,
                   bit_mapping)
    return drawing.tostring(), (width, height)
