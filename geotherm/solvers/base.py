from ..models.base import BaseModel
from ..units import u


class BaseSolver(BaseModel):
    defaults = {
        "T_surface": u(25,"degC"),
        "T_max": u(1500,"degC"),
        "T_lithosphere": u(1300,"degC")
    }
