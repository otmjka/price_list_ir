from helpers.skus import get_company, get_dosage_form_str, get_tn
from db.verified import report_row_num_un_uuid

def report_by_verified(plist_values, indexes):
    # rows_id = indexes['rows_id']
    rows_id_inv = indexes['rows_id_inv']
    # terms_docs = indexes['terms_docs']
    verf_row_num_un_uuid = report_row_num_un_uuid()

    verf_items = list(verf_row_num_un_uuid.items())

    # verf_items [(817, '0766899c-4404-42e9-8469-f63ffb5f1839'), ...]

    for row_num, un_id in verf_items[:10]:
        code, name, company, tp = plist_values[row_num]
        un_row_num = rows_id_inv[un_id]
        verf = get_tn(un_row_num)
        form = get_dosage_form_str(un_row_num)
        company_un = get_company(un_row_num)
        print('{};{}[{}] -> [{}] [{}]'.format(verf, form, company_un, name, company))

"""
l-тироксин 100 берлин-хеми;таблетки[БЕРЛИН-КЕМИ АГ] -> [L-Тироксин Берлин-Хеми табл. 100 мкг х50] [Berlin-Chemie AG/Menarini Group]
l-тироксин 50 берлин-хеми;таблетки[БЕРЛИН-КЕМИ АГ] -> [L-Тироксин Берлин-Хеми табл. 75 мкг х100] [Berlin-Chemie AG/Menarini Group]
l-лизина эсцинат;концентрат для приготовления раствора для внутривенного для введения[ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО "ГАЛИЧФАРМ"] -> [L-Лизина эсцинат конц. д/приг. р-ра для в/в введ 1мг/мл 5мл х10] [Завод Медсинтез]
l-тироксин 125 берлин-хеми;таблетки[БЕРЛИН-КЕМИ АГ] -> [L-Тироксин Берлин-Хеми табл. 150 мкг х100] [Berlin-Chemie AG/Menarini Group]
l-тироксин-акри;таблетки[ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "ХИМИКО-ФАРМАЦЕВТИЧЕСКИЙ КОМБИНАТ "АКРИХИН"] -> [L-Тироксин-Акри табл. 100 мкг х50] [Акрихин]
l-тироксин 100 берлин-хеми;таблетки[БЕРЛИН-КЕМИ АГ] -> [L-Тироксин Берлин-Хеми табл. 125 мкг х100] [Berlin-Chemie AG/Menarini Group]
l-тироксин 75 берлин-хеми;таблетки[БЕРЛИН-КЕМИ АГ] -> [L-Тироксин табл. 0.1 мг уп.яч.конт х100] [Озон]
l-тироксин-акри;таблетки[ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "ХИМИКО-ФАРМАЦЕВТИЧЕСКИЙ КОМБИНАТ "АКРИХИН"] -> [Megaday Иммуно с вит. С со вкусом апельсина мармелад/паст. 20 г х1] [Марми КФ ]
l-лизина эсцинат;концентрат для приготовления раствора для внутривенного для введения[ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ТОВАРИЩЕСТВО "ГАЛИЧФАРМ"] -> [L-Тироксин Берлин-Хеми табл. 100 мкг х100] [Berlin-Chemie AG/Menarini Group]
l-тироксин 150 берлин-хеми;таблетки[БЕРЛИН-КЕМИ АГ] -> [L-Тироксин Берлин-Хеми табл. 50 мкг х50] [Berlin-Chemie AG/Menarini Group]
"""

# вывести строку прайса строку UN

# get_tn(rows_id_inv['0766899c-4404-42e9-8469-f63ffb5f1839']) # 'l-тироксин 100 берлин-хеми'
