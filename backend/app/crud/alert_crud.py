from app.crud.base_crud import CRUDBase
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertRead

class CRUDAlert(CRUDBase[Alert, AlertCreate, AlertRead]):
    pass

alert = CRUDAlert(Alert)