from api.public.algv2.pg_models import Base
from api.pg_database import sync_engine

Base.metadata.create_all(sync_engine)
