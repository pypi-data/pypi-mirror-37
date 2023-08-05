from django.db import models


class Dhcp4Options(models.Model):
    option_id = models.AutoField(primary_key=True)
    code = models.PositiveIntegerField()
    value = models.TextField(blank=True, null=True)
    formatted_value = models.TextField(blank=True, null=True)
    space = models.CharField(max_length=128, blank=True, null=True)
    persistent = models.IntegerField()
    dhcp_client_class = models.CharField(max_length=128, blank=True, null=True)
    dhcp4_subnet_id = models.PositiveIntegerField(blank=True, null=True)
    host = models.ForeignKey('Hosts', models.DO_NOTHING, blank=True, null=True)
    scope = models.ForeignKey('DhcpOptionScope', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dhcp4_options'


class Dhcp6Options(models.Model):
    option_id = models.AutoField(primary_key=True)
    code = models.PositiveSmallIntegerField()
    value = models.TextField(blank=True, null=True)
    formatted_value = models.TextField(blank=True, null=True)
    space = models.CharField(max_length=128, blank=True, null=True)
    persistent = models.IntegerField()
    dhcp_client_class = models.CharField(max_length=128, blank=True, null=True)
    dhcp6_subnet_id = models.PositiveIntegerField(blank=True, null=True)
    host = models.ForeignKey('Hosts', models.DO_NOTHING, blank=True, null=True)
    scope = models.ForeignKey('DhcpOptionScope', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dhcp6_options'


class DhcpOptionScope(models.Model):
    scope_id = models.PositiveIntegerField(primary_key=True)
    scope_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dhcp_option_scope'


class HostIdentifierType(models.Model):
    type = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'host_identifier_type'


class Hosts(models.Model):
    host_id = models.AutoField(primary_key=True)
    dhcp_identifier = models.BinaryField(max_length=128)  # must be binary to store values
    dhcp_identifier_type = models.ForeignKey(HostIdentifierType, models.DO_NOTHING, db_column='dhcp_identifier_type')
    dhcp4_subnet_id = models.PositiveIntegerField(blank=True, null=True)
    dhcp6_subnet_id = models.PositiveIntegerField(blank=True, null=True)
    ipv4_address = models.PositiveIntegerField(blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    dhcp4_client_classes = models.CharField(max_length=255, blank=True, null=True)
    dhcp6_client_classes = models.CharField(max_length=255, blank=True, null=True)
    dhcp4_next_server = models.PositiveIntegerField(blank=True, null=True)
    dhcp4_server_hostname = models.CharField(max_length=64, blank=True, null=True)
    dhcp4_boot_file_name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hosts'
        unique_together = (('dhcp_identifier', 'dhcp_identifier_type', 'dhcp4_subnet_id'), ('dhcp_identifier', 'dhcp_identifier_type', 'dhcp6_subnet_id'), ('ipv4_address', 'dhcp4_subnet_id'),)


class Ipv6Reservations(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=39)
    prefix_len = models.PositiveIntegerField()
    type = models.PositiveIntegerField()
    dhcp6_iaid = models.PositiveIntegerField(blank=True, null=True)
    host = models.ForeignKey(Hosts, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ipv6_reservations'
        unique_together = (('address', 'prefix_len'),)


class Lease4(models.Model):
    address = models.PositiveIntegerField(primary_key=True)
    hwaddr = models.CharField(max_length=20, blank=True, null=True)
    client_id = models.CharField(max_length=128, blank=True, null=True)
    valid_lifetime = models.PositiveIntegerField(blank=True, null=True)
    expire = models.DateTimeField()
    subnet_id = models.PositiveIntegerField(blank=True, null=True)
    fqdn_fwd = models.IntegerField(blank=True, null=True)
    fqdn_rev = models.IntegerField(blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey('LeaseState', models.DO_NOTHING, db_column='state', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease4'


class Lease6(models.Model):
    address = models.CharField(primary_key=True, max_length=39)
    duid = models.CharField(max_length=128, blank=True, null=True)
    valid_lifetime = models.PositiveIntegerField(blank=True, null=True)
    expire = models.DateTimeField()
    subnet_id = models.PositiveIntegerField(blank=True, null=True)
    pref_lifetime = models.PositiveIntegerField(blank=True, null=True)
    lease_type = models.ForeignKey('Lease6Types', models.DO_NOTHING, db_column='lease_type', blank=True, null=True)
    iaid = models.PositiveIntegerField(blank=True, null=True)
    prefix_len = models.PositiveIntegerField(blank=True, null=True)
    fqdn_fwd = models.IntegerField(blank=True, null=True)
    fqdn_rev = models.IntegerField(blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    hwaddr = models.CharField(max_length=20, blank=True, null=True)
    hwtype = models.PositiveSmallIntegerField(blank=True, null=True)
    hwaddr_source = models.ForeignKey('LeaseHwaddrSource', models.DO_NOTHING, db_column='hwaddr_source', blank=True, null=True)
    state = models.ForeignKey('LeaseState', models.DO_NOTHING, db_column='state', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease6'


class Lease6Types(models.Model):
    lease_type = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease6_types'


class LeaseHwaddrSource(models.Model):
    hwaddr_source = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lease_hwaddr_source'


class LeaseState(models.Model):
    state = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'lease_state'


class SchemaVersion(models.Model):
    version = models.IntegerField(primary_key=True)
    minor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schema_version'
