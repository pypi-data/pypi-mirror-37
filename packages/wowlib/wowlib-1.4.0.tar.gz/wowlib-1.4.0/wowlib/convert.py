# -*- coding: utf-8 -*-

###########################
# 所有的转换操作
# peakgao 2018.10.20
###########################

import os
from .common import getFileMd5,readFileLastMd5,writeFileLastMd5
from .color import Color
from .excel2ts import ExcelToTs
from .excel2cs import ExcelToCs
from .excel2bcc import ExcelToBcc
from .excel2h import ExcelToH
from .excel2dbc import ExcelToDbc

def RealExcelToTarget(srcFile, dstFile, convType, csType, hasGT):
    if convType == "ts":
        return ExcelToTs(srcFile, dstFile, csType, hasGT, '|')
    elif convType == "cs":
        return ExcelToCs(srcFile, dstFile, csType)
    elif convType == "bcc":
        return ExcelToBcc(srcFile, dstFile, csType, hasGT, '|')
    elif convType == "h":
        return ExcelToH(srcFile, dstFile, csType)
    elif convType == "dbc":
        return ExcelToDbc(srcFile, dstFile, csType, hasGT, '|')
    else:
        raise Exception("Unknow convert type: " + convType)

def ExcelToTarget(srcFile, convType, csType, hasGT):
    errId = 0
    errMsg = ''
    try:
        #clr = Color()

        fn = os.path.basename(srcFile)
        ft = os.path.basename(os.path.splitext(srcFile)[0])
        dstFile = os.path.normpath(os.path.dirname(srcFile) + "\\" + convType + "\\" + convType + "_" + ft + "." + convType)
        logFile = os.path.normpath(os.path.dirname(srcFile) + "\\log\\" + fn + "." + convType  + "." + csType + ".txt")
        
        parent_path = os.path.dirname(dstFile)
        if not os.path.isdir(parent_path):
            os.makedirs(parent_path)

        parent_path = os.path.dirname(logFile)
        if not os.path.isdir(parent_path):
            os.makedirs(parent_path)
        
        needConvert = True
        if os.path.exists(dstFile) and os.path.exists(logFile):
            lastMd5 = readFileLastMd5(logFile)
            if lastMd5 != "" and lastMd5 == getFileMd5(srcFile):
                needConvert = False
        
        if needConvert:
            ret,msg = RealExcelToTarget(srcFile, dstFile, convType, csType, hasGT)
            if ret == -1:
                #clr.print_red_text(msg)
                errId = -1
                errMsg = msg
            elif ret == 0:
                errId = 0
                errMsg = msg
            else:
                newMd5 = getFileMd5(srcFile)
                writeFileLastMd5(logFile, newMd5)
                errId = 1                
        else:
            errId = 2

    except ModuleNotFoundError as err:
        #clr.print_red_text(str(err))
        errId = -1
        errMsg = str(err)
    except BaseException as err:
        #clr.print_red_text(str(err))
        errMsg = str(err)

    return dstFile,errId,errMsg

