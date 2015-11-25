#include "bench.h"
#include <QDebug>
#include <QMap>
#include <QElapsedTimer>
#include <iostream>

#define A 65
#define C 67
#define T 84
#define G 71

Bench::Bench()
{

}

Bench::~Bench()
{

}

int Bench::translate(int count, const QString &seq)
{

    if (seq.isEmpty())
        return -1;

    QMap<QChar, QChar> maps;
    maps[A] = T;
    maps[T] = A;
    maps[C] = G;
    maps[G] = C;



    for (int c=0; c<count; ++c)
    {
        QString reverse;

        for (int i=seq.size()-1; i>=0; i--)
            reverse.append(maps[seq[i]]);

    }




}


