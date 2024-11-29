from django.db import models
from django.db.models import Q


class UniqueConstraintMixin:
    @staticmethod
    def get_constraints(model_name, field_constraints):
        constraints = []
        for field_names, name_suffix in field_constraints:
            constraints.append(
                models.UniqueConstraint(
                    fields=field_names,
                    condition=Q(deleted_at__isnull=True),
                    name=f'{model_name}_unique_{name_suffix}'
                )
            )
        return constraints
