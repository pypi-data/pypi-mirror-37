import os
import time
import pytest

import testing_utils
from testing_utils import call_gui_callback


sm_path_recursive_resize = os.path.join(testing_utils.TEST_ASSETS_PATH, "unit_test_state_machines", "recursive_resize")

state_path_root = "YCBQQV"
state_path_P = "YCBQQV/IZCVSG"
state_path_PC = "YCBQQV/IZCVSG/PAMWNB"
state_path_e = "YCBQQV/IZCVSG/PAMWNB/YRGGWX"
state_path_A = "YCBQQV/IZCVSG/QUVLJG"
state_path_Hi = "YCBQQV/EUPXUC"
state_path_Ex = "YCBQQV/PBUVVY"


def open_test_state_machine():
    import rafcon.gui.singleton

    smm_m = rafcon.gui.singleton.state_machine_manager_model
    main_window_controller = rafcon.gui.singleton.main_window_controller
    menubar_ctrl = main_window_controller.get_controller('menu_bar_controller')
    state_machines_ctrl = main_window_controller.get_controller("state_machines_editor_ctrl")

    call_gui_callback(menubar_ctrl.on_open_activate, None, None, sm_path_recursive_resize)
    time.sleep(0.5)
    testing_utils.wait_for_gui()  # Wait for gaphas view

    sm_m = smm_m.state_machines[smm_m.selected_state_machine_id]
    sm_id = sm_m.state_machine.state_machine_id
    sm_gaphas_ctrl = state_machines_ctrl.get_controller(sm_id)
    canvas = sm_gaphas_ctrl.canvas
    gaphas_view = sm_gaphas_ctrl.view.editor

    return sm_m, canvas, gaphas_view


def get_state_handle_pos(view, state_v, handle):
    i2v = view.get_matrix_i2v(state_v)
    item_pos_handle = (handle.pos.x.value, handle.pos.y.value)
    view_pos_handle = i2v.transform_point(*item_pos_handle)
    return view_pos_handle


def resize_state(view, state_v, rel_size, num_motion_events, recursive, monkeypatch):
    from rafcon.gui.mygaphas.tools import MoveHandleTool
    from rafcon.gui.utils.constants import RECURSIVE_RESIZE_MODIFIER
    from gaphas.item import SE, NW
    import gtk.gdk

    def get_resize_handle(x, y, distance=None):
        return state_v, state_v.handles()[SE]
    monkeypatch.setattr("rafcon.gui.mygaphas.aspect.StateHandleFinder.get_handle_at_point", get_resize_handle)
    monkeypatch.setattr("rafcon.gui.mygaphas.aspect.ItemHandleFinder.get_handle_at_point", get_resize_handle)

    resize_tool = MoveHandleTool(view)
    start_pos_handle = get_state_handle_pos(view, state_v, state_v.handles()[SE])

    # Start resize: Press button
    button_press_event = gtk.gdk.Event(type=gtk.gdk.BUTTON_PRESS)
    button_press_event.button = 1
    call_gui_callback(resize_tool.on_button_press, button_press_event)
    # Do resize: Move mouse
    motion_event = gtk.gdk.Event(type=gtk.gdk.MOTION_NOTIFY)
    motion_event.state |= gtk.gdk.BUTTON_PRESS_MASK
    if recursive:
        motion_event.state |= RECURSIVE_RESIZE_MODIFIER
    for i in xrange(num_motion_events):
        motion_event.x = start_pos_handle[0] + rel_size[0] * (float(i + 1) / num_motion_events)
        motion_event.y = start_pos_handle[1] + rel_size[1] * (float(i + 1) / num_motion_events)
        call_gui_callback(resize_tool.on_motion_notify, motion_event)

    # Stop resize: Release button
    button_release_event = gtk.gdk.Event(type=gtk.gdk.BUTTON_RELEASE)
    button_release_event.button = 1
    call_gui_callback(resize_tool.on_button_release, button_release_event)

    monkeypatch.undo()
    monkeypatch.undo()


