import os
import nltk
from rivescript import RiveScript

__author__ = 'Gangeshwar'


class bot():
    """This is a bare minimal example for how to write your own RiveScript bot!

For a more full-fledged example, try running: `python rivescript brain`
This will run the built-in Interactive Mode of the RiveScript library. It has
some more advanced features like supporting JSON for communication with the
bot. See `python rivescript --help` for more info.

example.py is just a simple script that loads the RiveScript documents from
the 'brain/' folder, and lets you chat with the bot.

Type /quit when you're done to exit this example.
"""

    def __init__(self):
        self.currentOperation = None
        self.rs = RiveScript()
        self.rs.load_directory(os.path.dirname(__file__) + "/rep_src")
        self.rs.sort_replies()

    def sanitizeUserQuery(self, userQuery):
        return userQuery

    def identifyOperation(self, userQuery):
        """
        function identifyOperation(string: userQuery)
        Output: ([keywords_in_input], [action_in_input])
        """
        userQuery = self.sanitizeUserQuery(userQuery)
        queryTokens = nltk.word_tokenize(userQuery)
        pos = nltk.pos_tag(queryTokens)
        keywords = []
        verbs = []
        adjective = []
        for w in pos:
            if w[1] == 'NN' or w[1] == 'NNP':
                keywords.append(str(w[0]))
            if w[1] == 'VB' or w[1] == 'VBD' or w[1] == 'VBN':
                verbs.append(w[0])
            if w[1] == 'JJ':
                adjective.append(w[0])

        # print(str(keywords).rsplit() + " " + str(verbs).rsplit() + " " + str(adjective).rsplit())
        return (keywords, verbs, adjective)

    def reply(self, user, msg):
        # t = self.identifyOperation(msg)
        # print(' '.join(t[0] + t[1] + t[2]))
        return self.rs.reply(user, msg)
