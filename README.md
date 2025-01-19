<!-- Might be unnecessary. -->
> [!TIP]
> Latest version is 0.2.1 BETA. If you attempt to update your Destiny application, run it instead, and it will auto-update.
<!-- BUFFER -->
> ## About
**Destiny** is an anti-virus application (not software[^1]) made entirely from the programming language Python and uses a few libraries for compatibility.

The ideal goal of **Destiny** is to create a lightweight anti-virus application which is updated regularly with critical information and the latest hashes[^2] to keep the end-user safe.
<!-- BUFFER -->
> ## Inquiries
1: Is **Destiny** open source or free to modify?
 - Yes, **Destiny** is _technically_ open source and with **[Unlicense](https://unlicense.org)**, you can use the application, modify it to your needs, and even use the framework for your own. Credit is appreciated when doing so, but it isn't required.

2: Where does **Destiny** get the hash information and data from?
  - **Destiny** gets hash file information and critical information from [MalwareBazaar](https://bazaar.abuse.ch), [VXVault](https://vxvault.net/ViriList.php), and other GitHub repositories that are actively maintained.

3: **Destiny** won't auto-update, why?
- Some versions of **Destiny** don't support auto-updating or don't have HTTP requirements. Make sure you're connected to the internet and a valid Operating System before running **Destiny**.

4: What libraries does **Destiny** use?
- **Destiny** uses [HashLib](https://docs.python.org/3/library/hashlib.html), [OS](https://docs.python.org/3/library/os.html), [ShUtil](https://docs.python.org/3/library/shutil.html) and [JSON](https://docs.python.org/3/library/json.html).

<!-- BUFFER -->
> ### Citations
[^2]: Hashes and the form of "hashing" is an anti-virus method which uses a file or directory's hash > (Unique Identifier) to identify potential malware by referencing a batch/list of known malware hashes.
  See [here (Hash Function)](https://en.wikipedia.org/wiki/Hash_function) or [here (File verification)](https://en.wikipedia.org/wiki/File_verification) for more information.
[^1]: The difference between (an) __application__ and (a) __software__ is legal terminology. __Application__ refers to: "" A type of __software__ built to perform a function or functions to/for the user. "". When licensing an __application__, it _typically_ allows code usage, but not User Interface usage. __Software__ refers to: "" All types of programs, system __software__, middleware, and app __software__. "". When licensing __software__, it _typically_ does not allow any usage.
