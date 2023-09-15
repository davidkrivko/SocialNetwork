def custom_upload_path(instance, filename):
    return f"posts_photos/{instance.user.username}/{instance.id}/{filename}"
