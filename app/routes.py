from sys import argv

from aiohttp import web
from index import get_sources
from servers.helpers import get_item, search_tn

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
  response = get_item(i, sources)
  return web.json_response(response)

async def handle_tn(request):
  body = await request.json()
  query = body['query']

  idx = sources[2]
  response = search_tn(query, idx)

  return web.json_response(response)
