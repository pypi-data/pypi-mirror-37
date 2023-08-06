# -*- coding: utf-8 -*-

###########################
# 公共的枚举值定义
# peakgao 2018.10.20
###########################

from enum import Enum,unique

@unique
class FieldType(Enum):
    Byte = 0
    Short = 1
    Int = 2
    Float = 3
    ByteArray = 4
    ShortArray = 5
    IntArray = 6
    FloatArray = 7
    String = 8
    NString = 9
    Remark = 10
    Index = 11
    Key = 12
    Map = 13  

def saveUtf8File(filename, contents):
    parent_path = os.path.dirname(filename)
    if not os.path.isdir(parent_path):
        os.makedirs(parent_path) # 递归创建目录
    fh = open(filename, 'w', encoding='utf-8')
    fh.write(contents)
    fh.close()

def getTypeByName(typeName):
    typeName == typeName.lower()
    if typeName == "byte":
        return FieldType.Byte
    elif typeName == "short":
        return FieldType.Short
    elif typeName == "int":
        return FieldType.Int
    elif typeName == "float":
        return FieldType.Float
    elif typeName == "byte[]":
        return FieldType.ByteArray
    elif typeName == "short[]":
        return FieldType.ShortArray
    elif typeName == "int[]":
        return FieldType.IntArray
    elif typeName == "float[]":
        return FieldType.FloatArray
    elif typeName == "string":
        return FieldType.String
    elif typeName == "nstring":
        return FieldType.NString
    elif typeName == "remark":
        return FieldType.Remark
    elif typeName == "index":
        return FieldType.Index
    elif typeName == "key":
        return FieldType.Key
    elif typeName == "map":
        return FieldType.Map
    else:
        return None

import os,hashlib#,datetime

def getFileMd5(filename):
    if not os.path.isfile(filename):
        return ''
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

"""
starttime = datetime.datetime.now()
print(getFileMd5("E:\\works\\nodejs\\python\\demo.xls"))
endtime = datetime.datetime.now()
print('运行时间：%ds'%((endtime-starttime).seconds))
"""

def readFileLastMd5(filename):
    s = ""
    if not os.path.isfile(filename):
        return s    
    f = open(filename)    
    try:
        s = f.read()
    finally:
        f.close()
    return s

def writeFileLastMd5(filename, strMd5):
    parent_path = os.path.dirname(filename)
    if not os.path.isdir(parent_path):
        os.makedirs(parent_path) # 递归创建目录    
    f = open(filename, 'w')    
    try:
        f.write(strMd5)
    finally:
        f.close()

