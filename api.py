# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic."""

import endpoints
from protorpc import remote, messages

from models import User, Game
from models import StringMessage, NewGameForm, GameForm

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))

@endpoints.api(name='tic_tac_toe', version='v1')
class TicTacToeApi(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))


    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user1 = User.query(User.name == request.user_name1).get()
        if not user1:
            raise endpoints.NotFoundException(
                    'A User with: %s name does not exist!' % request.user_name1 )

        user2 = User.query(User.name == request.user_name2).get()
        if not user2:
            raise endpoints.NotFoundException(
                    'A User with: %s name does not exist!' % request.user_name2)

        game = Game.new_game(user1.key, user2.key)

        return game.to_form('Good luck playing Tic Tac Toe!')

api = endpoints.api_server([TicTacToeApi])
