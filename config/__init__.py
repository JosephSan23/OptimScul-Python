import pymysql

# Le decimos a Django que use PyMySQL emulando a mysqlclient
pymysql.install_as_MySQLdb()