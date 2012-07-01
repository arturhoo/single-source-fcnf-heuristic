#!/bin/bash
bold=`tput bold`
normal=`tput sgr0`

FILES=instancias/glpk/*
for f in $FILES
do
    echo  ${bold}$f${normal}
    for i in 1 2 3
    do
        echo '>> Execução GLPK '$i
        glpsol --model modelo.mod --data $f -o sol.out | grep -i 'time'
        cat sol.out | grep -i 'minimum'
    done
done

FILES=instancias/py/*
for f in $FILES
do
    echo  ${bold}$f${normal}
    for i in 1 2 3
    do
        echo '>> Execução Python '$i
        python solver.py -i $f | egrep -i 'tempo|objetivo'
    done
done
