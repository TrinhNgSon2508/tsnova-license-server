from license_manager import verify_saved_license
from activate_ui import ActivateWindow

# import UI chính của TSNOVA
from tsnova_ui import TSNovaApp


if verify_saved_license():

    # mở app chính
    app = TSNovaApp()
    app.mainloop()

else:

    # mở màn activation
    activate_window = ActivateWindow()
    activate_window.mainloop()