import pygetwindow as gw

from pywinauto.application import Application
from pywinauto.findwindows import find_windows
from ..core.logger import logger, log_action, log_result


def get_active_window():

    try:

        win = gw.getActiveWindow()

        if not win:
            logger.debug("No active window found")
            return None

        title = str(win.title).strip()

        if not title:
            logger.debug("Active window has no title")
            return None

        logger.debug(f"Active window: {title}")
        return title

    except Exception as e:

        logger.error(f"Active window error: {e}", exc_info=True)

        return None



def focus_window(title_keyword):

    try:
        logger.info(f"Attempting to focus window: {title_keyword}")

        handles = find_windows(
            title_re=f".*{title_keyword}.*"
        )

        if not handles:

            logger.warning(f"Window not found: {title_keyword}")

            return False


        app = Application().connect(
            handle=handles[0]
        )

        window = app.window(
            handle=handles[0]
        )

        window.set_focus()

        window_title = window.window_text()
        logger.info(f"Focused window: {window_title}")
        log_result(True, f"Focused: {window_title}")

        return True


    except Exception as e:

        logger.error(f"Focus failed for {title_keyword}: {e}", exc_info=True)
        log_result(False, f"Failed to focus {title_keyword}")

        return False