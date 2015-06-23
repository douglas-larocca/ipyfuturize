# ipyfuturize

A cell magic for [futurize](http://python-future.org/futurize.html)

## usage & demo

`Ctrl+Enter` overwrites the active cell

![ipyfuturize](demo_inplace.png)

`Ctrl+Shift+Enter` puts the output in a new cell

![ipyfuturize](demo_newcell.png)

## install

```
%install_ext https://raw.github.com/douglas-larocca/ipyfuturize/master/ipyfuturize.py
```

then

```
%load_ext ipyfuturize
```

and use with

```
%%futurize
```
