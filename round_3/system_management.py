import mysql.connector

class Task:
    def __init__(self, title, description, due_date, status='todo'):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status

class WorkManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='work_management'
        )
        self.cursor = self.conn.cursor()

    def create_task(self, task):
        sql = "INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s)"
        values = (task.title, task.description, task.due_date, task.status)
        self.cursor.execute(sql, values)
        self.conn.commit()
        print("Task created successfully.")

    def read_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            print(task)

    def update_task_status(self, task_id, new_status, new_title=None, new_description=None, new_due_date=None):
            update_fields = []
            values = []

            if new_status:
                update_fields.append("status = %s")
                values.append(new_status)
            if new_title:
                update_fields.append("title = %s")
                values.append(new_title)
            if new_description:
                update_fields.append("description = %s")
                values.append(new_description)
            if new_due_date:
                update_fields.append("due_date = %s")
                values.append(new_due_date)

            if not update_fields:
                print("No fields to update.")
                return

            sql = "UPDATE tasks SET " + ", ".join(update_fields) + " WHERE id = %s"
            values.append(task_id)
            self.cursor.execute(sql, tuple(values))
            self.conn.commit()
            print("Task updated successfully.")

    def delete_task(self, task_id):
        sql = "DELETE FROM tasks WHERE id = %s"
        values = (task_id,)
        self.cursor.execute(sql, values)
        self.conn.commit()
        print("Task deleted successfully.")

    # def __del__(self):
    #     self.cursor.close()
    #     self.conn.close()

# Example usage:
if __name__ == "__main__":
    work_manager = WorkManager()

    # Create a new task
    # new_task = Task("Complete project", "Review the design", "2024-04-10")
    # work_manager.create_task(new_task)

    # Read all tasks
    work_manager.read_tasks()

    # Update task status and other fields
    # work_manager.update_task_status(4, 'in_progress', new_title="Complete project", new_description="Finish the coding project", new_due_date="2024-04-15")
    
    # Delete a task
    # work_manager.delete_task(1)
