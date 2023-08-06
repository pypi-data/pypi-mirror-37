# -*- coding: utf-8 -*-

###########################
# Excel数据校验
# peakgao 2018.10.23
###########################

import os
import xlrd
from .common import FieldType,getTypeByName,getCellName

def ExcelVerify(srcFile, strSeparator = '|'):
    srcFile = os.path.abspath(srcFile)
    if not os.path.isfile(srcFile):
        return 0, "Missing '" + srcFile + "'"

    book = xlrd.open_workbook(srcFile)
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    if nrows == 0 or ncols == 0: # 空文件
        return 0, "Not data from '" + srcFile + "'"

    check_head = True # 是否在检测头部信息区    
    verify_array = [] # 记录每一列的校验代码
    type_array = [] # 记录每一列的字段类型

    idx_verify = -1 # 字段数据校验行，两个#
    idx_name = -1 # 字段名
    idx_type = -1 # 字段类型
    
    for row in range(nrows):
        if check_head: # 头部区域
            col0_str = sheet.cell_value(row, 0)
            if col0_str.find('###') == 0:
                continue
            elif col0_str.find('##') == 0:
                idx_verify = row
                code = col0_str[2:]
                verify_array.append(code)
                for col in range(1, ncols):
                    code = sheet.cell_value(row, col)
                    verify_array.append(code)
                continue
            elif col0_str.find('#') == 0:
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
                continue
        else: # 数据区域
            for col in range(ncols):
                strCode = verify_array[col]
                strCellName = getCellName(row, col)
                fieldType = type_array[col]
                val = sheet.cell_value(row, col)
                
                if isinstance(val, float) and (val % 1 == 0): # Excel的整数读出来都是浮点，小数位为0，奇特，所以做下面处理
                    val = int(val)
                strVal = str(val)
                #if isinstance(strVal, str):
                strVal = strVal.strip() # 裁剪前后空白字符
                strVal = strVal.replace("\\", "\\\\") # 英文反斜杠要转义
                strVal = strVal.replace("\"", "\\\"") # 英文双引号要转义

                if fieldType == FieldType.Byte:
                    v = int(strVal)
                    innerCode = "v>=0 and v<=255"
                    if not eval(innerCode): print('[%s] verify fail with inner code [%s]' % (strCellName, innerCode))
                elif fieldType == FieldType.Short:
                    v = int(strVal)
                    innerCode = "v>=-32768 and v<=32767"
                    if not eval(innerCode): print('[%s] verify fail with inner code [%s]' % (strCellName, innerCode))
                elif fieldType == FieldType.Int or fieldType == FieldType.Index:
                    v = int(strVal)
                elif fieldType == FieldType.Float:
                    v = float(strVal)
                elif fieldType == FieldType.ByteArray:
                    strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                    v = strVal.split(strSeparator)
                    for i in range(len(v)):
                        v[i] = int(v[i])
                    innerCode = "v[i]>=0 and v[i]<=255"
                    for i in range(len(v)):
                        if not eval(innerCode): print('[%s:%d] verify fail with inner code [%s]' % (strCellName, i, innerCode))
                elif fieldType == FieldType.ShortArray:
                    strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                    v = strVal.split(strSeparator)
                    for i in range(len(v)):
                        v[i] = int(v[i])
                    innerCode = "v[i]>=-32768 and v[i]<=32767"
                    for i in range(len(v)):
                        if not eval(innerCode): print('[%s:%d] verify fail with inner code [%s]' % (strCellName, i, innerCode))
                elif fieldType == FieldType.IntArray:
                    pass
                elif fieldType == FieldType.FloatArray:
                    pass
                elif (fieldType == FieldType.Key or 
                    fieldType == FieldType.Remark or
                    fieldType == FieldType.Map or
                    fieldType == FieldType.String or
                    fieldType == FieldType.NString):
                    v = strVal
                else:
                    pass
                
                if strCode != '' and not eval(strCode): print('[%s] verify fail with code [%s]' % (strCellName, strCode))
    return 1, "OK"