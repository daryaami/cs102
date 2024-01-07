from datetime import datetime
import statistics
import typing as tp
from datetime import date

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    resp = get_friends(user_id, fields=['bdate'])
    today = date.today()
    ages = []

    for friend in resp.items:
        try:
            bdate = datetime.strptime(friend['bdate'], '%d.%m.%Y')
            age = today.year - bdate.year - \
                ((today.month, today.day) < (bdate.month, bdate.day))
            ages.append(age)
        except:
            pass
        
    try:
        median_age = statistics.median(ages)
    except:
        return None
    return median_age
