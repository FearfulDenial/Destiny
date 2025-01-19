
import hashlib,os,shutil,json
# Directories
ScriptDirectory = os.path.dirname(__file__)
Database = os.path.join(ScriptDirectory,"Database.json")
History = os.path.join(ScriptDirectory,"History.log")
Quarantine = os.path.join(ScriptDirectory,"Quarantine")
Ruleset = os.path.join(ScriptDirectory,"Ruleset.json")

def Calculate(Path,Algorithm="sha256"):
    try:
        with open(Path,"rb") as File:
            Data = File.read()
            return hashlib.new(Algorithm,Data).hexdigest()
    except Exception as Exceptor:
        return None

def OperationScan(Operation,Kwargs):
    Operation = str(Operation).lower()
    try:
        if Operation == "file":
            Hash = Calculate(Kwargs.get("path"))
            Log(f"Scanning {Kwargs.get("path")}\n- Hash: {Hash if Hash else "None"}")
            if Hash and Hash in Kwargs.get("signatures"):
                return True,Kwargs.get("signatures")[Hash]
            return False,None
        elif Operation == "directory":
            InfFiles = []
            for Root,Dir,Files in os.walk(Kwargs.get("path")):
                for File in Files:
                    Path = os.path.join(Root,File)
                    Inf,Reason = OperationScan("File", {"path": Path, "signatures": Kwargs.get("signatures")})
                    if Inf:
                        InfFiles.append((Path,Reason))
            return InfFiles
    except Exception as Exceptor:
        Log(f"While operating Ruleset under {Operation}, got {str(Exceptor)}")
        return False,None if Operation == "file" else []
def OperationRuleset(Operation,Kwargs):
    Operation = str(Operation).lower()
    try:
        if Operation == "load":
            with open(Ruleset,"r") as File:
                return json.load(File)
        elif Operation == "scan":
            Alerts = []
            RuleChecked = False
            for Rule in Kwargs.get("ruleset"):
                if Rule.get("type") == "file":
                    Conditions = Rule.get("conditions",{})
                    PathContains = Conditions.get("path_contains",[])
                    ExtensionIs = Conditions.get("extension_is",[])
                    if PathContains and ExtensionIs and any(v in Kwargs.get("path") for v in PathContains) and any(Kwargs.get("path").endswith(e) for e in ExtensionIs):
                        Alerts.append(Rule.get("alert","Unknown Alert provided."))
                        RuleChecked = True
                else:
                    Log(f"Unknown Rule Type '{Rule.get("type","Unknown")}'.")
            return RuleChecked,Alerts
        else:
            Log("No Operation provided.")
            return {} if Operation == "load" else None,None
    except Exception as Exceptor:
        Log(f"While operating Ruleset under {Operation}, got {str(Exceptor)}")
        return {} if Operation == "load" else None,None
def OperationSignature(Operation,Kwargs):
    Operation = str(Operation).lower()
    try:
        if Operation == "load":
            with open(Database,"r") as File:
                return json.load(File)
        elif Operation == "save":
            Data = OperationSignature("Load")
            Data[Kwargs.get("hash","Unknown Hash")] = Kwargs.get("reason","Unknown Reason")
            with open(Database,"w") as File:
                json.dump(Data,File,indent=4)
                Log(f"Database updated with {Kwargs.get("hash","Unknown Hash")} and {Kwargs.get("reason","Unknown Reason")}")
        else:
            Log("No Operation provided.")
            return set() if Operation == "load" else None
    except Exception as Exceptor:
        Log(f"While operating Signature under {Operation}, got {str(Exceptor)}")
        return set() if Operation == "load" else None
# Quarantine Sys
def QuarantineFile(Path):
    if not os.path.exists(Quarantine):
        os.makedirs(Quarantine)
    try:
        TruePath = os.path.join(Quarantine,os.path.basename(Path))
        shutil.move(Path,TruePath)
        Log(f"Quarantined {Path}")
        return True,"Completed"
    except Exception as Exceptor:
        return False,Exceptor
# Misc
def Log(Event): #TODO Performant logging
    try:
        Lines = 0
        with open(History, "r") as File:
            Lines = File.readlines()
        if len(Lines) > 100:
            with open(History, "w") as File:
                File.write("Cleared logs due to Limit of 100 lines.\n")
        with open(History, "a") as File:
            File.write(Event + "\n")
    except Exception as Exceptor:
        print(f"Attempted to log '{Event}' but got an Exceptor, '{Exceptor}'.")
def Main():
    #TODO Ruleset implementation per file using `Ruleset`
    Signatures,Ruleset = OperationSignature("Load",None),OperationRuleset("Load",None)
    Path = input("Enter the path to scan: ")
    Files = OperationScan("Directory",{"path": Path, "signatures": Signatures})
    FileCount = len(Files) if Files else 0
    Log(f"Scanned {Path}, got {Files} {"(No infected files)" if not Files else ""}")
    if Files:
        Log(f"Found infected files.")
        Quarantine = input(f"Would you like to quarantine {FileCount} infected files?")
        if Quarantine.lower() == "yes":
            for File,Reason in Files:
                Success,Message = QuarantineFile(File)
                Log(f"Quarantined {File} due to '{Reason}'" if Success else f"Failed to Quarantine {File} because of '{Reason}', got {Message}")
    else:
        print(f"No infected files found in {Path}.")

if __name__ == "__main__":
    Main()