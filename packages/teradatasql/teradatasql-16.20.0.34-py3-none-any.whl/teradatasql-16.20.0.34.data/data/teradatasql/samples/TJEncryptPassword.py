# Copyright 2018 Teradata. All rights reserved.
#
#   File:       TJEncryptPassword.py
#   Purpose:    Encrypts a password, saves the encryption key in one file, and saves the encrypted password in a second file
#
#               This program accepts eight command-line arguments:
#
#                 1. Transformation - Algorithm/mode/padding values from this set:
#                    [DES/DESede/AES]/[CBC/CFB/OFB]/[NoPadding/PKCS5Padding]	
#                                     Example AES/CBC/PKCS5Padding
#
#                 2. KeySizeInBits  - keysize argument for the NewCipher method.
#                                     Specify -default to use the transformation's default key size.
#                                     Example: -default
#
#                                     To use AES with a 192-bit or 256-bit key, specify those key size values
#                                     Example: 256
#
#                 3. MAC            - algorithm argument for the Mac.getInstance method.
#                                     HmacSHA1 and HmacSHA256 are available
#                                     Example: HmacSHA256
#
#                 4. PasswordEncryptionKeyFileName - a filename in the current directory, a relative pathname, or an absolute pathname.
#                                     The file is created by this program. If the file already exists, it will be overwritten by the new file.
#                                     Example: PassKey.properties
#
#                 5. EncryptedPasswordFileName - a filename in the current directory, a relative pathname, or an absolute pathname.
#                                     The filename or pathname that must differ from the PasswordEncryptionKeyFileName.
#                                     The file is created by this program. If the file already exists, it will be overwritten by the new file.
#                                     Example: EncPass.properties
#
#                 6. Hostname       - the Teradata Database hostname.
#                                     Example: whomooz
#
#                 7. Username       - the Teradata Database username.
#                                     Example: guest
#
#                 8. Password       - the Teradata Database password to be encrypted.
#                                     Unicode characters in the password can be specified with the backslash uXXXX escape sequence.
#                                     Example: please
#
#               Overview
#               --------
#
#               Teradata Python Driver Stored Password Protection enables an application to provide a connection password in encrypted form to
#               the Teradata Python Driver, and also enables an application to provide the NEW_PASSWORD connection parameter's value in encrypted form.
#
#               There are several different ways that an application may specify a password to the Teradata Python Driver, all of which may use an
#               encrypted password:
#                 1. A login password specified as the "password" value in the dataSourceName parameter in the sql.open()) method.
#                 2. A login password specified within the LOGDATA connection parameter
#
#               If the password, however specified, begins with the prefix "ENCRYPTED_PASSWORD(" then the specified password must follow this format:
#
#                 ENCRYPTED_PASSWORD(PasswordEncryptionKeyResourceName,EncryptedPasswordResourceName)
#
#               The PasswordEncryptionKeyResourceName must be separated from the EncryptedPasswordResourceName by a single comma.
#               The PasswordEncryptionKeyResourceName specifies the name of a properties file that contains the password encryption key and associated information.
#               The EncryptedPasswordResourceName specifies the name of a properties file that contains the encrypted password and associated information.
#               The two resources are described below.
#
#               This program works in conjunction with Teradata Python Driver Stored Password Protection.
#               This program creates the files containing the password encryption key and encrypted password, which can be subsequently specified to
#               the Teradata Python Driver via the "ENCRYPTED_PASSWORD(" syntax.
#
#               You are not required to use this program to create the files containing the password encryption key and encrypted password.
#               You can develop your own software to create the necessary files.
#               The only requirement is that the files must match the format expected by the Teradata JDBC Driver, which is documented below.
#
#               This program encrypts the password and then immediately decrypts the password, in order to verify that the password can be
#               successfully decrypted. This program mimics the implementation of the Teradata Python Driver's password decryption, and is
#               intended to openly illustrate its operation and enable scrutiny by the community.
#
#               The encrypted password is only as safe as the two files. You are responsible for restricting access to the files containing the
#               password encryption key and encrypted password. If an attacker obtains both files, the password can be decrypted.
#               The operating system file permissions for the two files should be as limited and restrictive as possible, to ensure that only the
#               intended operating system userid has access to the files.
#
#               The two files can be kept on separate physical volumes, to reduce the risk that both files might be lost at the same time.
#               If either or both of the files are located on a network volume, then an encrypted wire protocol can be used to access the
#               network volume, such as sshfs, encrypted NFSv4, or encrypted SMB 3.0.
#
#               Password Encryption Key File Format
#               -----------------------------------
#
#               The password encryption key file is a properties file.
#               The file must contain the following string properties:
#
#                 version=1
#
#                       The version number must be 1.
#                       This property is required.
#
#                 transformation=TransformationName
#                       This value is made up of 3 parts, separated by forward slash from this set:
#                       [DES/DESede/AES]/[CBC/CFB/OFB]/[NoPadding/PKCS5Padding]	
#                             Example AES/CBC/DES/PKCS5Padding
#
#                       These values defined the encryption algorithm, cipher mode and padding method that will be used for encryption
#                       This property is required.
#
#                 algorithm=AlgorithmName
#
#                       This value must correspond to the algorithm used for encryption.
#                       This value must be "DES", "DESede" or "AES".
#                       This property is required.
#
#                 match=MatchValue
#
#                       The password encryption key and encrypted password files must contain the same match value.
#                       The match values are compared to ensure that the two specified files are related to each other,
#                       serving as a "sanity check" to help avoid configuration errors.
#                       This property is required.
#
#                       This program uses a timestamp as a shared match value, but a timestamp is not required.
#                       Any shared string can serve as a match value. The timestamp is not related in any way to the encryption of the
#                       password, and the timestamp cannot be used to decrypt the password.
#
#                 key=HexDigits
#
#                       This value is the password encryption key, encoded as hex digits.
#                       This property is required.
#
#                 mac=AlgorithmName
#
#                       This value is used to determine which sort of Keyed-Hash Message Authentication Code object is created.
#                       Valid values are "HmacSHA256" and "HmacSHA1"
#                       Teradata JDBC Python Driver Stored Password Protection performs Encrypt-then-MAC for protection from a padding oracle attack.
#                       This property is required.
#
#                 mackey=HexDigits
#
#                       This value is the MAC key, encoded as hex digits.
#                       This property is required.
#
#               Encrypted Password File Format
#               ------------------------------
#
#               The encrypted password file is a text file in Java Properties file format, using the ISO 8859-1 character encoding.
#               The file must contain the following string properties:
#
#                 version=1
#
#                       The version number must be 1.
#                       This property is required.
#
#                 match=MatchValue
#
#                       The password encryption key and encrypted password files must contain the same match value.
#                       The match values are compared to ensure that the two specified files are related to each other,
#                       serving as a "sanity check" to help avoid configuration errors.
#                       This property is required.
#
#                       This program uses a timestamp as a shared match value, but a timestamp is not required.
#                       Any shared string can serve as a match value. The timestamp is not related in any way to the encryption of the
#                       password, and the timestamp cannot be used to decrypt the password.
#
#                 password=HexDigits
#
#                       This value is the encrypted password, encoded as hex digits.
#                       This property is required.
#
#                 params=HexDigits
#
#                       This value contains the ASN.1 encoded cipher algorithm parameters, if any, encoded as hex digits.
#                       It contains the Initialization vector used in the cipher.NewCBCDecrypter(), cipher.NewCFBEncrypter(),
#                       and cipher.NewOFB() methods.
#                       This property is required.
#
#                 hash=HexDigits
#
#                       This value is the expected message authentication code (MAC), encoded as hex digits.
#                       After encryption, the expected MAC is calculated using the ciphertext, transformation name, and algorithm parameters if any.
#                       Before decryption, the Teradata JDBC Driver calculates the MAC using the ciphertext, algorithm name, and algorithm
#                       parameters, and verifies that the calculated MAC matches the expected MAC.
#                       If the calculated MAC differs from the expected MAC, then either or both of the files may have been tampered with.
#                       This property is required.
#
#               Algorithm, Key Size, and MAC
#               ---------------------------------
#
#               The Algorithm parameter is the name of a cryptographic algorithm such as "DES", "DESede" or "AES". Padding is used with each of these algorithms.
#
#               Teradata Python Driver Stored Password Protection uses a symmetric encryption algorithm such as "DES", "DESede" or "AES", in which the same secret key is used
#               for encryption and decryption of the password.
#
#               Teradata JDBC Driver Stored Password Protection does not use an asymmetric encryption algorithm such as RSA, with separate public and private keys.
#
#               ECB (Electronic Codebook) is the simplest block cipher encryption mode. The input is divided into blocks, and each block is encrypted separately.
#               ECB is unsuitable for encrypting data whose total byte count exceeds the algorithm's block size, and is therefore unsuitable for use with
#               Teradata Python  Driver Stored Password Protection.
#               CBC (Cipher Block Chaining) is a more complex block cipher encryption mode. With CBC, each ciphertext block is dependent on all plaintext blocks
#               processed up to that point. CBC is suitable for encrypting data whose total byte count exceeds the algorithm's block size, and is therefore
#               used with Teradata Python Driver Stored Password Protection.
#
#               Teradata Python Driver Stored Password Protection hides the password length in the encrypted password file by extending the length of the
#               UTF8-encoded password with trailing null bytes. The length is extended to the next 512-byte boundary.
#
#               The 512-byte boundary is compatible with many block ciphers. AES, for example, has a block size of 128 bits (16 bytes), and is therefore
#               compatible with the 512-byte boundary.
#
#               A block cipher with padding, such as AES/CBC/PKCS5Padding, can be used to encrypt data of any length.
#               However, CBC with padding is vulnerable to a "padding oracle attack", so Teradata Python Driver Stored Password Protection performs Encrypt-then-MAC
#               for protection from a padding oracle attack.
#               MAC algorithm HmacSHA256 and HmacSHA1 are both available.
#
#               The strength of the encryption depends on your choice of cipher alogrithm and key size.
#               AES uses a 128-bit (16 byte), 192-bit (24 byte), or 256-bit (32 byte) key. Specify 128, 192, or 256 as the keysize argument for
#               the crypto rand.Read method.
#
#               Resource Names
#               --------------
#
#               This program has command-line arguments PasswordEncryptionKeyFileName and EncryptedPasswordFileName to specify filenames.
#               In contrast, the Teradata Python Driver's "ENCRYPTED_PASSWORD(" syntax uses resource names, rather than filenames, in order to offer
#               more flexibility for file storage location and access.
#
#
#               The resource name can begin with the "file:" prefix and specify a relative pathname for the Teradata Python Driver to load the resource
#               from a relative-pathname file.
#
#               Example with files in current directory:
#
#                 ENCRYPTED_PASSWORD(file:JohnDoeKey.properties,file:JohnDoePass.properties)
#
#               Example with relative paths:
#
#                 ENCRYPTED_PASSWORD(file:../dir1/JohnDoeKey.properties,file:../dir2/JohnDoePass.properties)
#
#               The resource name can begin with the "file:" prefix and specify an absolute pathname for the Teradata JDBC Driver to load the resource
#               from an absolute-pathname file.
#
#               Example with absolute paths on Windows:
#
#                 ENCRYPTED_PASSWORD(file:c:/dir1/JohnDoeKey.properties,file:c:/dir2/JohnDoePass.properties)
#
#               Example with absolute paths on Linux:
#
#                 ENCRYPTED_PASSWORD(file:/dir1/JohnDoeKey.properties,file:/dir2/JohnDoePass.properties)
#
#       EXAMPLE USAGE:
#               python -x TJEncryptPassword.py AES/CBC/NoPadding -default HmacSHA256 ./key.txt ./pass.txt mydbsname user1 user1_password

