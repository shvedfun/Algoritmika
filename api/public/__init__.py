from fastapi import APIRouter, Depends

from api.auth import authent
# from api.public.health import views as health
# from api.public.hero import views as heroes
# from api.public.team import views as teams
from api.public.alg import views as algv1
from api.public.algv2 import views as algv2
from api.public.algv2 import whatcrm

api = APIRouter()


# api.include_router(
#     health.router,
#     prefix="/health",
#     tags=["Health"],
#     dependencies=[Depends(authent)],
# )
# api.include_router(
#     heroes.router,
#     prefix="/heroes",
#     tags=["Heroes"],
#     dependencies=[Depends(authent)],
# )
# api.include_router(
#     teams.router,
#     prefix="/teams",
#     tags=["Teams"],
#     dependencies=[Depends(authent)],
# )
# api.include_router(
#     algv1.router,
#     prefix='/api/v1',
#     tags=["AlgV1"],
#     dependencies=[Depends(authent)]
# )
api.include_router(
    algv2.router,
    prefix='/api/v2',
    tags=["AlgV2"],
    # dependencies=[Depends(authent)]
)
api.include_router(
    whatcrm.router,
    prefix='/api/v1/whatcrm',
    tags=["WhatCRM"],
    # dependencies=[Depends(authent)]
)
