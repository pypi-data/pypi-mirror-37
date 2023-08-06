# -*- coding: utf-8 -*-

###########################
# Excel数据校验
# peakgao 2018.10.23
###########################

import os
import xlrd
from .common import FieldType,FieldInfo,getTypeByName,getCellName

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

    check_head = True # 是否在扫描头部信息区
    fieldList = [] # 记录有效的字段信息列表，无效的都忽略了

    idx_desc = -1 # 字段中文描述行，一个#
    idx_verify = -1 # 字段数据校验行，两个#
    idx_cstype = -1 # c/s归类类型行，三个#
    idx_name = -1 # 字段名
    idx_type = -1 # 字段类型
    idx_data = -1 # 数据行
    
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
                #csType = csType.upper()

                # 综合校验所有列
                for col in range(ncols):
                    fType = getTypeByName(sheet.cell_value(row, col))
                    fName = sheet.cell_value(idx_name, col)
                    if fType != None and fName != '': # 有效的列，必须类型有效且名字不为空
                        isValidField = True
                        if idx_cstype != -1: # 存在CS信息，则进行类型匹配处理
                            strCSType = sheet.cell_value(idx_cstype, col)
                        else: # 不存在CS信息，则当所有列满足条件
                            strCSType = "CS"
                        
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
                break
    # 处理数据
    
    n = len(fieldList)
    for k in range(n):
        fieldInfo = fieldList[k]
        col = fieldInfo.col           
        fieldType = fieldInfo.type				
        strCode = fieldInfo.verify

        for row in range(idx_data, nrows):
            strCellName = getCellName(row, col)
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
                    if strCode != '' and not eval(strCode): print('[%s] verify fail with code [%s]' % (strCellName, strCode))
                strCode = ''
            elif fieldType == FieldType.ShortArray:
                strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                v = strVal.split(strSeparator)
                for i in range(len(v)):
                    v[i] = int(v[i])
                innerCode = "v[i]>=-32768 and v[i]<=32767"
                for i in range(len(v)):
                    if not eval(innerCode): print('[%s:%d] verify fail with inner code [%s]' % (strCellName, i, innerCode))
                    if strCode != '' and not eval(strCode): print('[%s] verify fail with code [%s]' % (strCellName, strCode))
                strCode = ''
            elif fieldType == FieldType.IntArray:
                strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                v = strVal.split(strSeparator)
                for i in range(len(v)):
                    v[i] = int(v[i])
                for i in range(len(v)):
                    if strCode != '' and not eval(strCode): print('[%s] verify fail with code [%s]' % (strCellName, strCode))
                strCode = ''
            elif fieldType == FieldType.FloatArray:
                strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                v = strVal.split(strSeparator)
                for i in range(len(v)):
                    v[i] = float(v[i])
                for i in range(len(v)):
                    if strCode != '' and not eval(strCode): print('[%s] verify fail with code [%s]' % (strCellName, strCode))
                strCode = ''
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