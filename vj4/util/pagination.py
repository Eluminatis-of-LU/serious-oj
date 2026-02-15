import asyncio
from vj4 import error


async def paginate(cursor, page: int, page_size: int):
  if page <= 0:
    raise error.ValidationError('page')
  
  # Motor 3.x removed cursor.count(). We need to use collection.count_documents()
  # Extract collection and filter from cursor's delegate
  delegate = cursor.delegate
  collection = cursor.collection
  filter_spec = delegate._spec if hasattr(delegate, '_spec') else {}
  
  # Count documents using the collection
  count, page_docs = await asyncio.gather(
    collection.count_documents(filter_spec),
    cursor.skip((page - 1) * page_size).limit(page_size).to_list()
  )
  
  num_pages = (count + page_size - 1) // page_size
  return page_docs, num_pages, count
