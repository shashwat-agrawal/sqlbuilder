import inspect
import os
import re
import uuid

TESTBASE = None

def testbase():
    global TESTBASE
    if TESTBASE is None:
        TESTBASE = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

    return TESTBASE

def testdir():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    return os.path.join(
        testbase(),
        os.environ['TMPDIR_BASENAME'],
        os.path.relpath(module.__file__, testbase()),
        re.sub('-', '', uuid.uuid4().hex)
    )

def mkpath_tree_fatal(inpath, struct):
    if isinstance(struct, dict):
        os.makedirs(inpath)
        for subdir in sorted(struct.keys()):
            mkpath_tree_fatal(os.path.join(inpath, subdir), struct[subdir])
    elif isinstance(struct, list) or isinstance(struct, str):
        os.makedirs(os.path.dirname(inpath))
        file_text = ''
        if isinstance(struct, list):
            file_text = struct.join('\n')
        else:
            file_text = struct
        with open(inpath, 'w') as fp:
            fp.write(file_text)
    return