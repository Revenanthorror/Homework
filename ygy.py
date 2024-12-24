from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

TASKS_FILE = 'tasks.txt'

class Task:
    def __init__(self, title, priority, isDone=False, id=None):
        self.title = title
        self.priority = priority
        self.isDone = isDone
        self.id = id

    def to_dict(self):
        return {
            'title': self.title,
            'priority': self.priority,
            'isDone': self.isDone,
            'id': self.id
        }

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                try:
                    tasks_data = json.load(f)
                    self.tasks = [Task(**task) for task in tasks_data]
                except json.JSONDecodeError as e:
                    print("Oshibka pri dekodirovanii JSON:", e)
                except Exception as e:
                    print("Proizoshla oshibka:", e)

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def add_task(self, title, priority):
        task_id = len(self.tasks) + 1
        new_task = Task(title, priority, id=task_id)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def get_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.isDone = True
                self.save_tasks()
                return True
        return False

class HttpRequestHandler(BaseHTTPRequestHandler):
    task_manager = TaskManager()

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)

            title = task_data.get('title')
            priority = task_data.get('priority')

            if title and priority:
                new_task = self.task_manager.add_task(title, priority)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(new_task.to_dict()).encode())
            else:
                self.send_response(400)
                self.end_headers()

        elif self.path.startswith('/tasks/') and self.path.endswith('/complete'):
            task_id = int(self.path.split('/')[-2])
            if self.task_manager.complete_task(task_id):
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

    def do_GET(self):
        if self.path == '/tasks':
            tasks = self.task_manager.get_tasks()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Privet, rad videt' na moem servere</h1><p>Ispol'zyi /tasks chto bi ypravlyat' zadachami.</p></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=HttpRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting server on http://localhost:8000')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
#для создания задачи (post-запрос) используй команду в терминале curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "Gym", "priority": "low"}'
#там можно добаить другие задачи
#для получения списка задач (get-запрос) используй эту команду curl -X GET http://localhost:8000/tasks
