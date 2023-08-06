# -*- coding: utf-8 -*-

#####################################
# Excel将数据结构转成c/c++格式的头文件
# peakgao 2018.10.25
#####################################

import os
import xlrd
from .common import FieldType,FieldInfo,getTypeByName,getCellName,getFieldSize,getFuncName,getTypeNameForCpp,saveUtf8File,ensureDirExist

def ExcelToH(srcFile, dstFile, csType):
    strCellName = ''
    try:
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

        out = "" # 输出文本
        recordSize = 0
        maxNameLength = 0
        maxTypeLength = 0

        # 扫描数据头信息
        for row in range(nrows):
            if check_head: # 头部区域
                strCellName = getCellName(row, 0)
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
                        strCellName = getCellName(row, col)
                        fType = getTypeByName(sheet.cell_value(row, col))
                        fName = sheet.cell_value(idx_name, col)
                        if fType != None and fName != '': # 有效的列，必须类型有效且名字不为空
                            isValidField = True
                            if idx_cstype != -1: # 存在CS信息，则进行类型匹配处理
                                strCSType = sheet.cell_value(idx_cstype, col).strip('#')
                                if strCSType == '' or strCSType.upper().find(csType) < 0:
                                    isValidField = False
                                else:
                                    isValidField = True
                            else: # 不存在CS信息，则当所有列满足条件
                                strCSType = csType
                                isValidField = True
                            
                            if isValidField: # 有效字段，记录下来
                                fieldInfo = FieldInfo()
                                fieldInfo.col = col
                                if idx_desc >= 0:
                                    fieldInfo.desc = sheet.cell_value(idx_desc, col).strip('#')
                                if idx_verify >= 0:
                                    fieldInfo.verify = sheet.cell_value(idx_verify, col).strip('#')
                                fieldInfo.cstype = strCSType
                                fieldInfo.name = fName
                                fieldInfo.type = fType
                                fieldList.append(fieldInfo)
                                
                                recordSize += getFieldSize(fieldInfo.type)
                                if len(fieldInfo.name) > maxNameLength:
                                    maxNameLength = len(fieldInfo.name)
                                type_len = len(getTypeNameForCpp(fType))
                                if type_len > maxTypeLength:
                                    maxTypeLength = type_len
                    break

        # 处理数据

        # 写表名
        # tableName = sheet.name[0].upper() + sheet.name[1:].lower()
        tableName = sheet.name.capitalize()

        out += "struct Entry_" + tableName + " : public Entry\n"
        out += "{\n"

        # 处理字段名列表            
        n = len(fieldList)
        maxTypeLength = (maxTypeLength+3) & ~3
        maxNameLength = (maxNameLength+1+3) & ~3
        for i in range(n):
            fieldInfo = fieldList[i]
            out += "    " + getTypeNameForCpp(fieldInfo.type).ljust(maxTypeLength) + (fieldInfo.name + ";").ljust(maxNameLength)
            if fieldInfo.desc != '':
                out += "// " + fieldInfo.desc
            out += "\n"
        out += "};\n"

        ensureDirExist(os.path.dirname(dstFile))
        saveUtf8File(dstFile, out)

    except BaseException as err:
        if strCellName != '':
            return -1, '[' + strCellName + '] ' + str(err)
        else:
            return -1, str(err)

    return 1, "OK"
