import re
SPACE = ' '

def tokenize(string):
  lower_str = string.lower()
  splitted = lower_str.split(SPACE)
  # x
  # xx
  # -
  # x-xxx
  # xx-xxx
  # ()"'.,- посмотреть в блакноте я делал визуализацию
  result = splitted
  return result

def get_bow(name: str):
  return re.split(r"\+|\|\*| |\n|\(|\)|\[|\]|'|\"|\t|«|»|&|;|:|,", name.lower())

# bag_of_words = re.split(
#         r"\+|\|\*| |\n|\(|\)|\-|\[|\]|'|\"|\t|«|»|&|;|:|,",
#         name
#     )
#     bow = list()
#     for word in bag_of_words:
#         if len(word) == 0: # ""
#             continue
#         # {'2', '4', 'в', 'и', 'с', '…'}
#         # '4' 661 раствор для гемодиализа [калий 4 ммоль/л] ['раствор', 'для', 'гемодиализа', 'калий', '4', 'ммоль/л']
#         # '2' 662 раствор для гемодиализа [калий 2 ммоль/л]
#         # 245 `…` [порошок для приготовления …]
#         if len(word) == 1:
#             one.append((i, word))
#             if word in single_stop:
#                 continue
#         # {'el', 'е1', 'на', 'со', '№0', '№1', '№2', '№3', '№4'}
#         # 268 `el` [вспомогательное вещество-капсулы желатиновые твердые №0 el]
#         # 600 `е1` [вспомогательное вещество-капсулы целлюлозные №0 е1]
#         if len(word) == 2:
#             two.append((i, word))
#             if word in dual_stop:
#                 continue
#         # 529 `№00` [вспомогательное вещество-капсулы целлюлозные №00]
#         if len(word) == 3:
#             three.append((i, word))
#
#
#         bow.append(word)
