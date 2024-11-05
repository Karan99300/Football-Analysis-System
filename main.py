from utils import read_video, save_video
from tracker import Tracker
from team_assignment import TeamAssignment
import cv2

def main():
    video_frames = read_video('Input Videos/08fd33_4.mp4')
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/tracks_stubs.pkl')
    
    team_assignment = TeamAssignment()
    team_assignment.assign_team_color(video_frames[0], tracks['players'][0])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assignment.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assignment.team_colors[team]
    
    output_video_frames = tracker.draw_annotations(video_frames, tracks) 
    
    save_video(output_video_frames, 'Output Videos/output.avi')
    
if __name__ == '__main__':
    main()