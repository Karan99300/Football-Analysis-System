import numpy as np
import cv2

class PerspectiveTransformation:
    def __init__(self,):
        #lengths of the rectangles on a football pitch
        rectangle_width = 68
        rectangle_length = 23.32
        
        self.pixel_vertices = np.array([[110, 1035], [265, 275], [910, 260], [1640, 915]]).astype(np.float32)
        self.target_vertices = np.array([[0, rectangle_width], [0, 0], [rectangle_length, 0], [rectangle_length, rectangle_width]]).astype(np.float32)
        
        self.perspective_transformation = cv2.getPerspectiveTransform(self.pixel_vertices, self.target_vertices)
        
    def transform_point(self, point):
        p = (int(point[0]), int(point[1]))
        is_inside = cv2.pointPolygonTest(self.pixel_vertices, p, False) >= 0
        if not is_inside:
            return None
        
        reshaped_point = point.reshape(-1,1,2).astype(np.float32)
        transformed_point = cv2.perspectiveTransform(reshaped_point, self.perspective_transformation)
        return transformed_point.reshape(-1,2)
        
    def apply_transform_to_tracks(self, tracks):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = np.array(track_info['position_adjusted'])
                    position_transformed = self.transform_point(position)
                    if position_transformed is not None:
                        position_transformed = position_transformed.squeeze().tolist()
                    tracks[object][frame_num][track_id]['position_transformed'] = position_transformed
                    
                    
        
        