import binascii
import codecs
import datetime
import sys

import Crypto.Cipher
from Crypto import Random
from Crypto.Cipher import AES, DES, DES3
from Crypto.Hash import HMAC, SHA, SHA256

import teradatasql

hmacsha256 = "HmacSHA256"
hmacsha1 = "HmacSHA1"

def load_properties(filepath, sep='=', comment_char='#'):
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def decryptPassword(sPassKeyFilename, sEncPassFilename):
    parmKeys = load_properties(sPassKeyFilename)
    parmValue = load_properties(sEncPassFilename)

    sTransParts = parmKeys["transformation"].split("/")
    if len(sTransParts) != 3:
        print("Illegal Transformation value: {}".format(parmKeys["transformation"]))
    sMode = sTransParts[1]

    try:
        abyCipherText = (codecs.decode(parmValue["password"], "hex"))
        abyKey = codecs.decode(parmKeys["key"], "hex")
        abyMacKey = (codecs.decode(parmKeys["mackey"], "hex"))
        ivEncoded = (codecs.decode(parmValue["params"], "hex"))

    except ValueError:
        print("Could not convert/decode data data")
        raise
    except KeyError:
        print("Could not retrieve value")
        raise

    # simple substitute for ASN1 decode
    ivNonEncoded = ivEncoded[2:]

    if "1" != parmKeys["version"]:
        print("Properties file {}  has unexpected or nonexistent version {}".format(
                     sPassKeyFilename, parmKeys["version"]))
        raise ValueError

    if "1" != parmValue["version"]:
        print("Properties file {}  has unexpected or nonexistent version {}".format(
                     sEncPassFilename, parmKeys["version"]))
        raise ValueError

    if parmKeys["match"] == "":
        print("Properties file {} is missing a match value".format(
                     sPassKeyFilename))
        raise ValueError

    if parmValue["match"] == "":
        print("Properties file {} is missing a match value".format(
                     sEncPassFilename))
        raise ValueError

    if parmKeys["match"] != parmValue["match"]:
        print("Properties file {} match value: {} differs from properties file {} match value: ".format(
                     sPassKeyFilename, parmKeys["match"], sEncPassFilename, parmValues["match"]))
        raise ValueError

    if parmKeys["mac"] == "HmacSHA1":
        hasher = HMAC.new(abyMacKey, digestmod=Crypto.Hash.SHA)
    elif parmKeys["mac"] == "HmacSHA256":
        hasher = HMAC.new(abyMacKey, digestmod=Crypto.Hash.SHA256)
    else:
        print(
            "Mac name must be HmacSHA1 or HmacSHA256 value {} is illegal".format(parmKeys["mac"]))
        raise ValueError

    hasher.update(abyCipherText)

    try:
        aby = str(parmKeys["transformation"])
        aby = aby.encode('utf-8')
        hasher.update(aby)
        hasher.update(ivEncoded)
        hashResult = hasher.hexdigest()
    except ValueError:
        print("Problems creating hash")
        raise ValueError

    parmHash = parmValue["hash"]

    if parmHash != hashResult:
        print("Hash mismatch indicates possible tampering with properties file ",
                     sPassKeyFilename, " and/or ", sEncPassFilename)
        raise ValueError

    # the mode values are the same for AES, DES, and DES3
    if sMode == "CBC":
        sPyMode = AES.MODE_CBC
    elif sMode == "CFB":
        sPyMode = AES.MODE_CFB
    elif sMode == "OFB":
        sPyMode = AES.MODE_OFB
    else:
        print(
            "Invalid mode value: {} valid values are: CBS, CFB and OFB".format(sMode))
        raise ValueError

    algorithm = parmKeys["algorithm"]
    if algorithm == "AES":
        if sMode == "CFB":
            cur_cipher = AES.new(abyKey, sPyMode, ivNonEncoded, segment_size=128)
        else:
            cur_cipher = AES.new(abyKey, sPyMode, ivNonEncoded)
    elif algorithm == "DES":
        if sMode == "CFB":
            cur_cipher = DES.new(abyKey, sPyMode, ivNonEncoded, segment_size=64)
        else:
            cur_cipher = DES.new(abyKey, sPyMode, ivNonEncoded)
    elif algorithm == "DESede":
        if sMode == "CFB":
            cur_cipher = DES3.new(abyKey, sPyMode, ivNonEncoded, segment_size=64)
        else:
            cur_cipher = DES3.new(abyKey, sPyMode, ivNonEncoded)
    else:
        print(
            "Invalid algorithm value: {} valid values are: AES, DES and DESede".format(algorithm))
        raise ValueError

    # decrypt the password
    abyCleartext = cur_cipher.decrypt(abyCipherText)
    n = abyCleartext.index(0)
    sDecryptedPassword = abyCleartext[:n].decode("utf-8")
    print("Decrypted password: ", sDecryptedPassword)
    return sDecryptedPassword

