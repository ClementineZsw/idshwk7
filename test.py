from PIL import Image
def mod(x,y):
    return x%y
def toasc(strr):
    return int(strr, 2)
def plus(string1): 
    #Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。
    return string1.zfill(8)
def get_key(strr):
    string1=""
    for i in range(len(strr)):
        #逐个字节将要隐藏的文件内容转换为二进制，并拼接起来 
        #1.先用ord()函数将s的内容逐个转换为ascii码
        #2.使用bin()函数将十进制的ascii码转换为二进制
        #3.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空
        #4.又由于ascii码转换二进制后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位
        string1=string1+""+plus(bin(ord(strr[i])).replace('0b',''))
    #print(string) 
    return string1
def encode(str1,str2,str3): 
    im = Image.open(str1) 
    #获取图片的宽和高
    width,height= im.size[0],im.size[1]
    #print("width:"+str(width))
    #print("height:"+str(height))
    key = get_key(str2) 
    #print(key)
    keylen = len(key)
    #print(keylen) 
    count = 0
    # print(height*width)
    for h in range(height):
        for w in range(width):
            pixel = im.getpixel((w,h))
            a=pixel[0]
            b=pixel[1]
            c=pixel[2]
            if count == keylen:
                break
            #下面的操作是将信息隐藏进去 
            #分别将每个像素点的RGB值余2，这样可以去掉最低位的值
            #再从需要隐藏的信息中取出一位，转换为整型
            #两值相加，就把信息隐藏起来了
            a= a-mod(a,2)+int(key[count])
            im.putpixel((w,h),(a,b,c)) 
            count+=1
        if count == keylen:
            break
    im.save(str3)
def decode(str1,str2): 
    b="" 
    im = Image.open(str2)
    lenth = str1*8 
    #print(lenth) 
    width,height = im.size[0],im.size[1]
    #print("width:"+str(width))
    #print("height:"+str(height))
    count = 0
    for h in range(height): 
        for w in range(width):
            #获得(w,h)点像素的值
            pixel = im.getpixel((w, h))
            if count ==lenth:
                break
            count+=1
            b=b+str(mod(int(pixel[0]),2))
            
        if count == lenth:
            break
    result_str=""
    for i in range(0,len(b),8):
        #以每8位为一组二进制，转换为十进制            
        stra = toasc(b[i:i+8]) 
        #将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
        #print((stra))
        result_str+=chr(stra)
    print(result_str)
if __name__ == '__main__':
    #原始图片
    str1="test.png"
    #嵌入字符串
    str2="57119325 zhao shi wu"
    #保存的文件
    str3="save.png"
    #提取的字符长度
    str1_de=len(str2)
    #提取的新信息文件
    str2_de="save.png"

    #print(get_key(str2))    
    encode(str1,str2,str3)
    decode(str1_de,str2_de)
