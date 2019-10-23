from sys import argv

from aiohttp import web
from index import get_sources
from servers.helpers import candidates_by_price_row, search_tn
from db.uploads import load_uploads_list
### fast app start
MOCK_ENTRY_POINT = 'simple_server.py'
MOCK_SOURCES = ({}, {}, {'tn_idx': {'terms_docs': {}}})
# do not load sources if ...
is_mock_entry = MOCK_ENTRY_POINT in argv

print('loading data... {}'.format(argv))
sources = MOCK_SOURCES if is_mock_entry else get_sources()


# sources = get_sources()
print('finished!')

async def handle_index(request):
  i = request.match_info.get('id', 0)
  # с клиента приходит индекс
  response = candidates_by_price_row(i, sources)
  return web.json_response(response)

async def handle_tn(request):
  body = await request.json()
  query = body['query']

  idx = sources[2]
  response = search_tn(query, idx)

  return web.json_response(response)


async def handle_all_uploads(request):
  uploads_recs = load_uploads_list()
  response = [dict(hash=hash, fp=fp) for hash, fp in uploads_recs]

  return web.json_response(response)

async def handle_all_uploads(request):
  # uploads_recs = load_uploads_list()
  # upload_id = request.match_info.get('id', 0)
  """
  load or get from cache plist with require id
  and get first 100 in page
  
  plist item pname, pcompany
  best candidate
  """
  response = dict(proba='123')
  return web.json_response(response)


