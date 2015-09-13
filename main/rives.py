__author__ = 'Gangeshwar'

from rivescript import RiveScript

rs = RiveScript()
# rs.load_directory('rep_src')
rs.load_file("rep_src/begin.rs")
rs.load_file("rep_src/config.rs")
rs.load_file("rep_src/English.rs")
rs.load_file("rep_src/objects.rs")
rs.load_file("rep_src/replies.rs")
rs.load_file("rep_src/English/EnglishAdj.rsl")
rs.load_file("rep_src/English/EnglishNouns.rsl")
rs.load_file("rep_src/English/EnglishVerbs.rsl")
rs.sort_replies()

"""This is a bare minimal example for how to write your own RiveScript bot!

For a more full-fledged example, try running: `python rivescript brain`
This will run the built-in Interactive Mode of the RiveScript library. It has
some more advanced features like supporting JSON for communication with the
bot. See `python rivescript --help` for more info.

example.py is just a simple script that loads the RiveScript documents from
the 'brain/' folder, and lets you chat with the bot.

Type /quit when you're done to exit this example.
"""


def reply(msg):
    return rs.reply("user", msg)

# vim:expandtab
