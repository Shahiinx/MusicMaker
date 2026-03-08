import os
import glob
import asyncio
import time
from pyrogram import Client, filters

last_cleanup_time = 0
PROTECTED_KEYWORD = "bot" 

async def delete_temp_files():
    global last_cleanup_time
    while True:
        await asyncio.sleep(100)
        current_time = time.time()
        if current_time - last_cleanup_time >= 100:
            try:
                downloads = os.path.realpath("downloads")
                if os.path.exists(downloads):
                    for file in os.listdir(downloads):
                        if PROTECTED_KEYWORD.lower() in file.lower():  
                            continue
                        file_path = os.path.join(downloads, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            import shutil
                            shutil.rmtree(file_path)

                files_to_delete = glob.glob("*.webm") + glob.glob("*.jpg") + glob.glob("*.png")
                for file_path in files_to_delete:
                    file_name = os.path.basename(file_path)
                    if PROTECTED_KEYWORD.lower() in file_name.lower():
                        continue
                    if os.path.exists(file_path):
                        os.remove(file_path)

                last_cleanup_time = current_time

            except Exception:
                pass

asyncio.ensure_future(delete_temp_files())