import sys
import os
import shutil
import win_lock
from subprocess import Popen, PIPE
work_dir = os.path.realpath(os.path.join(os.path.dirname(win_lock.__file__), os.pardir,os.pardir,'work'))
test_dir = os.path.realpath(os.path.join(os.path.dirname(win_lock.__file__), os.pardir,os.pardir,'tests'))

def build(file_):
    with open('data_wrapper.py','r') as f:
        wrapper = f.readlines()
        wrapper[0] = wrapper[0].replace('$',os.path.basename(file_))
    with open(os.path.join(work_dir,'data_wrapper.py'),'w') as f:
        print("Adding {} to bulid wrapper".format(file_))
        f.writelines(wrapper)
    
    print("Copying {} to files to {}".format(file_, work_dir))
    shutil.copy(file_, work_dir)
    

    py_in = os.path.realpath(os.path.join(sys.executable,os.pardir,'Scripts','pyinstaller.exe'))
    try:
        this_dir = os.getcwd()
        os.chdir(work_dir)
        args = [py_in, '-F', '--add-data', '{};.'.format(file_), os.path.abspath('data_wrapper.py'), '-n', 
                os.path.basename(file_)]
        print("Building with args {}".format(args))
        p = Popen(args, stdout = PIPE, stderr = PIPE)
        out, err = p.communicate()
        os.chdir(this_dir)    
        print("OUT:  {}\nERR:   {}".format(out,err))
    except Exception as e:
        print("Failed: \n{}".format(e))
        raise e






if __name__ == '__main__':
    build(os.path.join(test_dir,'test_data','test_text.txt.wl'))    