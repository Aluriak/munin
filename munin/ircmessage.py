"""
Definition of an IRC message as instance of IRCMessage object.

"""


class IRCMessage:

    def __init__(self, all_message, author):
        self.author = author
        self.all = all_message
        # get target of msg and msg itself
        if ':' in all_message and all_message.find(':') < all_message.find(' '):
            self.dest, self.message = all_message.split(':', 1)
            assert (self.dest + ':' + self.message) == all_message
        else:  # no explicit recipient
            self.dest, self.message = None, all_message

    @property
    def hasdest(self):
        return self.dest is not None

    def __iter__(self):
        return iter(self.all)

    def __str__(self):
        return self.author + '|' + self.all
