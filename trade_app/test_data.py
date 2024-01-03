from box import Box

fake_player = Box({
        'playerId' : 11,
        'name' : 'Test Player Name',
        'position' : 'PG',
        'stats' : {
            '2024_total' : {
                'avg' : {
                    'PTS': 15.0,
                    'BLK': 1.0,
                    'STL': 1.0,
                    'AST': 6.0,
                    'OREB': 2.0,
                    'DREB': 3.0,
                    'TO': 2.0,
                    'FGM': 80,
                    'FTM': 90,
                    '3PTM': 7, 
                    'FGA': 100, 
                    '3PTA': 10,
                    'FTA': 100
                }
            }
        }
    })

fake_player_2 = Box({
        'playerId' : 12,
        'name' : 'Test Player Name 2',
        'position' : 'C',
        'stats' : {
            '2024_total' : {
                'avg' : {
                    'PTS': 5.0,
                    'BLK': 3.0,
                    'STL': 3.0,
                    'AST': 2.0,
                    'OREB': 4.0,
                    'DREB': 5.0,
                    'TO': 1.0,
                    'FGM': 60,
                    'FTM': 80,
                    '3PTM': 3.0, 
                    'FGA': 100, 
                    '3PTA': 10,
                    'FTA': 100
                }
            }
        }
    })

fake_player_3 = Box({
        'playerId' : 13,
        'name' : 'Test Player Name 3',
        'position' : 'SG',
        'stats' : {
            '2024_total' : {
                'avg' : {
                    'PTS': 2.0,
                    'BLK': 1.0,
                    'STL': 1.0,
                    'AST': 3.0,
                    'OREB': 1.0,
                    'DREB': 3.0,
                    'TO': 1.0,
                    'FGM': 70,
                    'FTM': 85,
                    '3PTM': 4.0, 
                    'FGA': 100, 
                    '3PTA': 10,
                    'FTA': 100
                }
            }
        }
    })

fake_player_4 = Box({
        'playerId' : 14,
        'name' : 'Test Player Name 4',
        'position' : 'PF',
        'stats' : {
            '2024_total' : {
                'avg' : {
                    'PTS': 3.0,
                    'BLK': 2.0,
                    'STL': 1.0,
                    'AST': 4.0,
                    'OREB': 6.0,
                    'DREB': 8.0,
                    'TO': 3.0,
                    'FGM': 50,
                    'FTM': 50,
                    '3PTM': 1.0, 
                    'FGA': 100, 
                    '3PTA': 10,
                    'FTA': 100
                }
            }
        }
    })

fake_team = Box({
    'team_id' : 100,
    'team_name' : 'Test Team',
    'roster' : [fake_player, fake_player_2]
})

fake_team_2 = Box({
    'team_id' : 900,
    'team_name' : 'Test Team 2',
    'roster' : [fake_player_3, fake_player_4]
})

fake_league = Box({
    'league_id' : 10,
    'year' : 2024,
    'settings' : {
        'name' : 'Test League'
    },
    'teams' : [fake_team, fake_team_2]
})