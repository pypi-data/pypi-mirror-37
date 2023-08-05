import os
import jpype


def init_jvm():
    jvm_path = jpype.get_default_jvm_path()
    file_path = os.path.dirname(os.path.realpath(__file__))
    jars_path = os.path.join(file_path, 'jars')
    jars = [os.path.join(jars_path, f) for f in os.listdir(jars_path)]
    jpype.startJVM(jvm_path, '-Djava.class.path={}'.format(os.pathsep.join(jars)), '-Dfile.encoding=UTF8', '-ea')


def load_okt():
    if not jpype.isJVMStarted():
        init_jvm()

    return jpype.JPackage('net.ingtra.pyokt').OpenKoreanTextWrapper


def java_bool(bool):
    return jpype.java.lang.Boolean(bool)