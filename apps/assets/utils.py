from django.utils.text import slugify

def version_filename_save(instance, filename):
    name, ext = filename.split(filename.split('.')[0])
    filename = slugify(instance.asset.name) + slugify(instance.asset.version) +  ext
    return filename
