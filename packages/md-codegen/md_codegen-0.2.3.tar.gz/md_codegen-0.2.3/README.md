# Codegen

# Description
**codegen** is tool for generating code for [microservice accelerator](https://github.houston.entsvcs.net/zongying-cao/micro-service-accelerator).
It currently invoke [nodejs-codegen](https://github.com/cao5zy/nodejs-codegen) to generate micro-service project for nodejs.   

# Installation
```
pip install md_codegen
```
**codegen** is developed and tested on python 3.x. Please make sure python 3.x has already installed on your system prior to install it.

# Usage
```
codegen <url> -u <username> -p <password> -o <output path>
```
* `url`: the url to download the *microservice definitions*. It would follow the pattern `http://<host>:<port>/_api/interfacedef_get_service/query/:login/interface_entries`.   
* `u`: the username to access the account. If it is omitted, the program will prompt to input `username`.    
* `p`: the password to access the account. If it is omitted, the program will prompt to input `password`.  
* `o`: the output path to store the generated code. If it is omitted, the generated code will be stored in the current folder.   

> If you want to update the interface defintion to your code, you should commit the changes in your local and make sure your local git repository is clean or the code generation will abort.
