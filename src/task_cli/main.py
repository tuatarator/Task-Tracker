import argparse
import json
import os.path
import time

DATA_FILE = '../data_copy.json'

# Загружаем данные
def load_data():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except:
                return []
    return []

def save_data(new_data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=2, ensure_ascii=False)
    return

#add new task
def add_task(args):
    allData = load_data()
    
    newId = 1
    for record in allData:
        if int(record["id"]) >= newId:
                 newId = int(record["id"]) + 1
    formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(formatted)
    newTask = {
        "id" : newId,
        "description" : args.text,
        "status" : "todo",
        "createdAt" : formatted,
        "updatedAt" : formatted
    }
    newData = allData
    newData.append(newTask)
    try:
        save_data(newData)
        print('New task saved!')
        return
    except:
        print("ERROR while sawing newTask")
        return
    
#delete task
def remove_task(args):
    removingId = args.id
    allData = load_data()
    newData = allData
    for num in range(len(allData)):
        if newData[num["id"]] == removingId:
            newData[num].remove()

#udpate task by id
def update_task(args):
    taskId = args.id
    allData = load_data()

    for task in allData:
        if task["id"] == taskId:
            task["description"] = args.text
            save_data(allData)
            break
    else:
        add_task(args)
    return

#update task status
def mark_task(args):
    # return print(args)
    allData = load_data()
    for task in allData:
        if task["id"] == args.id:
            if args.command == "mark-done":
                task["status"] = "done"
            elif args.command =="mark-in-progress":
                task["status"] = "in-progress"
    save_data(allData)
    return

# Listing tasks by status
def task_list(args):
    showStatus = args.status
    allData = load_data()
    taskList = []

    if (showStatus != "all"):
        for record in allData:
            if record["status"] == showStatus:
                taskList.append(' '.join([str(record["id"]), record["description"], record["status"]]))
        return print('\n'.join(taskList))
    
    for record in allData:
        taskList.append(' '.join([str(record["id"]), record["description"], record["status"]]))

    return print('\n'.join(taskList))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # parser argument 'add text'
    parse_add = subparsers.add_parser("add", help="add new task")
    parse_add.add_argument("text", type=str, help= "task name")
    parse_add.set_defaults(func=add_task)

    # parse argument 'remove id'
    parse_remove = subparsers.add_parser("remove", help="remove task")
    parse_remove.add_argument("id", type=int, help= "task id")
    parse_remove.set_defaults(func=remove_task)

    #parse 'list status'
    parse_list = subparsers.add_parser("list", help="show tasks by status, default all")
    parse_list.add_argument("status",nargs="?",choices=["todo", "in-progress", "done"],default="all")
    parse_list.set_defaults(func=task_list)

    #parse 'update id'
    parse_update = subparsers.add_parser("update", help="update task by id")
    parse_update.add_argument("id", type=int, help="task id")
    parse_update.add_argument("text", type= str, help="new task text")
    parse_update.set_defaults(func=update_task)

    parse_mark_in_progress = subparsers.add_parser("mark-in-progress", help="")
    parse_mark_in_progress.add_argument("id", type=int, help="task id")
    parse_mark_in_progress.set_defaults(func=mark_task)

    parse_mark_done = subparsers.add_parser("mark-done", help="")
    parse_mark_done.add_argument("id", type=int, help="task_id")
    parse_mark_done.set_defaults(func=mark_task)

    args = parser.parse_args()
    args.func(args)
 
if __name__ == '__main__':
    main()

