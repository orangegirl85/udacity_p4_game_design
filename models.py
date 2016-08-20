"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

from google.appengine.ext import ndb
from protorpc import messages

class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

class Game(ndb.Model):
    """Game object"""
    user1 = ndb.KeyProperty(required=True, kind='User')
    user2 = ndb.KeyProperty(required=True, kind='User')
    game_over = ndb.BooleanProperty(required=True, default=False)
    current_player = ndb.StringProperty(default='PLAYER_X')
    board = ndb.StringProperty(repeated=True)

    @classmethod
    def new_game(cls, user1, user2):
        """Creates and returns a new game"""
        game = Game(user1=user1,
                    user2=user2,
                    game_over=False,
                    current_player='PLAYER_X',
                    board=['', '', '', '', '', '', '', '', ''])
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name1 = self.user1.get().name
        form.user_name2 = self.user2.get().name
        form.current_player = self.current_player
        form.board = self.board
        form.game_over = self.game_over
        form.message = message
        return form


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    game_over = messages.BooleanField(2, required=True)
    message = messages.StringField(3, required=True)
    user_name1 = messages.StringField(4, required=True)
    user_name2 = messages.StringField(5, required=True)
    current_player = messages.StringField(6, required=True)
    board = messages.StringField(7, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name1 = messages.StringField(1, required=True)
    user_name2 = messages.StringField(2, required=True)
