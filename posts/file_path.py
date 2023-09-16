def custom_upload_path(instance, filename):
    file, ext = filename.split(".")

    return f"posts_photos/{instance.id}_{file}.{ext}"
