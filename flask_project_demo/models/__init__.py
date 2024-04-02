"""Modulo contenente tutte le classi ORM collegate al database."""

from flask_project_demo.models.user import User

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
__all__ = ["User"]
