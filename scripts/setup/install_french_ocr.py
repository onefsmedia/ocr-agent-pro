#!/usr/bin/env python3
"""
French Language Pack Installer for Tesseract OCR
Downloads and installs French language support for OCR Agent Pro
"""

import os
import requests
import shutil
import tempfile
from pathlib import Path

class TesseractFrenchInstaller:
    def __init__(self):
        self.tessdata_path = Path("C:/Program Files/Tesseract-OCR/tessdata")
        self.temp_dir = Path(tempfile.gettempdir())
        self.french_urls = [
            "https://github.com/tesseract-ocr/tessdata_best/raw/main/fra.traineddata",
            "https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata",
            "https://github.com/tesseract-ocr/tessdata_fast/raw/main/fra.traineddata"
        ]
    
    def check_permissions(self):
        """Check if we have write permissions to tessdata directory"""
        try:
            test_file = self.tessdata_path / "test_write_permissions.tmp"
            test_file.touch()
            test_file.unlink()
            return True
        except (PermissionError, OSError):
            return False
    
    def download_french_pack(self):
        """Download French language pack from GitHub"""
        print("📥 Downloading French language pack...")
        
        for i, url in enumerate(self.french_urls):
            try:
                print(f"   Trying source {i+1}/{len(self.french_urls)}: {url.split('/')[-2]}")
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Save to temp directory first
                temp_file = self.temp_dir / "fra.traineddata"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                
                file_size = temp_file.stat().st_size / (1024 * 1024)  # MB
                print(f"   ✅ Downloaded: {file_size:.1f} MB")
                
                return temp_file
                
            except requests.exceptions.RequestException as e:
                print(f"   ❌ Failed: {e}")
                continue
        
        raise Exception("All download sources failed")
    
    def install_french_pack(self, temp_file):
        """Install French pack to tessdata directory"""
        target_file = self.tessdata_path / "fra.traineddata"
        
        if not self.check_permissions():
            print("❌ No write permissions to tessdata directory")
            print(f"   Please run as administrator or manually copy:")
            print(f"   From: {temp_file}")
            print(f"   To:   {target_file}")
            return False
        
        try:
            shutil.copy2(temp_file, target_file)
            print(f"✅ Installed French language pack to: {target_file}")
            return True
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def verify_installation(self):
        """Verify French language pack is installed"""
        french_file = self.tessdata_path / "fra.traineddata"
        
        if french_file.exists():
            size_mb = french_file.stat().st_size / (1024 * 1024)
            print(f"✅ French language pack verified: {size_mb:.1f} MB")
            return True
        else:
            print("❌ French language pack not found")
            return False
    
    def test_french_ocr(self):
        """Test French OCR functionality"""
        try:
            import pytesseract
            from PIL import Image, ImageDraw
            
            # Set Tesseract path
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            
            # Check available languages
            languages = pytesseract.get_languages()
            print(f"📋 Available languages: {', '.join(languages)}")
            
            if 'fra' in languages:
                print("✅ French language detected in Tesseract")
                
                # Create test image with French text
                img = Image.new('RGB', (400, 100), color='white')
                draw = ImageDraw.Draw(img)
                draw.text((20, 30), 'Bonjour le monde!', fill='black')
                
                # Test French OCR
                french_text = pytesseract.image_to_string(img, lang='fra')
                print(f"🧪 French OCR Test: '{french_text.strip()}'")
                
                # Test combined French+English
                combined_text = pytesseract.image_to_string(img, lang='fra+eng')
                print(f"🧪 French+English OCR Test: '{combined_text.strip()}'")
                
                return True
            else:
                print("❌ French language not detected")
                return False
                
        except Exception as e:
            print(f"❌ OCR test failed: {e}")
            return False

def main():
    print("🇫🇷 TESSERACT FRENCH LANGUAGE INSTALLER")
    print("=" * 50)
    
    installer = TesseractFrenchInstaller()
    
    # Check if already installed
    if installer.verify_installation():
        print("French language pack already installed!")
        installer.test_french_ocr()
        return
    
    try:
        # Download French pack
        temp_file = installer.download_french_pack()
        
        # Install French pack
        if installer.install_french_pack(temp_file):
            # Verify installation
            if installer.verify_installation():
                print("\n🎉 French language support successfully installed!")
                installer.test_french_ocr()
            else:
                print("\n❌ Installation verification failed")
        else:
            print("\n❌ Installation failed")
            
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()
            
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")

if __name__ == "__main__":
    main()