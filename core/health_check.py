from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from django.db.utils import OperationalError
import psutil
from datetime import datetime

class HealthCheckView(APIView):
    def get(self, request):
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now(),
            'database': self.check_database(),
            'memory_usage': self.get_memory_usage(),
            'cpu_usage': self.get_cpu_usage(),
        }
        if not all(health_status.values()):
            health_status['status'] = 'unhealthy'
            return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(health_status, status=status.HTTP_200_OK)

    def check_database(self):
        try:
            connections['default'].cursor()
            return True
        except OperationalError:
            return False

    def get_memory_usage(self):
        memory = psutil.virtual_memory()
        return {
            'total': self.format_bytes(memory.total),
            'available': self.format_bytes(memory.available),
            'percent': f"{memory.percent}%",
            'limit': self.format_bytes(psutil.virtual_memory().total)
        }

    def get_cpu_usage(self):
        return f"{psutil.cpu_percent(interval=1)}%"

    def format_bytes(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"
