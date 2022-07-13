from discord import TextChannel, Thread

def find_thread(name: str, channel: TextChannel) -> Thread:
    nameFormatted = name.lower().replace(' ','')

    foundThread = None

    for thread in channel.threads:
        threadName = thread.name.lower().replace(' ', '')

        if threadName == nameFormatted:
            foundThread = thread
    
    return foundThread