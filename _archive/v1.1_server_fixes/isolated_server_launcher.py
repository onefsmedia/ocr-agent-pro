#!/usr/bin/env python3
"""
Isolated Flask Server Launcher
Uses subprocess to avoid signal handling issues
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def main():
    print("🚀 OCR Agent Pro - Isolated Server Launcher")
    print("=" * 55)
    
    # Ensure we're in the right directory
    project_dir = Path(r'c:\OCR Agent')
    os.chdir(project_dir)
    
    # Create a dedicated server script
    server_script = """
import os
import sys
sys.path.insert(0, r'c:\\OCR Agent')

try:
    from app import create_app
    app = create_app()
    print("🌐 Server ready at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
"""
    
    # Write the server script to a file
    script_path = project_dir / "isolated_server.py"
    with open(script_path, 'w') as f:
        f.write(server_script)
    
    print("✅ Created isolated server script")
    print("✅ Starting server in separate process...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 55)
    
    try:
        # Start the server in a separate process
        process = subprocess.Popen([
            sys.executable, 
            str(script_path)
        ], 
        cwd=str(project_dir),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        print(f"✅ Server process started (PID: {process.pid})")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("✅ Server stopped")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Clean up
        try:
            script_path.unlink()
        except:
            pass

if __name__ == "__main__":
    main()