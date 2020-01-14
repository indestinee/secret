# secret
save secrets with AES

## example
```shell
$ ./secret.sh
[WRN] you must remember the key, otherwise lose all data
[I N] key:
 -- order -------------------------------------------
   1. cryptor.display_items()   display all items
   2. cryptor.load(id=x)        load item (ID: x)
   3. cryptor.dump(data, name)  save data
   4. cryptor.help()            that's me :)
 ----------------------------------------------------

SQL: >> SELECT id,name FROM information    ((),)
----------------------------------------------------------------
  id: 1  name: Alfred
  id: 2  name: Boom 3D
----------------------------------------------------------------

In [1]: cryptor.load(id=2)
SQL: >> SELECT name,data FROM information WHERE id=?    ((2,),)
Out[1]:
{'name': 'Boom 3D, ...}
```