def assert_state_size_and_meta_data_consistency(state_m, state_v, size, canvas):
    from rafcon.utils.geometry import equal
    from rafcon.gui.helpers.meta_data import check_gaphas_state_meta_data_consistency
    assert equal(size, (state_v.width, state_v.height), 5), "State {}: view size wrong".format(state_m.state.name)
    assert equal(size, state_m.get_meta_data_editor()["size"], 5), "State {}: meta size wrong".format(state_m.state.name)
    check_gaphas_state_meta_data_consistency(state_m, canvas, recursive=True)


def add_vectors(vec1, vec2):
    return [v1 + v2 for v1, v2 in zip(vec1, vec2)]


def transform_size_v2i(view, state_v, size):
    v2i = view.get_matrix_v2i(state_v)
    item_size = v2i.transform_distance(*size)
    return item_size


def print_state_sizes(state_m, canvas, state_names=None):
    from rafcon.core.states.container_state import ContainerState
    state_v = canvas.get_view_for_model(state_m)
    meta_size = state_m.get_meta_data_editor()["size"]
    view_size = state_v.width, state_v.height
    meta_pos = state_m.get_meta_data_editor()["rel_pos"]
    view_pos = state_v.position
    if state_names is None or state_m.state.name in state_names:
        print "{} size: {} ?= {}".format(state_m.state.name, meta_size, view_size)
        print "{} pos: {} ?= {}".format(state_m.state.name, meta_pos, view_pos)
    if isinstance(state_m.state, ContainerState):
        for child_state_m in state_m.states.itervalues():
            print_state_sizes(child_state_m, canvas)


@pytest.mark.parametrize("state_path,recursive,rel_size", [
    (state_path_root, False, (40, 40)),
    (state_path_root, True, (40, 40)),
    (state_path_P, False, (20, 20)),
    (state_path_P, True, (20, 20)),
    (state_path_Hi, False, (20, 20)),
    (state_path_Hi, True, (20, 20)),
    (state_path_Ex, False, (20, 20)),
    (state_path_Ex, True, (20, 20)),
    (state_path_PC, False, (10, 10)),
    (state_path_PC, True, (10, 10))
])
def test_simple_state_size_resize(state_path, recursive, rel_size, caplog, monkeypatch):
    testing_utils.run_gui(gui_config={'HISTORY_ENABLED': True})

    try:
        from rafcon.gui.helpers.meta_data import check_gaphas_state_meta_data_consistency
        sm_m, canvas, view = open_test_state_machine()

        state_m = sm_m.get_state_model_by_path(state_path)
        state_v = canvas.get_view_for_model(state_m)

        orig_state_size = state_m.get_meta_data_editor()["size"]
        check_gaphas_state_meta_data_consistency(state_m, canvas, recursive=True)
        print "\ninitial:"
        print_state_sizes(state_m, canvas, ["C"])

        view_rel_size = transform_size_v2i(view, state_v, rel_size)
        resize_state(view, state_v, rel_size, 3, recursive, monkeypatch)
        new_state_size = add_vectors(orig_state_size, view_rel_size)
        print "\nfirst resize:"
        print_state_sizes(state_m, canvas, ["C"])
        assert_state_size_and_meta_data_consistency(state_m, state_v, new_state_size, canvas)

        rel_size = (-rel_size[0], -rel_size[1])
        view_rel_size = transform_size_v2i(view, state_v, rel_size)
        resize_state(view, state_v, rel_size, 3, recursive, monkeypatch)
        print "\nsecond resize:"
        print_state_sizes(state_m, canvas, ["C"])
        assert_state_size_and_meta_data_consistency(state_m, state_v, orig_state_size, canvas)

        call_gui_callback(sm_m.history.undo)
        print "\nfirst undo:"
        print_state_sizes(state_m, canvas, ["C"])
        assert_state_size_and_meta_data_consistency(state_m, state_v, new_state_size, canvas)

        call_gui_callback(sm_m.history.undo)
        print "\nsecond undo:"
        print_state_sizes(state_m, canvas, ["C"])
        assert_state_size_and_meta_data_consistency(state_m, state_v, orig_state_size, canvas)

        call_gui_callback(sm_m.history.redo)
        assert_state_size_and_meta_data_consistency(state_m, state_v, new_state_size, canvas)

        call_gui_callback(sm_m.history.redo)
        assert_state_size_and_meta_data_consistency(state_m, state_v, orig_state_size, canvas)

    finally:
        testing_utils.close_gui()
        testing_utils.shutdown_environment(caplog=caplog)
