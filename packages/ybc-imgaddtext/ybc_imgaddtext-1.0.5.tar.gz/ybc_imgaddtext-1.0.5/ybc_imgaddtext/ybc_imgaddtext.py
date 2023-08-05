from PIL import Image, ImageDraw, ImageFont

# img="C:\\Users\wangty\Pictures\Saved Pictures\\notwidth.jpg"
# img2="C:\\Users\wangty\Pictures\Saved Pictures\\yuanfudao.png"
# text="哈哈哈哈哈哈反反复复"
#
# dongimg="C:\\Users\wangty\Pictures\Saved Pictures\\求红包动图.gif"
# dongtext="老板给个红包呗"

# def imgwithimg(img,img2):
#     toImage = Image.new('RGBA', (400, 400))
#     fromImge = Image.open(img)
#     toImage.paste(fromImge, loc)
#     toImage.show()

# def imgaddimg(img,img2):
#     bgimg = Image.open(img)
#     jgz = Image.open(img2)
#     bgimg.paste(jgz, (0,100))
#     bgimg.show()

# def dongimgwithtext(img,text):
#     bgimg = Image.open(img)
#     draw = ImageDraw.Draw(bgimg)
#     ttfront = ImageFont.truetype('simhei.ttf', 24)
#     draw.text((0, 1), text, fill=(0, 0, 255), font=ttfront)
#     # bgimg.show()
#     # bgimg.save("./dongnew.jpg")

def imgwithtext(img,text,loc='top'):
    #打开背景图
    bgimg = Image.open(img)
    ttfront = ImageFont.truetype('STHUPO.TTF', 24)
    # 获得文字长和宽
    textinfo = ttfront.getsize(text)

    #如果输入的文字长度小于15，则直接进行图文融合，否则先扩大图片为（360,100）再进行图文融合
    if len(text)<=15 and bgimg.size[0]>=textinfo[0]:
        #获得图片长和宽 bgimg.size
        draw = ImageDraw.Draw(bgimg)
        if loc=="bottom":
            textloc=bgimg.size[1]-textinfo[1]
            
        elif loc=="center":
            textloc=(bgimg.size[1]-textinfo[1])//2
            
        elif loc=="top":
            textloc=0
        #bgimg.size[0]-textinfo[0])//2将文字居中，bgimg.size[1]-textinfo[1]将文字置底
        draw.text(((bgimg.size[0]-textinfo[0])//2,textloc), text, fill=(0, 0, 0), font=ttfront)
        bgimg.show()
        bgimg.save("./new.jpg")
    else:

        #算出原图长宽比例，使用比例，等比缩放图片bgimg.size[0]//bgimg.size[1]
        #重置图片大小  Image.ANTIALIAS参数是给图片添加滤镜效果
        resizebgimg=bgimg.resize((15*textinfo[1],(15*textinfo[1]*bgimg.size[1])//bgimg.size[0]))

        draw = ImageDraw.Draw(resizebgimg)
        resizebgimgront = ImageFont.truetype('STHUPO.TTF', 24)
        text = text[:15]
        # 获得文字长和宽
        textinfo = resizebgimgront.getsize(text)
        if loc=="bottom":
            rebgtextloc=resizebgimg.size[1] - textinfo[1]
            
        elif loc=="center":
            rebgtextloc=(resizebgimg.size[1] - textinfo[1])//2
            
        elif loc=="top":
            rebgtextloc=0
        draw.text(((resizebgimg.size[0] - textinfo[0]) // 2, rebgtextloc),
                  text, fill=(0, 0, 0), font=resizebgimgront)
        resizebgimg.show()
        resizebgimg.save("./resizeimg.jpg")

