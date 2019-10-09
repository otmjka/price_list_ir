### price list

from helpers.prices import extract_pline, show_pline

### Zones

from zones.common import handle_zones, flat_zones, add_lists, show_res

### Verified

from indexes.verified import show_verified, get_sku_index_in_results

### Helpers

from indexes.skus import get_sku_row_by_id

def display_info(verified_items, sources):
    # sources
    skus_by_company_row = sources['skus_by_company_row']
    skus_by_dosage_row = sources['skus_by_dosage_row']
    plist = sources['plist']
    verified = sources['verified']
    idx = sources['idx']

    res_plot = list()
    for i, (price_i, un_id) in enumerate(verified_items):
        print('\n ############')
        pname, pcompany = extract_pline(price_i, plist)

        zones = handle_zones(pname, pcompany, idx)
        # tn_zone, dosage_zone, company_zone = zones
        flats = flat_zones(zones, skus_by_dosage_row=skus_by_dosage_row, skus_by_company_row=skus_by_company_row)
        flat_skus_tn, flat_skus_dosage, flat_skus_c = flats

        # price
        show_pline(i, price_i, plist)

        # verified
        show_verified(price_i, verified, flats, idx)

        results = add_lists([flat_skus_tn, flat_skus_dosage, flat_skus_c], [0.5, 0.4, 0.1])
        sku_row = get_sku_row_by_id(un_id, idx)
        
        # for plot
        index = get_sku_index_in_results(sku_row, results)
        res_plot.append((price_i, index))
        
        print('---', index)
        show_res(results, sku_row, idx)
