import motor.motor_asyncio
import functools
import yarl
from pymongo.operations import UpdateOne, UpdateMany, InsertOne, DeleteOne, DeleteMany, ReplaceOne

from vj4.util import options

options.define('db_host', default='localhost', help='Database hostname or IP address.')
options.define('db_port', default=27017, help='Database port.')
options.define('db_name', default='test', help='Database name.')
options.define('db_username', default='', help='Database username.')
options.define('db_password', default='', help='Database password.')
options.define('db_auth_source', default='',
               help='Database name associated with the user\'s credential.')


class BulkOperationBuilder:
  """Compatibility layer for old-style bulk operations."""
  def __init__(self, collection, ordered=False):
    self.collection = collection
    self.ordered = ordered
    self.operations = []
    self._filter = None
    self._upsert = False

  def find(self, filter_spec):
    """Set the filter for the next operation."""
    self._filter = filter_spec
    self._upsert = False
    return self

  def upsert(self):
    """Set upsert flag for the next operation."""
    self._upsert = True
    return self

  def update_one(self, update):
    """Add an update_one operation."""
    if self._filter is None:
      raise ValueError("Must call find() before update_one()")
    self.operations.append(UpdateOne(self._filter, update, upsert=self._upsert))
    self._filter = None
    self._upsert = False
    return self

  def update(self, update):
    """Add an update_many operation."""
    if self._filter is None:
      raise ValueError("Must call find() before update()")
    self.operations.append(UpdateMany(self._filter, update, upsert=self._upsert))
    self._filter = None
    self._upsert = False
    return self

  def replace_one(self, replacement):
    """Add a replace_one operation."""
    if self._filter is None:
      raise ValueError("Must call find() before replace_one()")
    self.operations.append(ReplaceOne(self._filter, replacement, upsert=self._upsert))
    self._filter = None
    self._upsert = False
    return self

  def remove_one(self):
    """Add a delete_one operation."""
    if self._filter is None:
      raise ValueError("Must call find() before remove_one()")
    self.operations.append(DeleteOne(self._filter))
    self._filter = None
    self._upsert = False
    return self

  def remove(self):
    """Add a delete_many operation."""
    if self._filter is None:
      raise ValueError("Must call find() before remove()")
    self.operations.append(DeleteMany(self._filter))
    self._filter = None
    self._upsert = False
    return self

  async def execute(self):
    """Execute all queued operations."""
    if not self.operations:
      return None
    return await self.collection.bulk_write(self.operations, ordered=self.ordered)


class MotorCollectionWrapper:
  """Wrapper around Motor collection to add compatibility methods."""
  def __init__(self, collection):
    self._collection = collection

  def initialize_unordered_bulk_op(self):
    """Create an unordered bulk operation builder."""
    return BulkOperationBuilder(self._collection, ordered=False)

  def initialize_ordered_bulk_op(self):
    """Create an ordered bulk operation builder."""
    return BulkOperationBuilder(self._collection, ordered=True)

  def __getattr__(self, name):
    """Delegate all other attributes to the underlying collection."""
    return getattr(self._collection, name)


async def init():
  global _client, _db

  query = dict()
  if options.db_auth_source:
    query['authSource'] = options.db_auth_source
  url = yarl.URL.build(scheme='mongodb',
                       host=options.db_host,
                       path='/' + options.db_name,
                       port=options.db_port,
                       user=options.db_username if options.db_username else None,
                       password=options.db_password if options.db_password else None,
                       query=query)
  _client = motor.motor_asyncio.AsyncIOMotorClient(str(url))
  _db = _client.get_default_database()
  
  # Verify connection by pinging the database
  await _client.admin.command('ping')


@functools.lru_cache()
def coll(name):
  return MotorCollectionWrapper(_db[name])


@functools.lru_cache()
def fs(name):
  return motor.motor_asyncio.AsyncIOMotorGridFSBucket(_db, bucket_name=name)
