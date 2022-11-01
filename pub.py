from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# TODO(developer)
project_id = "otpreader-335517"
subscription_id = "my-sub"
# Number of seconds the subscriber should listen for messages
timeout = 500.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

# 0. OTP: 449225 - time: 2022-11-01 20:23:48+05:30
# 1. OTP: 577161 - time: 2022-11-01 19:15:49+05:30
# 2. OTP: 374415 - time: 2022-11-01 19:15:28+05:30
# 3. OTP: 408116 - time: 2022-11-01 10:12:11+05:30