from django.core.validators import RegexValidator, ValidationError


def validate_year(self, value):
    # TODO: Add more max checks for year validation
    validator = RegexValidator(re.compile('\b\d{4}\b'), "invalid year")

    try:
        validator(value)
    except ValidationError:
        raise ValidationError('The value you\'ve added is not a valid year')

    return value