def writeProp(f, sName, sValue):
    f.write(sName + "=" + sValue)
    return

def createPasswordEncryptionKeyFile(sTransformation, sKeySizeInBits, sMac, sPassKeyFilename):

    nKeySizeBytesDes = 8
    nKeySizeBytesDes3 = 24
    nKeySizeBytesAes = 16  # 24 or 32 also legal

    sTransParts = sTransformation.split("/")
    if len(sTransParts) != 3:
        print("Illegal Transformation value:",  sTransParts)
        raise ValueError

    sMode = sTransParts[1]
    sAlgorithm = sTransParts[0]

    if "-default" == sKeySizeInBits:  # if using the default
        if sAlgorithm == "AES":
            iKeySizeBytes = nKeySizeBytesAes
        elif sAlgorithm == "DES":
            iKeySizeBytes = nKeySizeBytesDes
        elif sAlgorithm == "DESede":
            iKeySizeBytes = nKeySizeBytesDes3
        else:
            log.Error(
                "Invalid algorithm value:%s valid values are: AES, DES and DESede", sAlgorithm)
            raise ValueError
    else:  # user passed a bit size value
        iKeySizeBytes = int(int(sKeySizeInBits)/8)

    # the mode values are the same for AES, DES, and DES3
    if sMode == "CBC":
        sPyMode = AES.MODE_CBC
    elif sMode == "CFB":
        sPyMode = AES.MODE_CFB
    elif sMode == "OFB":
        sPyMode = AES.MODE_OFB
    else:
        print(
            "Invalid mode value: {} valid values are: CBS, CFB and OFB".format(sMode))
        raise ValueError

    sPadding = sTransParts[2]
    if ("PKCS5Padding" != sPadding) and ("NoPadding" != sPadding):
        print(
            "Invalid Padding option: {} valid values are NoPadding and PKCS5Padding".format(sPadding))
        raise ValueError

    abyKeyval = Random.new().read(iKeySizeBytes)  # create encryption key

    if sMac == hmacsha256:
        abyMacKey = Random.new().read(SHA256.block_size)
    elif sMac == hmacsha1:
        abyMacKey = Random.new().read(SHA.block_size)
    else:
        print("Mac name must be " + hmacsha1 + " or " +
                     hmacsha256 + " value: " + sMac + " is illegal")
        raise ValueError

    f = open(sPassKeyFilename, "w")

    writeProp(f, "version", "1\n")
    writeProp(f, "algorithm", sAlgorithm + "\n")
    writeProp(f, "match", str(datetime.datetime.now()) + "\n")
    writeProp(f, "key", (codecs.encode(abyKeyval, "hex")).decode() + "\n")
    writeProp(f, "mackey", (codecs.encode(abyMacKey, "hex").decode()) + "\n")
    writeProp(f, "transformation", sTransformation + "\n")
    writeProp(f, "mac", sMac + "\n")
    f.close()

    return

