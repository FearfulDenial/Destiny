
# Auto-Updater for Destiny AV. This is not required and can be removed after installation.
#TODO Add a check to see if the user wants to update the AV before updating it.
import requests,hashlib,os

ScriptDirectory = os.path.dirname(__file__)
GitHub = "https://raw.githubusercontent.com/FearfulDenial/Destiny/main/"
Files = {
    "destiny": "Destiny.py",
    "database": "Database.json",
    "ruleset": "Ruleset.json"
}

# Imported from Destiny.py
def Calculate(Path,Algorithm="sha256"):
    try:
        with open(Path,"rb") as File:
            Data = File.read()
            return hashlib.new(Algorithm,Data).hexdigest()
    except Exception as Exceptor:
        return None

def Download(Url,Path):
    try:
        Response = requests.get(Url,timeout=10)
        Response.raise_for_status()
        with open(Path,"wb") as File:
            File.write(Response.content)
        return True
    except Exception as Exceptor:
        return False

def Checksum(Url):
    try:
        Response = requests.get(Url,timeout=10)
        Response.raise_for_status()
        Hash = hashlib.sha256(Response.content).hexdigest()
        return Hash
    except Exception as Exceptor:
        return None
    
def Update():
    for i,v in Files.items():
        Path = os.path.join(ScriptDirectory,v)
        Url = GitHub + v
        RemoteChecksum = Checksum(Url)
        LocalChecksum = Calculate(Url)
        if RemoteChecksum != LocalChecksum:
            print(f"Updating {v}...")
            if Download(Url,Path):
                print(f"Updated {v} successfully.")
            else:
                print(f"Failed to update {v}.")
        else:
            print(f"{v} is up to date.")