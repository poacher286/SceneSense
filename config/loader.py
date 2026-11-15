class ConfigLoader:

    def load(self):

        return {
            "capture_fps": 5,
            "serial_port": "/dev/tty.usbserial",
            "ai_model": "clip",
            # Logging configuration
            "logging_config": {
                "level": "INFO",                    # DEBUG | INFO | WARNING | ERROR
                "console_format": True,             # Enable colorized console output
                "file_output": "/logs/scenesense/", # Log file directory
                "file_name": "app.log",             # Base log filename
                "max_file_size_mb": 10,             # Rotate at this size (MB)
                "keep_last_files": 5,               # Keep N rotated files
                "performance_profiling": True       # Enable timing hooks for critical operations
            }
        }