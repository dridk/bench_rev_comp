#ifndef BENCH_H
#define BENCH_H
#include <QString>

class Bench
{
public:
    Bench();
    ~Bench();


    int translate(int count, const QString& seq);
};

#endif // BENCH_H
