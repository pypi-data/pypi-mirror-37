from django.db import models


class Comments(models.Model):
    domain = models.ForeignKey('Domains', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    modified_at = models.IntegerField()
    account = models.CharField(max_length=40, blank=True, null=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'comments'


class Cryptokeys(models.Model):
    domain = models.ForeignKey('Domains', models.DO_NOTHING)
    flags = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cryptokeys'


class Domainmetadata(models.Model):
    domain = models.ForeignKey('Domains', models.DO_NOTHING)
    kind = models.CharField(max_length=32, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domainmetadata'


class Domains(models.Model):
    name = models.CharField(unique=True, max_length=255)
    master = models.CharField(max_length=128, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6)
    notified_serial = models.PositiveIntegerField(blank=True, null=True)
    account = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domains'


class Records(models.Model):
    id = models.BigAutoField(primary_key=True)
    domain = models.ForeignKey(Domains, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=64000, blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True)
    prio = models.IntegerField(blank=True, null=True)
    change_date = models.IntegerField(blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True)
    ordername = models.CharField(max_length=255, blank=True, null=True)
    auth = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records'


class Supermasters(models.Model):
    ip = models.CharField(primary_key=True, max_length=64)
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'supermasters'
        unique_together = (('ip', 'nameserver'),)


class Tsigkeys(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tsigkeys'
        unique_together = (('name', 'algorithm'),)
