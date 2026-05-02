from attendance.models import WorkerArrival


def register_attendance_successfully(worker, image, node):
    attendance = WorkerArrival()
    attendance.worker = worker
    attendance.arrival_image = image
    attendance.node = node
    attendance.save()
