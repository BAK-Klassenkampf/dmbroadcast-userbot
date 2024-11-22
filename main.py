from telethon import TelegramClient
import os
import time

sent_to = map(int, open("sent.txt", "r", encoding="utf-8").read().split("\n"))

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

client = TelegramClient('dmbroadcast', api_id, api_hash)
client.start()

async def main():
    dialogs = await client.get_dialogs()
    groups = [dialog for dialog in dialogs if dialog.is_group]
    for index in range(len(groups)):
        group = groups[index]
        print(index, group.name, group.id)

    group_index = int(input("Enter group to broadcast messages to: "))
    group = groups[group_index]

    self = await client.get_me()
    participants = await client.get_participants(group.id)

    if not any(participant.id == self.id and hasattr(participant.participant, "admin_rights") and participant.participant.admin_rights is not None for participant in participants): 
        print("You are not an admin in this group") 
        return
    
    message = open("message.txt", "r", encoding="utf-8").read()

    print(f"Sending message to {len(participants)} participants in {group.name}")
    print("Message:")
    print(message)
    input("Press enter to continue")

    async for participant in client.iter_participants(group.id):
        if participant.id in sent_to:
            continue
        if participant.id == self.id:
            continue
        try:
            await client.send_message(participant.id, message)
            print(f"Sent message to {participant.id}")
        except Exception as e:
            print(f"Failed to send message to {participant.id}")
            print(e.__class__.__name__)
            print(e)
        time.sleep(2)

with client:
    client.loop.run_until_complete(main())