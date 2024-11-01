import collections
import copy
import io
import json
from zipfile import ZipFile

from vj4.service import bus
from vj4.model.adaptor import problem
from vj4.model import fs

async def _on_problem_data_change(e):
    value = e['value']
    pdoc = await problem.get(value['domain_id'], value['pid'])
    pdata = await problem.get_data(pdoc)
    data = await fs.get(pdata['_id'])
    bytes = await data.read()
    zip = ZipFile(io.BytesIO(bytes))
    configFile = zip.open("Config.json")
    congFileStr = configFile.read()
    config = json.loads(congFileStr)
    configFile.close()
    await data.close()

def init():
    bus.subscribe(_on_problem_data_change, ['problem_data_change'])