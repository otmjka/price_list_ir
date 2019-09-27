import re
import db.un as db_un
from helpers.skus import str_to_dict, get_dosage

# {
# ...
#   ['bc479032-5c43-4f32-a98f-e020fcb77f1d']: {
#     'name': 'вспомогательное вещество-капсулы целлюлозные №00',
#     'docs': {46077, 47318}
#   }
# ...
# }
def get_dosage_items():

  skus = db_un.get_en_skus()
  dosages = dict() # {[id]: value}

  for un_id, data_str, row_num in skus:
    sku_data = str_to_dict(data_str)
    man_forms = sku_data['man_forms']
    for man_form in man_forms:
      dosage_form = man_form['dosage_form']
      name = dosage_form['name']
      dosage_id = dosage_form['id']
      if dosage_id not in dosages:
        dosages[dosage_id] = dict(name=name)
      if 'docs' not in dosages[dosage_id]:
        dosages[dosage_id]['docs'] = set()
      docs = dosages[dosage_id]['docs']
      docs.add(row_num)
  return dosages

# m = 0
# m = max(m, len(man_forms))
# print(m)
# => 5


# dosages_items = list(dosages.items())[:1000]
# dosages_items[245]
#
# # one_let = set()
# # two_let = set()
# three_let = set()
# for row, value in three:
#     print('{} `{}` [{}]'.format(row, value, dosages_items[row][1]['name']))
#     three_let.add(value)
# three_let
#
# ## 268 `el` [вспомогательное вещество-капсулы желатиновые твердые №0 el]
# # 600 `е1` [вспомогательное вещество-капсулы целлюлозные №0 е1]
# for row in dosages_items[529][1]['docs']:
#     print(skus[row][0])
#
def build_forms_idx():
  dosages_dict = get_dosage_items()
  dosages_items = list(dosages_dict.items())
  one = list()
  two = list()
  three = list()
  single_stop = {'в', 'и', 'с'}
  dual_stop = {'на', 'со'}
  for i, (form_id, form_dict) in enumerate(dosages_items):
    name = form_dict['name']
    docs = form_dict['docs']
    bag_of_words = re.split(
      r"\+|\|\*| |\n|\(|\)|\-|\[|\]|'|\"|\t|«|»|&|;|:|,",
      name
    )
    bow = list()
    for word in bag_of_words:
      if len(word) == 0: # ""
        continue
      # {'2', '4', 'в', 'и', 'с', '…'}
      # '4' 661 раствор для гемодиализа [калий 4 ммоль/л] ['раствор', 'для', 'гемодиализа', 'калий', '4', 'ммоль/л']
      # '2' 662 раствор для гемодиализа [калий 2 ммоль/л]
      # 245 `…` [порошок для приготовления …]
      if len(word) == 1:
        one.append((i, word))
        if word in single_stop:
            continue
      # {'el', 'е1', 'на', 'со', '№0', '№1', '№2', '№3', '№4'}
      # 268 `el` [вспомогательное вещество-капсулы желатиновые твердые №0 el]
      # 600 `е1` [вспомогательное вещество-капсулы целлюлозные №0 е1]
      if len(word) == 2:
        two.append((i, word))
        if word in dual_stop:
            continue
      # 529 `№00` [вспомогательное вещество-капсулы целлюлозные №00]
      if len(word) == 3:
        three.append((i, word))
      bow.append(word)
  #     bow = [word for word in bag_of_words if len(word) > 0]
    print('[{}] [{}]'.format(i, len(docs)))
    print('{}\n{}\n{}\n\n'.format(name, bag_of_words, bow))

