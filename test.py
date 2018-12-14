#测试数据

import os
import json
import numpy as np

def readtxt(path,encoding):
    with open(path, 'r', encoding = encoding) as f:
        lines = f.readlines()
    return lines

def fileWalker(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'\\'+fn)
            fileArray.append(eachpath)
    return fileArray

def email_parser(email_path):
    punctuations = """,.<>()*&^%$#@!'";~`[]{}|、\\/~+_-=?"""
    content_list = readtxt(email_path, 'iso-8859-1')
    content = (' '.join(content_list)).replace('\r\n', ' ').replace('\t', ' ')
    clean_word = []
    for punctuation in punctuations:
        content = (' '.join(content.split(punctuation))).replace('  ', ' ')
        clean_word = [word.lower()
                      for word in content.split(' ') if len(word) > 2]
    return clean_word

def filter(ham_word_pro, spam_word_pro, test_file):
    test_paths = fileWalker(test_file)
    result=[]
    for test_path in test_paths:
        email_spam_prob = 0.0
        spam_prob = 0.3116
        ham_prob = 0.6884
        file_name = test_path.split('\\')[-1]
        prob_dict = {}
        words = set(email_parser(test_path))  #当前测试集中某一邮件分词集合
        for word in words:
            Psw = 0.0
            if word not in spam_word_pro:
                Psw = 0.4   #如果词语未出现在所有邮件中，则记为0.4
            else:
                Pws = spam_word_pro[word] #该词在垃圾邮件中的频率
                Pwh = ham_word_pro[word] #该词在正常邮件中的频率
                Psw = spam_prob*(Pws/(Pwh*ham_prob+Pws*spam_prob)) #该词的贝叶斯概率
            prob_dict[word] = Psw #加入到字典中
        numerator = 1
        denominator_h = 1
        for k, v in prob_dict.items():
            numerator *= v
            denominator_h *= (1-v)
        if numerator+denominator_h==0:
            email_spam_prob=1
        else:
            email_spam_prob = round(numerator/(numerator+denominator_h), 4)
        if email_spam_prob > 0.5:
            # write_result((test_path.split('_')[1]).split('.')[0]+" 0")
            index1=int((test_path.split('_')[1]).split('.')[0])
            result.append([index1,0])
            print(file_name, 'spam', email_spam_prob)
        else:
            # write_result((test_path.split('_')[1]).split('.')[0] + " 1")
            index1 = int((test_path.split('_')[1]).split('.')[0])
            result.append([index1, 1])
            print(file_name, 'ham', email_spam_prob)
        # print(prob_dict)
        # print('******************************************************')
        # break
    result.sort(key=lambda x:x[0])
    for i in range(len(result)):
        write_result(str(result[i][0])+","+str(result[i][1]))
    print(result)

def read_dict(txt):
    with open(txt, 'r') as file:
        js = file.read()
        dic = json.loads(js)
        file.close()
        return dic

def write_result(str_result):
    eml_dir='data2\\'
    with open(eml_dir+'result.txt','a+') as file:
        content=file.read()
        file.write(content+str_result+'\n')
        file.close()

def main():
    eml_dir = 'data2\\'
    test_file = r'' + eml_dir + 'test'

    ham_dic = read_dict(eml_dir + 'ham_dic.txt')
    spam_dic = read_dict(eml_dir + 'spam_dic.txt')
    filter(ham_dic, spam_dic, test_file)

if __name__ == '__main__':
    main()