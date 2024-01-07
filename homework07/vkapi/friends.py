import sys
import dataclasses
import math
import time
import typing as tp
from tqdm import tqdm

from vkapi.config import VK_CONFIG
from vkapi.session import Session
# from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    user_id = user_id
    fields = fields
    count = count

    s = Session(base_url=domain)
    response = s.get('friends.get', {
        'access_token': access_token, 'count': count, 'user_id': user_id, 'fields': fields, 'v': v}).json()
    if 'error' in response:
        raise Exception(response['error']['error_msg'])

    friends_response = FriendsResponse(
        response['response']['count'], response['response']['items'])
    return friends_response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    s = Session(base_url=VK_CONFIG['domain'])

    if not target_uids:
        if not target_uid:
            return []
        try:
            common_friends: MutualFriends = s.get('friends.getMutual', {'access_token': VK_CONFIG['access_token'], 'source_uid': source_uid,
                                                  'target_uid': target_uid, 'count': count, 'v': VK_CONFIG['version'], 'order': order, 'offset': offset}).json()
            return common_friends['response']
        except:
            return []
        
    if not progress:
        progress = tqdm
    
    mutual_friends_list = []

    for uid in progress(target_uids):
        try:
            time.sleep(0.001)
            response = s.get('friends.getMutual', {'access_token': VK_CONFIG['access_token'], 'source_uid': source_uid, 
                                                   'target_uid': uid, 'count': count, 'v': VK_CONFIG['version'], 'order': order, 'offset': offset}).json()
            mutual_friends: MutualFriends = {'id': uid, 'common_friends': response['response'], 'common_count': len(response['response'])}
            mutual_friends_list.append(mutual_friends) 
        except:
            pass

    return mutual_friends_list
