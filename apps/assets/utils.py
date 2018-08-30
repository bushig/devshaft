from django.utils.text import slugify

def version_filename_save(instance, filename):
    name, ext = filename.split(filename.split('.')[0])
    final_name = "_".join([slugify(instance.release.asset.name), slugify(instance.release.version), slugify(instance.note)])
    filename =  final_name + ext
    return 'assets/releases/'+filename
