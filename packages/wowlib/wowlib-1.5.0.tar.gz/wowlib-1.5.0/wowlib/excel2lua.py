# -*- coding: utf-8 -*-

###########################
# Excel转成lua格式文本
# peakgao 2018.10.26
###########################

import os
import xlrd
from .common import FieldType,FieldInfo,getTypeByName,getCellName,saveUtf8File,ensureDirExist

def ExcelToLua(srcFile, dstFile, csType, hasGT, strSeparator):
    srcFile = os.path.abspath(srcFile)
    if not os.path.isfile(srcFile):
        return 0, "Missing '" + srcFile + "'"

    book = xlrd.open_workbook(srcFile)
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    if nrows == 0 or ncols == 0: # 空文件
        return 0, "Not data from '" + srcFile + "'"

    check_head = True # 是否在扫描头部信息区
    fieldList = [] # 记录有效的字段信息列表，无效的都忽略了

    idx_desc = -1 # 字段中文描述行，一个#
    idx_verify = -1 # 字段数据校验行，两个#
    idx_cstype = -1 # c/s归类类型行，三个#
    idx_name = -1 # 字段名
    idx_type = -1 # 字段类型
    idx_data = -1 # 数据行

    hasIndexCol = False # 是否第一列是索引列
    hasNString = False # 是否存在中文字符串字段
    hadWriteIndex = False
    sep = ''
    isEmpty = False
    totalText = '' # 输出的字符串
    
    # 扫描数据头信息
    for row in range(nrows):
        if check_head: # 头部区域
            col0_str = sheet.cell_value(row, 0)
            if col0_str.find('###') == 0:
                idx_cstype = row
                continue
            elif col0_str.find('##') == 0:
                idx_verify = row
                continue
            elif col0_str.find('#') == 0:
                idx_desc = row
                continue
            elif idx_name == -1:
                idx_name = row
                continue
            elif idx_type == -1:
                idx_type = row
                idx_data = row + 1
                check_head = False
                csType = csType.upper()

                # 综合校验所有列
                for col in range(ncols):
                    fType = getTypeByName(sheet.cell_value(row, col))
                    fName = sheet.cell_value(idx_name, col)
                    if fType != None and fName != '': # 有效的列，必须类型有效且名字不为空
                        isValidField = True
                        if idx_cstype != -1: # 存在CS信息，则进行类型匹配处理
                            strCSType = sheet.cell_value(idx_cstype, col)
                            if strCSType == '' or strCSType.upper().find(csType) < 0:
                                isValidField = False
                            else:
                                isValidField = True
                        else: # 不存在CS信息，则当所有列满足条件
                            strCSType = csType
                            isValidField = True
                        
                        if isValidField: # 有效字段，记录下来
                            fDesc = sheet.cell_value(idx_desc, col)
                            fVerify = sheet.cell_value(idx_verify, col)
                            fieldInfo = FieldInfo()
                            fieldInfo.col = col
                            fieldInfo.desc = fDesc.strip('#')
                            fieldInfo.verify = fVerify.strip('#')
                            fieldInfo.cstype = strCSType.strip('#')
                            fieldInfo.name = fName
                            fieldInfo.type = fType
                            fieldList.append(fieldInfo)

                            if hasNString == False and fType == FieldType.NString:
                                hasNString = True
                break

    # 处理数据
    strCellName = ''
    try:
        tableName = sheet.name.capitalize()
        if hasNString and hasGT:
            totalText += "require 'getstring'\nCfg = Cfg or {}\n"
        if fieldList[0].type == FieldType.Index or fieldList[0].type == FieldType.Key or fieldList[0].type == FieldType.Map:
            hasIndexCol = True
        totalText += "Cfg." + tableName + " = {\n"

        for row in range(idx_data, nrows):
            hadWriteIndex = False
            n = len(fieldList)
            for i in range(n):
                fieldInfo = fieldList[i]
                col = fieldInfo.col
                fieldType = fieldInfo.type
                strCellName = getCellName(row, col)
                strFieldName = fieldInfo.name
                val = sheet.cell_value(row, col)
                
                if isinstance(val, float) and (val % 1 == 0): # Excel的整数读出来都是浮点，小数位为0，奇特，所以做下面处理
                    val = int(val)
                strVal = str(val)
                #if isinstance(strVal, str):
                strVal = strVal.strip() # 裁剪前后空白字符
                #strVal = strVal.replace("\\", "\\\\") # 英文反斜杠要转义
                #strVal = strVal.replace("\"", "\\\"") # 英文双引号要转义

                if hasIndexCol:
                    if col <= 0:
                        sep = ""
                    else:
                        sep = ","
                else:
                    if col == 0:
                        sep = ""
                    else:
                        sep = ","
                
                if len(strVal) == 0:
                    isEmpty = True
                else:
                    isEmpty = False
        
                if not hasIndexCol:
                    if col == 0:
                        totalText = totalText + "{"

                if fieldType == FieldType.Remark:
                    totalText = totalText + sep + strFieldName + '=""'
                elif fieldType == FieldType.Index or fieldType == FieldType.Key:
                    if hasIndexCol and (not hadWriteIndex):
                        totalText = totalText + "[" + strVal + "]={" + sep + strFieldName + "=" + strVal
                        hadWriteIndex = True
                elif (fieldType == FieldType.Byte or 
                    fieldType == FieldType.Short or
                    fieldType == FieldType.Int or
                    fieldType == FieldType.Index or
                    fieldType == FieldType.Float or
                    fieldType == FieldType.Key):
                    if isEmpty:
                        strVal = "0"
                    totalText = totalText + sep + strFieldName + "=" + strVal
                elif fieldType == FieldType.Map:
                    if hasIndexCol and (not hadWriteIndex):
                        totalText = totalText + '"' + strVal  + '"={' + sep + strFieldName + '="' + strVal + '"'
                        hadWriteIndex = True
                elif fieldType == FieldType.String:
                    if isEmpty:
                        totalText = totalText + sep + strFieldName + '=""'
                    else:
                        totalText = totalText + sep + strFieldName + '=[[' + strVal + ']]'
                elif fieldType == FieldType.NString:
                    if isEmpty:
                        totalText = totalText + sep + strFieldName + '=""'
                    elif hasGT:
                        totalText = totalText + sep + strFieldName + '=_GT([[' + strVal + ']])'
                    else:
                        totalText = totalText + sep + strFieldName + '=[[' + strVal + ']]'
                elif (fieldType == FieldType.ByteArray or 
                    fieldType == FieldType.ShortArray or
                    fieldType == FieldType.FloatArray or
                    fieldType == FieldType.IntArray):
                    strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                    if isEmpty:
                        totalText = totalText + sep + strFieldName + "={" + strVal + "}"
                    else:
                        strVal = strVal.replace(strSeparator, ",")
                        totalText = totalText + sep + strFieldName + "={" + strVal + "}"
                else:
                    totalText = totalText + sep + strVal
                    #print(sheet.cell_value(row, col))

            totalText = totalText + "},\n"

        totalText = totalText + "}\n"
        ensureDirExist(os.path.dirname(dstFile))
        saveUtf8File(dstFile, totalText)

    except BaseException as err:
        if strCellName != '':
            return -1, '[' + strCellName + '] ' + str(err)
        else:
            return -1, str(err)

    return 1, "OK"
