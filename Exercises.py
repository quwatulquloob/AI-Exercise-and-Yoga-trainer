import cv2
import numpy as np
import time

from IPython.utils import frame

import PoseModule as pm
import os

from AudioCommSys import text_to_speech
import threading

import face_detection as face_det


class utilities:
    list_threads = []

    def __init__(self) -> None:
        pass

    def illustrate_exercise(self, example, exercise):
        seconds = 3
        img = cv2.imread(example)
        img = cv2.resize(img, (980, 550))

        cv2.imshow("Exercise Illustration", img)
        cv2.waitKey(1)

        # instruction1 = "Up next is " + exercise + " IN!"

        # if exercise != "Warm Up":
        #     text_to_speech(instruction1)

        while seconds > 0:
            img = cv2.imread(example)
            img = cv2.resize(img, (980, 550))
            # print("in here1")

            time.sleep(1)
            speaker_thread = threading.Thread(
                target=text_to_speech, args=(str(int(seconds))), kwargs={}
            )
            speaker_thread.start()
            speaker_thread.join()
            cv2.putText(
                img,
                exercise + " started in: " + str(int(seconds)),
                (300, 50),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (51, 153, 102),
                4,
            )

            ret, jpeg = cv2.imencode(".jpg", img)

            # print("yielding or naaaaaaa")
            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            cv2.imshow("Exercise Illustration", img)
            seconds -= 1
            cv2.waitKey(1)
        cv2.destroyAllWindows()

    def repitition_counter(self, per, count, direction):
        list_threads = []
        if per == 100 and direction == 0:
            count += 0.5
            direction = 1
        if per == 0 and direction == 1:
            count += 0.5
            direction = 0
            if int(count) != 0:
                print("here")
                speaker_thread = threading.Thread(
                    target=text_to_speech, args=(str(int(count))), kwargs={}
                )
                list_threads.append(speaker_thread)
                speaker_thread.start()
                speaker_thread.join()

            for t in list_threads:
                t.join()

        return {"count": count, "direction": direction}

    def display_rep_count(self, img, count, total_reps):

        cv2.putText(img, str(int(count)), (480, 120), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 15)

    def get_performance_bar_color(self, per):
        color = (0, 205, 205)
        if 0 < per <= 30:
            color = (51, 51, 255)
        if 30 < per <= 60:
            color = (0, 165, 255)
        if 60 <= per <= 100:
            color = (0, 255, 255)
        return color

    def position_info_floor_exercise(self, img, isRightPosition):
        if isRightPosition:
            cv2.putText(
                img,
                "Right Position",
                (10, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (128, 128, 0),
                3,
            )
        else:
            cv2.putText(
                img,
                "incorrect position",
                (10, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )

    def position_info_standing_exercise(self, img, isRightPosition):
        if isRightPosition:
            cv2.putText(
                img,
                "Facing Foward",
                (10, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 128, 0),
                3,
            )
        else:
            cv2.putText(
                img,
                "Not Facing Foward",
                (10, 350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )

    #
    def draw_performance_bar(self, img, per, bar, color, count):
        # Calculate the center and radius for the circular bar
        center = (270, 200)
        radius = 125

        # Calculate the end angle based on the percentage
        end_angle = np.interp(per, (0, 100), (0, 360))

        # Draw the circular bar
        cv2.ellipse(img, center, (radius, radius), 0, 0, end_angle, color, 3)

        # Draw the filled portion of the circular bar
        if per > 100:
            cv2.ellipse(img, center, (radius, radius), 0, 0, end_angle, color, cv2.FILLED)

        # Display the percentage text
        cv2.putText(img, f'{int(per)} %', (1100, 600), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

class simulate_target_exercies():
    # print("dif")

    def __init__(self, difficulty_level=2, reps=1):
        self.reps = reps
        self.difficulty_level = difficulty_level

    def push_ups(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/push_up_illustration.jpeg", "Push ups"
        ):
            yield (i)

            cap = cv2.VideoCapture("videos/Push Up.mp4")
            detector = pm.posture_detector()
            count = 0
            direction = 0
            start = time.process_time()
            total_reps = self.reps * self.difficulty_level

            # Load the gift video
            gift_video = cv2.VideoCapture("gifts/pushup.gif")

            while count < total_reps:
                success, img = cap.read()
                img = detector.find_person(img, False)
                landmark_list = detector.find_landmarks(img, False)
                is_person_facing_forward = False

                if len(landmark_list) != 0:
                    left_arm_angle = detector.find_angle(img, 11, 13, 15)
                    # right_arm_angle = detector.find_angle(img, 12, 14, 16)

                    per = np.interp(left_arm_angle, (60, 140), (0, 100))
                    bar = np.interp(left_arm_angle, (60, 140), (650, 100))

                    shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                    shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                    waist_x1, waist_y1 = landmark_list[24][1:]

                    color = utilities().get_performance_bar_color(per)

                    is_person_facing_forward = face_det.is_in_right_direction(
                        img, shoulder_x1, shoulder_x2, waist_x1
                    )
                    # When exercise is in start or terminal state
                    if per == 100 or per == 0:
                        color = (0, 255, 0)
                        rep = utilities().repitition_counter(per, count, direction)
                        count = rep["count"]
                        direction = rep["direction"]
                    utilities().draw_performance_bar(img, per, bar, color, count)

                utilities().display_rep_count(img, count, total_reps)
                utilities().position_info_floor_exercise(img, is_person_facing_forward)

                # Display gift video in the left top corner
                ret, gift_frame = gift_video.read()
                if ret:
                    h, w, _ = img.shape
                    gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                    img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

                ret, jpeg = cv2.imencode(".jpg", img)
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
                )
                img = cv2.resize(img, (1300, 700))
                cv2.imshow("Push ups", img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                if count >= total_reps:
                    break

                cap.release()
                gift_video.release()
                cv2.destroyAllWindows()

    def Dead_Bugs(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/dead-bug-exercise.jpg", "Dead Bugs"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/dead bugs.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/deadbugs.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                right_leg_angle = detector.find_angle(img, 15, 24, 28)
                left_leg_angle = detector.find_angle(img, 16, 23, 27)
                cv2.circle(
                    img, (landmark_list[15][1], landmark_list[15][2]), 15, (151, 151, 0), cv2.FILLED)
                #
                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (51, 153, 102), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (153, 204, 0), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[16][1], landmark_list[16][2]), 15, (153, 204, 204), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (255, 255, 255), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (204, 204, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (0, 128, 0), cv2.FILLED)

                per = np.interp(right_leg_angle, (190, 274), (0, 100))
                bar = np.interp(right_leg_angle, (190, 274), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            img = cv2.resize(img, (1200, 1000))
            cv2.imshow("Dead Bugs", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if count >= total_reps:
                break

        cap.release()
        gift_video.release()
        cv2.destroyAllWindows()
    def Heal_Slides(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/heal slides.jpg", "Heal Slides"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Supine Heel Slides.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/healslides.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                right_leg_angle = detector.find_angle(img, 24, 26, 28)
                left_leg_angle = detector.find_angle(img, 12, 24, 28)

                cv2.circle(
                    img, (landmark_list[26][1], landmark_list[26][2]), 15, (153, 204, 204), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (0, 128, 0), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (225, 0, 225), cv2.FILLED)

                per = np.interp(right_leg_angle, (180, 260), (0, 100))
                bar = np.interp(right_leg_angle, (180, 260), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Heal Slides", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count >= total_reps:
                break

            cap.release()
            gift_video.release()
        cv2.destroyAllWindows()

    def Straight_Leg_Raise(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/straight-leg-raise-test.png", "Straight leg raise"
        ):
            yield (i)

        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("videos/Side Lying Leg Raises.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/straightlegraise.gif")

        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                # right_leg_angle = detector.find_angle(img, 24, 26, 28)
                left_leg_angle = detector.find_angle(img, 12, 24, 28)

                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (204, 204, 225), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (0, 128, 0), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (225, 0, 225), cv2.FILLED)

                per = np.interp(left_leg_angle, (165, 180), (0, 100))
                bar = np.interp(left_leg_angle, (165, 180), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            img = cv2.resize(img, (1200, 1200))
            cv2.imshow("Straight leg raise", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def bicep_curls(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/bicep_curls_illustration.jpeg", "BICEP CURLS"
        ):
            yield (i)

        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("videos/hammer curl.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/Bicep_curls.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while True:
            success, img = cap.read()
            if not success:
                break
            is_person_facing_foward = False
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            if len(landmark_list) != 0:
                right_arm_angle = detector.find_angle(img, 12, 14, 16)

                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (204, 204, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[14][1], landmark_list[14][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[16][1], landmark_list[16][2]), 15, (0, 225, 225), cv2.FILLED)

                per = np.interp(right_arm_angle, (38, 165), (0, 100))
                bar = np.interp(right_arm_angle, (38, 165), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Bicep Curls", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if count >= total_reps:
                break

        cap.release()
        gift_video.release()
        cv2.destroyAllWindows()

    def mountain_climbers(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/mountain_climber_illustraion.jpeg", "MOUNTAIN CLIMBERS"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Mountain Climbers.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/mountainclimber.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()

            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)
                left_leg_angle = detector.find_angle(img, 24, 26, 28)

                right_leg_angle = detector.find_angle(img, 23, 25, 27)
                cv2.circle(
                    img, (landmark_list[11][1], landmark_list[11][2]), 15, (151, 151, 0), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[13][1], landmark_list[13][2]), 15, (51, 153, 102), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (51, 153, 102), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[15][1], landmark_list[15][2]), 15, (153, 204, 0), cv2.FILLED)

                cv2.circle(
                    img, (landmark_list[26][1], landmark_list[26][2]), 15, (153, 204, 204), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[14][1], landmark_list[14][2]), 15, (255, 255, 255), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (204, 204, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[16][1], landmark_list[16][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (0, 128, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (225, 0, 225), cv2.FILLED)

                per = np.interp(right_leg_angle, (220, 280), (0, 100))
                bar = np.interp(right_leg_angle, (220, 280), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_x2 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]

                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Mountain Climber", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count >= total_reps:
                break
        cap.release()
        gift_video.release()
        cv2.destroyAllWindows()

    def squats(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/squats_illustration.jpeg", "SQUATS"
        ):
            yield (i)

        cap = cv2.VideoCapture("")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/squat.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                right_leg_angle = detector.find_angle(img, 24, 26, 28)
                left_leg_angle = detector.find_angle(img, 23, 25, 27)

                per = np.interp(left_leg_angle, (190, 240), (0, 100))
                bar = np.interp(left_leg_angle, (190, 240), (650, 100))
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (225, 0, 225), cv2.FILLED)

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Squats", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Glutebridge(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/Glute bridge.jpg", "GluteBridge"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Glute bridge.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/Glut_bridge.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                # right_leg_angle = detector.find_angle(img, 24, 26, 28)
                left_leg_angle = detector.find_angle(img, 12, 24, 28)
                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (225, 0, 225), cv2.FILLED)

                per = np.interp(left_leg_angle, (125, 170), (0, 100))
                bar = np.interp(left_leg_angle, (125, 170), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]

                color = utilities().get_performance_bar_color(per)
                is_person_facing_foward = face_det.is_person_facing_front(
                    img, shoulder_x1, shoulder_y1, shoulder_x2, shoulder_y2
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )

            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Glute Bridge", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Wall_Pushup(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/wall pushups.jpg", "Wall_Pushup"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/wall pushups.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/wallpushups.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()
        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False

            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)
                cv2.circle(
                    img, (landmark_list[11][1], landmark_list[11][2]), 15, (128, 0, 128), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[13][1], landmark_list[13][2]), 15, (0, 0, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[15][1], landmark_list[15][2]), 15, (128, 128, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (51, 153, 102), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[14][1], landmark_list[14][2]), 15, (0, 128, 128), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[16][1], landmark_list[16][2]), 15, (128, 128, 0), cv2.FILLED)

                per = np.interp(left_arm_angle, (60, 140), (0, 100))
                bar = np.interp(left_arm_angle, (60, 140), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Wall_Pushup", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Siting_Leg_raise(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/seated leg raise.jpg", "Siting_Leg_raise"
        ):
            yield (i)

        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture("videos/Seated Leg Extension.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture(
            "animatedgifts/Bulgarian Split Squat Bodyweight fitness exercise workout animation video male muscle highlight 4K.mp4")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:
                left_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_arm_angle = detector.find_angle(img, 12, 14, 16)
                right_leg_angle = detector.find_angle(img, 23, 25, 27)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (225, 0, 225), cv2.FILLED)

                per = np.interp(right_leg_angle, (220, 280), (0, 100))
                bar = np.interp(right_leg_angle, (220, 280), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Wall_Pushup", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Tricep_Dips(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/Tricep dips.jpg", "Tricep_Dips"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Tricep Dips   On Box.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/tricep dips.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:

                right_arm_angle = detector.find_angle(img, 12, 14, 16)
                # right_leg_angle = detector.find_angle(img, 23, 25, 27)
                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[14][1], landmark_list[14][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[16][1], landmark_list[16][2]), 15, (128, 128, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (128, 0, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (51, 51, 51), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (0, 128, 0), cv2.FILLED)

                per = np.interp(right_arm_angle, (93, 158), (0, 100))
                bar = np.interp(right_arm_angle, (93, 158), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Tricep_Dips", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Lunges(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/Lunges.jpg", "Lunges"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Lunges.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/lunges.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:

                # right_arm_angle = detector.find_angle(img, 11, 13, 15)
                right_leg_angle = detector.find_angle(img, 23, 25, 27)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (128, 128, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[24][1], landmark_list[24][2]), 15, (128, 0, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[26][1], landmark_list[26][2]), 15, (51, 51, 51), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (0, 128, 0), cv2.FILLED)

                per = np.interp(right_leg_angle, (70, 167), (0, 100))
                bar = np.interp(right_leg_angle, (70, 167), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Lunges", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Side_Laying(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/straight-leg-raise-test.png", "Side_Laying"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Side Lying Leg Raises.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/side leg raise.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:

                right_leg_angle = detector.find_angle(img, 23, 28, 27)

                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[28][1], landmark_list[28][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (128, 128, 0), cv2.FILLED)

                per = np.interp(right_leg_angle, (53, 94), (0, 100))
                bar = np.interp(right_leg_angle, (53, 94), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Side_Laying", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Arms_Raise(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/armraise.png", "Arms_Raise"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/Arms Range of motion.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/arms raise.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:

                right_leg_angle = detector.find_angle(img, 15, 0, 16)

                cv2.circle(
                    img, (landmark_list[15][1], landmark_list[11][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[0][1], landmark_list[13][2]), 15, (225, 0, 225), cv2.FILLED)
                # cv2.circle(
                #     img, (landmark_list[16][1], landmark_list[15][2]), 15, (128, 128, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[12][1], landmark_list[12][2]), 15, (128, 0, 0), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[14][1], landmark_list[14][2]), 15, (51, 51, 51), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[16][1], landmark_list[16][2]), 15, (0, 128, 0), cv2.FILLED)

                per = np.interp(right_leg_angle, (25, 300), (0, 100))
                bar = np.interp(right_leg_angle, (25, 300), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_standing_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))

            cv2.imshow("Arms_Raise", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Clam_Shells(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/Clam Shell_illustration..jpg", "Clam_Shells"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/clam_shells.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/camshells.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:

                right_leg_angle = detector.find_angle(img, 25, 27, 26)

                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[27][1], landmark_list[27][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[26][1], landmark_list[26][2]), 15, (128, 0, 0), cv2.FILLED)

                per = np.interp(right_leg_angle, (167, 320), (0, 100))
                bar = np.interp(right_leg_angle, (167, 320), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Clam shells", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()

    def Situps(self):
        for i in utilities().illustrate_exercise(
                "TrainerImages/wall pushups.jpg", "Situps"
        ):
            yield (i)

        cap = cv2.VideoCapture("videos/SIT-UPS.mp4")
        # Load the gift video
        gift_video = cv2.VideoCapture("gifts/situps.gif")
        detector = pm.posture_detector()
        count = 0
        direction = 0
        start = time.process_time()

        total_reps = self.reps * self.difficulty_level

        while count < total_reps:
            success, img = cap.read()
            img = detector.find_person(img, False)
            landmark_list = detector.find_landmarks(img, False)
            is_person_facing_foward = False
            if len(landmark_list) != 0:

                right_leg_angle = detector.find_angle(img, 0, 23, 25)

                cv2.circle(
                    img, (landmark_list[0][1], landmark_list[0][2]), 15, (0, 225, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[23][1], landmark_list[23][2]), 15, (225, 0, 225), cv2.FILLED)
                cv2.circle(
                    img, (landmark_list[25][1], landmark_list[25][2]), 15, (128, 0, 0), cv2.FILLED)

                per = np.interp(right_leg_angle, (190, 310), (0, 100))
                bar = np.interp(right_leg_angle, (55, 115), (650, 100))

                shoulder_x1, shoulder_y1 = landmark_list[12][1:]
                shoulder_x2, shoulder_y2 = landmark_list[11][1:]
                waist_x1, waist_y1 = landmark_list[24][1:]

                color = utilities().get_performance_bar_color(per)

                is_person_facing_foward = face_det.is_in_right_direction(
                    img, shoulder_x1, shoulder_x2, waist_x1
                )
                # When exercise is in start or terminal state
                if per == 100 or per == 0:
                    color = (0, 255, 0)
                    rep = utilities().repitition_counter(per, count, direction)
                    count = rep["count"]
                    direction = rep["direction"]
                utilities().draw_performance_bar(img, per, bar, color, count)

            utilities().display_rep_count(img, count, total_reps)
            utilities().position_info_floor_exercise(img, is_person_facing_foward)
            # Display gift video in the left top corner
            ret, gift_frame = gift_video.read()
            if ret:
                h, w, _ = img.shape
                gift_frame = cv2.resize(gift_frame, (w // 5, h // 5))  # Adjust the size as needed
                img[0:gift_frame.shape[0], 0:gift_frame.shape[1]] = gift_frame

            ret, jpeg = cv2.imencode(".jpg", img)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
            )
            img = cv2.resize(img, (1500, 1200))
            cv2.imshow("Situps", img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            if count == (self.reps * self.difficulty_level):
                break
        cv2.destroyAllWindows()


    def complete_path(self):
        target_exercises = simulate_target_exercies(self.difficulty_level)
        squats_performance = target_exercises.squats()
        bicep_curls_performance = target_exercises.bicep_curls()
        mc_performance = target_exercises.mountain_climbers()
        pushup_performance = target_exercises.push_ups()
        Heal_Slides_performance = target_exercises.Heal_Slides()
        Siting_Leg_raise_performance = target_exercises.Siting_Leg_raise
        Wall_Pushup_performance = target_exercises.Wall_Pushup()
        Tricep_dips_performance = target_exercises.Tricep_Dips()
        Lunges_performance = target_exercises.Lunges()
        Side_Laying_performance = target_exercises.Side_Laying()
        Arms_Raise_performance = target_exercises.Arms_Raise()
        Clam_Shells_performance = target_exercises.Clam_Shells()
        Situps_performance = target_exercises.Situps()
        elbowpain_performance = target_exercises.elbowpain()
        kneepain_performance = target_exercises.kneepain()
        Glutebridge_performance = target_exercises.Glutebridge()


        print("---------------")
        for i in bicep_curls_performance:
            yield (i)

        for i in mc_performance:
            yield (i)

        for i in pushup_performance:
            yield (i)

        for i in squats_performance:
            yield (i)
        for i in pushup_performance:
            yield (i)
        for i in Heal_Slides_performance:
            yield (i)
        for i in Wall_Pushup_performance:
            yield (i)
        for i in Siting_Leg_raise_performance:
            yield (i)
        for i in Tricep_dips_performance:
            yield (i)
        for i in Lunges_performance:
            yield (i)
        for i in Side_Laying_performance:
            yield (i)
        for i in Arms_Raise_performance:
            yield (i)
        for i in Clam_Shells_performance:
            yield (i)
        for i in Situps_performance:
            yield (i)
        for i in elbowpain_performance:
            yield (i)
        for i in kneepain_performance:
            yield (i)
        for i in Glutebridge_performance:
            yield (i)

        simulate_target_exercies.mountain_climbers()
        simulate_target_exercies.bicep_curls()
        simulate_target_exercies.push_ups()
        simulate_target_exercies.squats()
        simulate_target_exercies.Dead_Bugs()
        simulate_target_exercies.Heal_Slides()
        simulate_target_exercies.Wall_Pushup()
        simulate_target_exercies.Siting_Leg_raise()
        simulate_target_exercies.Lunges()
        simulate_target_exercies.Tricep_Dips()
        simulate_target_exercies.Side_Laying()
        simulate_target_exercies.Arms_Raise()
        simulate_target_exercies.Clam_Shells()
        simulate_target_exercies.Situps()
        simulate_target_exercies.Glutebridge()


def main():
    print("TODO")


if __name__ == "__main__":
    main()
