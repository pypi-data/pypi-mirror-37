class PerSecondStats:
    def __init__(self, camera_key, stat_time, num_tracked_people, has_saved_image):
        self.camera_key = camera_key
        self.stat_time = stat_time
        self.num_tracked_people = num_tracked_people
        self.has_saved_image = has_saved_image

    def to_json(self):
        return {
            "CameraKey": self.camera_key,
            "DateTime": self.stat_time.strftime("%Y-%m-%d %H:%M:%S"),
            "NumTrackedPeople": self.num_tracked_people,
            "HasSavedImage": self.has_saved_image
        }
