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

#
# Indexes
#

def all_idx():
    # skus
    skus_idx = build_sku_row_idx() # dict_keys(['rows_id', 'rows_id_inv'])
    un_skus = get_en_skus()

    # trade_name

    tn_idx = build_tn_indexes()

    # dosage

    dosage_idx = build_dosage_forms_idx() # dict_keys(['terms_docs', 'row_id', 'id_row', 'recs'])

    # company

    addr_company_idx = get_addr_company_table()# dict_keys(['recs', 'addr_cmp', 'cmp_addreses'])
    company_idx = build_company_idx() # dict_keys(['company_id_idx', 'company_id_idx_inv', 'terms_docs', 'companies_table', 'companies_synonyms'])


    ### build

    # after cells: company, dosage, skus
    idx = dict(
        addr_company_idx=addr_company_idx, company_idx=company_idx,
        skus_idx=skus_idx,
        un_skus=un_skus,
        dosage_idx=dosage_idx,
        tn_idx=tn_idx
    )

    return idx