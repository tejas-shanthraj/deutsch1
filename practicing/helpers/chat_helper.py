import openai
from openai import OpenAI

import time
import re

from tqdm import tqdm

from .config import ASSISTANT_ID_EN, PERSONAL_KEY

client = OpenAI(
    api_key = PERSONAL_KEY,
)

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
        elif run_retrieve.status == "failed":
            print("Run failed with msg: ", run_retrieve.last_error)
            break

        else:
            WAIT_SECONDS = 1
            print(f'Run was not completed. Waiting for {WAIT_SECONDS} seconds, before trying again')
            for i in tqdm(range(WAIT_SECONDS)):                
                time.sleep(1)

    return answer, conv_id


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
                    response = message.content[0].text.value
                    # Extract the first sentence before "---"
                    first_sentence = re.search(r'^(.*?)(?=\n---)', response, re.DOTALL)
                    first_sentence_result = first_sentence.group(1).strip() if first_sentence else None
                    # Remove the word before ":" and ":"
                    first_sentence_result = first_sentence_result.split(": ", 1)[-1].strip() if first_sentence_result else response

                    # Extract the first sentence after "---"
                    next_sentence = re.search(r'---\s*(.*?)\n', response, re.DOTALL)
                    next_sentence_result = next_sentence.group(1).strip() if next_sentence else None
                    # Remove the word before ":" and ":"
                    next_sentence_result = next_sentence_result.split(": ", 1)[-1].strip() if next_sentence_result else ''
                    
                    combined_result = f"{first_sentence_result}\n\n{next_sentence_result}"
                    answer = combined_result.replace("Assistant:", "").replace("Student:", "")
                    break
        else:
            print('Run was not completed')
            time.sleep(1)


    return answer