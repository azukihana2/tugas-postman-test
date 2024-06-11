import mysql.connector

def run_script(script_path):
    with open(script_path, 'r') as file:
        script = file.read()

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )

    cursor = conn.cursor()
    for result in cursor.execute(script, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    run_script('db.sql')
