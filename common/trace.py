

import os
import sys
import types
import traceback

tab="  "
callLevel=-1

def log(logName,msg):
    print msg

def objectName(obj):
    name=repr(obj)
    if (hasattr(obj,"__class__") and
        name[0]=="<" and name[-1]==">" and "0x" in name):
        class_=obj.__class__.__name__
        id_=hex(id(obj))
        return "%s(%s)"%(class_,id_)
    return name

def functionName(func):
    module="%s."%func.__module__ if hasattr(func,"__module__") else ""
    class_="%s."%func.im_class.__name__ if hasattr(func,"im_class") else ""
    if class_:
        return "%s.%s"%(class_,func.__name__)
    else:
        return "%s.%s"%(module,func.__name__)

def traceModule(module=None):
    if not module:
        try:
            raise ZeroDivisionError
        except ZeroDivisionError:
            frame=sys.exc_info()[2].tb_frame.f_back
        module=frame.f_globals

    moduleName=module["__name__"]
    logName="%s_trace"%moduleName.split(".")[0]
    print "trace module",moduleName

    for key,value in module.items():
        if key[0]=="_": continue
        if hasattr(value,"__module__") and value.__module__==moduleName:
            if type(value) is types.FunctionType:
                print "\tfunction",key
            elif type(value) is type.ClassType:
                traceClass(value,logName)
            elif type(value) is type.TypeType:
                traceClass(value,logName)

def traceClass(class_,logName):
    if not logName:
        moduleName=class_.__module__
        logName="%s_trace"%moduleName.split(".")[0]
    print "\tclass",class_.__name__
    for key in class_.__dict__:
        value=getattr(class_,key)
        if key[0]=="_": continue
        if callable(value):
            print "\t\t%s"%key
            setattr(class_,key,traceFunction(value,logName))

def traceFunction(function,logName=None):
    if not logName:
        moduleName=function.__module__
        logName="%s_trace"%moduleName.split(".")[0]

    def newFunction(*args,**kw):
        global callLevel
        callLevel+=1

        prefix=tab*callLevel
        argString=",".join(map(objectName,args))
        kwString=",".join("%s:%s"%(key,objectName(value)) for key,value in kw.items())
        callString="%s%s("%(prefix,functionName(functionName))
        if argString: callString+=argString
        if kwString: callString+=kwString
        callString+=")"
        log(logName,callString)

        try:
            ret=function(*args,**kw)
        except:
            lines=traceback.format_exc().split("\n")
            lines=["%s%s"%(prefix,line) for line in lines]
            for line in lines: log(logName,line)
            callLevel-=1
            raise
        if ret is not None:
            returnString="%sreturn %s"%(prefix,objectName(ret))
            log(logName,returnString)
        callLevel-=1
        return ret

    return newFunction

trace=traceFunction



