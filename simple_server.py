from aiohttp import web
import aiohttp_cors
from state import State
from index import get_sources
from helpers.skus import get_sku_id_by_row, get_tn_from_data, get_sku_data_by_row, show_sku_by_row
from zones.tn import tn_zone


print('loading data...')
sources = ({}, {}, {'tn_idx': {'terms_docs': {}}})
print('finished!')
s = State()

def get_pitem(index: int, src):
  pcode = 1749
  pname = '5-Нок табл. 50 мг х50'
  pcompany = 'Lek – Сотекс'
  index = 39
  return dict(pcode=pcode, pname=pname, pcompany=pcompany, index=index)

def make_response(res, sources):
  idx = sources[2]
  pname = res['pname']
  tn = list()
  tn_zone_skus = tn_zone(pname, idx['tn_idx']['terms_docs'])
  for i, (term, sku_docs) in enumerate(tn_zone_skus):
    if sku_docs == None:
      sku_term_info = dict(index=i, term=term, sku_docs=[], sku_un_id_list=[], sku_trade_names=[])
      tn.append(sku_term_info)
      continue
    sku_un_id_list = [get_sku_id_by_row(sku_doc, idx) for sku_doc in sku_docs]
    sku_trade_names = [get_tn_from_data(get_sku_data_by_row(sku_doc, idx)) for sku_doc in sku_docs]
    sku_term_info = dict(index=i, term=term, sku_docs=sku_docs, sku_un_id_list=sku_un_id_list,
                         sku_trade_names=sku_trade_names)
    tn.append(sku_term_info)
  return tn

def get_item(i):
  res = get_pitem(i, sources)
  tn = make_response(res, sources)
  res['tn'] = tn
  flat = list()
  for term in tn:
    flat += term['sku_docs']
  res['flat'] = flat
  idx = sources[2]
  res['flat_sku_value'] = [show_sku_by_row(doc, idx) for doc in res['flat']]
  return res

async def handle_next(req):
  i = s.set_i(s.get_i() + 1)
  response = get_item(i)
  return web.json_response(response)

async def handle_prev(req):
  i = s.set_i(s.get_i() - 1)
  response = get_item(i)
  return web.json_response(response)

async def handle_index(request):
  i = request.match_info.get('index', s.get_i())
  response = get_item(i)
  return web.json_response(response)

async def handle_tn(request):
  body = await request.json()
  return web.json_response(body)


app = web.Application()

# `aiohttp_cors.setup` returns `aiohttp_cors.CorsConfig` instance.
# The `cors` instance will store CORS configuration for the
# application.
cors = aiohttp_cors.setup(app)

# To enable CORS processing for specific route you need to add
# that route to the CORS configuration object and specify its
# CORS options.
resource_next = cors.add(app.router.add_resource("/next"))
resource_prev = cors.add(app.router.add_resource("/prev"))
resource_index = cors.add(app.router.add_resource('/index/{index}'))
resource_tn = cors.add(app.router.add_resource("/tn"))

route = cors.add(
    resource_next.add_route("GET", handle_next), {
        "http://localhost:3000": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })

route = cors.add(
    resource_prev.add_route("GET", handle_prev), {
        "http://localhost:3000": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })
route = cors.add(
    resource_tn.add_route("POST", handle_tn), {
        "http://localhost:3000": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })

route = cors.add(
    resource_index.add_route("GET", handle_index), {
        "http://localhost:3000": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })




if __name__ == '__main__':
  web.run_app(app)
