# -*- mode: python; coding: utf-8; -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class ObjectPermission(models.Model):
    user = models.ForeignKey(User)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()