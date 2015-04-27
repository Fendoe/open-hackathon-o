# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------------
# Copyright (c) Microsoft Open Technologies (Shanghai) Co. Ltd.  All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------------

import sys

sys.path.append("..")
from hackathon.database.models import Hackathon, User, UserEmail, UserHackathonRel
from hackathon.database import db_adapter
from hackathon.enum import RGStatus
from hackathon.hackathon_response import *


class HackathonManager():
    def __init__(self, db):
        self.db = db

    def get_hackathon_by_name_or_id(self, hack_id=None, name=None):
        if hack_id is None:
            return self.get_hackathon_by_name(name)
        return self.get_hackathon_by_id(hack_id)

    def get_hackathon_by_name(self, name):
        return self.db.find_first_object_by(Hackathon, name=name)

    def get_hackathon_by_id(self, hackathon_id):
        return self.db.find_first_object_by(Hackathon, id=hackathon_id)

    def get_hackathon_stat(self, hackathon_id):
        hackathon = self.get_hackathon_by_id(hackathon_id)
        if hackathon is None:
            return not_found("hackathon not found")

        reg_list = hackathon.registers.filter_by(status=RGStatus.AUDIT_PASSED).all()

        reg_count = len(reg_list)
        stat = {
            "total": reg_count,
            "hid": hackathon_id,
            "online": 0,
            "offline": reg_count
        }

        if reg_count > 0:
            user_id_list = [r.user_id for r in reg_list]
            user_id_online = self.db.count(User, (User.id.in_(user_id_list) & (User.online == 1)))
            stat["online"] = user_id_online
            stat["offline"] = reg_count - user_id_online

        return stat

    def get_hackathon_list(self, name=None):
        if name is not None:
            return db_adapter.find_first_object_by(Hackathon, name=name).dic()
        return map(lambda u: u.dic(), db_adapter.find_all_objects(Hackathon))


hack_manager = HackathonManager(db_adapter)