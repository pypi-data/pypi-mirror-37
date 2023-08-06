# -*- coding: utf-8 -*-

###########################
# Excel转成Ts格式文本
# peakgao 2018.10.20
###########################

import os
import xlrd
#from pathlib import Path
from .common import FieldType,getTypeByName,saveUtf8File

def ExcelToTs(srcFile, dstFile, csType, hasGT, strSeparator):
    srcFile = os.path.abspath(srcFile)
    if not os.path.isfile(srcFile):
        return 0, "Missing '" + srcFile + "'"

    book = xlrd.open_workbook(srcFile)
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    # 循环打印每一行的内容
    #for i in range(nrows):            print(sheet.row_values(i))
    #for i in range(ncols):            print(sheet.col_values(i))

    check_head = True # 是否在检测头部信息区
    cstype_array = bytearray(ncols) # 记录每一列是否匹配csType
    for col in range(ncols): cstype_array[col] = 1
    type_array = [] # 记录每一列的字段类型

    idx_desc = -1 # 字段中文描述行，一个#
    idx_verify = -1 # 字段数据校验行，两个#
    idx_cstype = -1 # c/s归类类型行，三个#
    idx_name = -1 # 字段名
    idx_type = -1 # 字段类型

    hasIndexCol = False # 是否第一列是索引列
    hasNString = False # 是否存在中文字符串字段
    hadWriteIndex = False
    sep = ''
    isEmpty = False
    totalText = '' # 输出的字符串
    
    for row in range(nrows):
        if check_head: # 头部区域
            col0_str = sheet.cell_value(row, 0)
            if col0_str.find('###') == 0:
                idx_cstype = row
                csType = csType.upper()
                for col in range(ncols):
                    if sheet.cell_value(row, col).upper().find(csType) < 0:
                        cstype_array[col] = 0
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
                check_head = False
                for col in range(ncols):
                    iFieldType = getTypeByName(sheet.cell_value(row, col))
                    type_array.append(iFieldType)
                    if hasNString == False and iFieldType == FieldType.NString:
                        hasNString = True
                        if hasGT:
                            totalText += "import _GT from './getstring';\n"
                if type_array[0] == FieldType.Index or type_array[0] == FieldType.Key or type_array[0] == FieldType.Map:
                    hasIndexCol = True
                totalText += "export default {\n"
                continue

        else: # 数据区域
            hadWriteIndex = False
            for col in range(ncols):
                if cstype_array[col] == 1: # 有效列
                    fieldType = type_array[col]
                    strFieldName = sheet.cell_value(idx_name, col)
                    val = sheet.cell_value(row, col)
                    
                    if isinstance(val, float) and (val % 1 == 0): # Excel的整数读出来都是浮点，小数位为0，奇特，所以做下面处理
                        val = int(val)
                    strVal = str(val)
                    #if isinstance(strVal, str):
                    strVal = strVal.strip() # 裁剪前后空白字符

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
                        totalText = totalText + sep + strFieldName + ':""'
                    elif fieldType == FieldType.Index or fieldType == FieldType.Key:
                        if hasIndexCol and (not hadWriteIndex):
                            totalText = totalText + "[" + strVal + "]:{" + sep + strFieldName + ":" + strVal
                            hadWriteIndex = True
                    elif (fieldType == FieldType.Byte or 
                        fieldType == FieldType.Short or
                        fieldType == FieldType.Int or
                        fieldType == FieldType.Index or
                        fieldType == FieldType.Float or
                        fieldType == FieldType.Key):
                        if isEmpty:
                            strVal = "0"
                        totalText = totalText + sep + strFieldName + ":" + strVal
                    elif fieldType == FieldType.Map:
                        if hasIndexCol and (not hadWriteIndex):
                            totalText = totalText + "'" + strVal  + "':{" + sep + strFieldName + ":'" + strVal + "'"
                            hadWriteIndex = True
                    elif fieldType == FieldType.String:
                        if isEmpty:
                            totalText = totalText + sep + strFieldName + ':""'
                        else:
                            totalText = totalText + sep + strFieldName + ':"' + strVal + '"'
                    elif fieldType == FieldType.NString:
                        if isEmpty:
                            totalText = totalText + sep + strFieldName + ':""'
                        elif hasGT:
                            totalText = totalText + sep + strFieldName + ':_GT("' + strVal + '")'
                        else:
                            totalText = totalText + sep + strFieldName + ':"' + strVal + '"'
                    elif (fieldType == FieldType.ByteArray or 
                        fieldType == FieldType.ShortArray or
                        fieldType == FieldType.FloatArray or
                        fieldType == FieldType.IntArray):
                        strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                        if isEmpty:
                            totalText = totalText + sep + strFieldName + ":[" + strVal + "]"
                        else:
                            strVal = strVal.replace(strSeparator, ",")
                            totalText = totalText + sep + strFieldName + ":[" + strVal + "]"
                    else:
                        totalText = totalText + sep + strVal
                        #print(sheet.cell_value(row, col))

            totalText = totalText + "},\n"

    totalText = totalText + "};\n"
    saveUtf8File(dstFile, totalText)
    return 1, "OK"
