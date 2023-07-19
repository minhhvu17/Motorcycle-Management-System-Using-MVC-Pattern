from views.login_page import MainApplication
import os
from db.settingup import SettingUp as SettingUp

if __name__ == "__main__":
    SettingUp()
    app = MainApplication()
    file_name = "img/icon.ico"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    app.iconbitmap(file_path)
    app.title("Motorbike Management System")
    app.mainloop()