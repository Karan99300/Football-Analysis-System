from utils import read_video, save_video
from tracker import Tracker
from team_assignment import TeamAssignment
from player_ball_assignment import PlayerBallAssignment
import cv2
import numpy as np

def main():
    video_frames = read_video('Input Videos/08fd33_4.mp4')
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/tracks_stubs.pkl')
    
    tracks['ball'] = tracker.interpolate_ball_positions(tracks['ball'])
    
    team_assignment = TeamAssignment()
    team_assignment.assign_team_color(video_frames[0], tracks['players'][0])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assignment.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assignment.team_colors[team]
    
    player_assignment = PlayerBallAssignment()
    team_ball_control = []
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assignment.assign_ball_to_player(player_track, ball_bbox)
        
        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1])
            
    team_ball_control = np.array(team_ball_control)
            
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control) 
    
    save_video(output_video_frames, 'Output Videos/output.avi')
    
if __name__ == '__main__':
    main()