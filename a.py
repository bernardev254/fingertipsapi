import pymysql

cnx = pymysql.connect(host='ec2-3-231-39-248.compute-1.amazonaws.com',
                                user='ubuntu',
				port=3306,
				password='password',
                                database='fingertips')
cnx.close()
