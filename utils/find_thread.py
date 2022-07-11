from discord import TextChannel, Thread

async def find_thread(name: str, channel: TextChannel) -> Thread:
    nameFormatted = name.lower().replace(' ','')

    archived_thread = channel.archived_threads()

    async for thread in archived_thread:
        threadName = thread.name.lower().replace(' ', '')

        if threadName == nameFormatted:
            return thread

    for thread in channel.threads:
        threadName = thread.name.lower().replace(' ', '')

        if threadName == nameFormatted:
            return thread
    
    return None