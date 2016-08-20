# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic."""

import endpoints
from protorpc import remote, messages

from models import User, Game
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)

CANCEL_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)

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

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=CANCEL_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/cancel/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='PUT')
    def cancel_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            game.cancel_game()
            return game.to_form('Game has been cancelled!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')

        game.board[request.position] = game.current_player

        check_for_winner = self._check_for_winner(game.board)

        if check_for_winner:
            game.end_game()
            return game.to_form(' %s wins!' % game.current_player)
        else:
            game.current_player = self._switch_player(game)
            game.put()
            return game.to_form('Next move')


    def _switch_player(self, game):
        if(game.current_player == 'PLAYER_X') :
            game.current_player = 'PLAYER_O'
        else:
            game.current_player = 'PLAYER_X'
        return game.current_player

    def _we_have_a_winner(self, a,b,c, board):

        if (str(board[a]) == str(board[b])) & (str(board[b]) == str(board[c])) & ((str(board[a]) != str('')) | (str(board[b]) != str('')) | (str(board[c]) != str(''))):
            return True

        else:
            return False

    def _check_for_winner(self, board):
        # check rows
        a = 0
        b = 1
        c = 2
        while (c < len(board)):
            if (self._we_have_a_winner(a,b,c,board)):
                return True
            a += 3
            b += 3
            c += 3

        # check columns
        a = 0
        b = 3
        c = 6
        while (c < len(board)):
            if (self._we_have_a_winner(a,b,c,board)):
                return True
            a += 1
            b += 1
            c += 1

        # check diagonal right
        if (self._we_have_a_winner(0,4,8,board)):
            return True

        # check diagonal left
        if (self._we_have_a_winner(2,4,6,board)):
            return True

        # check if it's a draw...


api = endpoints.api_server([TicTacToeApi])
