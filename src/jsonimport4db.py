from sqlalchemy import Column, String, Integer, DateTime, Boolean
import os
import json
from collections import OrderedDict

import pandas as pd

from mo9mo9db.dbtables import Selfintroduction
from mo9mo9db.dbsession import get_db_engine

studymembers=[]
session = Selfintroduction.session()
engine = get_db_engine()

with open("after-introduction.json", "r", encoding="utf-8") as f:
    update_json = json.load(f)

pd_j = pd.json_normalize(update_json["data"])

for i in pd_j.itertuples():
    studymembers.append(Selfintroduction(
        guild_id = "603582455756095488",
        member_id = i.id,
        nickname = i.name,
        gender = i.gender,
        twitter_id = i.twitterID,
        specialty = i.specialty,
        before_study = i.learned,
        after_study = i.studyingnow,
        sendmsg_id = i.msgID,
    ))
session.bulk_save_objects(studymembers)
session.commit()