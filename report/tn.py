from prices.helpers import by_code

def tn_report(res, code_idx, plist, verf_row_num_un_uuid):
  for report_item in res[:10]:
    p = list(by_code(report_item[0], code_idx, plist).values[0])
    row_num = code_idx[p[0]]
    print('{} {} [{}]'.format(row_num, p[1], p[2]))
    print('\n')
    for i, (term, docs) in enumerate(report_item[1][0]):
      print(i, (docs != None and len(docs)) or '-', term)
    print('\n {}'.format(row_num in verf_row_num_un_uuid and verf_row_num_un_uuid[row_num]))
    print('\n\n')

