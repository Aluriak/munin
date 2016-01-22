"""
Counting votes of users about a poll and a predefined set of answer.

"""
import re
from collections import Counter

from munin.plugin import Plugin


class VoteCounter(Plugin):
    """
    Simple Plugin application.
    Repeat last sentence of user that correct it by using a regex.
    example:
        lucas| bot: poll "Who is the best" "me;lucas;no one" "lucas;michel;gerard"
    """
    REGEX     = re.compile(r"(.*)")
    REGEX_POLL = re.compile(r"""\s*poll\s*"([^"]+)"\s*"([^"]+)"\s*"([^"]+)"\s*""")
    REGEX_VOTE = re.compile(r"""\s*vote\s*([0-9]+)\s*""")
    REGEX_ENDS = re.compile(r"""\s*end\s*poll\s*""")
    REGEX_RESM = re.compile(r"""\s*resume\s*poll\s*""")
    REGEX_PRNT = re.compile(r"""\s*poll\s*votes?\s*""")

    def __init__(self, bot):
        super().__init__(bot)
        self.poll = None

    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (unused),
        according to regex matchs (used) and sudo mode (unused)"""
        results = ''
        author = message.author

        regres_poll = VoteCounter.REGEX_POLL.fullmatch(matched_groups[0])
        regres_vote = VoteCounter.REGEX_VOTE.fullmatch(matched_groups[0])
        regres_ends = VoteCounter.REGEX_ENDS.fullmatch(matched_groups[0])
        regres_resm = VoteCounter.REGEX_RESM.fullmatch(matched_groups[0])
        regres_prnt = VoteCounter.REGEX_PRNT.fullmatch(matched_groups[0])
        print('POLL:', regres_poll, regres_vote, regres_ends, regres_resm, regres_prnt)
        if regres_poll:
            groups = regres_poll.groups()
            self.poll    = str(groups[0])
            self.answers = tuple(groups[1].split(';'))
            self.voters  = {voter: None for voter in groups[2].split(';')}
            results += "Let's starts a new poll: "
            results += self.resume
        elif regres_vote and self.poll and author in self.voters:
            # author vote for parsed answer
            vote = int(regres_vote.groups()[0])
            if 0 <= vote < len(self.answers):
                self.voters[author] = vote
                print('VOTING:', author, 'said', vote)
        elif regres_ends and sudo and self.poll:
            results += 'poll is closed. Final results: ' + self.votes
            self.poll, self.voters, self.answers = None, None, None
        elif regres_resm and sudo:
            results += self.resume
        elif regres_prnt and sudo:
            results += self.votes

        return results


    @property
    def resume(self):
        print('DEBUG:', self.voters)
        nb_answer = len(self.answers)
        given_votes  = (voter for voter, vote in self.voters.items() if vote is not None)
        waited_votes = (voter for voter, vote in self.voters.items() if vote is     None)
        return '\n'.join((
            self.poll,
            '\n'.join(
                '    ' + str(idx).rjust(1 + nb_answer // 10) + ': ' + answer
                for idx, answer in enumerate(self.answers)
            ),
            'Voters:',
            '    Vote given   : ' + ', '.join(given_votes),
            '    Vote expected: ' + ', '.join(waited_votes),
        )) + '\n'

    @property
    def votes(self):
        max_answer_size = max(len(answer) for answer in self.answers)
        votes           = Counter((vote for vote in self.voters.values()))
        return '\n'.join((
            'Votes for the poll ' + self.poll + ':',
            '\n'.join(
                '\t' + answer.rjust(max_answer_size) + ':' + str(votes[idx])
                for idx, answer in enumerate(self.answers)
            ),
        )) + '\n'

    @property
    def help(self):
        return """VOTE COUNTER: usage example: «bot: poll "Who is the best" "me;lucas;no one" "lucas;michel;gerard"» """

    @property
    def only_on_explicit_dest(self):
        return False  # react on all messages
