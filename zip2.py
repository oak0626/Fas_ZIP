import struct
import zlib
import os

#  10진수로 변환 (data offset 구하기 위해)
def little2(hex): 
    return struct.unpack('<H', hex)[0] # little endian 정렬, 2byte

f = open('test.zip', 'rb+')

# 반복해서 local file signature offset 찾기
LocalFile_signature = b'\x50\x4B\x03\x04'
CentralFile_signature = b'\x50\x4B\x01\x02'
LocalFile_signature_offset = []
offset = 0

while True:
    f.seek(offset)
    hx =  f.read(4)

    if hx == LocalFile_signature:
        LocalFile_signature_offset.append(offset)
    elif hx == CentralFile_signature:
        CentralFile_signature_start_offset = offset
        break
    offset += 1

# 파일 이름과 data offset 찾기
name = []
data_offset = []
for i in range(len(LocalFile_signature_offset)):
    # Name Length
    nameLen_offset = LocalFile_signature_offset[i] + 26
    f.seek(nameLen_offset)
    nameLen_hex = f.read(2)
    nameLen = little2(nameLen_hex)

    # Extra Length
    extraLen_offset = nameLen_offset + 2
    f.seek(extraLen_offset)
    extraLen_hex = f.read(2)
    extraLen = little2(extraLen_hex)

    # Name
    name_offset = extraLen_offset + 2
    f.seek(name_offset)
    name_hex = f.read(nameLen)
    name.append(name_hex.decode())

    # data
    dataoffset = name_offset + nameLen + extraLen
    data_offset.append(dataoffset)    

print('file name :', name)
print('data offset :', data_offset)

# data 길이 구하기
dataLen = []
for i in range(len(data_offset)):
    if i == len(data_offset)-1:
        dataLen.append(CentralFile_signature_start_offset - data_offset[i])
    else:
        dataLen.append(LocalFile_signature_offset[i+1] - data_offset[i])

# data 영역 파일로 저장하기
for i in range(len(data_offset)):
    f.seek(data_offset[i])
    data = f.read(dataLen[i])
    if len(data) == 0:
        os.makedirs(name[i], exist_ok=True)
    else:
        data = zlib.decompress(data, -zlib.MAX_WBITS) # deflate 압축 풀기
        fw = open(name[i], 'wb+')
        fw.write(data)
        fw.close()