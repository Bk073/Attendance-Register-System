from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    name = 'attendanceregistersystem.attendance'

    def ready(self):
        try:
            import attendance.signals  # noqa F401
        except ImportError:
            pass
