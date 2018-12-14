
def readtxt(path,encoding):
    with open(path, 'r', encoding = encoding) as f:
        lines = f.readlines()
    return lines

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



print(email_parser('data2/spam/2.eml'))