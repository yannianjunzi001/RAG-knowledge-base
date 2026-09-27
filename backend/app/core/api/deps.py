"""FastAPI 依赖注入。"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_session


DbSession = Annotated[AsyncSession, Depends(get_session)]

