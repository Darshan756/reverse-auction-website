from django.db import models

class OrganizationTypes(models.TextChoices):
    INDIVIDUAL = 'individual', 'Individual'
    SOLE_PROPRIETORSHIP = 'sole_proprietorship', 'Sole Proprietorship'
    PARTNERSHIP = 'partnership', 'Partnership'
    PRIVATE_LIMITED = 'private_limited', 'Private Limited'
    PUBLIC_LIMITED = 'public_limited', 'Public Limited'
    NGO = 'ngo', 'NGO / Trust'
