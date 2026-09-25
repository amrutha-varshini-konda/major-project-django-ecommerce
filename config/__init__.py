import django.db.backends.mysql.base as mysql_base

# Bypass Django's MySQL minimum version requirement
mysql_base.DatabaseWrapper.check_database_version_supported = lambda self: None