from .tasks import create_random_note
import time

if __name__ == '__main__':
    result = create_random_note.delay(12)
    # at this time, our task is not finished, so it will return False
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)
    # sleep 10 seconds to ensure the task has been finished
    time.sleep(10)
    # now the task should be finished and ready method will return True
    print('Task finished? ', result.ready())
    print('Task result: ', result.result)

