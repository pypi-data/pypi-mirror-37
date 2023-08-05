import json
import os
import requests

# 根据 shici标题 和 作者 搜索古诗内容
def shici(title = '春晓', author = '孟浩然'):
    url='http://ybcdemo.yuanfudao.com:8093/ybc_poetry/ybc_poetry.php?title=%s&author=%s' % (title, author)
    r = requests.get(url)
    res = r.json()
#    print(res)
    
    status = res['status']
    if status == 1:
        content = ''.join(res['content'])
        return content
    
    if status == -1:
        return '未搜索到这首诗词'
    

def _shici(title = '春晓', author = '孟浩然'):
    # data文件夹路径
    data_path = os.path.abspath(__file__)
    data_path = os.path.split(data_path)[0]+'/data/'
    
    # 读取gushi.json文件中数据
    f_shi = open(data_path + 'gushi.json', encoding='utf-8')
    fileJson = json.load(f_shi)
    f_shi.close()
 
    for item in fileJson:
        if item['title'] == title and item['author'] == author:
            # 将古诗内容列表中的元素拼接成字符串
            content = ''.join(item['paragraphs'])
            return content
        
    # 读取ci.json文件中数据
    f_ci = open(data_path + 'ci.json', encoding='utf-8')
    fileJson = json.load(f_ci)
 
    for item in fileJson:
        if item['rhythmic'] == title and item['author'] == author:
            # 将词内容列表中的元素拼接成字符串
            content = ''.join(item['paragraphs'])
            return content
        
    # 未搜索到
    return '未搜索到这首诗词'
    
    
            

#def _data_gushi():
#    data_path = os.path.abspath(__file__)
#    data_path = os.path.split(data_path)[0]+'/shi/'
#
#    files_list = os.listdir(data_path)
##    print(files_list)
#    
#    f_w = open('gushi.json', 'w', encoding='utf-8')
#    
#    all_data = []
#    
#    for file in files_list:
##        print(data_path+file)
#        f = open(data_path + file, encoding='utf-8')
#        fileJson = json.load(f)
#        for item in fileJson:
#            new_item = item
#            new_item.pop('strains')
#            all_data.append(new_item)
#            
#    #    print(all_data)
#    json.dump(all_data, f_w, ensure_ascii=False)
#    f_w.close()


def _data_ci():
    data_path = os.path.abspath(__file__)
    data_path = os.path.split(data_path)[0]+'/ci/'

    files_list = os.listdir(data_path)
#    print(files_list)
    
    f_w = open('ci.json', 'w', encoding='utf-8')
    
    all_data = []
    
    for file in files_list:
#        print(data_path+file)
        f = open(data_path + file, encoding='utf-8')
        fileJson = json.load(f)
        for item in fileJson:
            all_data.append(item)
            
    #    print(all_data)
    json.dump(all_data, f_w, ensure_ascii=False)
    f_w.close()

def main():
    
    res = shici()
    print(res)
    
    res = shici('早发白帝城', '李白')
    print(res)
    
    res = shici('声声慢', '李清照')
    print(res)
    
    res = shici('早发白帝城', '李')
    print(res)


if __name__ == '__main__':
    main()



