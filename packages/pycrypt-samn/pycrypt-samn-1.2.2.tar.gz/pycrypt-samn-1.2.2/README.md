# pycrypt

A simple encryption module to encrypt and decrypt strings with a public/private key.

Can also generate an RSA key pair


## Installation
From GitHub repo
```
python setup.py install
```
From PyPi
```
pip install pycrypt-samn
```

## Generate RSA Key Pair

```
from pycrypt.encryption import Encryption

Encryption().generate_rsa_key_pair(public_file='~/rsa_pub',
                                   private_file='~/rsa_priv',
                                   secret_code='MySuperSecretKey')
```

## Encrypt string using a public key stored as an object

```
from pycrypt.encryption import Encryption

enc = Encryption().encrypt(publickey_file='~/rsa_pub',
                           privateData="clear test string needing encrypted")
```
```
print(enc.encrypted_message)

b'NJ4RV6idRk+KxZkpDoO9vK5P4zWE11ZZawjrwbnRi6v/xtZxmEMUt0FS1OBWzpa1vxAOM9XFqDkrvCRccNSES7nTAMrGV6ShSKkLwSpB+DhUO0Jq+5wDgq3CBCADM5LrGWWu6prxeqltK/vaNp7GtTUmX4kSOtSwNxWq91+gq9nPVJiTQSpBrsRorzcjWhByW+X3IxaTYNMLlBHikzhNjtnk1wBx0bAf/y7Oo6yj99J6Hr4FWg7jkwj+sakY+FaoK+qqKZAzCJzuJqtbbm8E8NNGKh9Dbej8U4j5FYkLkPM/EJXxInRMOybW8AbW7t+fE2bu4sYySf429PkHPiAXts1OTAs1RDVA8wvS7DOb1iU67LKRENpeFZB2bDb0QrfCvjFDzBw6anC1GPtnnTPvuqHo8CuBHfp7R6i0+JKyDi+2cbN8M8v7sIGY1XwK3T+pIIEplN3h7VHj/X1Dyg8SDgkl7btSrWIRzc51bQaXOYI2DPIji7wTW+hvG8YBru9/0Gw0/+YPmZ2A4Sb745QKo0eu9AWmoZ1TjoaLGnvwD5SzLCqoGXegZA6Dxd12EzqT0jyxhCLp7ksGRjcnYFAJX61P5h5YzGz8yJYnIkwPE4CL8cLVSRCUcbFFrjt9RIwbH2+f5Y9CO2zXpc/tb/NKBAClfxnNDa/Pisfr6b/bJTU='
```

## Encrypt string using a public key and output to a file

```
from pycrypt.encryption import Encryption

Encryption().encrypt(publickey_file='~/rsa_pub',
                     privateData="clear text string needing encrypted",
                     outpu_file='~/enc_message')
```

## Decrypt a string

```
from pycrypt.encryption import Encryption

enc_message = b'NJ4RV6idRk+KxZkpDoO9vK5P4zWE11ZZawjrwbnRi6v/xtZxmEMUt0FS1OBWzpa1vxAOM9XFqDkrvCRccNSES7nTAMrGV6ShSKkLwSpB+DhUO0Jq+5wDgq3CBCADM5LrGWWu6prxeqltK/vaNp7GtTUmX4kSOtSwNxWq91+gq9nPVJiTQSpBrsRorzcjWhByW+X3IxaTYNMLlBHikzhNjtnk1wBx0bAf/y7Oo6yj99J6Hr4FWg7jkwj+sakY+FaoK+qqKZAzCJzuJqtbbm8E8NNGKh9Dbej8U4j5FYkLkPM/EJXxInRMOybW8AbW7t+fE2bu4sYySf429PkHPiAXts1OTAs1RDVA8wvS7DOb1iU67LKRENpeFZB2bDb0QrfCvjFDzBw6anC1GPtnnTPvuqHo8CuBHfp7R6i0+JKyDi+2cbN8M8v7sIGY1XwK3T+pIIEplN3h7VHj/X1Dyg8SDgkl7btSrWIRzc51bQaXOYI2DPIji7wTW+hvG8YBru9/0Gw0/+YPmZ2A4Sb745QKo0eu9AWmoZ1TjoaLGnvwD5SzLCqoGXegZA6Dxd12EzqT0jyxhCLp7ksGRjcnYFAJX61P5h5YzGz8yJYnIkwPE4CL8cLVSRCUcbFFrjt9RIwbH2+f5Y9CO2zXpc/tb/NKBAClfxnNDa/Pisfr6b/bJTU='

enc = Encryption().decrypt(private_key_file='~/rsa_priv',
                           secret_code='MySuperSecretKey',                   
                           encrypted_data=enc_message)
```
Output:
```
In[2]: enc.decrypted_message
Out[2]: 'clear test string needing encrypted'
```

## Decrypt String from a File
```
from pycrypt.encryption import Encryption

enc = Encryption().decrypt(private_key_file='~/rsa_priv',
                           secret_code='MySuperSecretKey',                   
                           encrypted_data='~/enc_message')
```
Output:
```
In[2]: enc.decrypted_message
Out[2]: 'clear test string needing encrypted'
```

## Generate MD5 info of a file

```
from pycrypt.encryption import Encryption

md5_info = Encryption().md5('~/rsa_pub')
```
Produces an object with ByteString and HexString as properties
```
In[1]: md5_info.__dict__
Out[1]: 
{'ByteString': b'\x14n?\xc5\x88\xe9F\xa8\x0e\xaa\x10\xc0\xce\xb0~\x8e',
 'HexString': '146e3fc588e946a80eaa10c0ceb07e8e'}
```
