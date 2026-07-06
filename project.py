import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET

def load_data(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if not os.path.exists(filepath):
        print(f"Błąd: Plik {filepath} nie istnieje.")
        sys.exit(1)
        
    try:
        if ext == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif ext in ['.yml', '.yaml']:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif ext == '.xml':
            tree = ET.parse(filepath)
            root = tree.getroot()
            # Prosta konwersja XML -> słownik (dla płaskich struktur)
            return {child.tag: child.text for child in root}
        else:
            print(f"Błąd: Niewspierany format wejściowy {ext}")
            sys.exit(1)
    except Exception as e:
        print(f"Błąd składni pliku {filepath}: {e}")
        sys.exit(1)

def save_data(data, filepath):
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif ext in ['.yml', '.yaml']:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        elif ext == '.xml':
            root = ET.Element("root")
            for key, val in data.items():
                child = ET.SubElement(root, key)
                child.text = str(val)
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
        else:
            print(f"Błąd: Niewspierany format wyjściowy {ext}")
            sys.exit(1)
    except Exception as e:
        print(f"Błąd zapisu do pliku {filepath}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Sposób użycia: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)
        
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    data = load_data(file1)
    save_data(data, file2)
    print(f"Sukces! Przekonwertowano {file1} do {file2}")

if __name__ == "__main__":
    main()