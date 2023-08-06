import boto3

client = boto3.client('gamelift')


def search():
    response = client.search_game_sessions(AliasId='alias-784566b2-47e5-43e6-b19a-3271e09efd1f')
    return response['GameSessions']


def create(html):
    response = client.create_game_session(
        AliasId='alias-784566b2-47e5-43e6-b19a-3271e09efd1f',
        MaximumPlayerSessionCount=10,
        Name=html
    )
    return response['GameSession']


def enter(room_arn, player_id):
    response = client.create_player_session(
        GameSessionId=room_arn,
        PlayerId=player_id
    )
    return response
