import sys
sys.path.append('../')
from utils import get_center_bbox, measure_distance

class PlayerBallAssignment:
    def __init__(self,):
        self.max_player_ball_distance = 70
        
    def assign_ball_to_player(self, players, ball_bbox):
        ball_position = get_center_bbox(ball_bbox)
        minimum_distance = 99999
        assigned_player = -1
        
        for player_id, player in players.items():
            player_bbox = player['bbox']
            distance_left_foot = measure_distance((player_bbox[0], player_bbox[-1]), ball_position)
            distance_right_foot = measure_distance((player_bbox[2], player_bbox[-1]), ball_position)
            distance = min(distance_left_foot, distance_right_foot)
            
            if distance < minimum_distance:
                minimum_distance = distance
                assigned_player = player_id
                
        return assigned_player
        