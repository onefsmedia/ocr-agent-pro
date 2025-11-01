# Manual OnlyOffice Port Configuration Guide
# Step-by-step instructions to change OnlyOffice from port 80 to port 8000

## MANUAL CONFIGURATION STEPS:

### Step 1: Open Configuration File
1. Navigate to: C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\
2. Make a backup copy of nginx.conf (rename to nginx.conf.backup)
3. Open nginx.conf in a text editor (like Notepad++ or VSCode) AS ADMINISTRATOR

### Step 2: Find and Replace Port Settings
Look for these lines and change them:

FIND:    listen 80;
REPLACE: listen 8000;

FIND:    listen [::]:80;
REPLACE: listen [::]:8000;

### Step 3: Save the File
Save nginx.conf with the changes

### Step 4: Restart OnlyOffice Services
Open Command Prompt or PowerShell AS ADMINISTRATOR and run:

net stop "ONLYOFFICE Document Server Proxy"
net stop "ONLYOFFICE Document Server DocService"
net stop "ONLYOFFICE Document Server Converter"

net start "ONLYOFFICE Document Server Converter"
net start "ONLYOFFICE Document Server DocService"
net start "ONLYOFFICE Document Server Proxy"

### Step 5: Test the Configuration
Wait 30 seconds, then test:
- Open browser and go to: http://localhost:8000
- Should see OnlyOffice welcome page

## ALTERNATIVE: Use Services.msc
1. Press Win+R, type "services.msc", press Enter
2. Find the OnlyOffice services (Ds*)
3. Right-click each service -> Restart

## Files to Modify:
- C:\Program Files\ONLYOFFICE\DocumentServer\nginx\conf\nginx.conf

## Services to Restart:
- ONLYOFFICE Document Server Converter (DsConverterSvc)
- ONLYOFFICE Document Server DocService (DsDocServiceSvc)  
- ONLYOFFICE Document Server Proxy (DsProxySvc)