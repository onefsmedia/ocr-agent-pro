"""
Windows Service Wrapper for OCR Agent Pro
Allows running as a proper Windows service with auto-start on boot
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add project directory to path
project_dir = Path(r'c:\OCR Agent')
sys.path.insert(0, str(project_dir))

try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    SERVICE_AVAILABLE = True
except ImportError:
    SERVICE_AVAILABLE = False
    print("⚠️  pywin32 not available. Install with: pip install pywin32")

class OCRAgentWindowsService(win32serviceutil.ServiceFramework):
    """Windows Service for OCR Agent Pro"""
    
    _svc_name_ = "OCRAgentPro"
    _svc_display_name_ = "OCR Agent Pro Service"
    _svc_description_ = "OCR Agent Pro - Document Processing and AI Assistant Service"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        
        # Setup logging
        log_dir = project_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'service.log'
        
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('OCRAgentService')
    
    def SvcStop(self):
        """Stop the service"""
        self.logger.info("🛑 Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False
    
    def SvcDoRun(self):
        """Main service execution"""
        self.logger.info("🚀 OCR Agent Pro service starting...")
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        try:
            # Change to project directory
            os.chdir(project_dir)
            
            # Import and run the persistent server
            from persistent_server import OCRAgentService
            
            service = OCRAgentService()
            
            # Run in a separate thread to allow service control
            import threading
            server_thread = threading.Thread(target=service.run_with_auto_restart)
            server_thread.daemon = True
            server_thread.start()
            
            self.logger.info("✅ OCR Agent Pro service started successfully")
            
            # Wait for stop signal
            while self.running:
                if win32event.WaitForSingleObject(self.hWaitStop, 1000) == win32event.WAIT_OBJECT_0:
                    break
                    
                # Check if server thread is still alive
                if not server_thread.is_alive():
                    self.logger.error("💥 Server thread died, restarting...")
                    server_thread = threading.Thread(target=service.run_with_auto_restart)
                    server_thread.daemon = True
                    server_thread.start()
            
            self.logger.info("🏁 OCR Agent Pro service stopped")
            
        except Exception as e:
            self.logger.error(f"💥 Service error: {e}")
            servicemanager.LogErrorMsg(f"OCR Agent Pro service error: {e}")

def install_service():
    """Install the Windows service"""
    if not SERVICE_AVAILABLE:
        print("❌ Cannot install service: pywin32 not available")
        print("   Install with: pip install pywin32")
        return False
    
    try:
        win32serviceutil.InstallService(
            OCRAgentWindowsService,
            OCRAgentWindowsService._svc_name_,
            OCRAgentWindowsService._svc_display_name_,
            startType=win32service.SERVICE_AUTO_START,
            description=OCRAgentWindowsService._svc_description_
        )
        print("✅ OCR Agent Pro service installed successfully")
        print("   Service will auto-start on system boot")
        return True
    except Exception as e:
        print(f"❌ Service installation failed: {e}")
        return False

def uninstall_service():
    """Uninstall the Windows service"""
    if not SERVICE_AVAILABLE:
        print("❌ Cannot uninstall service: pywin32 not available")
        return False
    
    try:
        win32serviceutil.RemoveService(OCRAgentWindowsService._svc_name_)
        print("✅ OCR Agent Pro service uninstalled successfully")
        return True
    except Exception as e:
        print(f"❌ Service uninstallation failed: {e}")
        return False

def start_service():
    """Start the Windows service"""
    if not SERVICE_AVAILABLE:
        print("❌ Cannot start service: pywin32 not available")
        return False
    
    try:
        win32serviceutil.StartService(OCRAgentWindowsService._svc_name_)
        print("✅ OCR Agent Pro service started")
        return True
    except Exception as e:
        print(f"❌ Service start failed: {e}")
        return False

def stop_service():
    """Stop the Windows service"""
    if not SERVICE_AVAILABLE:
        print("❌ Cannot stop service: pywin32 not available")
        return False
    
    try:
        win32serviceutil.StopService(OCRAgentWindowsService._svc_name_)
        print("✅ OCR Agent Pro service stopped")
        return True
    except Exception as e:
        print(f"❌ Service stop failed: {e}")
        return False

def service_status():
    """Check service status"""
    if not SERVICE_AVAILABLE:
        print("❌ Cannot check status: pywin32 not available")
        return
    
    try:
        status = win32serviceutil.QueryServiceStatus(OCRAgentWindowsService._svc_name_)
        status_map = {
            win32service.SERVICE_STOPPED: "Stopped",
            win32service.SERVICE_START_PENDING: "Starting",
            win32service.SERVICE_STOP_PENDING: "Stopping", 
            win32service.SERVICE_RUNNING: "Running",
            win32service.SERVICE_CONTINUE_PENDING: "Continuing",
            win32service.SERVICE_PAUSE_PENDING: "Pausing",
            win32service.SERVICE_PAUSED: "Paused"
        }
        
        current_status = status_map.get(status[1], f"Unknown ({status[1]})")
        print(f"📊 OCR Agent Pro service status: {current_status}")
        
    except Exception as e:
        print(f"❌ Cannot check service status: {e}")

def main():
    """Main entry point for service management"""
    if len(sys.argv) == 1:
        # Run as regular service
        if SERVICE_AVAILABLE:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(OCRAgentWindowsService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            print("❌ pywin32 not available. Install with: pip install pywin32")
        return
    
    # Handle command line arguments
    command = sys.argv[1].lower()
    
    if command == 'install':
        install_service()
    elif command == 'uninstall':
        uninstall_service()
    elif command == 'start':
        start_service()
    elif command == 'stop':
        stop_service()
    elif command == 'status':
        service_status()
    elif command == 'restart':
        stop_service()
        time.sleep(2)
        start_service()
    else:
        print("OCR Agent Pro - Windows Service Manager")
        print("=" * 40)
        print("Usage:")
        print("  python windows_service.py install   - Install service")
        print("  python windows_service.py uninstall - Remove service")
        print("  python windows_service.py start     - Start service")
        print("  python windows_service.py stop      - Stop service")
        print("  python windows_service.py restart   - Restart service")
        print("  python windows_service.py status    - Check status")

if __name__ == '__main__':
    main()