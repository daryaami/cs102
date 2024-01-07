
from tqdm import tqdm
import pandas as pd
import sys

from vkapi.friends import get_friends, get_mutual
from research.network import ego_network, plot_ego_network, plot_communities, get_communities, describe_communities
from research.age import age_predict

pd.set_option('display.max_rows', None)

MY_ID = 401178649
maxim_id = 175551679
lera_id = 329996033
current_user = MY_ID
# print(age_predict(user_id=current_user))

resp = get_friends(current_user, fields=['deactivated'], count=30)

active_users_ids = [user["id"] for user in resp.items if not user.get("deactivated")]

friends = active_users_ids[:]
# print(friends)

# print(get_mutual(current_user, target_uids=friends, progress=tqdm))

network = ego_network(friends=friends)

# plot_ego_network(network)

communities = get_communities(network)
description = describe_communities(communities, resp.items, fields=["first_name", "last_name"])

print(description)

plot_communities(network)