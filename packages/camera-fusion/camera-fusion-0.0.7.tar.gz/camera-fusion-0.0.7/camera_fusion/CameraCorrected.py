"""OpenCV Camera class for lens correction with Charuco calibration."""

from .Camera import Camera

from pathlib import Path
import numpy as np
from threading import Event, Thread
import time
import subprocess
import os
import sys
try:
    import cv2
    from cv2 import aruco
except ImportError:
    raise ImportError('ERROR opencv-contrib-python must be installed!')

# TODO: implement height transform correction
# https://github.com/O-C-R/maproom-robots/tree/master/skycam

# TODO: AR example
# https://github.com/avmeer/ComputerVisionAugmentedReality
# Averaging
# ○ ArUco tags are hard to pick out perfectly each time
# ○ Position of the marker is noisy and subsequently the models would shake
# ○ Averaging the last three position matrices helped to stabilize the models.


def input_float(prompt=''):
    """Ask for a human float input.

    Args:
        prompt (string): Text to prompt as input.
    """
    # try:
    #     return raw_input(prompt)
    # except NameError:
    #     return input(prompt)

    while True:
        try:
            float_input = float(input(prompt))
        except ValueError:
            print('Please enter a float.\n')
            continue
        else:
            break
    return float_input


class CameraCorrected(Camera):
    """CameraCorrected class used to setup and use a camera with lens correction.

    Attributes:
        aruco_dict_num (int): ChAruco dictionnary number used for calibr.
        board (CharucoBoard): ChAruco board object used for calibration.
        cap (VideoCapture): OpenCV VideoCapture element.
        cam_id (string): Camera or V4L id (ex: /dev/video0 /dev/v4l_by_id/...).
        charuco_marker_size (float): black square length on the printed board.
        charuco_square_length (float): Aruco marker length on the print.
        focus (float): Camera focus value for camera which supports focusing.
        height (int): Camera frame height in pixels.
        width (int): Camera frame width in pixels.
        camera_matrix (OpenCV matrix): OpenCV camera correction matrix.
        dist_coeffs (OpenCV matrix): OpenCV distance correction coefficients.
        corners (list): List of detected corners positions as a buffer.
        ids (list): List of detected corners ids as a buffer.
        board_post (PostureBuffer): Buffer to filter the posture of the board.
        settings (list): List of OpenCV VideoCapture (v4l) settings.
        thread_ready (Event): Thread is ready Event.
        thread (threading.Thread): VideoCapture reading thread.
        t0 (time.time): Time counter buffer.

    """

    def __init__(self, cam_id, aruco_dict_num, focus=None, vertical_flip=None,
                 settings=None):
        """Initialize the CameraCorrected object variables.

        Args:
            cam_id (string): Camera or V4L id.
            aruco_dict_num (int): ChAruco dictionnary number used for calibr.
            vertical_flip (bool): Trigger vertical frame flipping.
            focus (float): Camera focus value for camera which supports focus.
            settings (list): list of tuple with specific camera settings.
        """
        Camera.__init__(self, cam_id, vertical_flip, settings)

        self.focus = focus

        # Corners points and identifiers buffers
        self.aruco_dict_num = aruco_dict_num
        self.corners = None
        self.ids = None

        # Moving/Rolling average posture filtering
        # TODO: Low pass filtering on translation and rotation
        self.board_post = PostureBuffer()

        # Parameter files folder
        if not Path('./data').exists():
            os.makedirs('./data')

    def initialize(self):
        """Set up camera and launch the calibration routine."""
        self._setup()

        # Camera correction
        self.calibrate_camera_correction()

        # Start the VideoCapture read() thread
        self.stop = False
        self.start_camera_thread()
        self.thread_ready.wait()

        # Quick test
        self.test_camera()
        print('Corrected camera %s initialization done!\n' % self.cam_id)

    def calibrate_camera_correction(self):
        """Calibrate the camera lens correction."""
        # Hints:
        # https://github.com/opencv/opencv/blob/master/samples/python/calibrate.py
        # https://longervision.github.io/2017/03/16/OpenCV/opencv-internal-calibration-chessboard/
        # http://www.peterklemperer.com/blog/2017/10/29/opencv-charuco-camera-calibration/
        # http://www.morethantechnical.com/2017/11/17/projector-camera-calibration-the-easy-way/
        # https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html

        defaultConfig_path = Path('./data/defaultConfig.xml')
        if defaultConfig_path.exists():
            print('  Found defaultConfig.xml.\nCAUTION: be sure settings in d'
                  'efaultConfig.xml match the current hardware configuration.')
            default_config = cv2.FileStorage(
                str(defaultConfig_path), cv2.FILE_STORAGE_READ)
            self.aruco_dict_num = int(
                default_config.getNode('charuco_dict').real())
            self.charuco_square_length = default_config.getNode(
                'charuco_square_lenght').real()  # ARGH, spelling mistake!
            self.charuco_marker_size = default_config.getNode(
                'charuco_marker_size').real()
            self.width = int(default_config.getNode(
                'camera_resolution').at(0).real())
            self.height = int(default_config.getNode(
                'camera_resolution').at(1).real())
            default_config.release()
        else:
            self.write_defaultConfig()
        aruco_dict = cv2.aruco.Dictionary_get(self.aruco_dict_num)

        # Create specific camera calibration if no one already exists
        # using the opencv_interactive-calibration program.
        cameraParameters_path = Path(
            './data/cameraParameters_%s.xml' % self.cam_id)
        if not cameraParameters_path.exists():
            print('\nStarting the camera id%s lens calibration.' % self.cam_id)
            self.cap.release()  # Release VideoCapture before CLI usage
            subprocess.call(
                ['opencv_interactive-calibration', '-d=0.25', '-h=7', '-w=5',
                 '-sz=%f' % self.charuco_square_length, '--t=charuco',
                 '-pf=' + str(defaultConfig_path),
                 '-ci=' + str(self.cam_id),
                 '-of=' + str(cameraParameters_path),
                 '-flip=' + str(self.vertical_flip).lower()])

            self.cap = cv2.VideoCapture(self.cam_id, cv2.CAP_V4L2)
            self.set_camera_settings()  # Re-set camera settings

        # Load the camera calibration file.
        if cameraParameters_path.exists():
            print('  Found cameraParameters_%s.xml' % self.cam_id)
            calibration_file = cv2.FileStorage(
                str(cameraParameters_path), cv2.FILE_STORAGE_READ)
            self.camera_matrix = calibration_file.getNode('cameraMatrix').mat()
            self.dist_coeffs = calibration_file.getNode('dist_coeffs').mat()
            self.width = int(calibration_file.getNode(
                'cameraResolution').at(0).real())
            self.height = int(calibration_file.getNode(
                'cameraResolution').at(1).real())

            if calibration_file.getNode('focus').isReal():  # If focus val
                self.focus = float(calibration_file.getNode('focus').real())
                self.set_focus(self.focus * 50)

            # Specific Fish-Eye parameters
            # self.r = calibrationParams.getNode("R").mat()
            # self.new_camera_matrix = calibrationParams.getNode(
            #     "newCameraMatrix").mat()
            calibration_file.release()
        else:
            raise ValueError(
                "cameraParameters_%s.xml not found!\n\t"
                "Please finish the calibration and press 's' to save to file."
                % self.cam_id)

        self.board = cv2.aruco.CharucoBoard_create(
                5, 7, self.charuco_square_length, self.charuco_marker_size,
                aruco_dict)
        print('Camera %s calibration correction done!' % self.cam_id)

    def detect_markers(self):
        """Detect ChAruco markers.

        Returns:
            frame (OpenCV Mat): A frame read from the VideoCapture method.
            corners (Numpy array): list of corners 2D coordinates.
            ids (Numpy array): list of detected marker identifiers.

        """
        parameters = cv2.aruco.DetectorParameters_create()
        frame = self.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rej = cv2.aruco.detectMarkers(
            gray, self.board.dictionary, parameters=parameters)
        corners, ids, rej, recov = cv2.aruco.refineDetectedMarkers(
            gray, self.board, corners, ids, rej,
            cameraMatrix=self.camera_matrix, distCoeffs=self.dist_coeffs)
        return frame, corners, ids

    def estimate_board_posture(self, frame=None, corners=None, ids=None):
        """Estimate ChAruco board posture.

        Arguments:
            frame (OpenCV Mat): A frame read from the VideoCapture method.
            corners (Numpy array): list of corners 2D coordinates.
            ids (Numpy array): list of detected marker identifiers.

        Return:
            frame (OpenCV Mat): Frame with the board posture drawn
        """
        # If we do not already have detect markers:
        if frame is None:
            frame, corners, ids = self.detect_markers()
        if ids is None:  # No detected marker
            frame = self.draw_text(frame, 'No ChAruco marker detected !')
            # time.sleep(0.1)  # Sleep to give the time to move the panel
        else:  # if there is at least one marker detected
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Draw axis for the global board
            retval, cha_corns, cha_ids = cv2.aruco.interpolateCornersCharuco(
                corners, ids, gray, self.board,
                cameraMatrix=self.camera_matrix, distCoeffs=self.dist_coeffs)

            if retval:
                frame_with_board = cv2.aruco.drawDetectedCornersCharuco(
                    frame, cha_corns, cha_ids, (0, 255, 0))
                # Posture estimation of the global ChAruco board
                retval, rvecs, tvecs = cv2.aruco.estimatePoseCharucoBoard(
                    cha_corns, cha_ids, self.board,
                    self.camera_matrix, self.dist_coeffs)

                if retval is True:
                    rvecs, tvecs = self.board_post.update(rvecs, tvecs)

                    frame = cv2.aruco.drawAxis(
                        frame_with_board, self.camera_matrix, self.dist_coeffs,
                        rvecs, tvecs, 4 * self.charuco_square_length)
                else:
                    frame = self.draw_text(
                        frame,  'Not enough Charuco markers detected.')
            else:
                frame = self.draw_text(
                    frame, 'Not enough resolution. Board is too far.')
        return frame

    def estimate_markers_posture(self, frame=None, corners=None, ids=None):
        """Estimate ChAruco markers posture.

        Arguments:
            frame (OpenCV Mat): A frame read from the VideoCapture method.
            corners (Numpy array): list of corners 2D coordinates.
            ids (Numpy array): list of detected marker identifiers.

        Return:
            frame (OpenCV Mat): Frame with all detected markers posture drawn.

        """
        # If we do not already have detect markers:
        if frame is None:
            frame, corners, ids = self.detect_markers()

        if ids is None:  # No detected marker
            frame = self.draw_text(frame, 'No ChAruco marker detected !')
            # time.sleep(0.1)  # Sleep to give the time to move the panel
        else:  # if there is at least one marker detected
            # Draw each detected marker
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(
                corners, self.charuco_square_length,
                self.camera_matrix, self.dist_coeffs)
            # Draw axis for each marker
            for rvec, tvec in zip(rvecs, tvecs):
                frame = cv2.aruco.drawAxis(
                    frame, self.camera_matrix, self.dist_coeffs,
                    rvec, tvec, self.charuco_square_length)
        return frame

    def estimate_board_and_markers_posture(self):
        """Estimate posture of ChAruco markers and posture of global board.

        Return:
            frame (OpenCV Mat): Frame with the board and markers postures.

        """
        frame, corners, ids = self.detect_markers()
        frame = self.estimate_markers_posture(frame, corners, ids)
        frame = self.estimate_board_posture(frame, corners, ids)
        return frame

    # def py_charuco_camera_calibration(self):
    #     """TODO: camera calibration with Python."""
    #     parameters = cv2.aruco.DetectorParameters_create()
    #     corners_list = []
    #     ids_list = []
    #     print('Move the charuco board in front of the', self.cam_id)
    #     while len(corners_list) < 50:
    #         frame = self.read()
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         corners, ids, rej = cv2.aruco.detectMarkers(
    #             gray, dictionary=aruco_dict, parameters=parameters)
    #         corners, ids, rej, recovered = cv2.aruco.refineDetectedMarkers(
    #             gray, cv2.aruco, corners, ids, rej,
    #             cameraMatrix=self.camera_matrix, distCoeffs=self.dist_coef)
    #         if corners is None or len(corners) == 0:
    #             print('No ChAruco corner detected!')
    #             continue
    #         ret, corners, ids = cv2.aruco.interpolateCornersCharuco(
    #             corners, ids, gray, cb)
    #         corners_list.append(corners)
    #         ids_list.append(ids)
    #         time.sleep(0.1)  # Sleep to give the time to move the panel

    #     print('Enough frames for %s calibration!' % self.cam_id)
    #     # Calibrate camera
    #     ret, K, dist_coef, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(
    #         corners_list, ids_list, cv2.aruco, (w, h), K,
    #         dist_coef, flags=cv2.CALIB_USE_INTRINSIC_GUESS)
    #     print('camera calib mat after\n%s' % K)
    #     print('camera dist_coef %s' % dist_coef.T)
    #     print('calibration reproj err %s' % ret)

    #     distCoeffsInit = np.zeros((5, 1))
    #     flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)  # noqa
    #     # flags = (cv2.CALIB_RATIONAL_MODEL)
    #     (ret, camera_matrix, distortion_coefficients0,
    #      rotation_vectors, translation_vectors,
    #      stdDeviationsIntrinsics, stdDeviationsExtrinsics,
    #      perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
    #      charucoCorners=allCorners, charucoIds=allIds, board=board,
    #      imageSize=imsize, cameraMatrix=cameraMatrixInit,
    #      distCoeffs=distCoeffsInit, flags=flags, criteria=(
    #         cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    def read_undistort(self):
        """Read an undistored camera frame."""
        return cv2.undistort(
            src=self.read(), cameraMatrix=self.camera_matrix,
            distCoeffs=self.dist_coeffs)

    def save_focus(self):
        """Save the camera focus value to the cameraParameters.xml file."""
        if self.focus:
            cameraParameters_path = Path(
                './data/cameraParameters_%s.xml' % self.cam_id)
            self.write_append_to_FileStorage(
                str(cameraParameters_path),
                string='<focus>%f</focus>\n' % self.focus)

    def set_focus(self, focus):
        """Set camera focus."""
        self.cap.set(28, focus * 0.02)  # CV_CAP_PROP_FOCUS
        # min: 0.0 (infinity), max: 1.0 (1cm), increment:0.02 for C525 & C920
        self.focus = self.cap.get(28)
        print('Camera %d | Focus set:%f' % (self.cam_id, self.focus))

    def show_focus_window(self):
        """Show a window with a focus slider."""
        cv2.namedWindow('Focus', cv2.WINDOW_FREERATIO)
        cv2.resizeWindow('Focus', 600, 30)
        focus = self.focus
        cv2.createTrackbar('Camera %d focus' % self.cam_id, 'Focus', 0, 20,
                           self.set_focus)
        if focus:
            cv2.setTrackbarPos('Camera %d focus' % self.cam_id, 'Focus',
                               int(focus * 50))

    def write_append_to_FileStorage(self, str_path, string):
        """Append a string to a .xml file opened with cv2.FileStorage.

        Args:
            str_path (str): the file path to append.
            string (str): the string to append.

        """
        f = open(str_path, 'r+')
        ln = f.readline()
        while ln != '</opencv_storage>\n':
            ln = f.readline()
        f.seek(f.tell() - 18)
        f.write(string)
        f.write('</opencv_storage>\n')
        f.close()

    def write_defaultConfig(self):
        """Write defaultConfig.xml with the ChAruco specific parameters."""
        print('\n')
        self.charuco_square_length = input_float(
                    'Enter the black square length in cm: ')
        self.charuco_marker_size = input_float(
                    'Enter the Aruco marker length in cm: ')
        defaultConfig_path = Path('./data/defaultConfig.xml')
        file = cv2.FileStorage(
            str(defaultConfig_path), cv2.FILE_STORAGE_WRITE)
        file.write('charuco_dict', self.aruco_dict_num)
        file.write('charuco_square_lenght', self.charuco_square_length)
        # ARGH, spelling mistake in the opencv_interactive-calibration app..
        # https://github.com/opencv/opencv/blob/master/apps/interactive-calibration/parametersController.cpp#L40
        file.write('charuco_marker_size', self.charuco_marker_size)
        file.write('max_frames_num', 40)
        file.write('min_frames_num', 20)

        # To write a right <camera_resolution> element we need to update
        # OpenCV to add std::vect<int> support, see my fork and discussion:
        # https://github.com/a1rb4Ck/opencv/commit/58a9adf0dd8ed5a7f1f712e99bf0f7b1340f39a8
        # http://answers.opencv.org/question/199743/write-sequence-of-int-with-filestorage-in-python/
        #
        # Working code with the fork:
        # file.write('camera_resolution', (
        #     [self.width, self.height]))
        #
        # <camera_resolution> is an Seq of Integers. In C++ it is written by <<
        # Python bindings must be added to support seq of int as std::vect<int>
        file.release()

        # Without updating OpenCV, we seek to append <camera_resolution>
        self.write_append_to_FileStorage(
            str(defaultConfig_path),
            string='<camera_resolution>\n  %d %d</camera_resolution>\n' % (
                self.width, self.height))


class PostureBuffer(object):
    """PostureBuffer class used to setup and use camera with lens correction.

    Attributes:
        window_length (int): Moving average window size (number of frame).
        avg_max_std (float): Maximum moving average standard deviation.
        buff_tvecs (Numpy array): Buffer of rotation vecs moving avg filter.
        buff_rvecs (Numpy array): Buffer of translation vecs moving avg filter.

    """

    def __init__(self, window_length=4, avg_max_std=0.1):
        """Initialize PostureBuffer class.

        Args:
            window_length (int): Moving average window size (number of frame).
            avg_max_std (float): Maximum moving average standard deviation.
        """
        self.window_length = window_length
        self.avg_max_std = avg_max_std
        self.buff_tvecs = None  # TODO: pre-allocate array of window_length
        self.buff_rvecs = None

    def update(self, rvecs, tvecs):
        """Update the moving average posture buffer and do the filtering.

        Arguments:
            rvecs (Numpy array): Posture rotation vectors (3x1).
            tvecs (Numpy array): Posture translation vectors (3x1).

        Returns:
            rvecs (Numpy array): Filtered (averaged) posture rotation vectors.
            tvecs (Numpy array): Filtered (avg) posture translation vectors.

        """
        # Notes:
        # https://github.com/avmeer/ComputerVisionAugmentedReality
        # ○ ArUco tags are hard to pick out perfectly each time.
        # ○ Position of the marker is noisy and the models would shake.
        # ○ Averaging the last THREE position matrices helped to stabilize.

        # Appending rvec and tvec postures to buffer
        if self.buff_rvecs is None:
            self.buff_rvecs = rvecs
        else:
            self.buff_rvecs = np.append(self.buff_rvecs, rvecs, axis=1)
        if self.buff_tvecs is None:
            self.buff_tvecs = tvecs
        else:
            self.buff_tvecs = np.append(self.buff_tvecs, tvecs, axis=1)

        if self.buff_rvecs.shape[1] > self.window_length:
            self.buff_rvecs = np.delete(self.buff_rvecs, 0, 1)

        if self.buff_tvecs.shape[1] > self.window_length:
            self.buff_tvecs = np.delete(self.buff_tvecs, 0, 1)
        # TODO: optimize delete without copying? But np.array are immutable..

        # Standard deviation filtering, if the board had a to big displacement.
        stdm = self.avg_max_std  # Moving/Rolling average filter max std
        rvecs_std = np.std(self.buff_rvecs, axis=1)
        if rvecs_std[0] > stdm or rvecs_std[1] > stdm or rvecs_std[2] > stdm:
            self.buff_rvecs = rvecs
        else:
            rvecs = np.mean(self.buff_rvecs, axis=1)

        tvecs_std = np.std(self.buff_tvecs, axis=1)
        if tvecs_std[0] > stdm or tvecs_std[1] > stdm or tvecs_std[2] > stdm:
            self.buff_tvecs = tvecs
        else:
            tvecs = np.mean(self.buff_tvecs, axis=1)

        return rvecs, tvecs
