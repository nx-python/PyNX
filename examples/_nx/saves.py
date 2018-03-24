import _nx
import os
import sys

title_id =  0x01007ef00011e000  # BotW

_nx.account_initialize()
user_id = _nx.account_get_active_user()

if user_id is None:
    print("No active user, you need to launch and close a game prior to launching hbl.")
    sys.exit()

_nx.fs_mount_savedata("save", title_id, user_id)

print(os.listdir("save:/"))
