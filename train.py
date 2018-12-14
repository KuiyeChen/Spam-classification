#训练数据


import os
import json

def readtxt(path,encoding):
    with open(path, 'r', encoding = encoding) as f:
        lines = f.readlines()
    return lines

def fileWalker(path):   #遍历所有的文件
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'\\'+fn)
            fileArray.append(eachpath)
    return fileArray

def email_parser(email_path):    #得到所有词的列表
    punctuations = """,.<>()*&^%$#@!'";~`[]{}|、\\/~+_-=?"""
    content_list = readtxt(email_path, 'iso-8859-1')
    content = (' '.join(content_list)).replace('\r\n', ' ').replace('\t', ' ')
    clean_word = []
    for punctuation in punctuations:
        content = (' '.join(content.split(punctuation))).replace('  ', ' ')
        clean_word = [word.lower()
                      for word in content.split(' ') if len(word) > 2]
    return clean_word


def get_word(email_file):
    word_list = []
    word_set = []
    email_paths = fileWalker(email_file)
    for email_path in email_paths:
        clean_word = email_parser(email_path)
        word_list.append(clean_word)
        word_set.extend(clean_word)
    return word_list, set(word_set)


def count_word_prob(email_list, union_set):
    word_prob = {} #建立一个字典，统计每一个词的词频，如出现，计数。未出现，即为0.01
    for word in union_set:
        counter = 0  #在所有文件中出现的次数
        for email in email_list:
            if word in email:
                counter += 1
            else:
                continue
        prob = 0.0
        if counter != 0:
            prob = counter/len(email_list)
        else:
            prob = 0.01
        word_prob[word] = prob
        print(word_prob)
    return word_prob


def main():
    eml_dir='data1\\'
    ham_file = r''+eml_dir+'ham'
    spam_file = r''+eml_dir+'spam'
    ham_list, ham_set = get_word(ham_file)
    spam_list, spam_set = get_word(spam_file)
    union_set = ham_set | spam_set
    ham_word_pro = count_word_prob(ham_list, union_set)
    spam_word_pro = count_word_prob(spam_list, union_set)
    write_dict(ham_word_pro,eml_dir+'ham_dic.txt')
    write_dict(spam_word_pro,eml_dir+'spam_dic.txt')


def write_dict(dic,file_path):
    js = json.dumps(dic)
    with open(file_path, 'w') as file:
        file.write(js)
        file.close()



if __name__ == '__main__':
    main()