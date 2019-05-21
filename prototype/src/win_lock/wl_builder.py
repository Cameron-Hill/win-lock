import sys
import os
import shutil
import win_lock
from subprocess import Popen, PIPE
from win_lock.log_manager import get_logger, project_root
logger = get_logger(__name__)

work_dir = os.path.join(project_root,'work')
test_dir = os.path.join(project_root,'tests')
log_file = os.path.join(project_root, 'logs', 'wrapper_logs.log')
log_file = os.environ.get('WRAPPER_LOGS',log_file)
base_wrapper_file = os.path.join(os.path.dirname(__file__),'data_wrapper.pyw')

def build(file_, remove=True):
    wrapper_file = os.path.join(work_dir, os.path.basename(base_wrapper_file))
    base_dir = os.path.dirname(file_)
    prepare_work(file_, wrapper_file)
    build_exe(file_, wrapper_file, base_dir)
    clean_work()
    if remove:
        os.remove(file_)


def prepare_work(file_, wrapper_file):
    os.mkdir(work_dir) if not os.path.exists(work_dir) else None
    logger.info("Copying wrapper: {} to {}".format(base_wrapper_file, work_dir))
    shutil.copy(base_wrapper_file,work_dir)
    with open(wrapper_file,'r') as f:
        wrapper = f.read()
        wrapper = wrapper.replace('$DATA_FILE',os.path.basename(file_))
        wrapper = wrapper.replace('$LOG_FILE',log_file)
    try:
        with open(os.path.join(work_dir,wrapper_file),'w') as f:
            logger.info("Adding {} to build wrapper".format(file_))
            f.writelines(wrapper)
    except IOError:
        logger.exception("Failed to write wrapper file to work {}".format(wrapper_file))
        raise
    logger.info("Copying {} to files to {}".format(file_, work_dir))
    shutil.copy(file_, work_dir)

def build_exe(file_, wrapper_file, base_dir):
    py_in = os.path.realpath(os.path.join(sys.executable,os.pardir,'Scripts','pyinstaller.exe'))
    try:
        this_dir = os.getcwd()
        os.chdir(work_dir)
        args = [py_in, '-F', '--noconsole', '--add-data', '{};.'.format(file_), wrapper_file, '-n',
                os.path.basename(file_)]
        logger.info("Building with args {}".format(args))
        p = Popen(args, stdout = PIPE, stderr = PIPE)
        out, err = p.communicate()
        os.chdir(this_dir)
        logger.debug("OUT:  {}\nERR:   {}".format(out.decode(), err.decode()))
        if 'completed successfully' in out.decode() or 'completed successfully' in err.decode():
            logger.info("Build Finished Successfully")
            try:
                target_file = os.path.join(work_dir,'dist',os.path.basename(file_)+'.exe')
                logger.info("Moving {} to {}".format(target_file, base_dir))
                shutil.copy(target_file, base_dir)
            except Exception as e:
                logger.exception("Failed to copy {} to {}".format(target_file, base_dir))
                raise
        else:
            logger.error("Build Failed")
            return
    except Exception as e:
        logger.exception("Failed: \n{}".format(e))
        raise e
    return target_file


def clean_work():
    logger.info("Cleaning Work Directory: {}".format(work_dir))
    for x in os.listdir(work_dir):
        if os.path.isdir(os.path.join(work_dir, x)):
            shutil.rmtree(os.path.join(work_dir, x))
        else:
            os.remove(os.path.join(work_dir, x))
    logger.info("Finished Cleaning Work Directory")
