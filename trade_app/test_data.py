fake_league = {
    'id' : 10,
    'settings' : {
        'name' : 'Test League'
    },
}

fake_player = {
        'id' : 11,
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
    }

fake_team = {
    'id' : 10,
    'name' : 'Test Team',
    'roster' : [fake_player]
}