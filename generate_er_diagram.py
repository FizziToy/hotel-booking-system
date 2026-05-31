import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings'
)

import django

django.setup()

from django.apps import apps
from django.db import models


PROJECT_APPS = [
    'accounts',
    'hotels',
    'bookings',
]


def get_field_type(field):
    if isinstance(field, models.ForeignKey):
        return 'int'

    if isinstance(field, models.CharField):
        return 'string'

    if isinstance(field, models.TextField):
        return 'string'

    if isinstance(field, models.EmailField):
        return 'string'

    if isinstance(field, models.BooleanField):
        return 'boolean'

    if isinstance(field, models.IntegerField):
        return 'int'

    if isinstance(field, models.FloatField):
        return 'float'

    if isinstance(field, models.DecimalField):
        return 'decimal'

    if isinstance(field, models.DateField):
        return 'date'

    if isinstance(field, models.DateTimeField):
        return 'datetime'

    return 'string'


def generate_mermaid():
    lines = []
    relations = []

    lines.append('erDiagram')

    for model in apps.get_models():
        app_label = model._meta.app_label

        if app_label not in PROJECT_APPS:
            continue

        model_name = model.__name__

        lines.append(f'    {model_name} {{')

        for field in model._meta.fields:
            field_type = get_field_type(field)

            if isinstance(field, models.ForeignKey):
                field_name = f'{field.name}_id'
            else:
                field_name = field.name

            if field.primary_key:
                lines.append(
                    f'        {field_type} {field_name} PK'
                )

            elif isinstance(field, models.ForeignKey):
                lines.append(
                    f'        {field_type} {field_name} FK'
                )

                related_model = field.related_model.__name__

                relations.append(
                    f'    {related_model} ||--o{{ {model_name} : contains'
                )

            else:
                lines.append(
                    f'        {field_type} {field_name}'
                )

        lines.append('    }')
        lines.append('')

    lines.extend(relations)

    return '\n'.join(lines)


def save_files():
    mermaid_code = generate_mermaid()

    with open('er_diagram.mmd', 'w', encoding='utf-8') as file:
        file.write(mermaid_code)

    html = f"""
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>ER Diagram</title>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <h1>ER-діаграма системи бронювання готелів</h1>

    <div class="mermaid">
{mermaid_code}
    </div>
</body>
</html>
"""

    with open('er_diagram.html', 'w', encoding='utf-8') as file:
        file.write(html)

    print('ER-діаграма успішно створена:')
    print('- er_diagram.mmd')
    print('- er_diagram.html')


if __name__ == '__main__':
    save_files()