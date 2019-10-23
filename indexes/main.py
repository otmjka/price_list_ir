# skus

from indexes.skus import build_sku_row_idx
from db.un import get_en_skus

# trade_name

from indexes.tn import build_tn_indexes

# dosage

from indexes.forms import build_dosage_forms_idx

# company

from db.company import get_addr_company_table
from indexes.company import build_company_idx
from indexes.company import build_skus_by_company_row
#
# Indexes
#

def all_idx():
    # skus
    skus_idx = build_sku_row_idx() # dict_keys(['rows_id', 'rows_id_inv'])
    print('{} loaded'.format(skus_idx.keys()))
    un_skus = get_en_skus()
    print('[{}] loaded'.format('un_skus'))

    # trade_name

    tn_idx = build_tn_indexes()
    print('{} loaded'.format(tn_idx.keys()))
    # dosage

    dosage_idx = build_dosage_forms_idx() # dict_keys(['terms_docs', 'row_id', 'id_row', 'recs'])
    print('{} loaded'.format(dosage_idx.keys()))
    # company

    addr_company_idx = get_addr_company_table()# dict_keys(['recs', 'addr_cmp', 'cmp_addreses'])
    print('{} loaded'.format(addr_company_idx.keys()))
    company_idx = build_company_idx() # dict_keys(['company_id_idx', 'company_id_idx_inv', 'terms_docs', 'companies_table', 'companies_synonyms'])
    print('{} loaded'.format(company_idx.keys()))

    ### build

    # after cells: company, dosage, skus
    idx = dict(
        addr_company_idx=addr_company_idx, company_idx=company_idx,
        skus_idx=skus_idx,
        un_skus=un_skus,
        dosage_idx=dosage_idx,
        tn_idx=tn_idx
    )
    skus_by_company_row = build_skus_by_company_row(idx)
    idx['skus_by_company_row'] = skus_by_company_row
    return idx
