# -*- coding: utf-8 -*-

###########################
# 所有的转换操作
# peakgao 2018.10.20
###########################

import os
from .common import getFileMd5,readFileLastMd5,writeFileLastMd5,ensureDirExist
from .color import Color
from .excel2ts import ExcelToTs
from .excel2lua import ExcelToLua
from .excel2cs import ExcelToCs
from .excel2bcc import ExcelToBcc
from .excel2h import ExcelToH
from .excel2dbc import ExcelToDbc

# 转换Excel文件到指定类型的数据文件
def ConvertExcelDataToFile(srcFile, dstFile, convType, csType, hasGT):
    if convType == "ts": # 文本数据,TypeScript使用
        return ExcelToTs(srcFile, dstFile, csType, hasGT, '|')
    elif convType == "bcc": # 二进制数据,C#使用
        return ExcelToBcc(srcFile, dstFile, csType, hasGT, '|')
    elif convType == "dbc": # 二进制数据,C/C++使用
        return ExcelToDbc(srcFile, dstFile, csType, hasGT, '|')
    elif convType == "lua": # 文本数据,Lua使用
        return ExcelToLua(srcFile, dstFile, csType, hasGT, '|')
    else:
        raise Exception("Unknow convert type: " + convType)

# 将Excel字段结构导出成指定类型的文件结构
def ExportExcelStructToFile(srcFile, dstFile, convType, csType):    
    if convType == "h": # 文本结构,C/C++使用
        return ExcelToH(srcFile, dstFile, csType)
    elif convType == "cs": # 文本结构,C#使用
        return ExcelToCs(srcFile, dstFile, csType)
    else:
        raise Exception("Unknow convert type: " + convType)

# 辅助方法，对原始文件有MD5码验证，只有改变了的Excel文件才进行转换
def ConvertExcelDataToFileWhenChanged(srcFile, dstFile, logFile, convType, csType, hasGT):
    errId = 0
    errMsg = ''
    try:
        #fn = os.path.basename(srcFile)
        #ft = os.path.basename(os.path.splitext(srcFile)[0])
        #dstFile = os.path.normpath(os.path.dirname(srcFile) + "\\" + convType + "\\" + convType + "_" + ft + "." + convType)
        #logFile = os.path.normpath(os.path.dirname(srcFile) + "\\log\\" + fn + "." + convType  + "." + csType + ".txt")
        
        ensureDirExist(os.path.dirname(dstFile))
        ensureDirExist(os.path.dirname(logFile))
        
        needConvert = True
        if os.path.exists(dstFile) and os.path.exists(logFile):
            lastMd5 = readFileLastMd5(logFile)
            if lastMd5 != "" and lastMd5 == getFileMd5(srcFile):
                needConvert = False
        
        if needConvert:
            ret,msg = ConvertExcelDataToFile(srcFile, dstFile, convType, csType, hasGT)
            if ret == 1:
                newMd5 = getFileMd5(srcFile)
                writeFileLastMd5(logFile, newMd5)
            errId = ret
            errMsg = msg             
        else:
            errId = 2
            errMsg = "NOT CHANGED" 

    except ModuleNotFoundError as err:
        errId = -1
        errMsg = str(err)
    except BaseException as err:
        errMsg = str(err)

    return errId,errMsg

