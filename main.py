from utils import read_video, save_video
from tracker import Tracker

def main():
    video_frames = read_video('Input Videos/08fd33_4.mp4')
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/tracks_stubs.pkl')
    output_video_frames = tracker.draw_annotations(video_frames, tracks) 
    
    save_video(output_video_frames, 'Output Videos/output.avi')
    
if __name__ == '__main__':
    main()