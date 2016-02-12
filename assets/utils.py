from django.core.exceptions import ValidationError

import re


# def validate_version(version):
#     #TODO: REDO to have lenght<10
    # #Checking string to contain only specified chars
    # if re.match(r'^[0-9\.]+$', version) is None:
    #     raise ValidationError("Version may contain only digits and dots")
    #
    # #Check each subversion
    # subversions = re.split(r'\.', version)
    # validated_subversions = []
    # for subverion in subversions:
    #     if subverion == '':
    #         raise ValidationError('Subversions cant be empty')
    #     if len(subverion)>3:
    #         raise ValidationError('Maximum lenght of subversion is 3 digits')
    #     validated_subversions.append(str(int(subverion)))
    #
    # validated_version ='.'.join(validated_subversions)
    # return validated_version