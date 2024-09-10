import openai
from openai import OpenAI

import time

from .config import CHAT_GPT_API_KEY, CHAT_GPT_DEFAULT_MODEL, CHAT_GPT_ORG, ASSISTANT_ID_EN, ASSISTANT_ID_RU

client = OpenAI(
    api_key = CHAT_GPT_API_KEY,
    organization = CHAT_GPT_ORG
)

def GetStartingMessageRU(situation):

    assistant_ru = client.beta.assistants.retrieve(ASSISTANT_ID_RU)
    thread = client.beta.threads.create()

    topic = situation.topic
    about = situation.about
    participants = situation.participants
    student_role = situation.student_role
    student_goal = situation.student_goal

    conversational_situation = f'Тема: {topic} \n Ситуация: {about} \n Участники: {participants} \n Роль Студента: {student_role} \n Цель Студента: {student_goal} .'
    
    conv_id = thread.id
    print('conversational_situation: ', conversational_situation)

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = conversational_situation
    )

    run_create = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant_ru.id,
        # instructions = instructions
    )

    completed = False
    answer = ''

    while not completed:
        run_retrieve = client.beta.threads.runs.retrieve(
            thread_id = thread.id,
            run_id = run_create.id
        )

        print('run_retrieve.completed_at: ', run_retrieve.completed_at)

        if run_retrieve.completed_at != None:
            completed = True
            messages = client.beta.threads.messages.list(
                thread_id = thread.id
            )
            for message in messages.data:
                if message.assistant_id == ASSISTANT_ID_RU:
                    # print('message.content[0]', message.content[0].text)
                    print('message.content[0].value', message.content[0].text.value)
                    answer = message.content[0].text.value
        else:
            print('Run was not completed')
            time.sleep(1)

    return answer, conv_id

def GetStartingMessageEN(situation):

    assistant_en = client.beta.assistants.retrieve(ASSISTANT_ID_EN)
    thread = client.beta.threads.create()

    topic = situation.topic
    about = situation.about
    participants = situation.participants
    student_role = situation.student_role
    student_goal = situation.student_goal

    conversational_situation = f'Topic: {topic} \n About: {about} \n Participants: {participants} \n Student role: {student_role} \n Student goal: {student_goal} .'
    
    conv_id = thread.id
    print('conversational_situation: ', conversational_situation)

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = conversational_situation
    )

    run_create = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant_en.id,
        # instructions = instructions
    )

    completed = False
    answer = ''

    while not completed:
        run_retrieve = client.beta.threads.runs.retrieve(
            thread_id = thread.id,
            run_id = run_create.id
        )

        print('run_retrieve.completed_at: ', run_retrieve.completed_at)

        if run_retrieve.completed_at != None:
            completed = True
            messages = client.beta.threads.messages.list(
                thread_id = thread.id
            )
            for message in messages.data:
                if message.assistant_id == ASSISTANT_ID_EN:
                    # print('message.content[0]', message.content[0].text)
                    print('message.content[0].value', message.content[0].text.value)
                    answer = message.content[0].text.value
        else:
            print('Run was not completed')
            time.sleep(1)

    return answer, conv_id

def GetTeacherResponseRU(message, conv_id):
    print('in GetTeacherResponse message: ', message)
    print('in GetTeacherResponse conv_id: ', conv_id)

    user_answer = message
    thread_id = conv_id

    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role = "user",
        content = user_answer
    )

    assistant_ru = client.beta.assistants.retrieve(ASSISTANT_ID_RU)

    run_create = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_ru.id,
    )

    completed = False
    answer = ''

    while not completed:
        run_retrieve = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = run_create.id
        )

        print('run_retrieve.completed_at: ', run_retrieve.completed_at)

        if run_retrieve.completed_at != None:
            completed = True
            messages = client.beta.threads.messages.list(
                thread_id = thread_id
            )
            for message in messages.data:
                if message.assistant_id == ASSISTANT_ID_RU:
                    # print('message.content[0]', message.content[0].text)
                    print('message.content[0].value', message.content[0].text.value)
                    answer = message.content[0].text.value
                    break
        else:
            print('Run was not completed')
            time.sleep(1)


    return answer


def GetTeacherResponseEN(message, conv_id):
    print('in GetTeacherResponse message: ', message)
    print('in GetTeacherResponse conv_id: ', conv_id)

    user_answer = message
    thread_id = conv_id

    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role = "user",
        content = user_answer
    )

    assistant_en = client.beta.assistants.retrieve(ASSISTANT_ID_EN)

    run_create = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_en.id,
    )

    completed = False
    answer = ''

    while not completed:
        run_retrieve = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = run_create.id
        )

        print('run_retrieve.completed_at: ', run_retrieve.completed_at)

        if run_retrieve.completed_at != None:
            completed = True
            messages = client.beta.threads.messages.list(
                thread_id = thread_id
            )
            for message in messages.data:
                if message.assistant_id == ASSISTANT_ID_EN:
                    # print('message.content[0]', message.content[0].text)
                    print('message.content[0].value', message.content[0].text.value)
                    answer = message.content[0].text.value
                    break
        else:
            print('Run was not completed')
            time.sleep(1)


    return answer