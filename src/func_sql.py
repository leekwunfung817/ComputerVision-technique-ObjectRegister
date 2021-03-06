import pymysql
# python3 -m pip install pymysql

def query(sql,config):
	if config['db'] is None:
		return
	dbc = config['db']
	conn  = pymysql.connect(host=dbc['host'], user=dbc['user'], password=dbc['password'], database=dbc['database'])
	# Create a cursor object 
	cur  = conn.cursor()
	# PRODUCT_ID = '1201'
	# price = 10000
	# PRODUCT_TYPE = 'PRI'
	# query = f"INSERT INTO PRODUCT (PRODUCT_ID, price,PRODUCT_TYPE) VALUES ('{PRODUCT_ID}', '{price}', '{PRODUCT_TYPE}')"
	cur.execute(sql) 
	print(f"{cur.rowcount} details inserted")
	conn.commit() 
	conn.close() 