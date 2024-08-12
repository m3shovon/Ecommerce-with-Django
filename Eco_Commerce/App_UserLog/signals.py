from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from App_UserLog.models import UserLog


@receiver(pre_save)
def log_object_changes(sender, instance, **kwargs):
    
    if sender.__name__ != "UserLog" and sender.__name__ != "Session":
        print("-----------------------------------------")
        print(sender.__name__)
        import inspect
        request = ""
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None

        ### Object is new, so we can't compare the changes###
        if not instance.pk:
            return

        original_instance = sender.objects.get(pk=instance.pk)
        changes = []
        for field in instance._meta.fields:
            field_name = field.name
            original_value = getattr(original_instance, field_name)
            new_value = getattr(instance, field_name)
            if original_value != new_value:
                changes.append(f"{field_name}: {original_value} -> {new_value}")
        
        if changes:
            action = f'Updated {sender.__name__} {instance} ({", ".join(changes)})'
            content_type = ContentType.objects.get_for_model(sender)
            if request is not None and sender.__name__ != "Session":
                UserLog.objects.create(
                    user=request.user,
                    action=action,
                    content_type=content_type,
                    object_id=instance.pk,
            )
            

@receiver(post_save)
def log_object_creation_update(sender, instance, created, **kwargs):
    if sender.__name__ != "UserLog":
        import inspect
        request=""
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None

        if created:
            action = f'Created {sender.__name__} {instance}'
        # else:
        #     original_instance = sender.objects.get(pk=instance.pk)
        #     changes = []
        #     for field in instance._meta.fields:
        #         field_name = field.name
        #         original_value = getattr(original_instance, field_name)
        #         new_value = getattr(instance, field_name)
        #         if original_value != new_value:
        #             changes.append(f"{field_name}: {original_value} -> {new_value}")
        #     action = f'Updated {sender.__name__} {instance} ({", ".join(changes)})'
    
            content_type = ContentType.objects.get_for_model(sender)

            if request and request.user.is_authenticated:
                UserLog.objects.create(
                    user=request.user,
                    action=action,
                    content_type=content_type,
                    object_id=instance.pk,
                )



@receiver(post_delete)
def log_object_deletion(sender, instance, **kwargs):
    if sender.__name__ != "UserLog" or sender.__name__ != "Session":
        # print("---------------------------------------------------------------------")
        import inspect 
        request=""
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None
        content_type = ContentType.objects.get_for_model(sender)
        # print(instance)
        # print(content_type)
        # print(sender.__name__)
        if request is not None and sender.__name__ != "Session":
            UserLog.objects.create(
                user=request.user,
                action=f'Deleted {sender.__name__} {instance}',
                content_type=content_type,
                object_id=instance.pk,
                )
