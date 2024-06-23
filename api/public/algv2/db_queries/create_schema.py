from api.public.algv2.db_models import Base
from api.database import sync_engine

Base.metadata.create_all(sync_engine)
