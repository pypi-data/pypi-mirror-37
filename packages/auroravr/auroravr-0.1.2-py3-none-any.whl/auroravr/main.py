import boto3

client = boto3.client('gamelift')


def search(alias_id):
    response = client.search_game_sessions(AliasId=alias_id)
    return response['GameSessions']


def create(alias_id, html, max_player):
    response = client.create_game_session(
        AliasId=alias_id,
        MaximumPlayerSessionCount=max_player,
        Name=html
    )
    return response['GameSession']


def enter(room_id, player_id):
    response = client.create_player_session(
        GameSessionId=room_id,
        PlayerId=player_id
    )
    return response
