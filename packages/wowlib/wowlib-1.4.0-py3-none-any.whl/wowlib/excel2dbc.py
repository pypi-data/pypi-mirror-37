# -*- coding: utf-8 -*-

###########################
# Excel转成dbc格式文本(用于C++读取的二进制文件)
# peakgao 2018.10.25
###########################

import os
import xlrd
from .common import FieldType,FieldInfo,getTypeByName,getCellName,getFieldSize,getFuncName,getTypeNameForCS,saveUtf8File

def ExcelToDbc(srcFile, dstFile, csType, hasGT, strSeparator):
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

    isEmpty = False
    fields = 0
    records = 0
    recordSize = 0
    
    
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

                            recordSize += getFieldSize(fieldInfo.type)
									
                fields = len(fieldList)
                records = nrows - idx_data
                break

    # 处理数据
    strCellName = ''
    try:
        import struct
        minId = 0xFFFFFFFF
        maxId = 0
        f = open(dstFile + ".1", 'wb')
        ff = open(dstFile + ".2", 'wb')
        ff.write(struct.pack('I', 0)) # 变长数据区前4个字节置为0，可用于空字符串和空数组的处理

        for row in range(idx_data, nrows):
            n = len(fieldList)
            for k in range(n):
                fieldInfo = fieldList[k]
                col = fieldInfo.col                
                fieldType = fieldInfo.type
                strCellName = getCellName(row, col)
                val = sheet.cell_value(row, col)
                
                if isinstance(val, float) and (val % 1 == 0): # Excel的整数读出来都是浮点，小数位为0，奇特，所以做下面处理
                    val = int(val)
                strVal = str(val)
                #if isinstance(strVal, str):
                strVal = strVal.strip() # 裁剪前后空白字符
                #strVal = strVal.replace("\\", "\\\\") # 英文反斜杠要转义
                #strVal = strVal.replace("\"", "\\\"") # 英文双引号要转义

                if len(strVal) == 0:
                    isEmpty = True
                else:
                    isEmpty = False

                if fieldType == FieldType.Byte:
                    f.write(struct.pack('B', int(strVal)))
                elif fieldType == FieldType.Short:
                    f.write(struct.pack('h', int(strVal)))
                elif fieldType == FieldType.Int:
                    f.write(struct.pack('i', int(strVal)))
                elif fieldType == FieldType.Index or fieldType == FieldType.Key:
                    v = int(strVal)
                    f.write(struct.pack('I', v))
                    if v > maxId: maxId = v
                    if v < minId: minId = v
                elif fieldType == FieldType.Float:
                    f.write(struct.pack('f', float(strVal)))
                elif (fieldType == FieldType.Map or
                    fieldType == FieldType.String or
                    fieldType == FieldType.NString):
                    if isEmpty:
                        f.write(struct.pack('I', 0))
                    else:
                        f.write(struct.pack('I', ff.tell()))
                        u8 = strVal.encode('utf-8')
                        #ff.write(struct.pack('H', len(u8)))
                        ff.write(u8)
                        f.write(struct.pack('B', 0)) # C++字符串的\0标记
                elif (fieldType == FieldType.ByteArray):
                    strVal = strVal.strip(strSeparator)
                    if isEmpty:
                        f.write(struct.pack('I', 0))
                    else:
                        f.write(struct.pack('I', ff.tell()))
                        v = strVal.split(strSeparator)
                        ff.write(struct.pack('I', len(v)))
                        for i in range(len(v)):
                            ff.write(struct.pack('B', int(v[i])))
                elif fieldType == FieldType.ShortArray:
                    strVal = strVal.strip(strSeparator)
                    if isEmpty:
                        f.write(struct.pack('I', 0))
                    else:
                        f.write(struct.pack('I', ff.tell()))
                        v = strVal.split(strSeparator)
                        ff.write(struct.pack('I', len(v)))
                        for i in range(len(v)):
                            ff.write(struct.pack('h', int(v[i])))
                elif fieldType == FieldType.IntArray:
                    strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                    if isEmpty:
                        f.write(struct.pack('I', 0))
                    else:
                        f.write(struct.pack('I', ff.tell()))
                        v = strVal.split(strSeparator)
                        ff.write(struct.pack('I', len(v)))
                        for i in range(len(v)):
                            ff.write(struct.pack('i', int(v[i])))
                elif fieldType == FieldType.FloatArray:
                    strVal = strVal.strip(strSeparator) # 裁剪前后分隔符
                    if isEmpty:
                        f.write(struct.pack('I', 0))
                    else:
                        f.write(struct.pack('I', ff.tell()))
                        v = strVal.split(strSeparator)
                        ff.write(struct.pack('I', len(v)))
                        for i in range(len(v)):
                            ff.write(struct.pack('f', float(v[i])))
                elif fieldType == FieldType.Remark:
                    f.write(struct.pack('I', 0))
        
        strCellName = ''
        ID = 0x00CCBBDD
        file = open(dstFile, 'wb')
        file.write(struct.pack('I', ID))
        file.write(struct.pack('I', records))
        file.write(struct.pack('I', fields))
        file.write(struct.pack('I', recordSize))
        file.write(struct.pack('I', ff.tell())) # 变长缓冲区大小
        #file.write(struct.pack('I', minId))
        #file.write(struct.pack('I', maxId))
        # 写入字段列表
        n = len(fieldList)
        for k in range(n):
            fieldInfo = fieldList[k]
            file.write(struct.pack('B', fieldInfo.type.value))

        # 写定长数据
        f_len = f.tell()
        f.close()
        f = open(dstFile + ".1", 'rb')
        data = f.read(f_len)
        file.write(data)
        f.close()
        os.remove(dstFile + ".1")

        # 写变长数据
        ff_len = ff.tell()
        ff.close()
        ff = open(dstFile + ".2", 'rb')
        data = ff.read(ff_len)
        file.write(data)
        ff.close()
        os.remove(dstFile + ".2")

        file.close()

    except BaseException as err:
        if strCellName != '':
            return -1, '[' + strCellName + '] ' + str(err)
        else:
            return -1, str(err)

    return 1, "OK"
