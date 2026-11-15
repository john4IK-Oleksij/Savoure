import django_stubs_ext
import pymysql

django_stubs_ext.monkeypatch()
pymysql.install_as_MySQLdb()
