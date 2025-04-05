from backend.models.mysql_connection_pool import MySQLPool

class UserModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def get_user(self, user_id):    
        params = {'user_id' : user_id}      
        rv = self.mysql_pool.execute("SELECT * from users where user_id=%(user_id)s", params)                
        data = []
        content = {}
        for result in rv:
            content = {'user_id': result[0], 'user_name': result[1], 'user_lastname': result[2], 'user_email': result[3]}
            data.append(content)
            content = {}
        return data

    def get_users(self):  
        rv = self.mysql_pool.execute("SELECT * from users")  
        data = []
        content = {}
        for result in rv:
            content = {'user_id': result[0], 'user_name': result[1], 'user_lastname': result[2], 'user_email': result[3]}
            data.append(content)
            content = {}
        return data

    def create_user(self, user_name, user_lastname, user_email):    
        data = {
            'user_name' : user_name,
            'user_lastname' : user_lastname,
            'user_email': user_email
        }  
        query = """insert into users (user_name, user_lastname, user_email) 
            values (%(user_name)s, %(user_lastname)s, %(user_email)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['user_id'] = cursor.lastrowid
        return data

    def update_user(self, user_id, user_name, user_lastname, user_email):    
        data = {
            'user_id' : user_id,
            'user_name' : user_name,
            'user_lastname' : user_lastname,
            'user_email': user_email
        }  
        query = """update users set user_name = %(user_name)s, user_lastname = %(user_lastname)s,
                    user_email= %(user_email)s where user_id = %(user_id)s"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        result = {'result':1} 
        return result

    def delete_user(self, user_id):    
        params = {'user_id' : user_id}      
        query = """delete from users where user_id = %(user_id)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        result = {'result': 1}
        return result 


