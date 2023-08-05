'''
Copyright 2017 Purdue University

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from multiprocessing import Process
import time
import datetime
import os
import cv2
import numpy as np

class CameraHandler(Process):
    """
    The thread to download snapshots from a single camera.

    Parameters
    ----------
    camera : camera object
        The camera from which snapshots will be taken.

    Attributes
    ----------
    camera : camera object
        The camera from which snapshots will be taken.
    id : int
        The ID of the the camera.
    url : str
        The URL of the camera image stream.
    duration : int
        The duration of downloading the images in seconds.
    interval : int
        The interval between each two successive snapshots.

    """

    # The path of the results directory.

    def __init__(self, cameras, chunk, duration, interval, result_path, remove_after_failure, image_difference_percentage):
        Process.__init__(self)
        self.cameras = cameras
        self.duration = duration
        self.interval = interval
        self.result_path = result_path
        self.chunk = chunk
        self.remove_after_failure = remove_after_failure
        self.image_difference_percentage = image_difference_percentage

    def run(self):
        """
        Download snapshots from the camera, and save locally.
        """
        print("Starting download of {} cameras from chunk {}".format(len(self.cameras),
                                                                     str(self.chunk)))

        # Set the starting timestamp, and process until the end of the duration.
        start_timestamp = time.time()

        while (time.time() - start_timestamp) < self.duration:
            # Set the timestamp of the start of the new loop iteration.
            loop_start_timestamp = time.time()
            # print("Loop Start", time.time())

            # bad_cams is initialized in the while loop so that the array is emptied after
            # each iteration
            bad_cams = []
            x = 0
            for camera in self.cameras:
                print("Process {} Downloading Image {} of {} at time {}".format(self.chunk, x, len(self.cameras), datetime.datetime.now()))
                x = x + 1
                try:
                    # Download the image.
                    frame, _ = camera.get_frame()
                except Exception:
                    if self.remove_after_failure:
                        print("Error retrieving from camera {}.  Marking camera for removal "
                              "from chunk {}.".format(str(camera.id), str(self.chunk)))
                        bad_cams.append(camera)
                else:
                    if frame is not None:
                        # Save the image.
                        frame_timestamp = time.time()
                        cam_directory = os.path.join(self.result_path, str(camera.id))
                        file_name = '{}/{}_{}.png'.format(
                            cam_directory, camera.id,
                            datetime.datetime.fromtimestamp(
                                frame_timestamp).strftime('%Y-%m-%d_%H-%M-%S-%f'))

                        if self.image_difference_percentage:
                            if frame.size != 0 and (type(camera.last_frame) == type(None) or (np.count_nonzero(np.absolute(camera.last_frame - frame)) * 100) / frame.size >= self.image_difference_percentage):
                                cv2.imwrite(file_name, frame)
                                camera.last_frame = frame
                            else:
                                # print("diff_{}".format(np.sum(camera.last_frame - frame) == 0))
                                # cv2.imwrite(file_name, frame)
                                print("Camera frame has not changed for {}.  Will retry after {}sec.".format(str(camera.id), str(self.interval)))
                        else:
                            cv2.imwrite(file_name, frame)
                    else:
                        if self.remove_after_failure:
                            print("Empty frame retrieved from camera {}. Marking camera for removal from chunk {}.".format(str(camera.id), str(self.chunk)))
                            bad_cams.append(camera)
                finally:
                    # These variables are explicitely set to None to encourage the garbage
                    # collector.
                    # Testing showed that without this these variables would persist.
                    frame = None
                    frame_timestamp = None
                    cam_directory = None
                    file_name = None

            # Remove all bad cameras
            if bad_cams and self.remove_after_failure:
                for bad_camera in bad_cams:
                    self.cameras.remove(bad_camera)

            # Sleep until the interval between frames ends.
            time_to_sleep = self.interval - (time.time() - loop_start_timestamp)
            if time_to_sleep > 0:
                print("Process {} going to sleep...".format(self.chunk))
                time.sleep(time_to_sleep)
            else:
                print("Warning: Retrieval time exceeded sleep time for chunk {}. Specified interval"
                      "cannot be met."
                      .format(self.chunk))
