_tools = None
_tools_index = 0


def start(view_manager) -> bool:
    """Start the app."""
    from picoware.gui.menu import Menu

    global _tools
    if _tools is None:
        _tools = Menu(
            view_manager.draw,
            "System",
            0,
            view_manager.draw.size.y,
            view_manager.foreground_color,
            view_manager.background_color,
            view_manager.selected_color,
            view_manager.foreground_color,
            2,
        )
        _tools.add_item("REPL")
        _tools.add_item("Text Editor")
        _tools.add_item("Python Editor")

        _tools.set_selected(_tools_index)

        _tools.draw()
    return True


def run(view_manager) -> None:
    """Run the app."""
    from picoware.system.buttons import (
        BUTTON_BACK,
        BUTTON_UP,
        BUTTON_DOWN,
        BUTTON_LEFT,
        BUTTON_CENTER,
        BUTTON_RIGHT,
    )

    global _tools
    if not _tools:
        return
    global _tools_index

    button: int = view_manager.button

    if button in (BUTTON_UP, BUTTON_LEFT):
        _tools.scroll_up()
    elif button in (BUTTON_DOWN, BUTTON_RIGHT):
        _tools.scroll_down()
    elif button == BUTTON_BACK:

        view_manager.back()
        _tools_index = 0
    elif button == BUTTON_CENTER:
        _tools_index = _tools.selected_index
        if _tools_index == 0:
            from picoware.applications import repl
	    from picoware.system.view import View
	    
            view_manager.add(View("repl", repl.run, repl.start, repl.stop))
            view_manager.switch_to("repl")
        elif _tools_index == 1:
            from picoware.applications import text_editor
            from picoware.system.view import View

            view_manager.add(View("text_editor", text_editor.run, text_editor.start, text_editor.stop))
            view_manager.switch_to("text_editor")
        elif _tools_index == 2:
            from picoware.applications import python_editor
            from picoware.system.view import View

            view_manager.add(View("editor", python_editor.run, python_editor.start, python_editor.stop))
            view_manager.switch_to("editor")


def stop(view_manager) -> None:
    """Stop the app."""
    from gc import collect

    global _tools
    if _tools:
        del _tools
        _tools = None
    collect()