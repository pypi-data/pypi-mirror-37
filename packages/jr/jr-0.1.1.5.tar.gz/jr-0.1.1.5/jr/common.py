# -*- coding: utf-8 -*-


class Value(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


class Node(object):
    def __init__(self, name, member, global_member=None):
        self.name = name
        self.member = Member(member)
        if not global_member:
            global_member = dict()
        self.global_member = Member(global_member)

    def __str__(self):
        return self.name


class Member(object):
    def __init__(self, member):
        for k, v in member.items():
            setattr(self, k, v)
