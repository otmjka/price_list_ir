def get_count(sku_data: dict, idx: dict):
  packs = sku_data['packs']
  count = packs['count'] # 1
  count_end = packs['count_end']
  level_type = packs['level_type'] # : 'primary'
  pack_type_id = packs['pack_type_id'] # упаковка контурная ячейковая(блистер)

  man_form_packs = packs['man_form_packs'] # list
  mfp_accum = ''
  for mf_pack in man_form_packs:
    base_measure_unit_id = mf_pack['base_measure_unit_id'] # шт
    base_measure_unit_count = mf_pack['base_measure_unit_count'] # 20
    base_measure_unit_count_end = mf_pack['base_measure_unit_count_end']
    mfp_accum += '[{}]'.format(base_measure_unit_count)

  return '[{}] [{}] [{}]'.format(count, level_type, mfp_accum)
"""
('2f2b5a30-5893-44c9-88a5-061f8e8c5b12',
 {'packs': {'count': 1,
   'count_end': None,
   'level_type': 'primary',
   'pack_type_id': '96b92d30-b8b8-4a1d-b4c7-d9f05b5f40cb',
   'man_form_packs': [{'man_form_key': 'e9ecc3efdad1f32ff5e42a5da646c836652172d8a98ae34902e623ae2a9a4344',
     'base_measure_unit_id': 'f8d9c546-c4c4-465b-a2ac-398ba9794921',
     'base_measure_unit_count': 20,
     'base_measure_unit_count_end': None}]},
  'purpose': None,
  'is_recipe': False,
  'man_forms': [{'key': 'e9ecc3efdad1f32ff5e42a5da646c836652172d8a98ae34902e623ae2a9a4344',
    'inns': [{'inn_id': '158da642-3f03-46ff-9962-1411c0d3c971',
      'base_measure_unit_id': '5d4f8663-d75e-4c69-a3fc-c0b8036d896a',
      'base_measure_unit_count': 0.008,
      'base_measure_unit_count_end': None}],
    'dosage_form_id': '0a5067b7-58a3-47c0-8931-00362e9ca835'}],
  'address_id': 'ccffd3e1-a197-4264-b0e6-f7b6602ac345',
  'trade_name': 'бромгексин',
  'cert_num_id': '5de4425e-1ae1-4f66-8eab-58db5c085a0c'})
"""
