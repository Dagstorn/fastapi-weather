import fastapi
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from infra.database import get_db
from schemas.auth_schemas import UserCreateRequest, Token, LoginRequest
from services import auth_service

router = fastapi.APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(
        create_user_req: UserCreateRequest,
        db: Session = Depends(get_db)
):
    auth_service.create_user(db, create_user_req)


@router.post("/login", response_model=Token)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    return auth_service.login_user(db, login_request.username, login_request.password)

