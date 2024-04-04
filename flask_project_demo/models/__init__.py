"""Modulo contenente tutte le classi ORM collegate al database."""

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(MappedAsDataclass, DeclarativeBase):
    """Classe base per le tabelle del db.

    Note
    ----
    Eredita dalla classe MappedAsDataclass per poter usare la
    funzione jsonify di Flask.

    See Also
    --------
    serialize | deserialize
    """


from flask_project_demo.models.user import (  # noqa: E402
    User,
    UserPostSchema,
    UserQuerySchema,
    UserSchema,
)

"""
la variabile speciale `__all__` serve a definire quali
porzioni di codice sono disponibili importando il modulo.
In questo caso la class `User` sarà disponibile direttamente
dal modulo flask_project_demo.models e si può usare come segue:

```python
from flask_project_demo.models import User
```

In realtà la classe è definita nel modulo flask_project_demo.models.user
e rimane comunque accessibile da quel modulo.
"""
__all__ = [
    "Base",
    "User",
    "UserPostSchema",
    "UserQuerySchema",
    "UserSchema",
]
