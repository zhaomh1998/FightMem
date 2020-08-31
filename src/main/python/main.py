from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
import app

if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    resource_path = appctxt.get_resource('.')
    window = app.MyWindow(resource_path)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
