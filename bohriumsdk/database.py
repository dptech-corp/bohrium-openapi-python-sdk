import sqlite3



class Database():

    def __init__(
            self,
            db_file: str = "brm.db"
        ) -> None:
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def init_db(self):
        sql = '''
        CREATE TABLE brm_job (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTGER NOT NULL,
            job_group_id INTGER NOT NULL,
            work_dir TEXT NOT NULL,
            job_hash TEXT NOT NULL
        )
        '''
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_record(self, job_id, job_group_id, work_dir, job_hash):
        sql = f'''
        INSERT INTO brm_job (job_id, job_group_id, work_dir, job_hash) VALUES ({job_id}, {job_group_id}, {work_dir}, {job_hash})
        '''
        self.cursor.execute(sql)
        self.conn.commit()


    def get_record(self, job_id):
        sql = f'''
        SELECT * FROM brm_job WHERE job_id = {job_id}
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    
    def get_all_record(self, job_id):
        sql = f'''
        SELECT * FROM brm_job
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def update_record(self, job_id, job_group_id, work_dir, job_hash):
        sql = f'''
        UPDATE brm_job SET job_group_id = {job_group_id}, work_dir = {work_dir}, job_hash = {job_hash} WHERE job_id = {job_id}
        '''
        self.cursor.execute(sql)
        self.conn.commit()

    def delete_record(self, job_id):
        sql = f'''
        DELETE FROM brm_job WHERE job_id = {job_id}
        '''
        self.cursor.execute(sql)
        self.conn.commit()