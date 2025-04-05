from backend.models.mysql_connection_pool import MySQLPool

class TaskModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()

    def get_task(self, task_id):    
        params = {'task_id' : task_id}      
        rv = self.mysql_pool.execute("""SELECT T.task_id, T.task_title, T.task_description, U.user_name, U.user_lastname from tasks T 
                                        inner join users U on T.user_id = U.user_id
                                        where T.task_id = %(task_id)s""", params)                
        data = []
        content = {}
        for result in rv:
            content = {'task_id': result[0], 'task_title': result[1], 'task_description': result[2], 'user_name': result[3], 'user_lastname': result[4]}
            data.append(content)
            content = {}
        return data

    def get_tasks(self):  
        rv = self.mysql_pool.execute("""SELECT T.task_id, T.task_title, T.task_description, U.user_name, U.user_lastname from tasks T 
                                        inner join users U on T.user_id = U.user_id""")  
        data = []
        content = {}
        for result in rv:
            content = {'task_id': result[0], 'task_title': result[1], 'task_description': result[2], 'user_name': result[3], 'user_lastname': result[4]}
            data.append(content)
            content = {}
        return data

    def create_task(self, title, description, user_id):    
        data = {
            'task_title' : title,
            'task_description' : description,
            'user_id' : user_id
        }  
        query = """insert into tasks (task_title, task_description, user_id) 
            values (%(task_title)s, %(task_description)s, %(user_id)s)"""    
        cursor = self.mysql_pool.execute(query, data, commit=True)   

        data['task_id'] = cursor.lastrowid
        return data

    def delete_task(self, task_id):    
        params = {'task_id' : task_id}      
        query = """delete from tasks where task_id = %(task_id)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        data = {'result': 1}
        return data

if __name__ == "__main__":    
    tm = TaskModel()     

    #print(tm.get_task(1))
    #print(tm.get_tasks())
    #print(tm.delete_task(67))
    #print(tm.get_tasks())
    print(tm.create_task('prueba 10', 'desde python', 1)) 