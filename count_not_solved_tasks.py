from methods import *


s = get_and_auth()
course_id, group_id = get_course(s)
lessons = get_all_lessons(s, course_id, group_id)

print("Ваши нерешённые задачи или незачтённые задачи:\n")

statuses = set()

for lesson in lessons:

    with_deadline = True
    if lesson['msBeforeDeadline'] is not None:
        if lesson['msBeforeDeadline'] < 0:
            break
    else:
        with_deadline = False

    if lesson['type'] != 'normal' or lesson['numPassed'] == lesson['numTasks']:
        continue
    lesson_id = lesson['id']
    tasks = get_all_tasks(s, lesson_id, course_id)
    for task_group in tasks:
        for task in task_group['tasks']:
            solution = task['solution']
            if solution is not None:
                statuses.add(tuple(solution['status'].values()))
            if solution is None or \
                    (not solution['score'] and solution['status']['type'] != 'review'):

                if with_deadline:
                    print(f"{lesson['title']}: {task['title']}")
                else:
                    print(f"{lesson['title']}: {task['title']} (Без ограничений по времени)")
