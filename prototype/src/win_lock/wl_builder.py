import sys
import os
import shutil
import win_lock
from subprocess import Popen, PIPE
work_dir = os.path.realpath(os.path.join(os.path.dirname(win_lock.__file__), os.pardir,os.pardir,'work'))

def build(file_):
    with open('data_wrapper.py','r') as f:
        wrapper = f.readlines()
        wrapper[0] = wrapper[0].replace('$',os.path.basename(file_))
    with open(os.path.join(work_dir,'data_wrapper.py'),'w') as f:
        f.writelines(wrapper)
    try:
        shutil.copy(file_, work_dir)
    except Exception:
        print("NOOOO")

    py_in = os.path.realpath(os.path.join(sys.executable,os.pardir,'Scripts','pyinstaller.exe'))
    try:
        p = Popen([py_in, '-F', '--add-data', '{};.'.format(file_), os.path.abspath('data_wrapper.py'), '-n',
                   os.path.basename(file_)], stdout = PIPE, stderr = PIPE)
        out, err = p.communicate()
        print(out)
        print()
        print(err)
        print("Success:")
    except Exception as e:
        print("Failed")
        a=1






if __name__ == '__main__':
    build(r'D:\cambo\Docs\Projects\win-lock\prototype\tests\test_data\test_text.txt')