def version_filename_save(instance, filename):
    ext = filename.split('.')[-1]
    filename = str(instance.version()) + str(instance.entry.name) + '.' + ext
    return filename
