from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != 'users':  # o la app principal donde defines modelos
        return

    # Definimos los grupos y sus permisos
    groups_permissions = {
        'Administrador': Permission.objects.all(),  # Todos los permisos
        'Moderador': [
            'approve_question', 'feature_question', 'approve_article', 'feature_article',
            'delete_question', 'delete_answer', 'delete_article',
        ],
        'Autor': [
            'add_article', 'change_article', 'delete_article',  # luego filtras para que sea *solo su artículo*
        ],
        'Usuario': [
            'add_question', 'add_answer', 'can_vote',
            'view_article', 'view_question', 'view_answer',
        ],
        'Revisor de Contenido': [
            'approve_question', 'approve_article',
        ],
        'Editor de Artículos': [
            'change_article',
        ]
    }

    for group_name, perms in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if isinstance(perms, list):
            group.permissions.clear()
            for perm_codename in perms:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"⚠️ Permiso {perm_codename} no encontrado (¿falta definir en modelos?)")
        else:
            # Si es Permission.objects.all()
            group.permissions.set(perms)

    print('✅ Grupos y permisos creados correctamente.')
