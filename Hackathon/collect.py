import lxml, json
import csv
from bs4 import BeautifulSoup
import requests
import re
import urllib
import io
from PIL import Image
from io import BytesIO
import urllib.parse, base64
import imagehash

def compare_images(path_zero, path_one):
    hash0=imagehash.average_hash(Image.open(path_zero))
    hash1=imagehash.average_hash(Image.open(path_one))

    differnce=hash1-hash0

    # if differnce == 64:
    #     return 0
    # else:
    print(count,":", differnce)
    return differnce





data={}
flag=[]
f=open("output.csv","w")
writer=csv.writer(f)
content=["name","user","href","file_type","source_file","difference"]
writer.writerow(content)

with open('url_test.html', 'r', encoding="utf8") as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    details = soup.find_all('div', jsaction="cFWHmd:s370ud;")
    # for i in details:
    #     print(i)
    count=1
    for i in range(len(details)):

        test=details[i]
        test_s=BeautifulSoup(str(test),'lxml')
        href=test_s.find_all("a")[-1].get("href")
        name=test_s.find_all("h3")[0].getText()
        source_file= test_s.find_all("img")[0].get("src")
        file_type="image"

        pat=r"(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))"
        string=test_s.find_all("div")[-1].getText()
        if('.' not in [*string[:3]]):
            string="www."+string
        user=re.findall(pat,string)[0]
        date_up=0
        alt_text=""
        
        # b_source= source_file.encode("UTF-8")
        if(source_file[:17]=="https://encrypted"):
            continue
        b_source=bytes(source_file, encoding='utf-8')
        b_source=b_source[b_source.find(b'/9'):]
        im=Image.open(io.BytesIO(base64.b64decode(b_source))).save('result.jpg')


        # img_match=re.findall(r'data:image/jpeg;base64,(.*?)', source_file)
        # print(img_match)
        # final_image = Image.open(BytesIO(base64.b64decode(source_file)))


        result=compare_images('test.jpg', 'result.jpg')
        if result <= 20:
            flag.append(count)
            content=[name, user, href, "image", source_file, result]
            writer.writerow(content)
        temp={
            "href":href,
            "name":name,
            "source_file": source_file,
            "file_type":"image",
            "user":user,
        }
        data[count]=temp
        # print(result)
        # print(f"name: {name}, href: {href}, ft: {file_type}, user: {user}")
        count+=1
print(flag)
# json_string=json.dumps(data)

# with open("image_data.json",'w') as outfile:
#     outfile.write(json_string)