def createEncryptedPasswordFile (sPassKeyFilename, sEncPassFilename, sPassword):

    if len(sPassword) == 0:
        print("Password cannot be a zero-length string")
        raise ValueError

    passKeys = load_properties(sPassKeyFilename)

    sTransParts = passKeys["transformation"].split("/")
    if len(sTransParts) != 3:
        print("Illegal Transformation value: ",
                     passKeys["transformation"])
        raise ValueError

    sMode = sTransParts[1]

    try:
        abyKey = codecs.decode(passKeys["key"], "hex")
        sMac = passKeys["mac"]
        abyMacKey = codecs.decode(passKeys["mackey"], "hex")
    except ValueError:
        print("Could not convert/decode data data")
        raise
    except KeyError:
        print("Could not retrieve value")
        raise

    if "1" != passKeys["version"]:
        print("Properties file {} has unexpected or nonexistent version {}".format(
                     sPassKeyFilename, parmKeys["version"]))
        raise ValueError
    print("{} specifies {} with {} bit key and {}".format(sPassKeyFilename,  passKeys["transformation"], len(abyKey)*8, sMac))

    isPKCS5Padding = False
    sPadding = sTransParts[2]
    if "PKCS5Padding" == sPadding:
        isPKCS5Padding = True
    elif "NoPadding" != sPadding:
        print(
            "Invalid Padding option: {} valid values are NoPadding and PKCS5Padding".format(sPadding))
        raise ValueError

    # the mode values are the same for AES, DES and DES3
    if sMode == "CBC":
        sPyMode = AES.MODE_CBC
    elif sMode == "CFB":
        sPyMode = AES.MODE_CFB
    elif sMode == "OFB":
        sPyMode = AES.MODE_OFB
    else:
        print(
            "Invalid mode value: {} valid values are: CBS, CFB and OFB".format(sMode))
        raise ValueError

    algorithm = passKeys["algorithm"]
    if "AES" == algorithm:
        iv = Random.new().read(AES.block_size)
        if sMode == "CFB":
            cur_cipher = AES.new(abyKey, sPyMode, iv, segment_size=128)
        else:
            cur_cipher = AES.new(abyKey, sPyMode, iv)
        blocksize = AES.block_size
    elif "DES" == algorithm:
        iv = Random.new().read(DES.block_size)
        if sMode == "CFB":
            cur_cipher = DES.new(abyKey, sPyMode, iv, segment_size=64)
        else:
            cur_cipher = DES.new(abyKey, sPyMode, iv)
        blocksize = DES.block_size
    elif "DESede" == algorithm:
        iv = Random.new().read(DES3.block_size)
        if sMode == "CFB":
            cur_cipher = DES3.new(abyKey, sPyMode, iv, segment_size=64)
        else:
            cur_cipher = DES3.new(abyKey, sPyMode, iv)
        blocksize = DES3.block_size
    else:
        print(
            "Invalid algorithm value:{} valid values are: AES, DES and DESede".format(algorithm))
        raise ValueError

    PADBLOCKSIZE = 512  # we zero-pad the password to 512 bytes
    abyPassword = bytes(sPassword, "utf-8")
    nPlaintextByteCount = (len(abyPassword) // PADBLOCKSIZE + 1) * PADBLOCKSIZE
    nTrailerByteCount = nPlaintextByteCount - len(abyPassword)
    buf = bytearray(nTrailerByteCount)
    buf = abyPassword + buf

    # extra processing if using PKCS5P, add extra blocksize of bytes
    # where each byte is the blocksize  */
    if isPKCS5Padding:
        arr = bytes([blocksize]) * blocksize
        buf = buf + arr
    buf = cur_cipher.encrypt(buf)
    # buf - holds plaintext buffered to 512 bytes + PKCS5P padding if required

    if passKeys["mac"] == "HmacSHA1":
        hasher = HMAC.new(abyMacKey, digestmod=Crypto.Hash.SHA)
    elif passKeys["mac"] == "HmacSHA256":
        hasher = HMAC.new(abyMacKey, digestmod=Crypto.Hash.SHA256)
    else:
        print(
            "Mac name must be HmacSHA1 or HmacSHA256 value {} is illegal".format(parmKeys["mac"]))
        raise ValueError

    # compute hash value
    hasher.update(buf)
    aby = passKeys["transformation"].encode()
    hasher.update(aby)

    # do our own asn1 conversion
    ivEncoded = bytes(0x04)
    asn1Hdr = bytearray()
    asn1Hdr.append(0x04)
    asn1Hdr.append(len(iv))
    ivEncoded = asn1Hdr + iv
    hasher.update(ivEncoded)
    sHash = hasher.hexdigest()

    f = open(sEncPassFilename, "w")

    writeProp(f, "version", passKeys["version"] + "\n")
    str1 = str(binascii.hexlify(buf))
    writeProp(f, "password", (codecs.encode(buf, "hex").decode() + "\n"))
    writeProp(f, "match", passKeys["match"] + "\n")
    writeProp(f, "hash", sHash + "\n")
    writeProp(f, "params", (codecs.encode(ivEncoded, "hex").decode() + "\n"))
    f.close()

    # end createEncryptedPasswordFile

if len (sys.argv) != 9:
    print ("Parameters: Transformation KeySizeInBits MAC PasswordEncryptionKeyFileName EncryptedPasswordFileName Hostname Username Password")
    exit (1)

sTransformation  = sys.argv [1]
sKeySizeInBits   = sys.argv [2]
sMac             = sys.argv [3]
sPassKeyFilename = sys.argv [4]
sEncPassFilename = sys.argv [5]
sHostname        = sys.argv [6]
sUsername        = sys.argv [7]
sPassword        = sys.argv [8]

createPasswordEncryptionKeyFile (sTransformation, sKeySizeInBits, sMac, sPassKeyFilename)
createEncryptedPasswordFile (sPassKeyFilename, sEncPassFilename, sPassword)
decryptPassword (sPassKeyFilename, sEncPassFilename)

sPassword = "ENCRYPTED_PASSWORD(file:{},file:{})".format (sPassKeyFilename, sEncPassFilename)

with teradatasql.connect (None, host=sHostname, user=sUsername, password=sPassword) as con:
    with con.cursor () as cur:
        cur.execute ('select user, session')
        print (cur.fetchone ())
